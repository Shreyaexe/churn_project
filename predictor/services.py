import joblib
import pandas as pd
from django.conf import settings

_pipeline = None

SERVICE_COLS = ["PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",
                "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]

ACTIONS = {
    "Low": "No action needed. Continue normal service and review at next billing cycle.",
    "Moderate": "Send a check-in call or email and offer a service review.",
    "High": "Priority outreach: offer a discount or contract upgrade and assign a retention agent.",
}


def get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = joblib.load(settings.MODEL_PATH)
    return _pipeline


def tenure_group(t):
    if t <= 12:
        return "0-1yr"
    if t <= 24:
        return "1-2yr"
    if t <= 48:
        return "2-4yr"
    return "4-6yr"


def risk_level(p):
    if p < 0.30:
        return "Low"
    if p < 0.60:
        return "Moderate"
    return "High"

def predict_churn(data):
    """data = dict of the form values (without customer_name)."""
    row = dict(data)
    row["SeniorCitizen"] = int(row["SeniorCitizen"])
    if row.get("TotalCharges") is None:
        row["TotalCharges"] = row["MonthlyCharges"] * row["tenure"]
    row["services_count"] = (
        sum(1 for c in SERVICE_COLS if row[c] == "Yes")
        + (1 if row["InternetService"] != "No" else 0)
    )
    row["tenure_group"] = tenure_group(row["tenure"])
    prob = float(get_pipeline().predict_proba(pd.DataFrame([row]))[0][1])
    level = risk_level(prob)
    return prob, level, ACTIONS[level], row
