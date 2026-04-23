# Système de Surveillance Thermique - Documentation Technique

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du système](#architecture-du-système)
3. [Composants matériels](#composants-matériels)
4. [Structure du code](#structure-du-code)
5. [Mode de fonctionnement](#mode-de-fonctionnement)
6. [Guide d'installation](#guide-dinstallation)
7. [Utilisation](#utilisation)
8. [Données et visualisation](#données-et-visualisation)
9. [Spécifications techniques](#spécifications-techniques)
10. [Dépannage](#dépannage)
11. [Limitations et améliorations futures](#limitations-et-améliorations-futures)

---

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
