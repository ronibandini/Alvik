/*
Arduino Alvik Explore and report
Roni Bandini, Buenos Aires 2024, @RoniBandini
https://bandini.medium.com
Firebeetle 2 + TFT Screen 320x240 IPS with GDI cable
MIT License
*/

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
uint16_t color = 0x00FF;
unsigned long StartTime = millis();

typedef struct struct_message {
    char a[512];

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
  Serial.print("Data: ");
  Serial.println(myData.a);
  
  const int maxArraySize = 4;
  String myArray[maxArraySize];

  splitStringToArray(myData.a, ',', myArray, maxArraySize);

    // Print the individual substrings
    for (int i = 0; i < maxArraySize; i++) {
        Serial.print("Element ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(myArray[i]);
    }

  screen.fillScreen(COLOR_RGB565_BLACK); 
  screen.setTextColor(COLOR_RGB565_LGRAY);
  screen.setFont(&FreeMono12pt7b);
  screen.setTextSize(2);
  screen.setCursor(/*x=*/0,/*y=*/30);
  screen.setTextWrap(true);
  screen.print("Alvik");
  delay(500);

  screen.setTextSize(1);
  screen.setCursor(/*x=*/0,/*y=*/100);
  screen.print(myArray[1]);
  screen.setCursor(/*x=*/0,/*y=*/130);
  screen.print("Battery: "+myArray[0]+"%");
  screen.setCursor(/*x=*/0,/*y=*/160);
  screen.print("Elapsed: "+myArray[2]+" sec");
  screen.setCursor(/*x=*/0,/*y=*/190);
  screen.print("Turns: "+myArray[3]);
  screen.setCursor(/*x=*/0,/*y=*/240);
  screen.print("----------------");
  screen.setCursor(/*x=*/0,/*y=*/300);
  screen.print("@RoniBandini");

}
 
void setup() {
  
  // Initialize Serial Monitor
  Serial.begin(115200);
  Serial.println("Started...");
  
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

  screen.drawXBitmap(/*x=*/100,/*y=*/h/2-16,/*bitmap gImage_Bitmap=*/gImage[0],/*w=*/32,/*h=*/32,color+=0x0700);
  delay(1000);    

  // Once ESPNow is successfully Init, we will register for recv CB to get recv packer info
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
}
 
void loop() {

}