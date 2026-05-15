import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
}


def grab_banner(sock):
    try:
        sock.settimeout(1)
        return sock.recv(1024).decode(errors="ignore").strip()
    except:
        return ""



def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        if sock.connect_ex((target, port)) == 0:
            service = COMMON_SERVICES.get(port, "Unknown")
            banner = grab_banner(sock)
            return {
                "port": port,
                "service": service,
                "banner": banner,
            }
    except:
        pass
    finally:
        sock.close()

    return None



def scan_target(target, start_port=1, end_port=1024, max_threads=100):
    results = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_port, target, port)
                   for port in range(start_port, end_port + 1)]

        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    results.sort(key=lambda x: x["port"])
    return results