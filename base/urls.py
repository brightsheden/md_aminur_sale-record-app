from django.urls import path
from base.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login', login_view, name='login'),
    path('salepannel', admin_view, name='admin')
    
]
