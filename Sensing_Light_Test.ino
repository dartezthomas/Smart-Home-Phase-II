/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>

const char* ssid     = "NETGEAR31";
const char* password = "bluerabbit622";

Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);


const char* host = "127.0.0.1";
int port = 4000;

WiFiClient client;
void setup()
{
    Serial.begin(115200);
    delay(10);

    // We start by connecting to a WiFi network

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

    Serial.print("connecting to ");
    Serial.println(host);

    // Use WiFiClient class to create TCP connections
    
    if (!client.connect(host, port)) {
        Serial.println("connection failed");
    }else{
      Serial.println("connected");
    }
}

void loop(){
   
  String lightLevel;
  //char* message = "Hello Hub";
  sensors_event_t event;
  tsl.getEvent(&event);
  float light;
  
  if (event.light){
    Serial.print(event.light); Serial.println(" lux");
    light = event.light;
  }else{
    light = 0;
  }
  lightLevel = String(light);
  int len = lightLevel.length();
  char message[len];
  lightLevel.toCharArray(message, len);
  
  if (client.connected()){
    Serial.println("Sending data to hub");
    client.write(message);
  }

  delay(10000);

    // We now create a URI for the request
    

}
