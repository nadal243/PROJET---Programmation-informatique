// Auteur : Nadal NGAKI MUPATI 

/*
 * @file           : esp32_iot_station.ino
 * @brief          : Station IoT Réelle - Capteur DHT22 + MQTT
 * * Bibliothèques requises : 
 * - Adafruit DHT Sensor Library
 * - PubSubClient (Nick O'Leary)
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// Configuration Matérielle
#define DHTPIN 4           // Pin DATA relié au GPIO 4
#define DHTTYPE DHT22      // Type de capteur réel utilisé

// Paramètres Réseau 
const char* SSID       = "VOTRE_WIFI";
const char* PASSWORD   = "VOTRE_MDP";
const char* MQTT_BROKER = "broker.hivemq.com";
const int   MQTT_PORT   = 1883;
const char* TOPIC_DATA  = "votre_nom/iot/sensors";

// Instances 
DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastUpdate = 0;

/* Connexion au point d'accès WiFi */
void setupWiFi() {
  Serial.print("\nTentative de connexion au réseau : ");
  Serial.println(SSID);
  WiFi.begin(SSID, PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connecté. IP : " + WiFi.localIP().toString());
}

/* Gestion de la résilience de la connexion MQTT */
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Connexion MQTT... ");
    
    // ID unique basé sur l'adresse MAC pour éviter les conflits sur le broker
    String clientId = "ESP32-STATION-";
    clientId += String((uint32_t)ESP.getEfuseMac(), HEX);

    if (client.connect(clientId.c_str())) {
      Serial.println("Succès.");
    } else {
      Serial.print("Échec (Etat: ");
      Serial.print(client.state());
      Serial.println("). Nouvel essai dans 5 secondes.");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin(); // Activation du capteur physique
  
  setupWiFi();
  client.setServer(MQTT_BROKER, MQTT_PORT);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  unsigned long now = millis();

  // Lecture et envoi toutes les 10 secondes (optimisation batterie/réseau)
  if (now - lastUpdate > 10000) {
    lastUpdate = now;

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    // Vérification de l'intégrité de la lecture physique
    if (isnan(h) || isnan(t)) {
      Serial.println("[ERREUR] Impossible de lire les données du capteur DHT22.");
      return; 
    }

    // Construction du Payload JSON (format standard de l'industrie)
    String payload = "{";
    payload += "\"temperature\":"; payload += String(t, 2);
    payload += ",\"humidity\":";    payload += String(h, 2);
    payload += ",\"unit\":\"Celsius\"";
    payload += "}";

    Serial.print("Publication sur le topic [" + String(TOPIC_DATA) + "] : ");
    Serial.println(payload);

    // Envoi effectif
    client.publish(TOPIC_DATA, payload.c_str());
  }
}