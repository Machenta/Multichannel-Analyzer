

volatile int i = 0;
float values[100];

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(3),myEventListener,FALLING);

}

// the loop routine runs over and over again forever:
void loop() {

}

void myEventListener() {
  
    long int t1 = micros();
    int sensorValue = analogRead(A0);
    float voltage = sensorValue * (5.0 / 1024);
    Serial.println(voltage);
    values[i]= voltage;
    i++;
    long int t2 = micros();
    Serial.print("Time taken by the task: "); Serial.print(t2-t1); Serial.println(" microsseconds");
}
