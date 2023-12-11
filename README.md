# TrackingLights
Within this project we will create a LED strip that follows the passing people. This is made possible with a camera that tracks those people. This brings back life inside the hallways, we were motivated to start this project because it looked like a challenge. Throughout the project there is a lot of potential of learning new things.

The lightstrip is 10 meters long. The strip itself is powered by an 24V powersupply and controlled by an ESP32, which, in turn, receives input from the raspberry pi. This raspberry pi is connected with a camera to monitor the light strip at the opposite side of the building. The camera and raspberry pi are hidden away behind glass. 


## Table of contents:
-------------------------------------------------------------------------------------------------------
...


## Required hardware: 
----------------------------------------------------------------------------------------------------------
Led strips: we use the tm1814 leds. These operate at 24V

Esp32: This is used to control the led's. The ESP receives data from the raspberry pi

Power supply led's + Esp32: Here we used a 24V+8A power supply. The led's have an average usage of 5A. So by using a power supply which could supply 8A, we have room for error.

24V-5V converter: Since the ESP32 runs on 5V, a converter is placed between the power supply of the leds and the ESP32.

raspberry pi: This will convert the raw footage from the camera into values, which will be send to the ESP.

Camera: For the camera we chose the raspberry pi camera V2. The V2 is an 8mp camera with the sony IMX219 sensor, the camera is easy to work with but has potential for more complicated things. This will connect to the raspberry pi.

Power supply raspberry pi: 5V

## Optional hardware:
---------------------------------------------------------------------------------------
Case for camera + raspberry pi: 

Case for power supply led's + ESP32: Since we want to hang our power supply behind the rails, we will 3d print a case to do so.

Cabletray: We used this to put in our ledstrips. These help defusing the light

support for cabletray: these were 3d printed to hold to cabletray onto the rails.
<img width="412" alt="image" src="https://github.com/vives-project-xp/TrackingLights/assets/113900709/61eeae69-4b6b-4d3e-8441-1cb5ffd2a1b8">


Joints for cabletray: Since we need to connect multiple trays, we 3d printed some joints.
<img width="412" alt="image" src="https://github.com/vives-project-xp/TrackingLights/assets/113900709/0d146088-aeea-4482-9afa-474ef9cd9fe7">



## Required software:
--------------------------------------------------------------------------------------------
MQTT: 

WLED: Since we did not find any excisting libraries for the tm1814(ledstrip), we will be using WLED. This is easy to use software with premade animations.

Python: 

## Communication between devices:
------------------------------------------------------------------
<img width="460" alt="image" src="https://github.com/vives-project-xp/TrackingLights/assets/113900709/991873ee-3a01-4c94-b453-779dc50f9773">



## Schematics + flowchart:
---------------------------------------------------------------------------------------------
<img width="460" alt="image" src="https://github.com/vives-project-xp/TrackingLights/assets/113900709/61e99522-55ce-46ce-83c7-ac4cafe26142">

## Files
--------------------------------------------------------------------------------------------
3d prints: these contain all our 3d printing files that we used in this project.


LED coding:

  -LED-coding: This is for controlling our LED strip using Adafruit library.
  
  -ledtest: This is for the lighting effects.
  
  -TM1814: header file for NeoPixel library. provides functions for controlling NeoPixel 
  
  -wled:

TrackingSoftware:

  -camerafeed: camerafeed live op html.
  
  -mov: testfilmpjes.
  
  -gititgnore: (werkt niet)
  
  -docker-compose: docker compose (start docker file) (verteld vb te restarten after failure)
  
  -dockerfile: docker file zelf (dependencies dowload)
  
  -lights: aansturen leds
  
  -MqttObj: commu met robbe
  
  -MQTT-topicTester: Test MQTT
  
  -trackingLight: main project.
 

## How to use the trackinglights:
--------------------------------------------------------------------------------------------
1) Het aansluiten van alle hardware.
   
-Led strips aansluiten op de 24V voeding (in ons geval x ampere). De ledstrips hebben een wit (ground) en rode (24V)     aansluiting. Je sluit deze parallel aan aan de bron. 

-Je sluit de 24V bron aan (in ons geval x ampere).

-Je sluit de ledstrips parallel aan. De ledstrips hebben een witte (ground) en rode (24V) aansluiting

-Je sluit de 24V-5V converter aan de 24V bron. De 5V uitgang zullen we nodig hebben voor het voeden van onze ESP32

-Je sluit de ESP32 aan aan de juiste zijde van de ledstrip

pin: 5V = 5V van converter

pin: GND = de grounding van de LED's, deze sluit je aan aan de witte wire van LED's

pin: 2 = data, deze sluit je aan aan de groene wire van LED's




Voor pi
-

-get docker.sh runnen (docker dowloaden)

-reposi copieren

-camera activeren (voor docker)  

-dockercontainer starten (blijft runnen, tot jij afzet)










