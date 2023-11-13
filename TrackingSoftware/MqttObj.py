import paho.mqtt.client as mqtt
import json

from credentials import USERNAME, PASSWORD


class MqttController:
    def __init__(self):
        # Define MQTT topics
        self.brightness_topic = "PM/Aurora/Aurora/brightness"
        self.color_topic = "PM/Aurora/Aurora/color"
        self.on_off_topic = "PM/Aurora/Aurora/on_off"
        self.preset_topic = "PM/Aurora/Aurora/preset"
        self.detected_topic = "PM/Aurora/Aurora/detected_color"

        # Define mqtt broker
        broker_address = "projectmaster.devbit.be"
        port = 1883

        # Define username and password
        username = USERNAME
        password = PASSWORD

        # Initialize mqtt connection
        self.mqtt_client = mqtt.Client()

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.mqttRecieve

        self.mqtt_client.username_pw_set(username, password)

        self.mqtt_client.connect(broker_address, port, 60)

        # Subscribe to topics on successful connection
        self.mqtt_client.subscribe(
            [
                (self.brightness_topic, 0),
                (self.color_topic, 0),
                (self.on_off_topic, 0),
                (self.preset_topic, 0),
                (self.detected_topic, 0),
            ]
        )

        self.mqtt_client.loop_start()

        # default values to use when need to reset
        self.resetValues = {"on": True, "color": [255, 255, 255], "bri": 125}

        self.input = {"on": True, "color": [255, 255, 255], "bri": 125, "dc": "FF0000"}

        self.preset = 0

        return

    # Callback when the client connects to the broker
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    # Send tracking data to mqtt
    def mqttTracking(self, trackingJson):
        trackingJson = json.dumps(trackingJson)
        print(trackingJson)

        self.mqtt_client.publish("PM/Aurora/Aurora/leddriver/api", trackingJson)
        return

    def mqttRecieve(self, client, userdata, message):
        print(f"Received message on topic {message.topic}: {message.payload.decode()}")

        try:
            received_data = json.loads(message.payload.decode())

            # Update data based on the received data
            if "bri" in received_data:
                self.input["bri"] = received_data["bri"]
                print(received_data["bri"])
            if "color" in received_data:
                self.input["color"] = received_data["color"]
                print(received_data["color"])
            if "on" in received_data:
                self.input["on"] = received_data["on"]
                print(received_data["on"])
            if "pr" in received_data:
                self.preset = 0
                print(received_data["pr"])
            if "dc" in received_data:
                self.input["dc"] = received_data["dc"]
                print(received_data["dc"])
            print(received_data)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def mqttUpdate(self):
        return

    def getPreset(self):
        return self.preset

    def preset3(self):
        print("Patern3")
        return

    def preset1(self):
        return

    def preset2(self):
        print("Patern2")
        return

    def getInput(self):
        return self.input


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
