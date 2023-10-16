import paho.mqtt.client as mqtt
import json

# Define MQTT topics
brightness_topic = "TrackingLights/brightness"
color_topic = "TrackingLights/color"
on_off_topic = "TrackingLights/on_off"
preset_topic = "TrackingLights/preset"

# Define MQTT broker details
broker_address = "mqtt.devbit.be"
port = 1883

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to topics on successful connection
    client.subscribe([(brightness_topic, 0), (color_topic, 0), (on_off_topic, 0), (preset_topic, 0)])

# Callback when a message is received from the broker
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")
    
    # Create JSON string based on the received message
    json_message = json.dumps({message.topic: message.payload.decode()})
    print(f"JSON representation: {json_message}")

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(broker_address, port, 60)

# Start MQTT loop (non-blocking)
mqtt_client.loop_start()

# Keep the program running
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Disconnect from MQTT broker
mqtt_client.loop_stop()
mqtt_client.disconnect()
