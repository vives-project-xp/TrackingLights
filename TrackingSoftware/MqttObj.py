import paho.mqtt.client as mqtt
import json

class MqttController:

	def __init__(self):
		# Define MQTT topics
		self.brightness_topic = "TrackingLights/brightness"
		self.color_topic = "TrackingLights/color"
		self.on_off_topic = "TrackingLights/on_off"
		self.preset_topic = "TrackingLights/preset"

		#Define mqtt broker
		broker_address = "mqtt.devbit.be"
		port = 1883

		#Initialize mqtt connection
		self.mqtt_client = mqtt.Client()

		self.mqtt_client.on_connect = self.on_connect
		self.mqtt_client.on_message = self.mqttRecieve


		self.mqtt_client.connect(broker_address, port, 60)

		# Subscribe to topics on successful connection
		self.mqtt_client.subscribe([(self.brightness_topic, 0), (self.color_topic, 0),
																(self.on_off_topic, 0), (self.preset_topic, 0)])

		self.mqtt_client.loop_start()

		#default values to use when need to reset
		self.resetValues = {'on': True, 'color': [255, 255, 255], 'pr': 0, 'bri': 125}

		self.input = {'on': True, 'color': [255, 255, 255], 'pr': 0, 'bri': 125}

		return

	# Callback when the client connects to the broker
	def on_connect(self, client, userdata, flags, rc):
		print(f"Connected with result code {rc}")

	#Send tracking data to mqtt
	def mqttTracking(self, trackingJson):
		trackingJson = json.dumps(trackingJson)
		self.mqtt_client.publish("TrackingLights/leddriver/api", trackingJson)
		return

	def mqttRecieve(self, client, userdata, message):

		print(f"Received message on topic {message.topic}: {message.payload.decode()}")

		try:
			received_data = json.loads(message.payload.decode())

			# Update data based on the received data
			if 'bri' in received_data:
					self.input['bri'] = received_data["bri"]
					print(received_data["bri"])
			if 'color' in received_data:
					self.input['color'] = received_data["color"]
					print(received_data["color"])
			if 'on' in received_data:
					self.input['on'] = received_data["on"]
					print(received_data["on"])
			if 'pr' in received_data:
					self.input = received_data["pr"]
					print(received_data["pr"])

		except json.JSONDecodeError as e:
			print(f"Error decoding JSON: {e}")

	def mqttUpdate(self):

		return	

	def getPreset(self): 
		return self.input['pr']


	def preset3(self):
		print("Patern3")
		return


	def preset1(self):
		print("Patern1")
		return

	def preset2(self):
		print("Patern2")
		return


def on_connect(client, userdata, flags, rc):
		print(f"Connected with result code {rc}")