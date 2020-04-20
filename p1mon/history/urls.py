from django.urls import path
from history import views

urlpatterns = [
    path('electricity/<str:timestep>', views.history_chart_elec, name='history_chart_elec'),
    path('gas/<str:timestep>', views.history_chart_gas, name='history_chart_gas'),
    path('costs/<str:timestep>', views.history_chart_costs, name='history_chart_costs'),
]