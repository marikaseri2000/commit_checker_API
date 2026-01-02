from google import genai
from config import gemini_api_key

client = genai.Client(api_key=gemini_api_key)
#now
def get_start_from_gemini(data: list)-> None:
    response = client.models.generate_content_stream(
        model="gemini-3-flash-preview",
        contents=f"""
        Analizza i dati che trovi in allegato che fanno riferimento al profilo github di Pippo.
        Restituisce un'analisi dettagliata con delle statiche di andamento del suo profilo in base agli iscritti. 
        Restituisci anche una serie di consigli per permettergli di crescere nella community.
        
        Dati:
        {str(data)}
        """
        )

    for chunk in response:  
        #'end' evita di andare a capo dopo ogni pezzetto
        #'flush=True' forza la stampa immediata a video senza aspettare il buffer 
        print(chunk.text, end="", flush=True)
