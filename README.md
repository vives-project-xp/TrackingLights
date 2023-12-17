# TrackingLights
Within this project we will create a LED strip that follows the passing people. This is made possible with a camera that tracks those people. This brings back life inside the hallways, we were motivated to start this project because it looked like a challenge. Throughout the project there is a lot of potential of learning new things.

The lightstrip is 10 meters long. The strip itself is powered by an 24V powersupply and controlled by an ESP32, which, in turn, receives input from the raspberry pi. This raspberry pi is connected with a camera to monitor the light strip at the opposite side of the building. The camera and raspberry pi are hidden away behind glass. 


## Table of contents:
-------------------------------------------------------------------------------------------------------
- [Required hardware](#required-hardware)
- [Optional hardware](#optional-hardware)
- [Required software](#required-software)
- [Communication between devices](#communication-between-devices)
- [Schematics + flowchart](#schematics-+-flowchart)
- [Files](#files)
- [How to use the trackinglights](#how-to-use-the-trackinglights)



## Required hardware: 
----------------------------------------------------------------------------------------------------------
Led strips: we use the tm1814 leds. These operate at 24V

Esp32: This is used to control the led's. The ESP receives data from the raspberry pi

Power supply led's + Esp32: Here we used a 24V+8A power supply. The led's have an average usage of 5A. So by using a power supply which could supply 8A, we have room for error.

24V-5V converter: Since the ESP32 runs on 5V, a converter is placed between the power supply of the leds and the ESP32.

Raspberry pi: This will convert the raw footage from the camera into values, which will be send to the ESP.

Camera: For the camera we chose the raspberry pi camera V2. The V2 is an 8mp camera with the sony IMX219 sensor, the camera is easy to work with but has potential for more complicated things. This will connect to the raspberry pi.

Power supply raspberry pi: 15W usb-C power brick for the raspberry pi

## Optional hardware:
---------------------------------------------------------------------------------------
Case for camera + raspberry pi

Case for power supply led's + ESP32: Since we want to hang our power supply behind the rails, we will 3d print a case to do so.

Cabletray: We used this to put in our ledstrips. These help defusing the light

Support for cabletray: these were 3d printed to hold to cabletray onto the rails.

<img width="412" alt="image" src="https://github.com/vives-project-xp/TrackingLights/assets/113900709/61eeae69-4b6b-4d3e-8441-1cb5ffd2a1b8">


Joints for cabletray: Since we need to connect multiple trays, we 3d printed some joints.

<img width="412" alt="image" src="https://github.com/vives-project-xp/TrackingLights/assets/113900709/0d146088-aeea-4482-9afa-474ef9cd9fe7">



## Required software:
--------------------------------------------------------------------------------------------

WLED: Since we did not find any excisting libraries for the tm1814(ledstrip), we will be using WLED. This is easy to use software with premade animations.

Python: The main programming language for this project.

Docker: This is used to run the python script on the raspberry pi

## Communication between devices:
------------------------------------------------------------------
<img width="460" alt="image" src="https://github.com/vives-project-xp/TrackingLights/assets/113900709/991873ee-3a01-4c94-b453-779dc50f9773">

De ESP32 werkt via WLED library met de leds

De esp krijgt communicatie van de raspberry pi via MQTT

We hebben een camera die met een bedrade connectie met de raspberry pi werkt.

## Schematics + flowchart:
---------------------------------------------------------------------------------------------
<img width="460" alt="image" src="https://github.com/vives-project-xp/TrackingLights/assets/113900709/61e99522-55ce-46ce-83c7-ac4cafe26142">

## Files
--------------------------------------------------------------------------------------------
3d prints: these contain all our 3d printing files that we used in this project.


LED coding:

 - a copy of the wled github repo 

TrackingSoftware:

  - camerafeed: live camera feed server
    
    - to have acces to the camera feed, you need to be connected to the same network as the raspberry pi 
  
  - mov: testing movies for our setup
    
  - Lights.py: controling the led's
  
  - MqttObj.py: communication between devices with MQTT
  
  - MQTT-topicTester.py: small program to test the MQTT communication to the ESP32 without using the Pi
  
  - TrackingLight.py: main project
 
docker-compose  
dockerfile

## How to use the trackinglights:
--------------------------------------------------------------------------------------------
### Connecting the hardware.

#### Ledstrips

In our setup, we have the power source in the middle of the 2 ledstrips. By doing this, we can reduce the power usage to counter the voltage drop. In this case the led's only use about 2A. During testing we also tried to power the led's from one side, however this resulted in a power usage of about 6A.
   
Connect the 24V power source to the both led strips. The red cable is 24V and the white cable is the GND.  Also connect the 2 connectors of the data cable. 

One connector on the sides of the ledstrip wil have holes, the other connector will have pins. The connector with the holes is the data input and will be connected to the ESP32. There will be 3 wires: a red wire (24V), a green wire (data input) and a white wire (GND) Do not use the red wire of the data cable. This is a 24V wire and will possibly damage the ESP32. The ground wire is save to use. Connect the green wire to an output pin of the ESP32 and the white wire to the ground of the ESP32.

Next up is the 24V-5V converter. We ran a different cable in the cable tray for 5V. This allows us to hide the power converter a bit better. Connect the 24V power source to the input of the converter. Connect the 5V output to the 5V pin of the ESP32. Connect the grounds of the input and output to each other. This way, we can use the ground of the ledstrip as the ground of the ESP32.

<img width="344" alt="image" src="https://github.com/vives-project-xp/TrackingLights/assets/113900709/f6251401-1f6a-4efd-876b-f74a726a33c1">

#### Raspberry pi

Connect the ribbon cable to the Raspberry Pi camera. The blue side of the ribbon cable should always be on the side of the black part of the connector. Connect the other side of the ribbon cable to the Raspberry Pi. The camera connector is located next to the HDMI ports. Be careful when connecting the ribbon cable, the connector is very fragile. Then connect the Raspberry Pi to the power brick.

### Installing the software.

#### WLED

We will begin by installing WLED on the ESP32. Connect the ESP32 to your computer with an USB-cable. Please access the following link using Chrome or Edge. (As of the writing of this tutorial, other browsers are not supported.)

[WLED-installation](https://install.wled.me/)

Press the install button and follow the directuions on the screen. When the installation is complete, you can keep the ESP32 connected to your computer for power, or you can connect it to another power source.

When the ESP32 boots without connecting to a network, it will create its own network called WLED-AP. Connect to this network and open a browser. Navigate to 1.2.3.4. You will be greeted by a WLED menu. Here you can configure the ESP32 to connect to your network.

<img width="344" alt="WLED setup page" src=img/WLED-install.png>

Click on the wifi setting button. Here you can scan for networks or manualy enter the SSID. After selecting the network, enter the password. The ESP32 will now connect to your network. 

It is higly recommended to set an mDNS name or save the generated ip adress. It will be easier to change the settings later on. Click on the save button to save the settings. The ESP32 will reboot and connect to your network.


<img width="344" alt="WLED wifi setup" src=img/WLED-wifi-setup.png>

When the ESP32 is connected to your network, you can access the WLED menu by navigating to the mDNS name or the IP adress. Once in the menu, you can change the settings to your liking.

<img width="500" alt="WLED menu" src=img/WLED-menu.png>

The most important settings for this project are the LED settings and the Sync settings.

<img width="500" alt="WLED config" src=img/WLED-config.png>

In the LED settings you can change the led type and the amount of led's. For this project we used the TM1814 led type. The amount of led's is 600 but this ledstrip already has the led's in groups of 6. So we set the amount of led's to 100 since we have 100 groups of 6 led's. It's also important to set the GPIO pin to the pin you connected the data wire to. In this case, we used GPIO pin 2. Because of the way we track people with the camera, we need to reverse the led's. This can be done by checking the reverse checkbox.

<img width="500" alt="WLED LED settings" src=img/WLED-led.png>

In the Sync settings you can enable the MQTT protocol. This will allow the ESP32 to receive data. The MQTT settings are as follows: 

<img width="500" alt="WLED MQTT settings" src=img/WLED-mqtt.png>

In the next step, we will setup a start-up routine. It was required for this project to default to white light when the ESP32 boots. This can be done by creating a preset. On the color wheel, select the color white. On the top-right of the screen, select the prefered brightness. In the preset menu on the right, click on the "+ Preset" button to create a new preset. Be sure to check the "Overwrite with state" checkbox. This will save the selected state as the preset. Click on the save button to save the preset. Next, click on the "+ Playlist" button. Select the preset we made earlier and set the duration 1 second. Uncheck the "Repeat indefinitely" checkbox and set the "Repeat" to 30 times. This will make sure the preset is played for 30 seconds while also making sure the led's recieve the signal frequent enough to not go back to the default rainbow animation. Click on the save button to save the playlist.

<img width="500" alt="WLED menu" src=img/WLED-menu2.png>

<img width="500" alt="WLED preset" src=img/WLED-preset.png>

<img width="500" alt="WLED playlist" src=img/WLED-playlist.png>

Now we need to set the playlist as the default. This can be done in the LED settings. Scroll down to the "Defaults" section and set "Apply preset" to "2". This should be the preset ID of the playlist.

<img width="500" alt="WLED defaults" src=img/WLED-default.png>

#### Raspberry pi

Acces your Raspberry Pi with your prefered method.

Run the following commands in the terminal to install docker.

```bash
curl -fsSL https://get.docker.com/ -o get-docker.sh
sh get-docker.sh
```

Next, clone the repository. There is one file that needs to be created manually. This is the credentials.py file and is located in the Trackingsoftware directory. This file contains the MQTT credentials. The file should look like this:

```python
USERNAME = "username"
PASSWORD = "password"
```
Change the username and password accordingly. The MQTT topics can be changed in the MqttObj.py file. The topics are located at the top of the file.

To see if the camera is detected, run the following command:
  
```bash
vcgencmd get_camera
```

If the camera is detected, you should see the following output:

```bash
supported=1 detected=1
```

If the camera is not detected, you should see the following output:

```bash
supported=1 detected=0
```

If the camera is not detected, you need to enable the camera. This can be done by running the following command:

```bash
sudo raspi-config nonint do_legacy 0
```

WARNING: in some cases, this will desable the creation of a desktop environment. For our project, this was not a problem since we are only using the Pi to track people. If you are using the Pi for other purposes, you might want to search the web for a different way to enable the camera.

Next, we can run the docker container. This can be done by running the following command in the main directory of the repository:

```bash
sudo docker compose up --build
```

The program will keep running until you stop it. To stop the program, you can use the following command:

```bash
sudo docker compose down
```
______________________________________________________________________________________________________________________
Created by Thibault Schroyens, Thomas Oddery, Szymon Dizewski and Maxime Vansteelandt on behalf of VIVES University
