from scanner import scan_ports
from utils import validate_ip, validate_ports, resolve_host


def print_port_details(ports):
    if not ports:
        print("No se encontraron puertos abiertos.")
        return

    print(f"{'Puerto':<8} {'Protocolo':<10} {'Estado':<15} {'Servicio':<20}")
    print("-" * 55)
    for port_info in ports:
        print(
            f"{port_info['port']:<8} {port_info['protocol']:<10} {port_info['status']:<15} {port_info['service']:<20}")


def main():
    print("---- Escáner de Puertos ----")

    protocol = input(
        "¿Qué tipo de puertos desea escanear? (TCP/UDP): ").strip().upper()
    if protocol not in ['TCP', 'UDP']:
        print("Protocolo inválido. Solo TCP o UDP.")
        return

    host = input("Ingrese el nombre del Host o la dirección IP: ").strip()

    if not validate_ip(host):
        print("Resolviendo host a IP...")
        resolved_ip = resolve_host(host)
        if resolved_ip:
            host = resolved_ip
            print(f"Host resuelto a: {host}")
        else:
            print("No se pudo resolver el host.")
            return
    else:
        print(f"Usando la dirección IP: {host}")

    try:
        start_port = int(
            input("Ingrese el puerto de inicio (0-65535): ").strip())
        end_port = int(input("Ingrese el puerto de fin (0-65535): ").strip())

        if not validate_ports(start_port, end_port):
            print("Rango de puertos inválido.")
            return
    except ValueError:
        print("Los puertos deben ser números enteros.")
        return

    print(
        f"Escaneando puertos {protocol} en {host} desde el puerto {start_port} hasta el puerto {end_port}...")

    open_ports = scan_ports(host, start_port, end_port, protocol=protocol)

    print_port_details(open_ports)


if __name__ == "__main__":
    main()
