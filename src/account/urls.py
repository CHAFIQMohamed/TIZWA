from django.urls import path

from account.views import registration_view
from account.views import logout_view
from account.views import login_view
from account.views import account_view
from account.views import must_authenticate_view

app_name = 'account'

urlpatterns = [    
    path('', account_view, name='home'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('must_authenticate/', must_authenticate_view, name='must_authenticate'),
    path('register/', registration_view, name='register'),
 ]