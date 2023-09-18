#include <FastLED.h>

#define NUM_LEDS 100 // Change this to the number of LEDs in your strip
#define DATA_PIN 8 // Change this to the GPIO pin you're using

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(64); // Adjust brightness (0-255)
}

void loop() {
  // Fill the entire strip with a single color
  fill_solid(leds, NUM_LEDS, CRGB(255, 255, 255)); // Red
  FastLED.show();
  delay(1000); // Pause for a second
  
}
