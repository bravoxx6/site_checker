import socket
import json



def check_port(host, ports_to_check):
    COMMON_PORTS = ports_to_check

    open_ports = []
    try:
        for port in COMMON_PORTS:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
        return {
            "host": host,
            "open_ports": open_ports,
            "error": None
            
        }
    except socket.error as e:
        return {
            "host": host,
            "open_ports": None,
            "error": f"Socket error: {e}",
        }
