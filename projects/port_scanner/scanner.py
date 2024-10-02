import socket
from concurrent.futures import ThreadPoolExecutor


def scan_tcp_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            if result == 0:
                service = socket.getservbyport(
                    port, 'tcp') if port <= 1024 else 'Desconocido'
                return {"port": port, "status": "abierto", "protocol": "TCP", "service": service}
            else:
                return {"port": port, "status": "cerrado", "protocol": "TCP", "service": "Desconocido"}
    except Exception as e:
        print(f"Error al escanear el puerto TCP {port}: {e}")
        return {"port": port, "status": "error", "protocol": "TCP", "service": "Desconocido"}


def scan_udp_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)
            s.sendto(b'', (host, port))

            try:
                data, _ = s.recvfrom(1024)
                service = socket.getservbyport(
                    port, 'udp') if port <= 1024 else 'Desconocido'
                return {"port": port, "status": "abierto", "protocol": "UDP", "service": service}
            except socket.timeout:
                return {"port": port, "status": "abierto o filtrado", "protocol": "UDP", "service": "Desconocido"}
            except socket.error:
                return {"port": port, "status": "cerrado", "protocol": "UDP", "service": "Desconocido"}
    except Exception as e:
        print(f"Error al escanear el puerto UDP {port}: {e}")
        return {"port": port, "status": "error", "protocol": "UDP", "service": "Desconocido"}


def scan_ports(host, start_port, end_port, protocol="TCP", threads=100):
    open_ports = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        if protocol == "TCP":
            futures = [executor.submit(scan_tcp_port, host, port)
                       for port in range(start_port, end_port + 1)]
        else:
            futures = [executor.submit(scan_udp_port, host, port)
                       for port in range(start_port, end_port + 1)]

        for future in futures:
            result = future.result()
            if result and result['status'] != "cerrado":
                open_ports.append(result)

    return open_ports
