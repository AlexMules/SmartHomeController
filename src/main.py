import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image
from clu_logic import CLUManager

# Configurarea aspectului general al aplicatiei (Tema intunecata si culoarea albastra)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SmartHomeDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Detectarea automata a folderului radacina pentru a localiza resursele (imagini/iconite)
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Folderul 'src'
        project_root = os.path.dirname(current_dir)  # Radacina proiectului

        self.logo_path = os.path.join(project_root, "pictures", "logo.ico")
        self.bg_path = os.path.join(project_root, "pictures", "background.jpg")

        # Initializarea managerului pentru logica Azure CLU
        self.clu = CLUManager()
        self.title("Smart Home Controller")

        # Setarea iconitei ferestrei cu gestionare de erori
        try:
            self.after(200, lambda: self.iconbitmap(self.logo_path))
        except Exception as e:
            print(f"Window icon error: {e}")

        # Configurarea dimensiunilor ferestrei
        self.geometry("1100x820")
        self.resizable(True, True)
        self.configure(fg_color="#121212")

        # Titlul principal al interfetei
        self.lbl_title = ctk.CTkLabel(
            self,
            text="SYSTEM CONTROL DASHBOARD",
            font=("Segoe UI", 32, "bold"),
            text_color="#3b8ed0"
        )
        self.lbl_title.pack(pady=(30, 20))

        # Containerul principal care organizeaza panourile stanga/dreapta
        self.container = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15)
        self.container.pack(padx=30, pady=10, fill="both", expand=True)

        # Configurarea sistemului de grile pentru layout responsiv
        self.container.grid_columnconfigure(0, weight=2)
        self.container.grid_columnconfigure(1, weight=3)
        self.container.grid_rowconfigure(0, weight=1)

        # --- PANOU STANGA: Input utilizator si Istoric ---
        self.left_panel = ctk.CTkFrame(self.container, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.lbl_in = ctk.CTkLabel(self.left_panel, text="USER COMMAND", font=("Arial", 14, "bold"))
        self.lbl_in.pack(anchor="w", pady=(0, 5))

        # Campul de intrare pentru comenzi (Entry)
        self.entry_command = ctk.CTkEntry(self.left_panel, placeholder_text="Ex: Turn on the lights...", height=45)
        self.entry_command.pack(fill="x", pady=5)
        self.entry_command.bind('<Return>', self.process_action)  # Permite trimiterea cu tasta Enter

        # Butonul de trimitere
        self.btn_send = ctk.CTkButton(self.left_panel, text="SUBMIT", command=self.process_action, height=45,
                                      font=("Arial", 13, "bold"))
        self.btn_send.pack(fill="x", pady=10)

        self.lbl_hist = ctk.CTkLabel(self.left_panel, text="COMMAND HISTORY", font=("Arial", 12, "bold"))
        self.lbl_hist.pack(anchor="w", pady=(20, 5))

        # Caseta text pentru istoricul comenzilor (setata pe disabled pentru a fi read-only)
        self.history_box = ctk.CTkTextbox(self.left_panel, height=300, font=("Consolas", 12), fg_color="#0a0a0a")
        self.history_box.pack(fill="both", expand=True)
        self.history_box.configure(state="disabled")

        # --- PANOU DREAPTA: Analiza Tehnica si Imagine ---
        self.right_panel = ctk.CTkFrame(self.container, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.lbl_analysis = ctk.CTkLabel(self.right_panel, text="CLU INTERPRETATION", font=("Arial", 14, "bold"))
        self.lbl_analysis.pack(anchor="w", pady=(0, 5))

        # Caseta pentru afisarea datelor JSON procesate (Intent, Confidence, Entities)
        self.tech_data_box = ctk.CTkTextbox(self.right_panel, height=280, font=("Consolas", 16), fg_color="#0a0a0a",
                                            border_width=1, border_color="#3b8ed0")
        self.tech_data_box.pack(fill="x", pady=(0, 20))
        self.tech_data_box.configure(state="disabled")

        # Incarcarea imaginii decorative
        try:
            self.raw_image = Image.open(self.bg_path)
            self.smart_home_image = ctk.CTkImage(
                light_image=self.raw_image,
                dark_image=self.raw_image,
                size=(400, 280)
            )
            self.img_label = ctk.CTkLabel(self.right_panel, image=self.smart_home_image, text="")
            self.img_label.pack(pady=10, anchor="center")
        except Exception as e:
            print(f"Decorative image not found: {e}")

        # Seteaza focusul pe fereastra principala la pornire
        self.focus_set()

    def process_action(self, event=None):
        """Functia principala care gestioneaza trimiterea textului la Azure si actualizarea UI-ului"""
        query = self.entry_command.get()
        if not query.strip(): return  # Ignora input-ul gol

        try:
            # Apelarea metodei din clu_logic pentru a obtine raspunsul JSON
            data = self.clu.get_clu_response(query)

            # Extragerea informatiilor relevante din JSON-ul primit
            prediction = data['result']['prediction']
            top_intent = prediction['topIntent']
            intent_confidence = prediction['intents'][0]['confidenceScore'] * 100
            entities = prediction.get('entities', [])

            # Formatarea etichetei intentiei (din CamelCase in text lizibil)
            display_intent = self.clu.format_label(top_intent)

            # Construirea raportului de analiza pentru caseta tehnica
            info = f"QUERY: '{query}'\n" + "=" * 30 + f"\nINTENT: {display_intent}\nCONFIDENCE: {intent_confidence:.2f}%\n" + "-" * 30 + "\nENTITIES FOUND:\n"

            if entities:
                for ent in entities:
                    info += f"* [{self.clu.format_label(ent['category'])}]: {ent['text']} ({ent['confidenceScore'] * 100:.1f}%)\n"
            else:
                info += "None detected.\n"

            # Actualizarea casetei de interpretare (Unlock -> Write -> Lock)
            self.tech_data_box.configure(state="normal")
            self.tech_data_box.delete("1.0", "end")
            self.tech_data_box.insert("end", info)
            self.tech_data_box.configure(state="disabled")

            # Actualizarea istoricului comenzilor (cele mai noi apar sus)
            self.history_box.configure(state="normal")
            self.history_box.insert("1.0", f"[IN]: {query}\n[OUT]: {display_intent}\n" + "-" * 40 + "\n")
            self.history_box.configure(state="disabled")

            # Curatarea campului de input si resetarea focusului
            self.entry_command.delete(0, "end")
            self.focus_set()

        except Exception as e:
            # Afisarea unei erori in cazul in care comunicarea cu Azure esueaza
            messagebox.showerror("Error", f"Azure Failure: {e}")


if __name__ == "__main__":
    # Pornirea buclei principale a aplicatiei
    app = SmartHomeDashboard()
    app.mainloop()