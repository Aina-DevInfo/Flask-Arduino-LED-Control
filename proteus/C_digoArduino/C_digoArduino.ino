const int led = 13;
const int led1 = 12;
int valor_dato = 0;

void setup()
{
  pinMode(led, OUTPUT);
  pinMode(led1, OUTPUT);
  digitalWrite (led, LOW);
  digitalWrite (led1, LOW);
  Serial.begin(9600);
  Serial.println("Conexión Establecida");
}

void loop(){
  
  while(Serial.available())
  {
    valor_dato = Serial.read();
  }
  
  if (valor_dato == '1')
  {
    digitalWrite (led, HIGH);
    digitalWrite (led1, HIGH);
  }
  else if (valor_dato == '0')
  {
    digitalWrite (led, LOW);
    digitalWrite (led1, LOW);
  }

  //int ldrValue = analogRead(A2); // Lire la valeur de la photoresistance sur A0 (0-1023)
  //Serial.println(ldrValue);      // Envoyer la valeur via la série
  //delay(100);
}
