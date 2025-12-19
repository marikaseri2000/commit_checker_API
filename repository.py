import datetime
import json
import os
import uuid

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

def save_json_db(db_name: str, record: dict) -> None:
    """Salva il nuovo oggetto nel db."""
    if not check_if_json_db_has_correct_shape(db_name):   #utile a vedere se esiste
        create_json_db(db_name)                           #creiamo uno nuovo
    
    db:list[dict]=[]                                     #una lista temporanea nella funzione
    with open(db_name, 'r') as f:
        db.extend(json.load(f))                          #preleva il contenutoi
    db.append(record)                                    #aggiunge i dati
    with open(db_name, "w", encoding='utf-8') as f:
        json.dump(db, f, indent=4,ensure_ascii=False)    #sovrascriviamo i dati nel db

def check_if_json_db_has_correct_shape(db_name: str) -> bool:
    """Verifica che il db esiste ed è nella forma corretta."""
    if not os.path.isfile(db_name):
        return False
    
    with open(db_name, "r") as f:
    #entro in lettura perchè io voglio controllare il tipo del dato
        data=json.load(f)                              #import json
        return isinstance(data, list)                  #ci restituisce un valore bool

def get_data_from_db(db_name: str) -> list[dict]:
    """Prende tutto il contenuto del bd e lo restituisce."""
    if not check_if_json_db_has_correct_shape(db_name):   
        create_json_db(db_name)
    
    with open(db_name, 'r') as f:
        return json.load(f)