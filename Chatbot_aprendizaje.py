import tkinter as tk
import json
import os
import difflib       # NUEVO: Para encontrar textos similares
import unicodedata   # NUEVO: Para quitar acentos

ARCHIVO_BD = 'base_conocimiento.json'

DATOS_INICIALES = {
    "hola": "¡Hola! ¿Cómo estás?",
    "como estas": "Muy bien, gracias por preguntar. ¿De qué te gustaría hablar?",
    "adios": "¡Hasta luego! Vuelve pronto.",
    "como te llamas": "Me llamo Chappie. ¡Soy un bot en entrenamiento!"
}

class ChappieBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Chappie - Adquisición de Conocimiento")
        self.root.geometry("450x550")
        self.root.configure(bg="#E5E7E9")
        
        self.modo_aprendizaje = False
        self.pregunta_pendiente = ""
        
        self.conocimiento = self.cargar_conocimiento()

        self.crear_interfaz()
        self.mostrar_mensaje("🤖 Chappie", "¡Hola! Soy Chappie. Escribe algo para comenzar.")

    def crear_interfaz(self):
        self.chat_history = tk.Text(self.root, state='disabled', bg="#FEF9E7", font=("Arial", 11), wrap="word")
        self.chat_history.place(x=15, y=15, width=420, height=450)

        self.user_input = tk.Entry(self.root, font=("Arial", 12))
        self.user_input.place(x=15, y=485, width=330, height=40)
        self.user_input.bind("<Return>", self.procesar_input)

        self.btn_send = tk.Button(self.root, text="Enviar", command=self.procesar_input, bg="#28B463", fg="white", font=("Arial", 10, "bold"))
        self.btn_send.place(x=355, y=485, width=80, height=40)

    def cargar_conocimiento(self):
        if os.path.exists(ARCHIVO_BD):
            with open(ARCHIVO_BD, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        else:
            with open(ARCHIVO_BD, 'w', encoding='utf-8') as archivo:
                json.dump(DATOS_INICIALES, archivo, indent=4)
            return DATOS_INICIALES

    def guardar_conocimiento(self):
        with open(ARCHIVO_BD, 'w', encoding='utf-8') as archivo:
            json.dump(self.conocimiento, archivo, indent=4)

    # --- NUEVA LÓGICA MEJORADA ---
    def limpiar_texto(self, texto):
        """Limpia el texto convirtiendo a minúsculas y quitando acentos y signos."""
        texto = texto.lower().strip()
        # Quita acentos (Ej: 'tú' -> 'tu', 'qué' -> 'que')
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
        # Quita todos los signos que puedan estorbar
        for char in ['?', '¿', '!', '¡', '.', ',', ':']:
            texto = texto.replace(char, '')
        return texto.strip()

    def mostrar_mensaje(self, emisor, mensaje):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"{emisor}: {mensaje}\n\n")
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)

    def procesar_input(self, event=None):
        texto_usuario = self.user_input.get().strip()
        if not texto_usuario: return
        
        self.user_input.delete(0, tk.END)
        self.mostrar_mensaje("👤 Tú", texto_usuario)

        texto_limpio = self.limpiar_texto(texto_usuario)

        if self.modo_aprendizaje:
            self.conocimiento[self.pregunta_pendiente] = texto_usuario
            self.guardar_conocimiento()
            self.mostrar_mensaje("🤖 Chappie", "¡Excelente! He guardado esa información en mi base de datos.")
            self.modo_aprendizaje = False
            self.pregunta_pendiente = ""
            
        else:
            # --- NUEVA BÚSQUEDA POR SIMILITUD ---
            preguntas_guardadas = list(self.conocimiento.keys())
            
            # get_close_matches busca el texto más parecido. Cutoff (0.75) es el % de similitud requerido.
            coincidencias = difflib.get_close_matches(texto_limpio, preguntas_guardadas, n=1, cutoff=0.75)

            if coincidencias:
                mejor_match = coincidencias[0] # Tomamos la más parecida
                self.mostrar_mensaje("🤖 Chappie", self.conocimiento[mejor_match])
            else:
                self.mostrar_mensaje("🤖 Chappie", "No tengo esa información en mi base de datos. ¿Qué debería responder cuando me digan eso?")
                self.modo_aprendizaje = True
                self.pregunta_pendiente = texto_limpio

if __name__ == "__main__":
    root = tk.Tk()
    app = ChappieBot(root)
    root.mainloop()