import customtkinter as ctk
import random
import pickle

class MiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App de Vocabulario")
        self.geometry("190x280")
        
        # Cargar base de datos
        try:
            with open("palabras.pkl", "rb") as file:
                self.palabras = pickle.load(file)
        except FileNotFoundError:  
            self.palabras = {}
            
        self.pantalla_menu()
        
    def limpiar_ventana(self):
        for widget in self.winfo_children():
            widget.destroy()

    def pantalla_menu(self):
        self.limpiar_ventana()
        self.label_titulo = ctk.CTkLabel(self, text="Menú Principal", font=("Arial", 16, "bold"))
        self.label_titulo.pack(pady=10)
        
        self.boton_Ing_Esp = ctk.CTkButton(self, text="Inglés - Español", command=self.pantalla_ingles_espanol)
        self.boton_Ing_Esp.pack(pady=5)
        
        self.boton_Esp_Ing = ctk.CTkButton(self, text="Español - Inglés", command=self.pantalla_espanol_ingles)
        self.boton_Esp_Ing.pack(pady=5)
        
        self.boton_agregar_palabras = ctk.CTkButton(self, text="Agregar palabras", command=self.pantalla_agregar_palabra)
        self.boton_agregar_palabras.pack(pady=5)

    def pantalla_ingles_espanol(self):
        if not self.palabras:
            self.pantalla_menu()
            # Un aviso rápido en consola o podrías usar un messagebox
            print("¡Primero debes agregar algunas palabras!")
            return

        self.palabra_ingles = random.choice(list(self.palabras.keys()))
        self.limpiar_ventana()
        
        self.label_titulo = ctk.CTkLabel(self, text="Traduce al Español:")
        self.label_titulo.pack(pady=10)
        
        self.label_pregunta = ctk.CTkLabel(self, text=self.palabra_ingles, font=("Arial", 14, "bold"))
        self.label_pregunta.pack(pady=5)
        
        self.ent_usuario = ctk.CTkEntry(self)
        self.ent_usuario.pack(pady=5)
        
        self.boton_confirma = ctk.CTkButton(self, text="Confirmar", command=self.confirmacion_ing_esp)
        self.boton_confirma.pack(pady=5)
        
        self.boton_volver_menu = ctk.CTkButton(self, text="Volver al menú", command=self.pantalla_menu)
        self.boton_volver_menu.pack(pady=5)

    def confirmacion_ing_esp(self):
        entrada_usu = self.ent_usuario.get().strip().lower()
        respuesta_correcta = self.palabras[self.palabra_ingles].lower()
        
        if entrada_usu == respuesta_correcta:
            self.label_titulo.configure(text="¡Bien!", text_color="green")
        else:
            self.label_titulo.configure(text=f"Mal (Era: {respuesta_correcta})", text_color="red")
            
        # Siguiente palabra
        self.palabra_ingles = random.choice(list(self.palabras.keys()))
        self.label_pregunta.configure(text=self.palabra_ingles)
        self.ent_usuario.delete(0, ctk.END)

    def pantalla_espanol_ingles(self):
        if not self.palabras:
            self.pantalla_menu()
            print("¡Primero debes agregar algunas palabras!")
            return

        # Elegimos una clave (inglés) pero mostraremos el valor (español)
        self.palabra_ingles = random.choice(list(self.palabras.keys()))
        self.palabra_espanol = self.palabras[self.palabra_ingles]
        
        self.limpiar_ventana()
        
        self.label_titulo = ctk.CTkLabel(self, text="Traduce al Inglés:")
        self.label_titulo.pack(pady=10)
        
        self.label_pregunta = ctk.CTkLabel(self, text=self.palabra_espanol, font=("Arial", 14, "bold"))
        self.label_pregunta.pack(pady=5)
        
        self.ent_usuario = ctk.CTkEntry(self)
        self.ent_usuario.pack(pady=5)
        
        self.boton_confirma = ctk.CTkButton(self, text="Confirmar", command=self.confirmacion_esp_ing)
        self.boton_confirma.pack(pady=5)
        
        self.boton_volver_menu = ctk.CTkButton(self, text="Volver al menú", command=self.pantalla_menu)
        self.boton_volver_menu.pack(pady=5)

    def confirmacion_esp_ing(self):
        entrada_usu = self.ent_usuario.get().strip().lower()
        respuesta_correcta = self.palabra_ingles.lower()
        
        if entrada_usu == respuesta_correcta:
            self.label_titulo.configure(text="¡Bien!", text_color="green")
        else:
            self.label_titulo.configure(text=f"Mal (Era: {respuesta_correcta})", text_color="red")
            
        # Siguiente palabra
        self.palabra_ingles = random.choice(list(self.palabras.keys()))
        self.palabra_espanol = self.palabras[self.palabra_ingles]
        
        self.label_pregunta.configure(text=self.palabra_espanol)
        self.ent_usuario.delete(0, ctk.END)

    def pantalla_agregar_palabra(self):
        self.limpiar_ventana()
        
        ctk.CTkLabel(self, text="Introduce la palabra en Inglés:").pack(pady=2)
        self.entry_ingles = ctk.CTkEntry(self)
        self.entry_ingles.pack(pady=5)
        
        ctk.CTkLabel(self, text="Introduce la palabra en Español:").pack(pady=2)
        self.entry_espanol = ctk.CTkEntry(self)
        self.entry_espanol.pack(pady=5)
        
        self.boton_agregar_palabra = ctk.CTkButton(self, text="Agregar", command=self.agregar_palabra_logica)
        self.boton_agregar_palabra.pack(pady=5)
        
        self.boton_volver_menu = ctk.CTkButton(self, text="Volver al menú", command=self.pantalla_menu)
        self.boton_volver_menu.pack(pady=5)
        
        self.boton_imprimir = ctk.CTkButton(self, text="Ver Palabras", command=self.imprimir)
        self.boton_imprimir.pack(pady=5)
        
        self.label_temporal_de_impresion = ctk.CTkLabel(self, text="")
        self.label_temporal_de_impresion.pack(pady=5)

    def agregar_palabra_logica(self):
        ing = self.entry_ingles.get().strip()
        esp = self.entry_espanol.get().strip()
        
        if ing and esp: # Evita agregar campos vacíos
            self.palabras[ing] = esp
            with open("palabras.pkl", "wb") as file:
                pickle.dump(self.palabras, file)
            
            self.entry_ingles.delete(0, ctk.END)
            self.entry_espanol.delete(0, ctk.END)
            self.label_temporal_de_impresion.configure(text="¡Palabra agregada con éxito!", text_color="green")

    def imprimir(self):
        if not self.palabras:
            self.label_temporal_de_impresion.configure(text="El diccionario está vacío.", text_color="orange")
            return
        palab_sin = "\n".join([f"{x} → {y}" for x, y in self.palabras.items()])
        self.label_temporal_de_impresion.configure(text=palab_sin, text_color="white")

if __name__ == "__main__":
    app = MiApp()
    app.mainloop()