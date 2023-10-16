import time
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

# Define messages to send
brightness_message = "50"  # Example brightness value
color_message = json.dumps([255, 0, 0])  # Example color value (as a JSON string)
on_off_message = "true"  # Example on/off state
preset_message = "2"  # Example preset value

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(broker_address, port, 60)

# Send messages
mqtt_client.publish(brightness_topic, brightness_message)
time.sleep(1)  # Wait for a short period between messages
mqtt_client.publish(color_topic, color_message)
time.sleep(1)
mqtt_client.publish(on_off_topic, on_off_message)
time.sleep(1)
mqtt_client.publish(preset_topic, preset_message)

# Disconnect from MQTT broker
mqtt_client.disconnect()
