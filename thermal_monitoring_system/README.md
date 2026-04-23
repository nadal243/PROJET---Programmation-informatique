# Système de Surveillance Thermique - Documentation Technique

## Vue d'ensemble

Le Système de Surveillance Thermique est une application IoT complète conçue pour monitorer en temps réel la température ambiante. Le système combine une carte Arduino équipée d'un capteur DHT11, d'indicateurs LED, d'une alarme sonore et d'une application Python pour l'enregistrement et la visualisation des données.

### Objectifs

- Acquérir des mesures de température en continu
- Analyser et classifier les mesures selon trois états de fonctionnement
- Fournir des alertes visuelles (LEDs) et sonores (BUZZER)
- Enregistrer les données dans un format exploitable (CSV)
- Visualiser les données en temps réel via graphiques interactifs

### Seuils de fonctionnement

| État | Plage de température | Indicateurs |
|------|-------------------|-----------|
| Normal | Inférieure à 28°C | LED Verte active |
| Attention | 28°C à 32°C | LED Jaune active |
| Critique | Supérieure à 32°C | LED Rouge + BUZZER actifs |

**Auteur** : Nadal NGAKI MUPATI  
**Date de création** : 2026-04-23
