from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.text_input, name='text_input'),
    path('output', views.text_output, name='text_output')
]