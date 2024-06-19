from django.urls import path,include
from . import views

app_name = 'MonitoringApp'

urlpatterns = [
   
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register_view'),
    path('dashboard/', views.show_dashbord, name='dashbord'),
    path('graph/', views.show_graph, name='show_graph'),
    path('fetch_sensor_values_ajax/', views.fetch_sensor_values_ajax, name='fetch_sensor_values_ajax'),
    path('post_sensor_values_ajax/', views.post_sensor_values_ajax, name='post_sensor_values_ajax'),

    
   
   
    
]
