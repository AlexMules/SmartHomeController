import requests
import os
import re
from dotenv import load_dotenv

# incarcarea variabilelor de mediu
load_dotenv()


class CLUManager:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_ENDPOINT")
        self.api_key = os.getenv("AZURE_API_KEY")
        self.project_name = os.getenv("AZURE_PROJECT_NAME")
        self.deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

    def format_label(self, text):
        formatted = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
        return formatted.upper()

    def get_clu_response(self, query):
        """Trimite cererea catre endpoint-ul Azure si returneaza raspunsul primit"""
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "id": "1",
                    "text": query,
                    "modality": "text",
                    "language": "en",
                    "participantId": "user"
                }
            },
            "parameters": {
                "projectName": self.project_name,
                "deploymentName": self.deployment_name,
                "verbose": True
            }
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()