from scanner import escanear_puertos
from utils import validar_ip, validar_puertos, resolver_host, mostrar_detalles_puertos


def main():
    print("---- Escaner de Puertos ----")

    protocolo = input(
        "¿Que tipo de puertos desea escanear? (TCP/UDP): ").strip().upper()
    if protocolo not in ['TCP', 'UDP']:
        print("Protocolo invalido. Solo TCP o UDP.")
        return

    host = input("Ingrese el nombre del Host o la direccion IP: ").strip()

    if not validar_ip(host):
        print("Resolviendo host a IP...")
        ip_resuelta = resolver_host(host)
        if ip_resuelta:
            host = ip_resuelta
            print(f"Host resuelto a: {host}")
        else:
            print("No se pudo resolver el host.")
            return
    else:
        print(f"Usando la direccion IP: {host}")

    try:
        puerto_inicio = int(
            input("Ingrese el puerto de inicio (0-65535): ").strip())
        puerto_fin = int(input("Ingrese el puerto de fin (0-65535): ").strip())

        if not validar_puertos(puerto_inicio, puerto_fin):
            print("Rango de puertos invalido.")
            return
    except ValueError:
        print("Los puertos deben ser numeros enteros.")
        return

    print(
        f"Escaneando puertos {protocolo} en {host} desde el puerto {puerto_inicio} hasta el puerto {puerto_fin}...")

    puertos_abiertos = escanear_puertos(
        host, puerto_inicio, puerto_fin, protocolo=protocolo)

    mostrar_detalles_puertos(puertos_abiertos)


if __name__ == "__main__":
    main()
