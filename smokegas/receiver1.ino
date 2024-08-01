// Arduino Alvik, smoke and methane receiver screem
// Roni Bandini, Buenos Aires August, 2024, @RoniBandini 
// Firebeetle 2 ESP32C6 + TFT Screen 320x240 IPS with GDI cable
// MIT License


#include <esp_now.h>
#include <WiFi.h>
#include <esp_wifi.h>
#include "DFRobot_GDL.h"
#include "icon.h"

/*M0*/
#if defined ARDUINO_SAM_ZERO
#define TFT_DC  7
#define TFT_CS  5
#define TFT_RST 6
#define TFT_BL  9
/*ESP32 and ESP8266*/
#elif defined(ESP32) || defined(ESP8266)
#define TFT_DC  D2
#define TFT_CS  D6
#define TFT_RST D3
#define TFT_BL  D13
/* AVR series mainboard */
#else
#define TFT_DC  2
#define TFT_CS  3
#define TFT_RST 4
#define TFT_BL  5
#endif

DFRobot_ST7789_240x320_HW_SPI screen(/*dc=*/TFT_DC,/*cs=*/TFT_CS,/*rst=*/TFT_RST);

int w = screen.width();
int h = screen.height();
int a = millis()/1000;
uint16_t color = 0xFFFFFF;
unsigned long StartTime = millis();

typedef struct struct_message {
    int smokeValue;
    int methaneValue;

} struct_message;

// Create a struct_message called myData
struct_message myData;
void splitStringToArray(const String& inputString, char delimiter, String array[], int maxSize) {
    int arrayIndex = 0;  
    int startIndex = 0;  

    for (int i = 0; i < inputString.length(); i++) {
        if (inputString.charAt(i) == delimiter || i == inputString.length() - 1) {
            array[arrayIndex] = inputString.substring(startIndex, i );
            arrayIndex++;
            
            startIndex = i + 1;
            
            if (arrayIndex >= maxSize) {
                break;
            }
        }
    }
}

void readMacAddress(){
  uint8_t baseMac[6];
  esp_err_t ret = esp_wifi_get_mac(WIFI_IF_STA, baseMac);
  if (ret == ESP_OK) {
    Serial.printf("%02x:%02x:%02x:%02x:%02x:%02x\n",
                  baseMac[0], baseMac[1], baseMac[2],
                  baseMac[3], baseMac[4], baseMac[5]);
  } else {
    Serial.println("Failed to read MAC address");
  }
}

// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("Bytes received: ");
  Serial.println(len);

  Serial.print("Smoke: ");
  Serial.println(myData.smokeValue);

  Serial.print("Methane: ");
  Serial.println(myData.methaneValue);
  

  screen.fillScreen(COLOR_RGB565_BLACK); 
  screen.setTextColor(COLOR_RGB565_LGRAY);
  screen.setFont(&FreeMono12pt7b);
  screen.setTextSize(3);
  screen.setCursor(/*x=*/0,/*y=*/40);
  screen.setTextWrap(true);
  screen.print("Alvik");
  delay(500);

  screen.setTextSize(2);
  screen.setCursor(/*x=*/0,/*y=*/100);
  screen.print("Smoke: ");
  screen.setCursor(/*x=*/0,/*y=*/140);
  screen.print(String(myData.smokeValue));
  
  screen.setCursor(/*x=*/0,/*y=*/200);
  screen.print("Methane: ");
  screen.setCursor(/*x=*/0,/*y=*/240);
  screen.print(String(myData.methaneValue));


}
 
void setup() {
  
  // Initialize Serial Monitor
  Serial.begin(115200);
  Serial.println("Alvik smoke and methane remote screen started...");  
  screen.begin();

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  readMacAddress();

  screen.fillScreen(COLOR_RGB565_BLACK); 

  screen.drawXBitmap(/*x=*/0,/*y=*/0,/*bitmap gImage_Bitmap=*/gImage[0],/*w=*/240,/*h=*/320,color);

  delay(2000);    

  // Once ESPNow is successfully Init, we will register for recv CB to get recv packer info
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
}
 
void loop() {

}