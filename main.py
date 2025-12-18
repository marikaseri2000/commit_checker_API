from console import print_menu
from service import get_followers

def main()-> None:
    while True:
        print_menu()
        option: int= input("Seleziona l'operazione che vuoi eseguire: ")
        match option:
            case "1":
                get_followers()
            case "2":
                print("Hai scelto di prendere le statistiche!")
            case "3":
                print("Hai scelto di prendere i dati di un giorno specifico!")
            case "exit":
                print("Perfetto, programma terminato, grazie mille!")
                break
            case _:
                print("Inserisci un'opzione valida!")

if __name__ == "__main__":
    main()