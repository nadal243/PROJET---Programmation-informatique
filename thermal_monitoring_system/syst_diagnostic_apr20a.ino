// Auteur : Nadal NGAKI MUPATI

#include <DHT.h>  // bibliotheque pour importer le capteur de température 

#define DHTPIN 2  // broche sur laquelle le capteur de température est branché
#define DHTTYPE DHT11 // capteur de température 

#define POT_PIN A0  // le potentiometre est braché sur la broche de sortie A0

#define LED_VERT 8  // la led verte est branchée à la broche 8
#define LED_JAUNE 7 // la led verte est branchée à la broche 7
#define LED_ROUGE 6 // la led verte est branchée à la broche 6
#define BUZZER 10   // le buzzer est branché à la broche 10

#define MODE_SIMULATION true  // pour permettre la simulation de la température afin d'obtenir une large plage de température 

DHT dht(DHTPIN, DHTTYPE);

// les valeurs initiales de potentiomètre et de température 
float temp = 0;
int potValue = 0;  

// initialisation de l'ensemble des broches entrées et sorties 
void setup() {
  Serial.begin(9600);

  pinMode(LED_VERT, OUTPUT);
  pinMode(LED_JAUNE, OUTPUT);
  pinMode(LED_ROUGE, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  dht.begin();
}

void loop() {

  // ===== ACQUISITION =====
  // mode simulation 
  if (MODE_SIMULATION) {
    potValue = analogRead(POT_PIN); 
    temp = map(potValue, 0, 1023, 20, 40);
  } 
  // mode réel 
  else {
    temp = dht.readTemperature();

    // pour gérer les erreurs de branchement par exemple 
    if (isnan(temp)) {
      Serial.println("ERROR");
      return;
    }
  }

  // LOGIQUE 
  if (temp < 28) {
    normalState();
  }
  else if (temp < 32) {
    warningState();
  }
  else {
    criticalState();
  }

  // ENVOI PYTHON 
  // envoi les valeurs de température et les valeurs de la resistance (potentiometre) 
  Serial.print("TEMP:");
  Serial.print(temp);
  Serial.print(";POT:");
  Serial.println(potValue);

// une temorisation de 0.5 secondes
  delay(500);
}

// ÉTATS 
void normalState() {
  digitalWrite(LED_VERT, HIGH);
  digitalWrite(LED_JAUNE, LOW);
  digitalWrite(LED_ROUGE, LOW);
  digitalWrite(BUZZER, LOW);
}

void warningState() {
  digitalWrite(LED_VERT, LOW);
  digitalWrite(LED_JAUNE, HIGH);
  digitalWrite(LED_ROUGE, LOW);
  digitalWrite(BUZZER, LOW);
}

void criticalState() {
  digitalWrite(LED_VERT, LOW);
  digitalWrite(LED_JAUNE, LOW);
  digitalWrite(LED_ROUGE, HIGH);
  digitalWrite(BUZZER, HIGH); 
}