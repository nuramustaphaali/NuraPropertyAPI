# apps/finance/urls.py
from django.urls import path
from .views import ReportPaymentView, CreateDealView, MyTransactionHistoryView, VerifyPaymentView, KPIAnalyticsView, AgentPerformanceView

urlpatterns = [
    path("report/", ReportPaymentView.as_view(), name="report-payment"),
    path("history/", MyTransactionHistoryView.as_view(), name="payment-history"),
    path("verify/<str:transaction_id>/", VerifyPaymentView.as_view(), name="verify-payment"),
    path("deals/create/", CreateDealView.as_view(), name="create-deal"),

    path("analytics/admin-kpi/", KPIAnalyticsView.as_view(), name="admin-kpi"),
    path("analytics/my-performance/", AgentPerformanceView.as_view(), name="agent-performance"),
]