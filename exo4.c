#include <stdio.h>

// fonction principale
int main() {
    int n, i = 0;
    char chaine[20];

    // 1. Saisie du nombre
    printf("Entrez un nombre entier positif : ");
    scanf("%d", &n);

    // pour la gestion du nombre positif
    if (n < 0) {
        printf("Erreur : le nombre doit �tre positif.\n");
        return 1;
    }

    // 2. Conversion chiffre en chaine de caractere par chiffre (stockage � l'envers)
    int temp = n;
    while (temp > 0) {
        int chiffre = temp % 10;
        chaine[i] = '0' + chiffre;
        temp = temp / 10;
        i++;
    }

    chaine[i] = '\0'; // Terminaison de la cha�ne

    // 3. Inversion du tableau pour corriger l'ordre
    int debut = 0;          // Commence au d�but de la cha�ne
    int fin = i - 1;        // Commence � la fin de la cha�ne

    while (debut < fin) {
        // �changer les caract�res aux positions 'debut' et 'fin'
        char temp = chaine[debut];
        chaine[debut] = chaine[fin];
        chaine[fin] = temp;

        // Avancer le d�but et reculer la fin
        debut++;
        fin--;
        }


    // 4. Affichage
    printf("La chaine obtenue est : %s\n", chaine);

    return 0;
}
