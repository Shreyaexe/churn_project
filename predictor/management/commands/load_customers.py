import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand

from predictor.models import Prediction
from predictor.services import get_pipeline, risk_level, tenure_group, ACTIONS, SERVICE_COLS


class Command(BaseCommand):
    help = "Score the Telco CSV with the trained model and load results for the dashboard"

    def handle(self, *args, **kwargs):
        path = settings.BASE_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
        df = pd.read_csv(path)
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"] * df["tenure"])
        names = df["customerID"].tolist()
        df = df.drop(columns=["customerID", "Churn"])
        df["services_count"] = (df[SERVICE_COLS] == "Yes").sum(axis=1) + (df["InternetService"] != "No").astype(int)
        df["tenure_group"] = df["tenure"].apply(tenure_group)

        probs = get_pipeline().predict_proba(df)[:, 1]
        Prediction.objects.filter(created_by__isnull=True).delete()  # safe to re-run

        objs = []
        for name, row, p in zip(names, df.to_dict("records"), probs):
            level = risk_level(float(p))
            objs.append(Prediction(
                customer_name=name, contract=row["Contract"], tenure=int(row["tenure"]),
                monthly_charges=float(row["MonthlyCharges"]), inputs=row,
                probability=float(p), risk_level=level, action=ACTIONS[level],
            ))
        Prediction.objects.bulk_create(objs, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(objs)} customers"))
