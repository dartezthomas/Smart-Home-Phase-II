#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <WiFi.h>


int beaconScanTime = 4;

const char* ssid     = "NETGEAR31";
const char* password = "jaggedboat471";

const char* host = "192.168.1.2";
int port = 4000;

char rssiSend[20];
String rssi;

int status = WL_IDLE_STATUS;
WiFiClient client;

typedef struct {
  char address[17];   // 67:f1:d2:04:cd:5d
  int rssi;
} BeaconData;

uint8_t bufferIndex = 0;  // Found devices counter
BeaconData buffer[50];    // Buffer to store found device data
//int8_t message_char_buffer[MQTT_MAX_PACKET_SIZE];

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks {
public:

  void onResult(BLEAdvertisedDevice advertisedDevice) {
    extern uint8_t bufferIndex;
    extern BeaconData buffer[];
    if(bufferIndex >= 50) {
      return;
    }
    // RSSI
    if(advertisedDevice.haveRSSI()) {
      buffer[bufferIndex].rssi = advertisedDevice.getRSSI();
    } else { buffer[bufferIndex].rssi =  0; }
    
    // MAC is mandatory for BT to work
    strcpy (buffer[bufferIndex].address, advertisedDevice.getAddress().toString().c_str());
    
    bufferIndex++;
    //Serial.printf("name: %s \n", advertisedDevice.getName().c_str());
    
    
    String mac = advertisedDevice.getAddress().toString().c_str();
    if (mac == "f6:ac:bc:64:cb:50"){
      rssi = String(advertisedDevice.getRSSI());
      rssi = rssi + '0';
      Serial.println(rssi);
      Serial.println(rssi.length());
      rssi.toCharArray(rssiSend, rssi.length());
      Serial.println(rssiSend);
      Serial.printf("MAC: %s \n", advertisedDevice.getAddress().toString().c_str());
      Serial.printf("name: %s \n", advertisedDevice.getName().c_str());
      Serial.printf("RSSI: %d \n", advertisedDevice.getRSSI());
    }
  }
  
    // Print everything via serial port for debugging
};

void setup() {
  Serial.begin(115200);
  BLEDevice::init(""); // Can only be called once
  // put your setup code here, to run once:

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  if (!client.connect(host, port)){
    Serial.println("Can't connect");
  }else{
    Serial.println("connected");
  }
}

void ScanBeacons() {
  delay(1000);
  BLEScan* pBLEScan = BLEDevice::getScan(); //create new scan
  MyAdvertisedDeviceCallbacks cb;
  pBLEScan->setAdvertisedDeviceCallbacks(&cb);
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  BLEScanResults foundDevices = pBLEScan->start(beaconScanTime);
  Serial.print("Devices found: ");
  //Serial.print(cb.getConcatedMessage());
  /*
  for (uint8_t i = 0; i < bufferIndex; i++) {
    Serial.print(buffer[i].address);
    Serial.print(" : ");
    Serial.println(buffer[i].rssi);
  }
  */
  // Stop BLE
  pBLEScan->stop();
  delay(1000);
  Serial.println("Scan done!");
  
}

void loop() {
  Serial.println("Start Scan");
  boolean result;
  ScanBeacons();

  bufferIndex = 0;
  
  if (!client.connected()){
      if (client.connect(host, port)){
        Serial.println("connected");
        Serial.println("Sending to Hub");
        client.write('1');
        delay(100);
        Serial.println(rssiSend);
        client.write(rssiSend);
        rssiSend[0] = (char)0;
       // Serial.println("After" + rssiSend);
        client.stop();
      }else{
        Serial.println("could not connect");
        client.stop();
        
      }
    }else{
      Serial.println("not connected");
      client.stop();
      delay(5000);
      return;
    }

  delay(5000);
  // put your main code here, to run repeatedly:

}
