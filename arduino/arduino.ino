const int led = 13;
const int led1 = 12;

void setup() {
  pinMode(led, OUTPUT);
  pinMode(led1, OUTPUT);
  digitalWrite(led, LOW);
  digitalWrite(led1, LOW);
  Serial.begin(9600);
  while (!Serial) {
    ;  // Wait for serial port to connect (needed for some Arduino models)
  }
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    if (command == '1') {
      digitalWrite(led, HIGH);
      digitalWrite(led1, HIGH);

    } else if (command == '0') {
      digitalWrite(led, LOW);
      digitalWrite(led1, LOW);
    } 

  }
  int ldrValue = analogRead(A2); // Lire la valeur de la photoresistance sur A0 (0-1023)
  ldrValue = map(ldrValue, 0, 1023, 0, 100);
  Serial.println(ldrValue);      // Envoyer la valeur via la série
  delay(100);
}