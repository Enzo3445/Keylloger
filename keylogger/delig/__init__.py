import atexit
import time
#sistema para dectar se o computador do usuario está ligado
def ao_fechar():
    with open("deslig.txt", 'a') as arquivo:
        arquivo.write(f"Atencao pc desligando: {time.ctime()}")

atexit.register(ao_fechar)
while True:
    time.sleep(1)