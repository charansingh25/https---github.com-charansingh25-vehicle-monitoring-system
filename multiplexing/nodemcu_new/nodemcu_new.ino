#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <SoftwareSerial.h>
#include <SimpleTimer.h>
#include <string.h>

#define BLYNK_PRINT Serial

string BLYNK_TEMPLATE_ID = "TMPL3lrT89xE3";
string BLYNK_TEMPLATE_ID = "smart car exhaust";
string BLYNK_AUTH_TOKEN = "Wyook9cHhlZ5BK3QRTrH9CWNs1DmbEZ-";


// #define BLYNK_TEMPLATE_ID "TMPL3lrT89xE3"
// #define BLYNK_TEMPLATE_NAME "smart car exhaust"
// #define BLYNK_AUTH_TOKEN "Wyook9cHhlZ5BK3QRTrH9CWNs1DmbEZ-"

char auth[] = "Wyook9cHhlZ5BK3QRTrH9CWNs1DmbEZ";
char ssid[] = "pseudo";
char pass[] = "25082002";

int firstVal, secondVal, thirdVal; // sensors

SoftwareSerial arduino(2, 3); // RX, TX

void setup() {
  Serial.begin(9600);
  arduino.begin(9600);
}

void loop() {
  if (Serial.available() == 0) {
    Blynk.run();
    timer.run(); // Initiates BlynkTimer
  }

  if (arduino.available() > 0) {
    String data = arduino.readStringUntil('\n');
    Serial.println(data); // Print received data to Serial Monitor

    // Split the received data into three values
    String values[3];
    int startIndex = 0;
    int endIndex;

    for (int i = 0; i < 3; ++i) {
      endIndex = data.indexOf(' ', startIndex);
      if (endIndex != -1) {
        values[i] = data.substring(startIndex, endIndex);
        startIndex = endIndex + 1;
      } else {
        values[i] = data.substring(startIndex);
        break; // Exit the loop if no more spaces are found
      }
    }

    // Convert the string values to integers
    firstVal = values[0].toInt();
    secondVal = values[1].toInt();
    thirdVal = values[2].toInt();

    // You can send these values to Blynk virtual pins here
    Blynk.virtualWrite(V1, firstVal);
    Blynk.virtualWrite(V2, secondVal);
    Blynk.virtualWrite(V3, thirdVal);

    Serial.println("\n");
  }
}
