from django.urls import path
from serialdata import views

urlpatterns = [
    path('live/<str:liveview>/', views.serialdata_live, name='serialdata_live'),
    path('live/charts/<str:liveview>/', views.serialdata_live_charts, name='serialdata_live_charts'),
    path('today/', views.serialdata_today, name='serialdata_today'),
    path('today/charts/', views.serialdata_today_charts, name='serialdata_today_charts'),
]