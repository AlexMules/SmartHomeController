# 🏠 Smart Home Controller

## 📋 Description
**Smart Home Controller** is a desktop application that translates natural human language into structured system commands. Built to overcome the limitations of rigid, rule-based parsers, this project integrates **Azure Conversational Language Understanding (CLU)** to process unstructured input and accurately extract user intents and entities.

Instead of relying on hard-coded keywords, the application uses machine learning and probabilistic inference to understand semantic context, manage positional invariance (free word order), and handle lexical variations (e.g., *"Turn on the lights"* vs. *"Kill the lights"*). The result is a robust, asynchronous dashboard that acts as the "brain" of a simulated smart home environment.<br><br>

## ⭐ Key Features
* **AI-Driven Inference (Azure CLU):** Maps natural language queries to structural JSON objects, extracting the **Top Intent** (e.g., `LightOn`) and **Entities** (e.g., `Location: kitchen`).
* **Semantic Post-Processing:** Uses Regular Expressions (Regex) to automatically format raw CamelCase labels into human-readable text (e.g., converting `TurnOnSmartLight` to `TURN ON SMART LIGHT`).
* **Confidence Scoring Validation:** Exposes the AI's confidence percentage for every inference, providing transparency into the model's decision-making process.
* **Contextual Command History:** Maintains an active, chronological log of user inputs and system outputs during the session.<br><br>

## 🛠️ Tech Stack
| **Component** | **Technology** |
| :--- | :--- |
| **Language** | Python |
| **Cloud & AI Engine** | Azure Cognitive Services (Conversational Language Understanding) |
| **GUI Framework** | CustomTkinter |

<br>

## 📂 Project Structure
```text
SmartHomeController/
├── pictures/
│   ├── logo.ico                        # Application window icon
│   └── background.jpg                  # Dashboard decorative background
├── src/
│   ├── main.py                         # UI initialization and main application loop
│   └── clu_logic.py                    # Azure API communication and regex formatting logic
├── .gitignore                          
└── README.md                           
```
<br>

## 🖼️ Screenshots
### Schema definition - Intents
<img alt="image" src="https://github.com/user-attachments/assets/379eef3d-2548-408c-bc62-37cc531f2c20" /><br><br>

### Schema definition - Entities
<img alt="image" src="https://github.com/user-attachments/assets/e654d847-84a5-4e5e-a989-81b18fa05627" /><br><br>

### Data labelling
<img alt="image" src="https://github.com/user-attachments/assets/e004ddc0-9d42-483a-917c-dc721e5d6da6" /><br><br>

### Model performance
<img alt="image" src="https://github.com/user-attachments/assets/b61ccdf7-6d87-49ab-9bf0-62cba95931fc" /><br><br>







