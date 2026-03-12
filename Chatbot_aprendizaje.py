import tkinter as tk
import json
import os

# Nombre del archivo que servirá como nuestra Base de Datos
ARCHIVO_BD = 'base_conocimiento.json'

# Las 3 líneas precargadas (Conocimiento inicial)
DATOS_INICIALES = {
    "hola": "¡Hola! ¿Cómo estás?",
    "como estas": "Muy bien, gracias por preguntar. ¿De qué te gustaría hablar?",
    "adios": "¡Hasta luego! Vuelve pronto."
}

class ChatBotAprendizaje:
    def __init__(self, root):
        self.root = root
        self.root.title("Módulo de Adquisición de Conocimiento")
        self.root.geometry("450x550")
        self.root.configure(bg="#E5E7E9")
        
        # Variables de estado para saber si está en "Modo Aprender"
        self.modo_aprendizaje = False
        self.pregunta_pendiente = ""
        
        # Cargar la base de datos (o crearla si no existe)
        self.conocimiento = self.cargar_conocimiento()

        self.crear_interfaz()
        self.mostrar_mensaje("🤖 Bot", "¡Hola! Soy un sistema de aprendizaje. Escribe algo para comenzar.")

    def crear_interfaz(self):
        # Pantalla de chat
        self.chat_history = tk.Text(self.root, state='disabled', bg="#FEF9E7", font=("Arial", 11), wrap="word")
        self.chat_history.place(x=15, y=15, width=420, height=450)

        # Caja de texto para escribir
        self.user_input = tk.Entry(self.root, font=("Arial", 12))
        self.user_input.place(x=15, y=485, width=330, height=40)
        self.user_input.bind("<Return>", self.procesar_input) # Para enviar con ENTER

        # Botón Enviar
        self.btn_send = tk.Button(self.root, text="Enviar", command=self.procesar_input, bg="#28B463", fg="white", font=("Arial", 10, "bold"))
        self.btn_send.place(x=355, y=485, width=80, height=40)

    # --- LÓGICA DE LA BASE DE DATOS ---
    def cargar_conocimiento(self):
        """Lee el archivo JSON. Si no existe, crea uno con los datos base."""
        if os.path.exists(ARCHIVO_BD):
            with open(ARCHIVO_BD, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        else:
            with open(ARCHIVO_BD, 'w', encoding='utf-8') as archivo:
                json.dump(DATOS_INICIALES, archivo, indent=4)
            return DATOS_INICIALES

    def guardar_conocimiento(self):
        """Sobrescribe el archivo JSON con el conocimiento nuevo."""
        with open(ARCHIVO_BD, 'w', encoding='utf-8') as archivo:
            json.dump(self.conocimiento, archivo, indent=4)

    # --- LÓGICA DEL CHAT ---
    def limpiar_texto(self, texto):
        """Limpia la pregunta de signos para que el match sea más fácil (ej. ¿Hola? -> hola)"""
        return texto.lower().replace("?", "").replace("¿", "").replace("!", "").replace("¡", "").strip()

    def mostrar_mensaje(self, emisor, mensaje):
        """Imprime un mensaje en la pantalla del chat"""
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"{emisor}: {mensaje}\n\n")
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END) # Auto-scroll hacia abajo

    def procesar_input(self, event=None):
        texto_usuario = self.user_input.get().strip()
        if not texto_usuario: return
        
        self.user_input.delete(0, tk.END)
        self.mostrar_mensaje("👤 Tú", texto_usuario)

        texto_limpio = self.limpiar_texto(texto_usuario)

        # ¿El bot estaba esperando que le enseñes una respuesta?
        if self.modo_aprendizaje:
            # 1. Guarda la nueva respuesta con la pregunta anterior
            self.conocimiento[self.pregunta_pendiente] = texto_usuario
            self.guardar_conocimiento()
            
            # 2. Confirma y resetea el estado
            self.mostrar_mensaje("🤖 Bot", "¡Excelente! He guardado esa información en mi base de datos. Ya lo sé para la próxima vez.")
            self.modo_aprendizaje = False
            self.pregunta_pendiente = ""
            
        else:
            # Flujo normal: Buscar la pregunta en la base de datos
            if texto_limpio in self.conocimiento:
                self.mostrar_mensaje("🤖 Bot", self.conocimiento[texto_limpio])
            else:
                # No encontró la respuesta, entra en Modo Aprendizaje
                self.mostrar_mensaje("🤖 Bot", "No tengo esa información en mi base de datos. ¿Qué debería responder cuando me digan eso?")
                self.modo_aprendizaje = True
                self.pregunta_pendiente = texto_limpio

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotAprendizaje(root)
    root.mainloop()