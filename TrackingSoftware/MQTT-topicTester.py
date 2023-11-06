import paho.mqtt.client as mqtt
import json


# Define MQTT broker details
broker_address = "mqtt.devbit.be"
port = 1883

# Define MQTT topics for brightness and color
brightness_topic = "TrackingLights/brightness"
color_topic = "TrackingLights/color"
detected_color_topic = "TrackingLights/detected_color"
on_off_topic = "TrackingLights/on_off"
preset_topic = "TrackingLights/preset"

# Function to send MQTT message
def send_mqtt_message(topic, message):
    client = mqtt.Client()
    client.connect(broker_address, port, 60)
    client.publish(topic, message)
    client.disconnect()

# Function to change brightness
def change_brightness():
    brightness = input("Enter the brightness value (0-255): ")
    message = json.dumps({"bri": int(brightness)})
    send_mqtt_message(brightness_topic, message)

# Function to change color
def change_color():
    color = input("Enter the color value (in hex, e.g., FFFFFF for white): ")
    message = json.dumps({"color": color})
    send_mqtt_message(color_topic, message)

    # Function to change color
def change_detected_color():
    color = input("Enter the color value (in hex, e.g., FFFFFF for white): ")
    message = json.dumps({"dc": color})
    send_mqtt_message(detected_color_topic, message)

# Function to turn on/off
def toggle_on_off():
    on_off = input("Enter 'on' to turn on or 'off' to turn off: ")
    message = json.dumps({"on": True if on_off == 'on' else False})
    send_mqtt_message(on_off_topic, message)

# Function to change preset
def change_preset():
    preset = input("Enter the preset value: ")
    message = json.dumps({"pr": int(preset)})
    send_mqtt_message(preset_topic, message)

# Main loop
while True:
    print("\nChoose what you want to change:")
    print("1. Brightness")
    print("2. Color")
    print("3. Detected color")
    print("3. On/Off")
    print("4. Preset")
    print("5. Quit")
    choice = input("Enter your choice (1-5): ")

    if choice == '1' or choice == 'b' or choice == 'B' or choice == "bri":
        change_brightness()
    elif choice == '2' or choice == 'c' or choice == 'C' or choice == "color":
        change_color()
    elif choice == '3' or choice == 'dc' or choice == 'DC':
        change_detected_color()
    elif choice == '4':
        toggle_on_off()
    elif choice == '5' or choice == 'p' or choice == "preset":
        change_preset()
    elif choice == '6' or choice == 'e' or choice == "exit":
        break
    else:
        print("Invalid choice. Please try again.")
