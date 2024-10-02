import re
import socket


def validate_ip(ip):
    patron = re.compile(
        r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    if patron.match(ip):
        return True
    return False


def validate_ports(start_port, end_port):
    return 0 <= start_port <= 65535 and 0 <= end_port <= 65535 and start_port <= end_port


def resolve_host(host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.error:
        return None
