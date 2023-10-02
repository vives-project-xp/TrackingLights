// Hackish sketch to get something going with UCS2912 based strips:
// http://www.greeled.net/rgbw-addressable-led-strip.html
// Tested with Adafruit NeoPixel version 1.0.3
// Hacked by G. Knauf 11/2015

#include <Adafruit_NeoPixel.h>
#include "Color_Definitions.h"
#ifdef __AVR__
#include <avr/power.h> // Comment out this line for non-AVR boards (Arduino Due, etc.)
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#ifdef __AVR_ATtiny85__
#define NEO_PIN		0  // NeoPixel DATA
#undef  LED_BUILTIN
//#define LED_BUILTIN	0  // LED on Model B
#define LED_BUILTIN	1  // LED on Model A
#else
#define NEO_PIN		6  // NeoPixel DATA
#endif

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS	60

#define BRIGHTNESS	64 // set max brightness

#define IWAIT		2000
#define SWAIT		20
#define LWAIT		50
#define HWAIT		1500

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, NEO_PIN, NEO_RGBW + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

void setup() {
#ifdef __AVR_ATtiny85__
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  // End of trinket special code
#endif

#ifdef LED_BUILTIN
  // Turn the onboard LED off by making the voltage LOW
  pinMode(LED_BUILTIN, OUTPUT); 
  digitalWrite(LED_BUILTIN, LOW);
#endif

  strip.begin();
  strip.setBrightness(BRIGHTNESS); // set brightness
  strip.show(); // Initialize all pixels to 'off'

#ifdef IWAIT
  delay(IWAIT);
#endif
}

void loop() {
  // strip.clear();
  // Some example procedures showing how to display to the pixels:
  colorWipe(RED, SWAIT);
  colorWipeReverse(DARKRED, SWAIT);
  colorWipe(GREEN, SWAIT);
  colorWipeReverse(DARKGREEN, SWAIT);
  colorWipe(MAGENTA, SWAIT);
  colorWipeReverse(DARKMAGENTA, SWAIT);
  colorWipe(BLUE, SWAIT);
  colorWipeReverse(DARKBLUE, SWAIT);
  colorWipe(TURQUOISE, SWAIT);
  colorWipeReverse(DARKTURQUOISE, SWAIT);
  colorWipe(WHITE_LED, SWAIT); // use the real White LEDs
  colorWipeReverse(DIMWHITE_LED, SWAIT); // use the real White LEDs
  delay(HWAIT);
  colorWipeReverse(BLACK, LWAIT);
  delay(HWAIT);

  // Send a theater pixel chase in...
  theaterChase(WHITE_LED, LWAIT); // use the real White LEDs
  // theaterChase(GRAY, LWAIT); // White
  theaterChase(MAROON, LWAIT); // Red
  theaterChase(NAVY, LWAIT); // Blue
  theaterChase(LIME, LWAIT); // Green
  theaterChase(PURPLE, LWAIT); // Purple

  rainbow(LWAIT);
  rainbowCycle(SWAIT);
  theaterChaseRainbow(LWAIT);
}

// This works only when the lib is initialized with NEO_RGBW pixel type! 
void setUCS2912PixelColor(uint16_t n, uint32_t c) {
  uint32_t t;

  switch(n % 3) {
    case 0:
      strip.setPixelColor(n, c);
      break;
    case 1:
      t = (c & 0xffffff00) | (strip.getPixelColor(n) & 0x000000ff);
      strip.setPixelColor(n, t);
      t = ((c & 0x000000ff) << 16) | (strip.getPixelColor(n+1) & 0xff00ffff);
      strip.setPixelColor(n+1, t);
      break;
    case 2:
      t = ((c & 0x00ff0000) >> 16) | (strip.getPixelColor(n-1) & 0xffffff00);
      strip.setPixelColor(n-1, t);
      t = strip.getPixelColor(n) & 0x00ff0000;
      t |= ((c & 0x0000ff00) << 16) | ((c & 0xff000000) >> 16) | (c & 0x000000ff);
      strip.setPixelColor(n, t);
      break;
  }
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint16_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    setUCS2912PixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

// Fill the dots one after the other with a color backward
void colorWipeReverse(uint32_t c, uint16_t wait) {
  for(uint16_t i=strip.numPixels(); i>0; i--) {
    setUCS2912PixelColor(i-1, c);
    strip.show();
    delay(wait);
  }
}

void rainbow(uint16_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      setUCS2912PixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint16_t wait) {
  uint16_t i, j;

  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      setUCS2912PixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint16_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (int i=0; i < strip.numPixels(); i=i+3) {
        setUCS2912PixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();
     
      delay(wait);
     
      for (int i=0; i < strip.numPixels(); i=i+3) {
        setUCS2912PixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint16_t wait) {
  for (int j=0; j < 256; j++) {     // cycle all 256 colors in the wheel
    for (int q=0; q < 3; q++) {
        for (int i=0; i < strip.numPixels(); i=i+3) {
          setUCS2912PixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
        }
        strip.show();
       
        delay(wait);
       
        for (int i=0; i < strip.numPixels(); i=i+3) {
          setUCS2912PixelColor(i+q, 0);        //turn every third pixel off
        }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
   return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else if(WheelPos < 170) {
    WheelPos -= 85;
   return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  } else {
   WheelPos -= 170;
   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  }
}

