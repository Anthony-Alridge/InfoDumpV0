from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^signUpPage/$', views.sign_up_page, name='sign_up')
    ]
