#include <stdio.h>

// Prototype des fonctions
int occurrences(char chaine[], char car);

// fonction principale
int main(void)
{
    char chaine[40];
    char car;

    printf("Saisir une chaine de caracteres : ");
    gets(chaine);

    printf("Saisir un caractere : ");
    scanf(" %c", &car);

    // Appel de la fonction occurrences et l'affecter dans une variable
    int occurrence = occurrences(chaine, car);
    printf("Nombre d'occurrences de '%c' : %d\n", car, occurrence);  // la gestion de l'affichage de l'occurence

    return 0;
}

int occurrences(char chaine[], char car)
{
    int i = 0;
    int occ = 0;

    // on parcourt la chaine de caractere
    while (chaine[i] != '\0')
    {
        if (car == chaine[i])
        {
            occ++;
        }
        i++;
    }
    return occ;
}
