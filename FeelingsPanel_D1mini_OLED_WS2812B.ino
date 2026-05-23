#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDRESS 0x3C
#define SDA_PIN D2
#define SCL_PIN D1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define BUTTON_PIN D3
bool previousButtonState = HIGH;
unsigned long lastButtonPressTime = 0;

#define LED_PIN D6
#define LED_COUNT 5
#define LED_BRIGHTNESS 45
Adafruit_NeoPixel leds(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

const char* feelings[] = {
  "HAPPY", "SAD", "ANGRY", "SCARED", "DISGUST",
  "ANXIOUS", "STRESSED", "TIRED", "CALM", "PROUD"
};

const int feelingCount = sizeof(feelings) / sizeof(feelings[0]);
int selectedFeeling = 0;

const int FIG_X = 64;
const int FIG_Y = 36;

uint32_t getColorForFeeling(int index) {
  switch (index) {
    case 0: return leds.Color(255, 180, 0);    // HAPPY - yellow
    case 1: return leds.Color(0, 40, 255);     // SAD - blue
    case 2: return leds.Color(255, 0, 0);      // ANGRY - red
    case 3: return leds.Color(120, 0, 255);    // SCARED - purple
    case 4: return leds.Color(0, 180, 40);     // DISGUST - green
    case 5: return leds.Color(255, 80, 0);     // ANXIOUS - orange
    case 6: return leds.Color(255, 0, 80);     // STRESSED - red/pink
    case 7: return leds.Color(90, 90, 180);    // TIRED - soft blue/purple
    case 8: return leds.Color(0, 180, 180);    // CALM - turquoise
    case 9: return leds.Color(255, 255, 255);  // PROUD - white
    default: return leds.Color(20, 20, 20);
  }
}

void updateLed() {
  uint32_t color = getColorForFeeling(selectedFeeling);
  for (int i = 0; i < LED_COUNT; i++) {
    leds.setPixelColor(i, color);
  }
  leds.show();
}

void drawHead(int x, int y) { display.drawCircle(x, y, 9, SSD1306_WHITE); }

void drawBody(int x, int y) {
  display.drawLine(x, y + 9, x, y + 22, SSD1306_WHITE);
  display.drawLine(x, y + 22, x - 8, y + 30, SSD1306_WHITE);
  display.drawLine(x, y + 22, x + 8, y + 30, SSD1306_WHITE);
}

void drawEyes(int x, int y) {
  display.fillCircle(x - 4, y - 3, 1, SSD1306_WHITE);
  display.fillCircle(x + 4, y - 3, 1, SSD1306_WHITE);
}

void drawSmile(int x, int y) {
  display.drawLine(x - 6, y + 4, x - 3, y + 7, SSD1306_WHITE);
  display.drawLine(x - 3, y + 7, x + 3, y + 7, SSD1306_WHITE);
  display.drawLine(x + 3, y + 7, x + 6, y + 4, SSD1306_WHITE);
}

void drawSadMouth(int x, int y) {
  display.drawLine(x - 6, y + 7, x - 3, y + 4, SSD1306_WHITE);
  display.drawLine(x - 3, y + 4, x + 3, y + 4, SSD1306_WHITE);
  display.drawLine(x + 3, y + 4, x + 6, y + 7, SSD1306_WHITE);
}

void drawStraightMouth(int x, int y) {
  display.drawLine(x - 6, y + 6, x + 6, y + 6, SSD1306_WHITE);
}

void drawHappy(int x, int y) {
  drawHead(x, y); drawEyes(x, y); drawSmile(x, y); drawBody(x, y);
  display.drawLine(x, y + 14, x - 22, y + 4, SSD1306_WHITE);
  display.drawLine(x, y + 14, x + 22, y + 4, SSD1306_WHITE);
  display.drawPixel(x - 27, y, SSD1306_WHITE);
  display.drawPixel(x - 28, y, SSD1306_WHITE);
  display.drawPixel(x - 27, y - 1, SSD1306_WHITE);
  display.drawPixel(x + 27, y, SSD1306_WHITE);
  display.drawPixel(x + 28, y, SSD1306_WHITE);
  display.drawPixel(x + 27, y - 1, SSD1306_WHITE);
}

void drawSad(int x, int y) {
  drawHead(x, y); drawEyes(x, y); drawSadMouth(x, y); drawBody(x, y);
  display.drawLine(x, y + 14, x - 17, y + 23, SSD1306_WHITE);
  display.drawLine(x, y + 14, x + 17, y + 23, SSD1306_WHITE);
  display.drawPixel(x + 8, y + 1, SSD1306_WHITE);
  display.drawPixel(x + 9, y + 2, SSD1306_WHITE);
}

void drawAngry(int x, int y) {
  drawHead(x, y);
  display.drawLine(x - 8, y - 6, x - 2, y - 4, SSD1306_WHITE);
  display.drawLine(x + 8, y - 6, x + 2, y - 4, SSD1306_WHITE);
  drawEyes(x, y); drawStraightMouth(x, y); drawBody(x, y);
  display.drawLine(x, y + 14, x - 22, y + 14, SSD1306_WHITE);
  display.drawLine(x, y + 14, x + 22, y + 14, SSD1306_WHITE);
  display.drawRect(x - 26, y + 12, 4, 4, SSD1306_WHITE);
  display.drawRect(x + 22, y + 12, 4, 4, SSD1306_WHITE);
}

void drawScared(int x, int y) {
  drawHead(x, y);
  display.drawCircle(x - 4, y - 3, 3, SSD1306_WHITE);
  display.drawCircle(x + 4, y - 3, 3, SSD1306_WHITE);
  display.drawCircle(x, y + 6, 3, SSD1306_WHITE);
  drawBody(x, y);
  display.drawLine(x, y + 14, x - 21, y + 7, SSD1306_WHITE);
  display.drawLine(x, y + 14, x + 21, y + 7, SSD1306_WHITE);
  display.drawLine(x - 27, y + 13, x - 24, y + 16, SSD1306_WHITE);
  display.drawLine(x + 27, y + 13, x + 24, y + 16, SSD1306_WHITE);
}

void drawDisgust(int x, int y) {
  drawHead(x, y);
  display.fillCircle(x - 4, y - 3, 1, SSD1306_WHITE);
  display.fillCircle(x + 4, y - 1, 1, SSD1306_WHITE);
  display.drawLine(x - 6, y + 7, x + 6, y + 3, SSD1306_WHITE);
  drawBody(x, y);
  display.drawLine(x, y + 14, x - 15, y + 20, SSD1306_WHITE);
  display.drawLine(x, y + 14, x + 22, y + 10, SSD1306_WHITE);
  display.drawLine(x + 22, y + 10, x + 25, y + 7, SSD1306_WHITE);
}

void drawAnxious(int x, int y) {
  drawHead(x, y);
  display.drawCircle(x - 4, y - 3, 2, SSD1306_WHITE);
  display.drawCircle(x + 4, y - 3, 2, SSD1306_WHITE);
  display.drawLine(x - 6, y + 6, x - 3, y + 8, SSD1306_WHITE);
  display.drawLine(x - 3, y + 8, x, y + 6, SSD1306_WHITE);
  display.drawLine(x, y + 6, x + 3, y + 8, SSD1306_WHITE);
  display.drawLine(x + 3, y + 8, x + 6, y + 6, SSD1306_WHITE);
  drawBody(x, y);
  display.drawLine(x, y + 14, x - 10, y + 23, SSD1306_WHITE);
  display.drawLine(x, y + 14, x + 10, y + 23, SSD1306_WHITE);
  display.drawLine(x - 18, y - 6, x - 14, y - 9, SSD1306_WHITE);
  display.drawLine(x + 18, y - 6, x + 14, y - 9, SSD1306_WHITE);
}

void drawStressed(int x, int y) {
  drawHead(x, y);
  display.drawCircle(x - 4, y - 3, 2, SSD1306_WHITE);
  display.drawCircle(x + 4, y - 3, 2, SSD1306_WHITE);
  drawStraightMouth(x, y); drawBody(x, y);
  display.drawLine(x, y + 14, x - 20, y + 8, SSD1306_WHITE);
  display.drawLine(x, y + 14, x + 20, y + 8, SSD1306_WHITE);
  display.drawLine(x - 20, y - 8, x - 15, y - 12, SSD1306_WHITE);
  display.drawLine(x - 12, y - 12, x - 9, y - 16, SSD1306_WHITE);
  display.drawLine(x + 20, y - 8, x + 15, y - 12, SSD1306_WHITE);
  display.drawLine(x + 12, y - 12, x + 9, y - 16, SSD1306_WHITE);
}

void drawTired(int x, int y) {
  drawHead(x, y);
  display.drawLine(x - 7, y - 3, x - 2, y - 3, SSD1306_WHITE);
  display.drawLine(x + 2, y - 3, x + 7, y - 3, SSD1306_WHITE);
  display.drawLine(x - 4, y + 6, x + 4, y + 6, SSD1306_WHITE);
  display.drawLine(x, y + 9, x - 2, y + 22, SSD1306_WHITE);
  display.drawLine(x - 2, y + 22, x - 10, y + 30, SSD1306_WHITE);
  display.drawLine(x - 2, y + 22, x + 5, y + 30, SSD1306_WHITE);
  display.drawLine(x - 1, y + 14, x - 18, y + 25, SSD1306_WHITE);
  display.drawLine(x - 1, y + 14, x + 14, y + 25, SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(x + 16, y - 12); display.print("Z");
  display.setCursor(x + 22, y - 17); display.print("z");
}

void drawCalm(int x, int y) {
  display.drawCircle(x, y, 13, SSD1306_WHITE);
  drawHead(x, y);
  display.drawLine(x - 7, y - 3, x - 2, y - 3, SSD1306_WHITE);
  display.drawLine(x + 2, y - 3, x + 7, y - 3, SSD1306_WHITE);
  drawSmile(x, y); drawBody(x, y);
  display.drawLine(x, y + 14, x - 17, y + 19, SSD1306_WHITE);
  display.drawLine(x, y + 14, x + 17, y + 19, SSD1306_WHITE);
}

void drawProud(int x, int y) {
  drawHead(x, y); drawEyes(x, y); drawSmile(x, y);
  display.drawLine(x, y + 9, x, y + 23, SSD1306_WHITE);
  display.drawLine(x, y + 15, x - 17, y + 15, SSD1306_WHITE);
  display.drawLine(x, y + 15, x + 17, y + 15, SSD1306_WHITE);
  display.drawLine(x, y + 23, x - 8, y + 30, SSD1306_WHITE);
  display.drawLine(x, y + 23, x + 8, y + 30, SSD1306_WHITE);
  display.drawCircle(x + 24, y - 4, 4, SSD1306_WHITE);
  display.drawPixel(x + 24, y - 4, SSD1306_WHITE);
}

void drawSelectedFigure() {
  switch (selectedFeeling) {
    case 0: drawHappy(FIG_X, FIG_Y); break;
    case 1: drawSad(FIG_X, FIG_Y); break;
    case 2: drawAngry(FIG_X, FIG_Y); break;
    case 3: drawScared(FIG_X, FIG_Y); break;
    case 4: drawDisgust(FIG_X, FIG_Y); break;
    case 5: drawAnxious(FIG_X, FIG_Y); break;
    case 6: drawStressed(FIG_X, FIG_Y); break;
    case 7: drawTired(FIG_X, FIG_Y); break;
    case 8: drawCalm(FIG_X, FIG_Y); break;
    case 9: drawProud(FIG_X, FIG_Y); break;
  }
}

void drawScreen() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(16, 0);
  display.print("HOW DO YOU FEEL?");
  display.drawLine(0, 10, 127, 10, SSD1306_WHITE);

  String name = feelings[selectedFeeling];
  int textWidth = name.length() * 6;
  int textX = (128 - textWidth) / 2;
  display.setCursor(textX, 13);
  display.print(name);

  drawSelectedFigure();
  display.display();
}

void readButton() {
  bool buttonState = digitalRead(BUTTON_PIN);

  if (previousButtonState == HIGH && buttonState == LOW && millis() - lastButtonPressTime > 300) {
    lastButtonPressTime = millis();
    selectedFeeling++;
    if (selectedFeeling >= feelingCount) selectedFeeling = 0;
    drawScreen();
    updateLed();
  }

  previousButtonState = buttonState;
}

void setup() {
  Serial.begin(115200);
  delay(500);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Wire.begin(SDA_PIN, SCL_PIN);

  leds.begin();
  leds.setBrightness(LED_BRIGHTNESS);
  leds.clear();
  leds.show();

  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    Serial.println("OLED not found.");
    while (true) delay(100);
  }

  drawScreen();
  updateLed();
}

void loop() {
  readButton();
}
