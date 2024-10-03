import customtkinter as ctk
import threading
from scanner import escanear_puertos
import utils

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AppEscanerPuertos(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Escaner de Puertos")
        self.geometry("725x500")
        self.host_var = ctk.StringVar()
        self.protocolo_var = ctk.StringVar(value="TCP")
        self.puerto_inicio_var = ctk.StringVar()
        self.puerto_fin_var = ctk.StringVar()
        self.crear_widgets()

    def crear_widgets(self):
        # formulario izquierda
        marco_form = ctk.CTkFrame(self)
        marco_form.grid(row=0, column=0, padx=(20, 2), pady=20, sticky="n")
        etiqueta_titulo = ctk.CTkLabel(
            marco_form, text="ESCANER DE PUERTOS", font=ctk.CTkFont(size=20, weight="bold"))
        etiqueta_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Campo de entrada para el Host/IP
        ctk.CTkLabel(marco_form, text="Host/direccion IP:").grid(row=1,
                                                                 column=0, padx=10, pady=5, sticky="w")
        entrada_host = ctk.CTkEntry(
            marco_form, textvariable=self.host_var, width=200)
        entrada_host.grid(row=1, column=1, pady=5, padx=10)

        # Puerto inicial
        ctk.CTkLabel(marco_form, text="Puerto Inicial:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w")
        entrada_puerto_inicio = ctk.CTkEntry(
            marco_form, textvariable=self.puerto_inicio_var, width=200)
        entrada_puerto_inicio.grid(row=2, column=1, pady=5, padx=10)

        # Puerto final
        ctk.CTkLabel(marco_form, text="Puerto Final:").grid(
            row=3, column=0, padx=10, pady=5, sticky="w")
        entrada_puerto_fin = ctk.CTkEntry(
            marco_form, textvariable=self.puerto_fin_var, width=200)
        entrada_puerto_fin.grid(row=3, column=1, pady=5, padx=10)

        # Menu desplegable
        ctk.CTkLabel(marco_form, text="Protocolo:").grid(
            row=4, column=0, padx=10, pady=5, sticky="w")
        menu_protocolo = ctk.CTkOptionMenu(
            marco_form, values=["TCP", "UDP"], variable=self.protocolo_var, width=200)
        menu_protocolo.grid(row=4, column=1, pady=5, padx=10)

        # Boton de escanear
        self.boton_escanear = ctk.CTkButton(
            marco_form, text="Escanear", command=self.iniciar_hilo_escaneo, width=324)
        self.boton_escanear.grid(row=5, column=0, columnspan=2, pady=20)

        # Tabla derecha
        marco_resultado = ctk.CTkFrame(self, fg_color="transparent")
        marco_resultado.grid(row=0, column=1, padx=(
            20, 2), pady=20, sticky="n")

        # Area de resultados
        self.texto_resultado = ctk.CTkTextbox(
            marco_resultado, width=320, height=460)
        self.texto_resultado.grid(row=0, column=0, pady=1)

    def iniciar_hilo_escaneo(self):
        self.boton_escanear.configure(text="Escaneando...", state="disabled")
        hilo_escaneo = threading.Thread(target=self.iniciar_escaneo)
        hilo_escaneo.start()

    def iniciar_escaneo(self):
        host = self.host_var.get().strip()
        protocolo = self.protocolo_var.get()
        puerto_inicio = self.puerto_inicio_var.get()
        puerto_fin = self.puerto_fin_var.get()

        # Validacion del host
        if not host:
            self.texto_resultado.insert(
                "end", "Error: Por favor, ingrese un host válido.\n")
            self.boton_escanear.configure(text="Escanear", state="normal")
            return

        # Validar si es una IP valida o resolver el host a una IP
        if not utils.validar_ip(host):
            ip_resuelta = utils.resolver_host(host)
            if not ip_resuelta:
                self.texto_resultado.insert(
                    "end", "Error: No se pudo resolver el host.\n")
                self.boton_escanear.configure(text="Escanear", state="normal")
                return
            host = ip_resuelta

        # Validacion de puertos
        try:
            puerto_inicio = int(puerto_inicio)
            puerto_fin = int(puerto_fin)
        except ValueError:
            self.texto_resultado.insert(
                "end", "Error: Los puertos deben ser números enteros.\n")
            self.boton_escanear.configure(text="Escanear", state="normal")
            return

        if not utils.validar_puertos(puerto_inicio, puerto_fin):
            self.texto_resultado.insert(
                "end", "Error: Los puertos deben estar en el rango de 0 a 65535.\n")
            self.boton_escanear.configure(text="Escanear", state="normal")
            return

        # Iniciar escaneo si las validaciones pasan
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert(
            "end", f"Escaneando {protocolo} en {host} del puerto {puerto_inicio} al {puerto_fin}...\n")

        puertos_abiertos = escanear_puertos(
            host, puerto_inicio, puerto_fin, protocolo=protocolo)

        if not puertos_abiertos:
            self.texto_resultado.insert(
                "end", "No se encontraron puertos abiertos.\n")
        else:
            self.texto_resultado.insert(
                "end", f"{'Puerto':<8} {'Protocolo':<10} {'Estado':<15} {'Servicio':<20}\n")
            self.texto_resultado.insert("end", "-" * 55 + "\n")
            for info_puerto in puertos_abiertos:
                linea_resultado = f"{info_puerto['puerto']:<8} {info_puerto['protocolo']:<10} {info_puerto['estado']:<15} {info_puerto['servicio']:<20}\n"
                self.texto_resultado.insert("end", linea_resultado)

        self.boton_escanear.configure(text="Escanear", state="normal")


if __name__ == "__main__":
    app = AppEscanerPuertos()
    app.mainloop()
