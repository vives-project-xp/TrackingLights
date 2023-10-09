import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/TrackingLights/cameraDetectionArray")  # Subscribe to the topic where the array is being published

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload}")

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT broker
mqtt_client.connect("mqtt.devbit.be", 1883, 60)  # Replace "broker_address" with your MQTT broker's address

# Start the MQTT loop
mqtt_client.loop_forever()
