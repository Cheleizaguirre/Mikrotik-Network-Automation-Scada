// Pin 7 = VERDE (ping ok)
// Pin 6 = ROJO  (ping fail)

void setup() {
  pinMode(7, OUTPUT);
  pinMode(6, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char dato = Serial.read();

    if (dato == 'G') {
      digitalWrite(7, HIGH);  // verde encendido
      digitalWrite(6, LOW);   // rojo apagado
    }
    else if (dato == 'R') {
      digitalWrite(6, HIGH);  // rojo encendido
      digitalWrite(7, LOW);   // verde apagado
    }
  }
}
