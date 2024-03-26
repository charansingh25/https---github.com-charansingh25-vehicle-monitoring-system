#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <FS.h>

const char* ssid = "IITJ_WLAN";
const char* password = "Charan#Deep#2508";
const String serverUrl = "http://220.158.144.58:5000/update_data";

int sensorPin = A0;

int numSensors = 3;
int sensorValues[3] = {0, 0, 0};
unsigned long startTime = 0;
int currentSensor = -1;

String sensorNames[] = {"MQ135", "MQ2", "MQ7"};
bool sensorActive[] = {false, false, false};

File dataFile;

void setup() {
  Serial.begin(9600);

  if (SPIFFS.begin()) {
    Serial.println("File system mounted successfully");
    dataFile = SPIFFS.open("mydata.txt", "w");
    if (!dataFile) {
      Serial.println("Error opening data file for writing");
    }
    else{
      Serial.println("Connected successfully\n");
    }
  } else {
    Serial.println("Error mounting file system");
  }

  for (int i = 0; i < numSensors; i++) {
    switchSensor(i);
    delay(100);
    sensorValues[i] = analogRead(sensorPin);
    if (sensorValues[i] > 0) {
      currentSensor = i;
      sensorActive[currentSensor] = true;
      break;
    }
  }

  if (currentSensor == -1) {
    Serial.println("No active sensor found.");
    while (1);
  }

  Serial.print("Active sensor: ");
  Serial.println(sensorNames[currentSensor]);
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - startTime >= 10000) {
    sensorActive[currentSensor] = false;
    currentSensor = (currentSensor + 1) % numSensors;
    sensorActive[currentSensor] = true;

    startTime = currentTime;

    Serial.print("Switched to Sensor ");
    Serial.println(sensorNames[currentSensor]);
  }

  sensorValues[currentSensor] = analogRead(sensorPin);

  if (dataFile) {
    dataFile.print(sensorNames[currentSensor]);
    dataFile.print(": ");
    dataFile.println(sensorValues[currentSensor]);
  } else {
    Serial.println("Error writing to data file");
  }

  delay(5000);
}

void switchSensor(int sensorNumber) {
  if (sensorNumber == 0) {
    pinMode(D1, OUTPUT);
    digitalWrite(D1, LOW);
  } else if (sensorNumber == 1) {
    pinMode(D2, OUTPUT);
    digitalWrite(D2, HIGH);
  } else if (sensorNumber == 2) {
    pinMode(D3, OUTPUT);
    digitalWrite(D3, LOW);
  }
}
