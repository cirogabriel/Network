
# Utils
import re
import socket


def validar_ip(ip):
    patron = re.compile(
        r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return patron.match(ip) is not None


def validar_puertos(puerto_inicio, puerto_fin):
    return 0 <= puerto_inicio <= 65535 and 0 <= puerto_fin <= 65535 and puerto_inicio <= puerto_fin


def resolver_host(host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.error:
        return None


def mostrar_detalles_puertos(puertos):
    if not puertos:
        print("No se encontraron puertos abiertos.")
        return

    print(f"{'Puerto':<8} {'Protocolo':<10} {'Estado':<15} {'Servicio':<20}")
    print("-" * 55)
    for puerto_info in puertos:
        print(
            f"{puerto_info['puerto']:<8} {puerto_info['protocolo']:<10} {puerto_info['estado']:<15} {puerto_info['servicio']:<20}")
