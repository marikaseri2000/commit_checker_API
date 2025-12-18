import json
import re
from client_github import fetch_users
from config import base_url
from requests import RequestException, Response
from repository import create_record, save_json_db

def get_followers() -> None:
    try:
        username = prompt_for_valid_username()
        
        if username is None:
            print("Lo username è vuoto.")
            return
        
        data = get_all_follower_from_pages(username)
        usernames=exstract_usernames(data)
        record=create_record(usernames)
        save_json_db("db/db.json", record)

        print(f"Salvati {len(usernames)} follower!")

    except RequestException as e:
        print(f"Errore di connessione: {e}")
    except json.JSONDecodeError as e:
        print(f"Errore nel database: {e}")
    except OSError as e:
        print(f"Errore file system: {e}")

def prompt_for_valid_username() -> str | None:
    """Chiede username finché non è valido o l'utente esce"""
    while True:
        username = input("Inserisci lo username GitHub: ").strip()

        if username.lower() == "exit":
            return None

        if not is_valid_username_format(username):
            print("Formato non valido. Usa solo lettere, numeri e trattini.")
            continue

        print(f"Profilo {username} trovato!")
        return username

def exstract_usernames(users: list[dict])->list[str]:
    """Estrae la lista degli ustenti dalla lista di dizionari generata da create_record."""
    usernames: list[str]=[]
    for user in users:
        usernames.append(user["login"])        
    return usernames

def has_next_page(response: Response) -> bool:
    """Verifica che esiste un'altra pagina per prendere i follower"""
    link_headers=response.headers.get("Link","")
    return "next" in link_headers              #è un dizionario e a Link devi accedere in questo modo

def is_valid_username_format(username: str) -> bool:
    """Controlla che il formato sia accettabile per GitHub"""
    if not username or not username.strip():
        return False
    if username.strip().lower() == "exit":
        return False
    return bool(re.match(r'^[a-zA-Z0-9-]{1,39}$', username.strip()))

def get_all_follower_from_pages(username: str)->list[dict]:
    """Prende tutte le pagine e ne restitusce la lista accorpata"""
    url = f"{base_url}/users/{username}/followers"
    page: int = 1
    users: list=[]

    while True:
        print(f"Sto contattando la pagina: {page}")
        response: list[dict]=fetch_users(url, page)
        users.extend(response.json())

        if not has_next_page(response):
            break

        page = page + 1

    return users
