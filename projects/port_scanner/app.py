import customtkinter as ctk
import threading
from scanner import scan_ports

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PortScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Escáner de Puertos")
        self.geometry("725x500")
        self.host_var = ctk.StringVar()
        self.protocol_var = ctk.StringVar(value="TCP")
        self.start_port_var = ctk.StringVar()
        self.end_port_var = ctk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # formulario izquierda
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=0, column=0, padx=(20, 2), pady=20, sticky="n")
        title_label = ctk.CTkLabel(
            form_frame, text="ESCÁNER DE PUERTOS", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Campo de entrada para el Host/IP
        ctk.CTkLabel(form_frame, text="Host/dirección IP:").grid(row=1,
                                                                 column=0, padx=10, pady=5, sticky="w")
        host_entry = ctk.CTkEntry(
            form_frame, textvariable=self.host_var, width=200)
        host_entry.grid(row=1, column=1, pady=5, padx=10)

        # Puerto inicial
        ctk.CTkLabel(form_frame, text="Puerto Inicial:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w")
        start_port_entry = ctk.CTkEntry(
            form_frame, textvariable=self.start_port_var, width=200)
        start_port_entry.grid(row=2, column=1, pady=5, padx=10)

        # Puerto final
        ctk.CTkLabel(form_frame, text="Puerto Final:").grid(
            row=3, column=0, padx=10, pady=5, sticky="w")
        end_port_entry = ctk.CTkEntry(
            form_frame, textvariable=self.end_port_var, width=200)
        end_port_entry.grid(row=3, column=1, pady=5, padx=10)

        # Menu desplegable
        ctk.CTkLabel(form_frame, text="Protocolo:").grid(
            row=4, column=0, padx=10, pady=5, sticky="w")
        protocol_option = ctk.CTkOptionMenu(
            form_frame, values=["TCP", "UDP"], variable=self.protocol_var, width=200)
        protocol_option.grid(row=4, column=1, pady=5, padx=10)

        # Boton
        scan_button = ctk.CTkButton(
            form_frame, text="Escanear", command=self.start_scan_thread, width=324)
        scan_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Tabla derecha
        result_frame = ctk.CTkFrame(self, fg_color="transparent")
        result_frame.grid(row=0, column=1, padx=(20, 2), pady=20, sticky="n")

        # Area de resultados
        self.result_text = ctk.CTkTextbox(result_frame, width=320, height=460)
        self.result_text.grid(row=0, column=0, pady=1)

    def start_scan_thread(self):
        """Inicia el escaneo en un hilo separado para no bloquear la interfaz"""
        scan_thread = threading.Thread(target=self.start_scan)
        scan_thread.start()

    def start_scan(self):
        """Función para iniciar el escaneo de puertos"""
        host = self.host_var.get().strip()
        protocol = self.protocol_var.get()
        start_port = self.start_port_var.get()
        end_port = self.end_port_var.get()

        # Validar las entradas
        if not host:
            self.result_text.insert(
                "end", "Error: Por favor, ingrese un host válido.\n")
            return

        try:
            start_port = int(start_port)
            end_port = int(end_port)
        except ValueError:
            self.result_text.insert(
                "end", "Error: Los puertos deben ser números enteros.\n")
            return

        # Limpiar el área de resultados
        self.result_text.delete("1.0", "end")
        self.result_text.insert(
            "end", f"Escaneando {protocol} en {host} del puerto {start_port} al {end_port}...\n")

        # Ejecutar el escaneo
        open_ports = scan_ports(host, start_port, end_port, protocol=protocol)

        if not open_ports:
            self.result_text.insert(
                "end", "No se encontraron puertos abiertos.\n")
        else:
            # Mostrar los resultados
            self.result_text.insert(
                "end", f"{'Puerto':<8} {'Protocolo':<10} {'Estado':<15} {'Servicio':<20}\n")
            self.result_text.insert("end", "-" * 55 + "\n")
            for port_info in open_ports:
                result_line = f"{port_info['port']:<8} {port_info['protocol']:<10} {port_info['status']:<15} {port_info['service']:<20}\n"
                self.result_text.insert("end", result_line)


if __name__ == "__main__":
    app = PortScannerApp()
    app.mainloop()
