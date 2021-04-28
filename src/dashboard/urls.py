from django.urls import path

from dashboard.views import index_view
from dashboard.views import home_dashboard_view
from dashboard.views import new_dashboard_view

app_name = 'dashboard'

urlpatterns = [
#    path('', index_view, name='index'),
    path('', home_dashboard_view, name='home'),
    path('new', new_dashboard_view, name="new"),
]
