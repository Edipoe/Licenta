from datetime import datetime, timedelta
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import random
from .models import Post, SensorData  # Importăm modelul SensorData


import sqlite3

con = sqlite3.connect("sensor_data.db")
con.execute("CREATE TABLE IF NOT EXISTS sensor_data(timestamp, sensor_name, ecg_data, spo2_level, heart_rate, temp, fall_detected)")

#
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Salvează utilizatorul în baza de date
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')  # Folosim 'password1' pentru a obține parola
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('MonitoringApp/dashboard.html')
#     else:
#         form = UserCreationForm()
#     return render(request, 'MonitoringApp/register.html', {'form': form})
#
#
# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('MonitoringApp/dashboard.html')
#
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('MonitoringApp/dashboard.html')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'MonitoringApp/login.html', {'form': form})
#
#
# def register_view(request):
#     posts = Post.objects.all()  # Obține toate articolele din baza de date
#     return render(request, 'MonitoringApp/register.html', {'posts': posts})


@login_required(login_url='user-login')
def show_graph(request, template_name='MonitoringApp/live_graph.html'):
    return render(request, template_name)


@login_required(login_url='user-login')
def fetch_sensor_values_ajax(request):
    data = {}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            con = sqlite3.connect("sensor_data.db")
            cursor = con.cursor()
            result = cursor.execute("SELECT timestamp, ecg_data, spo2_level, heart_rate, temp, fall_detected FROM sensor_data ORDER BY timestamp DESC LIMIT 1;")
            row = result.fetchone()
            if row:
                timestamp, ecg_data, spo2_level, heart_rate, temp, fall_detected = row
                sensor_data_array = {
                    'timestamp': timestamp,
                    'ecg_data': ecg_data if ecg_data is not None else 0.0,
                    'spo2_level': spo2_level if spo2_level is not None else 0,
                    'heart_rate': heart_rate if heart_rate is not None else 0,
                    'temp': temp if temp is not None else 0,
                    'fall_detected': fall_detected if fall_detected is not None else False,
                }
                
                data['fall_detected'] = fall_detected
                data['heart_rate'] = heart_rate
                data['spo2_level'] = spo2_level

                
                
            else:
                sensor_data_array = [{
                    'timestamp': datetime.now(),
                    'ecg_data': 0.0,
                    'spo2_level': 0,
                    'heart_rate': 0,
                    'fall_detected': False,
                }]
                data['fall_detected'] = False
                pass

            cursor.close()
            con.close()

            data['result'] = sensor_data_array
            print("Sensor data:", sensor_data_array)

        except Exception as e:
            print(f"Error reading sensor data: {e}")
            # sensor_data_array = {
            #     'timestamp': datetime.now(),
            #     'ecg_data': 0.0,
            #     'spo2_level': 0,
            #     'heart_rate': 0,
            #     'temp': 0,
            #     'fall_detected': False,
            # }
            # data['fall_detected'] = False
            # data['result'] = sensor_data_array

    else:
        data['result'] = 'Not Ajax'

    return JsonResponse(data)


@csrf_exempt
def post_sensor_values_ajax(request):
    try:
        sensor_data = json.loads(request.body)
        sensor_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fall_detected = True if sensor_data.get('fall_detected') == 'true' else False
        
        # Salvarea datelor în baza de date SQLite
        con = sqlite3.connect("sensor_data.db")
        cursor = con.cursor()

        cursor.execute("""
            INSERT INTO sensor_data (timestamp, sensor_name, ecg_data, spo2_level, heart_rate, temp, fall_detected) 
            VALUES (:timestamp, :sensor_name, :ecg_data, :spo2_level, :heart_rate, :temp, :fall_detected)
        """, sensor_data)
        con.commit()
        cursor.close()
        con.close()

        return JsonResponse({"ok": True})
    
    except Exception as e:
        print(f"Error saving sensor data: {e}")
        return JsonResponse({"ok": False})


@login_required(login_url='user-login')
def show_dashbord(request, template_name='MonitoringApp/dashboard.html'):
    return render(request, template_name)
