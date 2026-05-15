import requests
import os
import re
from dotenv import load_dotenv

# Incarcarea variabilelor de mediu din fisierul .env pentru securitatea datelor
load_dotenv()


class CLUManager:
    """
    Clasa responsabila de comunicarea cu serviciul Azure Conversational Language Understanding (CLU).
    Gestioneaza trimiterea comenzilor de tip text si procesarea raspunsurilor primite.
    """

    def __init__(self):
        # Preluarea credentialelor din variabilele de mediu
        self.endpoint = os.getenv("AZURE_ENDPOINT")
        self.api_key = os.getenv("AZURE_API_KEY")
        self.project_name = os.getenv("AZURE_PROJECT_NAME")
        self.deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

    def format_label(self, text):
        """
        Transforma etichetele de tip CamelCase in text lizibil (cu spatii si majuscule).
        Exemplu: 'LightOnInKitchen' -> 'LIGHT ON IN KITCHEN'
        """
        # Utilizarea unei expresii regulate pentru a insera un spatiu inaintea fiecarei litere mari
        # (cu conditia sa nu fie la inceputul sirului)
        formatted = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
        return formatted.upper()

    def get_clu_response(self, query):
        """
        Trimite o cerere HTTP POST catre endpoint-ul Azure si returneaza analiza semantica sub forma de JSON.
        """
        # Definirea header-elor necesare pentru autentificare si formatul datelor
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json"
        }

        # Construirea corpului cererii (payload) conform specificatiilor Azure CLU
        payload = {
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "id": "1",
                    "text": query,  # Textul introdus de utilizator
                    "modality": "text",  # Tipul de intrare
                    "language": "en",  # Limba in care este scris textul
                    "participantId": "user"  # Identificatorul emitatorului
                }
            },
            "parameters": {
                "projectName": self.project_name,
                "deploymentName": self.deployment_name,
                "verbose": True  # Returneaza informatii detaliate (scoruri de confidenta, etc.)
            }
        }

        # Executarea cererii catre serverul Azure
        response = requests.post(self.endpoint, headers=headers, json=payload)

        # Verificarea eventualelor erori HTTP (arunca o exceptie daca statusul nu este 200 OK)
        response.raise_for_status()

        # Returnarea raspunsului sub forma de dictionar Python (din format JSON)
        return response.json()