import time
import datetime
from datetime import date
import tkinter as tk
from tkinter import ttk
import requests
import pytz

# Diccionario de zonas horarias
ZONAS = {
    "Argentina": "America/Argentina/Buenos_Aires",
    "España": "Europe/Madrid",
    "Estados Unidos (Nueva York)": "America/New_York",
    "Japón": "Asia/Tokyo",
    "China": "Asia/Shanghai",
    "Brasil": "America/Sao_Paulo",
    "Chile": "America/Santiago",
    "Peru": "America/Lima",
}

def get_time_api(timezone):
    try:
        response = requests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        data = response.json()
        # Puede que la API devuelva la fecha con o sin 'Z' al final, por eso se usa fromisoformat con manejo de 'Z'
        dt_str = data['datetime']
        if dt_str.endswith('Z'):
            dt_str = dt_str[:-1]
        current_time = datetime.datetime.fromisoformat(dt_str)
        return current_time
    except Exception as e:
        print(f"Error fetching time from API: {e}")
        # Si falla la API, usar pytz
        return datetime.datetime.now(pytz.timezone(timezone)) 

class reloj_digital():
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.geometry("600x400")
        self.ventana.resizable(0,0)
        self.ventana.title("Reloj Digital con Tkinter y Python")
        self.ventana.config(bg="black")

        # Menú desplegable de países
        self.pais_var = tk.StringVar()
        self.pais_var.set("Argentina")
        self.combo = ttk.Combobox(self.ventana, textvariable=self.pais_var, values=list(ZONAS.keys()), state="readonly")
        self.combo.place(x=200, y=10)
        self.combo.bind("<<ComboboxSelected>>", self.actualizar_hora_pais)

        self.tiempo_label = tk.Label(self.ventana, text="", font=("Times New Roman", 50), fg="white", bg="black", padx=50, pady=7)
        self.semana_label = tk.Label(self.ventana, text="", font=("Times New Roman", 20), fg="green", bg="black", padx=15, pady=20)
        self.tiempo_label.place(x=155, y=50)
        self.semana_label.place(x=175, y=120)

        # Etiqueta para la hora del país seleccionado
        self.hora_pais_label = tk.Label(self.ventana, text="", font=("Times New Roman", 30), fg="cyan", bg="black")
        self.hora_pais_label.place(x=80, y=200)

        self.actualizar_tiempo()
        self.fecha_actual()
        self.actualizar_hora_pais()  # Mostrar la hora del país seleccionado al iniciar
        self.ventana.mainloop()

    def actualizar_tiempo(self):
        hora_actual = time.strftime("%H:%M:%S")
        self.tiempo_label.config(text=hora_actual)
        self.ventana.after(1000, self.actualizar_tiempo)

    def fecha_actual(self):
        datetime_object = datetime.datetime.now()
        dia_semana = datetime_object.strftime("%A")
        hoy = date.today()
        d1 = hoy.strftime("%d/%m/%Y")
        self.semana_label.config(text= d1 + " - " + dia_semana)

    def actualizar_hora_pais(self, event=None):
        pais = self.pais_var.get()
        zona = ZONAS[pais]
        hora_pais = get_time_api(zona).strftime("%H:%M:%S")
        self.hora_pais_label.config(text=f"Hora en {pais}: {hora_pais}")
        # Actualizar cada segundo la hora del país seleccionado
        self.ventana.after(1000, self.actualizar_hora_pais)

if __name__ == "__main__":
    main = reloj_digital()