from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SensorData(models.Model):
    sensor_name = models.CharField(max_length=255)
    ecg_data = models.TextField()  # Stocare de date brute de la ECG
    spo2_level = models.FloatField()  # Cantitatea de oxigen din sânge
    heart_rate = models.IntegerField()  # Ritmul cardiac
    fall_detected = models.BooleanField(default=False)  # Alarmă de cădere
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sensor_name} at {self.timestamp}'