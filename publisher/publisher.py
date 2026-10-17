import json
import os
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


MQTT_BROKER = os.getenv("MQTT_BROKER", "host.docker.internal")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "lab5/sensores")

MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="publisher-lab5"
)

client.username_pw_set(
    MQTT_USER,
    MQTT_PASSWORD
)


while True:
    try:
        print(f"Conectando a MQTT en {MQTT_BROKER}:{MQTT_PORT}")

        client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            60
        )

        break

    except Exception as e:
        print(f"MQTT no disponible: {e}")
        time.sleep(5)


client.loop_start()

print("Publicador MQTT iniciado correctamente")


while True:

    data = {
        "temperature": round(random.uniform(20, 32), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "illuminance": round(random.uniform(100, 900), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    mensaje = json.dumps(data)

    result = client.publish(
        MQTT_TOPIC,
        mensaje,
        qos=1
    )

    result.wait_for_publish()

    print(f"Publicado: {mensaje}")

    time.sleep(30)
