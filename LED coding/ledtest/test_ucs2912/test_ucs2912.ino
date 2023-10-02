// Hackish sketch to get something going with UCS2912 based strips:
// http://www.greeled.net/rgbw-addressable-led-strip.html
// Should be used with Adafruit NeoPixel version 1.0.3
// Hacked by G. Knauf 2015-12-07

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

// Enable serial output
//#define SERIAL_OUT	1

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#ifdef __AVR_ATtiny85__
#define NEO_PIN		0  // NeoPixel DATA
#undef  LED_BUILTIN
//#define LED_BUILTIN	0 // LED on Model B
#define LED_BUILTIN	1 // LED on Model A
#else
#define NEO_PIN		6  // NeoPixel DATA
#endif

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS	60

#define BRIGHTNESS	64 // set max brightness

#define RED		0x00FF0000 // --> RED
#define GREEN		0x0000FF00 // --> GREEN
#define BLUE		0x000000FF // --> BLUE
#define WHITE		0xFF000000 // --> WHITE LED
#define INIT_MSG	"Strip is set to 32-bit type (RGBW)"

#define IWAIT		2000
#define SWAIT		25
#define LWAIT		50
#define HWAIT		5000

uint32_t colors[4] = {RED, GREEN, BLUE, WHITE};
 
// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_GRBW    Pixels are wired for GRBW bitstream (f.e. SK6812)
//   NEO_RGBW    Pixels are wired for RGBW bitstream
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, NEO_PIN, NEO_RGBW + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

// NOTE: RGBW LEDs draw up to 80mA with all colors + white at full brightness!
// That means that a 60-pixel strip can draw up to 60x 80 = 4800mA, so you
// should use a 5A power supply; for a 144-pixel strip its max 11520mA = 12A!

void setup() {
#ifdef __AVR_ATtiny85__
  // This is for Trinket 5V 16MHz
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  // End of trinket special code
#endif

#ifdef LED_BUILTIN
  // Turn the onboard LED off by making the voltage LOW
  pinMode(LED_BUILTIN, OUTPUT); 
  digitalWrite(LED_BUILTIN, LOW);
#endif

  strip.begin(); // This initializes the NeoPixel library.
  strip.setBrightness(BRIGHTNESS); // set brightness
  strip.show(); // Initialize all pixels to 'off'

#ifdef SERIAL_OUT
  // initialize serial communication:
  while (!Serial);  // for Leonardo/Micro/Zero
  Serial.begin(9600);
  Serial.println(INIT_MSG);
#endif

#ifdef IWAIT
  delay(IWAIT);
#endif
}

void loop() {
  // Here we loop through the 4 colors in the colors array:
  // RED, GREEN, BLUE, LED_WHITE
  for (int i=0; i < 4; i++) {
#ifdef SERIAL_OUT
    serialWrite(colors[i]);
#endif
    setUCS2912AllPixels(colors[i]);
    strip.show();
    delay(HWAIT);
  }
}

// This function fills all pixels with a color.
void setUCS2912AllPixels(uint32_t c) {
  for(uint16_t i=0; i < strip.numPixels(); i++) {
    setUCS2912PixelColor(i, c);
  }
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

#ifdef SERIAL_OUT
// This function prints an uint32_t value as HEX and BIN
void serialWrite(uint32_t value) {
  if (value < 0x10000000)
    Serial.print("0");
  if (value < 0x1000000)
    Serial.print("0");
  if (value < 0x100000)
    Serial.print("0");
  if (value < 0x10000)
    Serial.print("0");
  if (value < 0x1000)
    Serial.print("0");
  if (value < 0x100)
    Serial.print("0");
  if (value < 0x10)
    Serial.print("0");
  Serial.print(value, HEX);
  Serial.print(" : ");
  for (uint32_t mask = 0x80000000; mask; mask >>= 1)
    Serial.print(mask & value ? '1' : '0');
  Serial.println();
}
#endif
