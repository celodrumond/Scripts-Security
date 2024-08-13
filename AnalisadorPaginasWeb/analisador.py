import requests
import urllib3
import threading
from texttable import Texttable 

dados = {}
conclusao = []
erro = []
lock = threading.Lock()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def definicao_ips(qtd,rede):
    aux = 0
    for j in range(qtd):
        dados[j] = []
    for i in range(255):
        target = f"http://{rede}.{i}"
        dados[aux].append(f"{target}")
        aux += 1
        if aux == qtd:
            aux = 0
        
def send_request(data):
    for target in data:
        try:
            requisicao = requests.get(target,verify=False,timeout=2)
            if requisicao.status_code == 200:
                with lock:
                    conclusao.append(target)
        except requests.exceptions.RequestException as e:
            with lock:
                erro.append(target)
    

def start_threads(qtd):
    threads = []
    for i in range(qtd):
        t = threading.Thread(target=send_request,args=(dados[i],))
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()
        
def print_dados():
    tabela = Texttable()
    tabela.add_row(["IPS","Status"])
    for target in conclusao:
        tabela.add_row([target,"200"])
    print(tabela.draw())
    
    
        
        
def main():
    rede = input("Digite a rede (ex:192.20.1): ")
    threads = int(input("Quantas Threads: "))
    definicao_ips(threads,rede)
    start_threads(threads)
    print("\n\n")
    print_dados()

main()
        