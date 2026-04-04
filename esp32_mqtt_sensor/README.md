# ESP32 WiFi / MQTT Sensor Starter

Projet personnel d'initiation à l'IoT avec ESP32.

## Objectifs
- Programmer un ESP32 en C/C++
- Se connecter au WiFi
- Envoyer des données via MQTT
- Comprendre la communication entre un microcontrôleur et un broker MQTT

## Ce que fait le programme
- se connecte au WiFi
- collecte les données en temps réel de la température et de l'humidité
- publie les données au format JSON sur un topic MQTT
- affiche les informations dans le moniteur série

## Matériel possible
- ESP32 DevKit
- capteur DHT22 ou BME280 

## Bibliothèques
- WiFi.h
- PubSubClient.h

## Améliorations possibles
- afficher les données sur Grafana / Node-RED
- stocker les mesures sur un serveur local
