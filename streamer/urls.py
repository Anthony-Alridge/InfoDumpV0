from django.conf.urls import url
from . import views

app_name = 'streamer'

urlpatterns = [
    url(r'^$', views.user_page, name='user_page'),
    url(r'^focusPage/$', views.focus_page, name='focus_page')
    ]