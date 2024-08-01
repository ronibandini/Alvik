// Alvik robot smoke and methane report
// Roni Bandini, August 2024
// DFRobot Firebeetle 2 ESP32C6, set CDC on boot enabled, C8
// Sensors: fFor extended periods of non-usage, it is advisable to preheat the sensors for at least 24 hours


#include <esp_now.h>
#include <WiFi.h>

int smokePin   = A3; 
int smokeValue = 0;

int methanePin    = A4; 
int methaneValue  = 0;

// REPLACE WITH YOUR RECEIVER MAC Address
uint8_t broadcastAddress[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00};


// Structure to send smoke and methane data
typedef struct struct_message {  
  int a;
  int b;  
} struct_message;

// Create a struct_message called myData
struct_message myData;

esp_now_peer_info_t peerInfo;

// callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
 
void setup() {
  // Init Serial Monitor
  Serial.begin(115200);
 
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
}
 
void loop() {

   smokeValue = analogRead(smokePin);  // read the input pin
   Serial.println("Smoke: ");  
   Serial.println(smokeValue);  

  methaneValue = analogRead(methanePin);  // read the input pin
   Serial.println("Methane: ");  
   Serial.println(methaneValue);  

  // Set values to send
  myData.a = smokeValue;
  myData.b = methaneValue;
    
  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
   
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }
  delay(2000);
}