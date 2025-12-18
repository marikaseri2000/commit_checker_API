import datetime
import uuid
import os
import json
from dotenv import load_dotenv
from requests import get, Response

#il TOKEN non deve essere pushato

load_dotenv()
base_url = os.getenv("BASE_URL")
URL = os.getenv("URL")
github_token = os.getenv("GITHUB_TOKEN")

def costruisci_github_headers(token:str)->dict:
    return {
            "Authorization": f"Bearer{token}",
            "X-GitHub-Api-Version": "2022-11-28"
    }   

def create_users_page(url: str, page:int, headers:dict)->Response:
    return get(f"{url}?page={page}", headers=headers)

def has_next_page(response: Response) -> bool:
    """Verifica che esiste un'altra pagina per prendere i follower"""
    link_headers=response.headers.get("Link","")
    return "next" in link_headers              #è un dizionario e a Link devi accedere in questo modo

def get_all_follower_from_pages(username: str)->list[dict]:
    """Prende tutte le pagine e ne restitusce la lista accorpata"""
    url = f"{base_url}/users/{username}/followers"
    page:int=1
    users: list=[]

    while True:
        print(f"Sto contattando la pagina: {page}")
        response: list[dict]=fetch_users(url, page)
        users.extend(response.json())

        if not has_next_page(response):
            break

        page = page + 1

    return users

def fetch_users(URL_users:str, page: int) -> list[dict]:
    """Esegue la chiamata per prendere tutti i dati dal server."""
    headers=costruisci_github_headers(github_token)
    return has_next_page(create_users_page(URL_users, page, headers))
    
    
def exstract_usernames(users: list[dict])->list[str]:
    """Estrae la lista degli ustenti dalla lista di dizionari generata da create_record."""
    usernames: list[str]=[]
    for user in users:
        usernames.append(user["login"])        
    return usernames

def create_record(usernames:list[str]) -> dict:
    """Crea un nuovo oggetto record da salvare nel db"""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    clean_date = now_utc.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return {
        "id": str(uuid.uuid4()),
        "creationAt": clean_date,
        "users": usernames,
        "numberOfUsers": len(usernames)
    }

def create_json_db(db_name: str) -> bool:
    """Creo la cartella se non esiste."""
    os.makedirs(os.path.dirname(db_name), exist_ok=True)   #import os
    with open(db_name, "w") as f: 
    #facciamo un with open perchè vogliamo accedere al file
        f.write("[]")
    return True

def check_if_json_db_has_correct_shape(db_name: str) -> bool:
    """Verifica che il db esiste ed è nella forma corretta."""
    if not os.path.isfile(db_name):
        return False
    
    with open(db_name, "r") as f:
    #entro in lettura perchè io voglio controllare il tipo del dato
        data=json.load(f)                              #import json
        return isinstance(data, list)                  #ci restituisce un valore bool
        
def save_json_db(db_name: str, record: dict) -> None:
    """Salva il nuovo oggetto nel db."""
    if not check_if_json_db_has_correct_shape(db_name):   #utile a vedere se esiste
        create_json_db(db_name)
    
    db:list[dict]=[]                                     #una lista temporanea nella funzione
    with open(db_name, 'r') as f:
        db.extend(json.load(f))
    db.append(record)                                    #aggiunge i dati
    with open(db_name, "w", encoding='utf-8') as f:
        json.dump(db, f, indent=4,ensure_ascii=False)    #sovrascriviamo i dati nel db



def main()-> None:
    print("Inizio programma")
    
    """
    lista_test=exstract_usernames(DATA)
    record=create_record(lista_test)
    save_json_db("db/db.json", record)
    """
    data= get_all_follower_from_pages("emanuelegurini")
    print(exstract_usernames(data))

if __name__ == "__main__":
    main()