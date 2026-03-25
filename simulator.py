import paho.mqtt.client as mqtt
import time
import random

# MQTT settings
broker = "localhost"
topic = "rehab/patient1/angle"

client = mqtt.Client()
client.connect(broker, 1883, 60)

print("Simulator started...")

while True:
    # fake angle data generating
    angle = random.randint(20, 90)

    # publish data
    client.publish(topic, angle)

    print(f"Sent angle: {angle}")

    time.sleep(2)  # send every 2 seconds