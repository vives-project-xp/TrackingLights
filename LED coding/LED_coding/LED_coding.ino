#include <TM1814.h>

#define PIN           6  // Define the pin connected to the data input of the LED strip
#define NUM_LEDS      50 // Define the number of LEDs in your strip

// Create an Adafruit_NeoPixel object
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_RGBW + NEO_KHZ800);

void setup() {
  // Initialize the strip
  strip.begin();
  strip.show();  // Initialize all pixels to 'off'
}

void loop() {
  // Set the entire strip to red
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, 255, 0, 0, 0);  // RGBW format: (R, G, B, W)
  }
  strip.show();

  // Delay for a while (in milliseconds)
  delay(1000);

  // Turn off the entire strip
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, 0, 0, 0, 0);
  }
  strip.show();

  // Delay again
  delay(1000);
}
