Feelings Panel – D1 mini, OLED and WS2812B
A small ESP8266/D1 mini project that lets the user select how they feel using one button.
The OLED screen shows a simple monochrome figure and the selected feeling. The WS2812B LED strip changes color to match the selected feeling.
Hardware
LOLIN/WEMOS D1 mini or compatible ESP8266 board
128×64 I2C OLED display, address `0x3C`
1 push button
WS2812B LED strip/module with 5 LEDs
USB power
Wiring
OLED
OLED	D1 mini
GND	G
VCC	3V3
SCL	D1
SDA	D2
Button
Button	D1 mini
One side	D3
Other side	G
Do not hold the button while powering or uploading. D3 is also used during ESP8266 boot.
WS2812B
WS2812B	D1 mini
5V	5V
GND	G
DIN	D6
Recommended: place a 330 Ω resistor between D6 and DIN.
Arduino libraries
Install these from Arduino IDE Library Manager:
Adafruit SSD1306
Adafruit GFX Library
Adafruit NeoPixel
Board settings
Use an ESP8266 board profile, for example:
Board: `LOLIN(WEMOS) D1 R2 \& mini`
Upload speed: `115200`
Feelings and colors
Feeling	LED color
HAPPY	Yellow
SAD	Blue
ANGRY	Red
SCARED	Purple
DISGUST	Green
ANXIOUS	Orange
STRESSED	Red/Pink
TIRED	Soft blue/purple
CALM	Turquoise
PROUD	White
