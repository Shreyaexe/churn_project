from django import forms

YN = ["Yes", "No"]
SVC = ["Yes", "No", "No internet service"]


def ch(options):
    return forms.ChoiceField(choices=[(o, o) for o in options])


class CustomerForm(forms.Form):
    customer_name = forms.CharField(max_length=100, required=False, label="Customer name / ID (optional)")
    gender = ch(["Female", "Male"])
    SeniorCitizen = forms.ChoiceField(choices=[("0", "No"), ("1", "Yes")], label="Senior citizen")
    Partner = ch(YN)
    Dependents = ch(YN)
    tenure = forms.IntegerField(min_value=0, max_value=72, label="Tenure (months)")
    PhoneService = ch(YN)
    MultipleLines = ch(["No", "Yes", "No phone service"])
    InternetService = ch(["DSL", "Fiber optic", "No"])
    OnlineSecurity = ch(SVC)
    OnlineBackup = ch(SVC)
    DeviceProtection = ch(SVC)
    TechSupport = ch(SVC)
    StreamingTV = ch(SVC)
    StreamingMovies = ch(SVC)
    Contract = ch(["Month-to-month", "One year", "Two year"])
    PaperlessBilling = ch(YN)
    PaymentMethod = ch(["Electronic check", "Mailed check",
                        "Bank transfer (automatic)", "Credit card (automatic)"])
    MonthlyCharges = forms.FloatField(min_value=0, label="Monthly charges")
    TotalCharges = forms.FloatField(min_value=0, required=False,
                                    label="Total charges (leave blank to auto-calculate)")
