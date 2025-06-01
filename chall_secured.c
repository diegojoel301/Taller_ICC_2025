#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void init()
{
    setvbuf(stdout, NULL, _IONBF, 0);  // Desactiva buffering de stdout
    setvbuf(stdin, NULL, _IONBF, 0);   // Desactiva buffering de stdin
    setvbuf(stderr, NULL, _IONBF, 0);  // Desactiva buffering de stderr
}

int menu()
{
    printf("1. Enviar mensaje\n");
    printf("2. Ver mensaje\n");
    printf("3. Exit\n");
    printf("Choose an option: ");

    int choice;
    scanf("%d", &choice);
    
    return choice;
}

void enviar_mensaje(char *msg)
{
    read(0, msg, 256);
    printf("Mensaje enviado: %s", msg);
}

void ver_mensaje(char *msg)
{
    puts("Mensaje recibido: ");
    printf(msg);
}

int main()
{
    init();
    char msg[256] = {0}; // Initialize msg to avoid garbage values

    memset(msg, 0, sizeof(msg)); // Clear the message buffer

    while(1)
    {           
        int choice = menu();
        switch(choice)
        {
            case 1:
                enviar_mensaje(msg);
                break;
            case 2:
                ver_mensaje(msg);
                break;
            case 3:
                printf("Exiting...\n");
                return 0;
            default:
                printf("Opción no válida. Intente de nuevo.\n");
        }
    }
}