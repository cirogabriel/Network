# Port Scanner

Una aplicación completa de escaneo de puertos con interfaces CLI y GUI, diseñada para detectar puertos abiertos en hosts remotos mediante protocolos TCP y UDP.

## Características

- **Escaneo TCP y UDP**: Soporte para ambos protocolos de red
- **Interfaz Dual**: 
  - CLI interactiva para uso en terminal
  - GUI moderna con CustomTkinter para facilidad de uso
- **Escaneo Paralelo**: Utiliza ThreadPoolExecutor con hasta 500 hilos concurrentes para máximo rendimiento
- **Validación Robusta**: 
  - Validación de direcciones IPv4
  - Validación de rangos de puertos (0-65535)
  - Resolución automática de hostnames a IP
- **Identificación de Servicios**: Detecta servicios conocidos asociados a puertos estándar
- **Manejo de Errores**: Gestión específica de timeouts y excepciones por protocolo

## Requisitos

```bash
Python 3.8+
customtkinter  # Solo para la interfaz GUI
```

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/cirogabriel/Network.git
cd Network/projects/port_scanner
```

2. Instala las dependencias (opcional, solo si usas GUI):
```bash
pip install customtkinter
```

## Uso

### Interfaz CLI

Ejecuta el programa en línea de comandos:

```bash
python main.py
```

El programa te solicitará:
- Tipo de protocolo (TCP/UDP)
- Host o dirección IP
- Puerto inicial
- Puerto final

**Ejemplo:**
```
---- Escaner de Puertos ----
¿Que tipo de puertos desea escanear? (TCP/UDP): TCP
Ingrese el nombre del Host o la direccion IP: example.com
Ingrese el puerto de inicio (0-65535): 20
Ingrese el puerto de fin (0-65535): 443
```

### Interfaz GUI

Ejecuta la aplicación gráfica:

```bash
python app.py
```

Completa los campos:
- **Host/dirección IP**: Dirección a escanear
- **Puerto Inicial**: Inicio del rango
- **Puerto Final**: Fin del rango
- **Protocolo**: Selecciona TCP o UDP

Haz clic en el botón **"Escanear"** para iniciar.


## Resultados

El programa devuelve una tabla con los siguientes campos:

| Puerto | Protocolo | Estado | Servicio |
|--------|-----------|--------|----------|
| 22 | TCP | abierto | ssh |
| 80 | TCP | abierto | http |
| 443 | TCP | abierto | https |

**Estados posibles:**
- `abierto`: Puerto activo
- `cerrado`: Puerto no responde
- `abierto o filtrado` (UDP): No hay respuesta clara
- `error`: Error durante el escaneo

## Capturas de Pantalla

### Interfaz GUI
![GUI Principal](./screenshots/gui-main.png)
*Interfaz gráfica principal - formulario de escaneo*

![GUI Resultados](./screenshots/gui-results.png)
*Resultados de escaneo en la GUI*

### Interfaz CLI
![CLI Ejecución](./screenshots/cli-execution.png)
*Ejecución de escaneo en terminal*

## Configuración Avanzada

### Número de Hilos
Puedes modificar el número máximo de hilos concurrentes editando el parámetro `hilos` en la función `escanear_puertos()`:

```python
puertos_abiertos = escanear_puertos(host, puerto_inicio, puerto_fin, protocolo=protocolo, hilos=500)
```

### Timeout
Ajusta los timeouts en `scanner.py`:
- TCP: `s.settimeout(1)` (línea en `escanear_puerto_tcp`)
- UDP: `s.settimeout(0.9)` (línea en `escanear_puerto_udp`)


## Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

## Autor

**Ciro Gabriel**  
GitHub: [@cirogabriel](https://github.com/cirogabriel)

---

**Nota**: Este proyecto forma parte del repositorio [Network](https://github.com/cirogabriel/Network)
