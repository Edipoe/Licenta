import paho.mqtt.client as mqtt
from .models import Message

# Funcția de tratare a mesajelor primite
def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    Message.objects.create(content=msg)

# Inițializarea clientului MQTT cu versiunea API-ului de callback specificată
client = mqtt.Client(callback_add=on_message)

# Conectarea la brokerul MQTT și abonarea la un subiect
client.connect("broker_address", 1883)
client.subscribe("topic")

# Pornirea buclei de gestionare a conexiunii
client.loop_start()
