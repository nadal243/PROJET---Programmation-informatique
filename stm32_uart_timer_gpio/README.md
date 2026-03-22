# STM32 GPIO / Timer / UART Starter

Projet personnel d'initiation au développement embarqué sur STM32.

## Objectifs
- Prendre en main STM32CubeIDE
- Programmer en C avec la bibliothèque HAL
- Utiliser :
  - GPIO
  - Timer
  - interruption
  - UART pour le debug

## Ce que fait le programme
- fait clignoter une LED
- déclenche une interruption périodique avec TIM2
- envoie des messages de debug sur l'UART toutes les secondes

## Outils
- STM32CubeIDE
- STM32 HAL
- Carte STM32 (à adapter selon le modèle)

## À adapter avant test
- broche LED
- instance UART
- configuration horloge
- configuration du timer selon la carte
