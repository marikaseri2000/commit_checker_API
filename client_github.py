from requests import Response, get
from config import github_token

def fetch_users(URL_users:str, page: int) -> Response:
    """Esegue la chiamata per prendere tutti i dati dal server."""
    headers={
            "Authorization": f"Bearer{github_token}",
            "X-GitHub-Api-Version": "2022-11-28"
    }   
    return get(f"{URL_users}?page={page}", headers=headers)


