import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time

# MQTT
broker = "localhost"
topic = "rehab/patient1/angle"

# InfluxDB config
url = "http://localhost:8086"
token = "VXppg374SlPoiX7nfz5GSYOdQyxxzMkF-figqb85kSYy_JxHZZv9nDd7UZz4KCVx_w00tryc-zs6TzlW5UTs5w=="
org = "RehabSense"
bucket = "rehab_data"

client_db = InfluxDBClient(url=url, token=token, org=org)
write_api = client_db.write_api(write_options=SYNCHRONOUS)

# MQTT callback
def on_message(client, userdata, msg):
    data = int(msg.payload.decode())
    print(f"Received: {data}")

    # create data point
    point = Point("rehab_angle") \
        .tag("patient", "patient1") \
        .field("angle", data) \
        .time(time.time_ns(), WritePrecision.NS)

    # write to DB
    write_api.write(bucket=bucket, org=org, record=point)

# MQTT setup
client = mqtt.Client()
client.connect(broker, 1883, 60)

client.subscribe(topic)
client.on_message = on_message

print("Backend + DB is running...")

client.loop_forever()