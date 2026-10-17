import json
import os
import time

import paho.mqtt.client as mqtt

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


MQTT_BROKER = os.getenv("MQTT_BROKER", "host.docker.internal")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "lab5/sensores")

MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")


print("Iniciando ingestor MQTT -> InfluxDB")


influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = influx_client.write_api(
    write_options=SYNCHRONOUS
)


def on_connect(client, userdata, flags, reason_code, properties):

    print(f"Conectado a MQTT. Código: {reason_code}")

    client.subscribe(
        MQTT_TOPIC,
        qos=1
    )

    print(f"Suscrito al topic: {MQTT_TOPIC}")


def on_message(client, userdata, msg):

    try:

        payload = msg.payload.decode("utf-8")

        print(f"Mensaje recibido: {payload}")

        data = json.loads(payload)

        point = (
            Point("environment")
            .tag("device", "sensor-lab5")
            .field("temperature", float(data["temperature"]))
            .field("humidity", float(data["humidity"]))
            .field("illuminance", float(data["illuminance"]))
        )

        write_api.write(
            bucket=INFLUX_BUCKET,
            org=INFLUX_ORG,
            record=point
        )

        print("Datos guardados correctamente en InfluxDB")

    except Exception as e:

        print(f"ERROR procesando mensaje: {e}")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="ingestor-lab5"
)


client.username_pw_set(
    MQTT_USER,
    MQTT_PASSWORD
)


client.on_connect = on_connect
client.on_message = on_message


while True:

    try:

        print(
            f"Conectando a MQTT en "
            f"{MQTT_BROKER}:{MQTT_PORT}"
        )

        client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            60
        )

        break

    except Exception as e:

        print(f"MQTT aún no disponible: {e}")
        time.sleep(5)


client.loop_forever()
