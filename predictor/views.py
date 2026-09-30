from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomerForm
from .models import Prediction
from .services import predict_churn


@login_required
def predict_view(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        name = data.pop("customer_name")
        prob, level, action, row = predict_churn(data)
        p = Prediction.objects.create(
            customer_name=name, contract=row["Contract"], tenure=row["tenure"],
            monthly_charges=row["MonthlyCharges"], inputs=row,
            probability=prob, risk_level=level, action=action,
            created_by=request.user,
        )
        return redirect("result", pk=p.pk)
    return render(request, "predict.html", {"form": form})


@login_required
def result_view(request, pk):
    return render(request, "result.html", {"p": get_object_or_404(Prediction, pk=pk)})


@login_required
def history_view(request):
    return render(request, "history.html", {"predictions": Prediction.objects.all()})

@login_required
def dashboard_view(request):
    qs = Prediction.objects.all()
    total = qs.count()
    high = qs.filter(risk_level="High").count()
    churners = qs.filter(probability__gte=0.5).count()
    rate = round(churners / total * 100, 1) if total else 0
    risk_data = [qs.filter(risk_level=r).count() for r in ["Low", "Moderate", "High"]]
    contracts = ["Month-to-month", "One year", "Two year"]
    contract_rates = []
    for c in contracts:
        sub = qs.filter(contract=c)
        n = sub.count()
        contract_rates.append(round(sub.filter(probability__gte=0.5).count() / n * 100, 1) if n else 0)
    return render(request, "dashboard.html", {
        "total": total, "high": high, "rate": rate,
        "risk_data": risk_data, "contracts": contracts, "contract_rates": contract_rates,
    })
