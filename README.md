# TrackingLights
Within this project we will create a ledstrip that follows the passing people. This is made possible with a camera that tracks those people.

The lightstrip is 10m. The strip itself is powered by an 24V powersupply, and controlled by an ESP32. Which at his turn get's input from the raspberry pi. This raspberry pi is connected with a camera to monitor the lightstrip at the opposite side of the building. The camera and raspberry pi are hidden away behind glass. 

Required hardware: 
----------------------------------------------------------------------------------------------------------
Led strips: we use the tm1814 leds. These operate at 24V

Esp32: This is used to control the led's. The ESP receives data from the raspberry pi

Power supply led's + Esp32: Here we used a 24V+15A power supply, since the esp32 draws power (5v) from the leds we don't need to make any adaptations to power it.

raspberry pi: This will convert the raw footage from the camera into values, which will be send to the ESP.

Camera: For the camera we chose the raspberry pi camera V2. The V2 is an 8mp camera with the sony IMX219 sensor, the camera is easy to work with but has potential for more complicated things. This will connect to the raspberry pi.

Power supply raspberry pi: 5V

Wiring: ....

Optional hardware:
---------------------------------------------------------------------------------------
Case for camera + raspberry pi: 

Case for power supply led's + ESP32: Since we want to hang our power supply behind the rails, we will 3d print a case to do so.

Cabletray: We used this to put in our ledstrips. These help defusing the light

support for cabletray: these were 3d printed to hold to cabletray onto the rails.

Joints for cabletray: Since we need to connect multiple trays, we 3d printed some joints.


Required software:
--------------------------------------------------------------------------------------------
MQTT: 

WLED: Since we did not find any excisting libraries for the tm1814(ledstrip), we will be using WLED. This is easy to use software with premade animations.

Python: 

Schematics + flowchart:
---------------------------------------------------------------------------------------------

