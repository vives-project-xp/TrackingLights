import paho.mqtt.client as mqtt
import json
import time
class MqttController:

	def __init__(self):
		# Define MQTT topics
		self.brightness_topic = "TrackingLights/brightness"
		self.color_topic = "TrackingLights/color"
		self.on_off_topic = "TrackingLights/on_off"
		self.preset_topic = "TrackingLights/preset"
		self.detected_topic = "TrackingLights/detected_color"

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
																(self.on_off_topic, 0), (self.preset_topic, 0), (self.detected_topic,0)])

		self.mqtt_client.loop_start()


		self.preset = 0
		self.color = "FFFFFF"


		#default values to use when need to reset
		self.resetValues = {"on": True, "color": [255,255,255], "bri": 125, "seg":{"i": [0,100,"FFFFFF"]}}

		self.detectionInput = {"on": True, "color": [255,255,255], "bri": 125, "seg":{"i": [0,100,"FFFFFF"]}}

		self.input = {"on": True, "bri": 125, "seg":{"i": [0,100, "FF0000"]}}

		

		return

	# Callback when the client connects to the broker
	def on_connect(self, client, userdata, flags, rc):
		print(f"Connected with result code {rc}")

	#Send tracking data to mqtt
	def mqttTracking(self, trackingJson):
		trackingJson = json.dumps(trackingJson)
		print(trackingJson)

		self.mqtt_client.publish("TrackingLights/leddriver/api", trackingJson)
		return

	def mqttRecieve(self, client, userdata, message):

		print(f"Received message on topic {message.topic}: {message.payload.decode()}")

		try:
			received_data = json.loads(message.payload.decode())


			# check for correct topic used
			# Update data based on the received data

			# color change outside detection
			if message.topic == self.color_topic:
				if 'color' in received_data:
						self.color = received_data['color']
						print(received_data["color"])

			if message.topic == self.detected_topic:
				# Background color
				if 'color' in received_data:
					self.detectionInput['color'] = received_data["color"]
					
				# Detection color
				if 'dc' in received_data:
					self.detectionInput['dc'] = received_data["dc"]
					print(received_data["dc"])

			#globals
			if 'bri' in received_data:
					self.input['bri'] = received_data["bri"]
					print(received_data["bri"])

			if 'on' in received_data:
					self.input['on'] = received_data["on"]
					print(received_data["on"])
			if 'pr' in received_data:
					self.preset = received_data['pr']
					print(received_data["pr"])


		except json.JSONDecodeError as e:
			print(f"Error decoding JSON: {e}")

	def mqttUpdate(self):
		self.input['seg']['i'] = [0,100, self.color]

		jsonConvert = json.dumps(self.input)
		print(jsonConvert)
		self.mqtt_client.publish("TrackingLights/leddriver/api", jsonConvert)
		time.sleep(1)
		return	

	def getPreset(self): 
		return self.preset


	def preset3(self):
		print("Patern3")
		return


	def preset1(self):

		var = self.resetValues
		
		var['seg']['i'] = [0, 100, "FF0000"]
		for x in range(0,100,2):
			var['seg']['i'].append([x,x,"00FF00"])
			
		first = json.dumps(var) 
		
		var['seg']['i'] = [0,100, "00FF00"]
		for x in range(1,100, 2):
			var['seg']['i'].append([x,x, "FF0000"])
		
		second = json.dumps(var)

		while(True):
			
			self.mqtt_client.publish("TrackingLights/leddriver/api", first)
			time.sleep(1)
			self.mqtt_client.publish("TrackingLights/leddriver/api", second)
			time.sleep(1)


		return



	def preset2(self):
		print("Patern2")
		return

	def preset420(self):
		self.mqttUpdate()
		return

	def getInput(self):
		return self.input

	def getDetectionInput(self):
		return self.detectionInput

def on_connect(client, userdata, flags, rc):
		print(f"Connected with result code {rc}")