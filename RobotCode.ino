// Robot firmware for ESP8266 motor control over Wi-Fi.
#include <ESP8266WiFi.h>

// Wi-Fi config
const char* ssid = "A";
const char* password = "asaad777";
const int serverPort = 8080;

// Motor pins
const int in1 = 16;
const int in2 = 5;
const int in3 = 4;
const int in4 = 0;
const int enableA = 12;
const int enableB = 14;

// Motion tuning
const int speedCar = 150;
const int turnSpeedOffsetLeft = 40;
const int turnSpeedOffsetRight = 60;
const int delayMs = 100;

WiFiServer server(serverPort);
static WiFiClient client;
static bool connected = false;
String request;

void forward();
void backward();
void right();
void left();
void stopMotors();
void handleRequest(const String& command);

void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  Serial.begin(9600);
  delay(10);

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(delayMs);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");

  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());

  server.begin();
  Serial.println("Server started");
}

void loop() {
  if (!connected) {
    client = server.available();
    if (client) {
      Serial.println("New client connected");
      connected = true;
    }
  }

  if (connected) {
    if (client.available()) {
      request = client.readStringUntil('\n');
      handleRequest(request);
    }
  }
}

void handleRequest(const String& command) {
  if (command == "forward") {
    Serial.println(command);
    forward();
    delay(delayMs);
    stopMotors();
    delay(delayMs / 5);
    return;
  }

  if (command == "right") {
    Serial.println(command);
    right();
    delay(delayMs);
    stopMotors();
    delay(delayMs);
    return;
  }

  if (command == "left") {
    Serial.println(command);
    left();
    delay(delayMs);
    stopMotors();
    delay(delayMs);
    return;
  }

  if (command == "stop") {
    stopMotors();
  }
}

void forward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enableA, speedCar);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enableB, speedCar);
}

void backward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enableA, speedCar);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enableB, speedCar);
}

void right() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enableA, speedCar - turnSpeedOffsetRight);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enableB, speedCar);
}

void left() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enableA, speedCar - turnSpeedOffsetLeft);

  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enableB, speedCar - turnSpeedOffsetLeft);
}

void stopMotors() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(enableA, 0);
  analogWrite(enableB, 0);
}
