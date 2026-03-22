// Auteur : Nadal NGAKI MUPATI

/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Projet de démarrage - STM32 GPIO / Timer / UART
  *
  * Ce que fait cette démo :
  * - Fait clignoter une LED
  * - Envoie des messages de débogage via UART
  * - Utilise une interruption de timer comme tâche périodique
  *
  * Notes :
  * - La structure du projet est généralement générée avec STM32CubeIDE.
  * - Ce fichier suppose que les pilotes HAL sont déjà configurés.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

#include "main.h"
#include <stdio.h>
#include <string.h>

/* Variables privées */
UART_HandleTypeDef huart2; // Structure de configuration pour l'UART2
TIM_HandleTypeDef htim2;   // Structure de configuration pour le Timer 2

/* USER CODE BEGIN PV */
volatile uint32_t timer_ticks = 0; // Compteur d'interruptions (volatile car modifié dans une ISR)
char tx_buffer[128];               // Tampon pour préparer les messages texte
/* USER CODE END PV */

/* Prototypes des fonctions privées*/
void SystemClock_Config(void);      // Configuration de l'horloge système
static void MX_GPIO_Init(void);     // Initialisation des ports d'entrées/sorties
static void MX_USART2_UART_Init(void); // Initialisation de la communication série
static void MX_TIM2_Init(void);     // Initialisation du Timer 2

/* Redirection de printf vers l'UART */
int __io_putchar(int ch)
{
  // Envoie un caractère via UART2 avec un délai d'attente maximum
  HAL_UART_Transmit(&huart2, (uint8_t *)&ch, 1, HAL_MAX_DELAY);
  return ch;
}

/* Fonction appelée à chaque fois que le Timer 2 déborde (Interruption) */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  if (htim->Instance == TIM2) // Vérifie que c'est bien l'interruption du Timer 2
  {
    timer_ticks++; // Incrémente le compteur de ticks
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5); // Alterne l'état de la LED
  }
}

int main(void)
{
  HAL_Init();              // Initialise la bibliothèque HAL
  SystemClock_Config();    // Configure les horloges du système

  MX_GPIO_Init();          // Initialise les GPIO (LED)
  MX_USART2_UART_Init();   // Initialise l'UART2 (Console)
  MX_TIM2_Init();          // Initialise le Timer 2

  // Démarre le Timer 2 en mode interruption
  HAL_TIM_Base_Start_IT(&htim2);

  printf("Démo STM32 démarrée\r\n");
  printf("Exemple GPIO + Timer + UART\r\n");

  uint32_t last_print = 0; // Variable pour suivre le temps du dernier affichage

  while (1) // Boucle principale (infini)
  {
    // Vérifie si 1000 ms se sont écoulées
    if ((HAL_GetTick() - last_print) >= 1000)
    {
      last_print = HAL_GetTick(); // Met à jour le temps du dernier affichage

      // Prépare une chaîne de caractères formatée
      snprintf(tx_buffer, sizeof(tx_buffer),
               "Uptime: %lu ms | Ticks Timer: %lu\r\n",
               HAL_GetTick(), timer_ticks);

      // Transmet le message par UART
      HAL_UART_Transmit(&huart2, (uint8_t *)tx_buffer, strlen(tx_buffer), HAL_MAX_DELAY);
    }

    HAL_Delay(10); // Petite pause pour stabiliser la boucle
  }
}

/**
  * @brief Fonction d'initialisation du Timer 2
  */
static void MX_TIM2_Init(void)
{
  __HAL_RCC_TIM2_CLK_ENABLE(); // Active l'horloge pour le périphérique TIM2

  htim2.Instance = TIM2;
  // Exemple pour une horloge à 16 MHz -> donne une horloge de timer à 1 kHz
  htim2.Init.Prescaler = 16000 - 1;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP; // Compte vers le haut
  htim2.Init.Period = 1000 - 1;        // Période de 1 seconde (1000 ms)
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

  // Initialise la base de temps
  if (HAL_TIM_Base_Init(&htim2) != HAL_OK)
  {
    Error_Handler(); // Appelle le gestionnaire d'erreur en cas d'échec
  }

  // Configure la priorité et active l'interruption du Timer 2 dans le contrôleur NVIC
  HAL_NVIC_SetPriority(TIM2_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(TIM2_IRQn);
}

/**
  * @brief Fonction d'initialisation de l'USART2
  */
static void MX_USART2_UART_Init(void)
{
  __HAL_RCC_USART2_CLK_ENABLE(); // Active l'horloge pour l'USART2

  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;               // Vitesse de 115200 bits/s
  huart2.Init.WordLength = UART_WORDLENGTH_8B; // 8 bits de données
  huart2.Init.StopBits = UART_STOPBITS_1;       // 1 bit de stop
  huart2.Init.Parity = UART_PARITY_NONE;         // Pas de parité
  huart2.Init.Mode = UART_MODE_TX_RX;          // Mode émission et réception
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;    // Pas de contrôle de flux matériel
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;

  // Initialise l'UART avec les paramètres ci-dessus
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief Fonction d'initialisation des GPIO
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  __HAL_RCC_GPIOA_CLK_ENABLE(); // Active l'horloge pour le port A

  // Met la broche à 0 (RESET) par défaut
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);

  // Configuration de la broche PA5 (LED)
  GPIO_InitStruct.Pin = GPIO_PIN_5;            // Broche numéro 5
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;  // Mode Sortie Push-Pull
  GPIO_InitStruct.Pull = GPIO_NOPULL;            // Pas de résistance de tirage
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW; // Vitesse de commutation faible
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);       // Applique la configuration
}

/* Emplacement vide : la config d'horloge réelle est normalement générée par CubeIDE */
void SystemClock_Config(void)
{
  /* Gardez ici la config générée pour votre carte spécifique */
}

/* Gestionnaire d'erreur en cas de problème d'initialisation */
void Error_Handler(void)
{
  __disable_irq(); // Désactive toutes les interruptions
  while (1)            // Boucle infinie pour bloquer le système
  {
  }
}
