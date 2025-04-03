import subprocess
import time

PORTAS = (34567, 34568, 34569, 34570, 34571, 35000, 35001, 35002, 35003)
IPS = (
    "191.252.38.73", "191.252.38.74", "191.252.38.75",
    "191.252.38.78", "191.252.38.79", "191.252.38.84",
    "191.252.38.86", "191.252.38.88", "191.252.38.93"
)

def fechar_tunel(porta):
    try:
        subprocess.run(f"pkill -f 'ssh -D {porta}'", shell=True, check=True)
        print(f"Túnel na porta {porta} fechado com sucesso.")
    except subprocess.CalledProcessError:
        print(f"Falha ao fechar túnel na porta {porta}.")

def recriar_tunel(porta, ip):
    try:
        subprocess.run(f"ssh -D {porta} -N -q -f root@{ip}", shell=True, check=True)
        print(f"Túnel recriado na porta {porta} para {ip}.")
        time.sleep(2)  # Tempo para estabilizar
    except subprocess.CalledProcessError:
        print(f"Falha ao recriar túnel na porta {porta}.")

def verificar_e_recriar_tunel(porta, ip):
    fechar_tunel(porta)
    recriar_tunel(porta, ip)
