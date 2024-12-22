from django.urls import path
from .views import KPIListCreateView, AssetKPICreateView
from .views import airflowValueView

urlpatterns = [
    path('kpis/', KPIListCreateView.as_view(), name='kpi-list-create'),
    path('assets/link/', AssetKPICreateView.as_view(), name='asset-kpi-link'),
    path('', KPIListCreateView.as_view(), name='kpi-list-create'),
    path('calculate-kpi/', airflowValueView.as_view(), name='calculate_kpi'),
]


