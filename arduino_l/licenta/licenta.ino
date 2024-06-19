//Includerea bibliotecilor necesare:
#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <MAX30100_PulseOximeter.h>


const char* ssid = "iPhone"; // Numele rețelei WiFi
const char* password = "123456789"; // Parola rețelei WiFi

const char* serverUrl = "http://172.20.10.2:8000/post_sensor_values_ajax/"; // Adresa IP și portul serverului Django

#define SENSOR_PIN A0 // Pinul senzorului analogic
//Configurarea senzorilor
void setup() {
  Serial.begin(115200);
  
  // Conectarea la rețea Wi-Fi
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectare la WiFi...");
    Serial.println(String(WiFi.status()));
  }
  
  Serial.println("Conectat la rețeaua WiFi");
  Serial.print("Adresa IP: ");
  Serial.println(WiFi.localIP());
}
//Citirea valorilor de la senzori
void loop() {
  // Citirea valorii de la senzor
  int sensorValue = analogRead(SENSOR_PIN);
  
  // Afisarea valorii citite
  Serial.print("Valoare senzor: ");
  Serial.println(sensorValue);
  
  // Verificarea conexiunii WiFi
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // Construirea payload-ului
    String payload = "{\"sensor_name\": \"ECG\", \"ecg_data\":" +String(sensorValue) + ", \"spo2_level\": 0, \"heart_rate\": 0, \"fall_detected\": false}";
//    String payload = "{\"sensor_name\":" + "\"Arduino\"," + 
//    "\"ecg_data\"" = random.randint(1, 4),  # Stocare de date brute de la ECG
//    spo2_level = random.randint(960, 999) / 10,  # Cantitatea de oxigen din sânge
//    heart_rate = random.randint(70, 120),  # Ritmul cardiac
//    fall_detectedString(sensorValue);
    
    // Configurarea antetului Content-Type
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
    // Trimiterea cererii POST și afișarea răspunsului
    int httpResponseCode = http.POST(payload);
    if (httpResponseCode > 0) {
      Serial.print("Răspuns HTTP: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Eroare HTTP: ");
      Serial.println(httpResponseCode);
    }
    
    // Eliberarea resurselor
    http.end();
  } else {
    Serial.println("Eroare de conexiune WiFi");
  }
  
  // Așteptare 5 secunde înainte de o nouă citire
  delay(5000);
}
