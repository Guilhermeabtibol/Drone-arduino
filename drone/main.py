import tkinter as tk
from tkinter import messagebox
import serial

# funcao para tentar conectar com o arduino
def conectar_arduino():
    try: 
        #tentar abrir a conexao com o arduino (quando for fazer o teste subistituir "COM3" pela porta)
        arduino = serial.Serial('COM3', 9600, timeout=1)
        status_label.config(text="Conectado ao Arduino")
        return arduino
    except: 
        status_label.config(text="Arduino nao encontrado")
        return None

# funcao para enviar comandos
def enviar_comando(comando):
    if arduino and arduino.is_open:
        arduino.write(comando.encode())
        status_label.conf(text=F"Comando enviado: {comando}")
    else: 
        status_label.config(text="Arduino desconectado")


def tecla_pressionada(event):
    tecla = event.char
    if tecla == 'w':
        enviar_comando("up")
        btn_subir.config(bg="lightgreen")
    elif tecla == 's':
        enviar_comando("down")
        btn_descer.config(bg="lightgreen")
    elif tecla == 'a':
        enviar_comando("left")
        btn_esquerda.config(bg="lightgreen")
    elif tecla == 'd':
        enviar_comando("right")
        btn_direita.config(bg="lightgreen")
    elif tecla == 'i':
        enviar_comando("forward")
        btn_frente.config(bg="lightgreen")
    elif tecla == 'k':
        enviar_comando("backward")
        btn_tras.config(bg="lightgreen")
    elif tecla == 't':
        enviar_comando("takeoff")
        btn_decolar.config(bg="lightgreen")
    elif tecla == 'l':
        enviar_comando("land") 
        btn_pousar.config(bg="lightgreen")


# funcao pra capturar a tecla q foi solta 
def tecla_soltada(event):
    tecla = event.char
    if tecla == 'w':
        btn_subir.config(bg="SystemButtonFace")  # Reverte cor para padrão
    elif tecla == 's':
        btn_descer.config(bg="SystemButtonFace")
    elif tecla == 'a':
        btn_esquerda.config(bg="SystemButtonFace")
    elif tecla == 'd':
        btn_direita.config(bg="SystemButtonFace")
    elif tecla == 'i':
        btn_frente.config(bg="SystemButtonFace")
    elif tecla == 'k':
        btn_tras.config(bg="SystemButtonFace")
    elif tecla == 't':
        btn_decolar.config(bg="SystemButtonFace")
    elif tecla == 'l':
        btn_pousar.config(bg="SystemButtonFace")

# inicializa a  interface grafica 
app = tk.Tk() 
app.title("Controle do drone")
app.geometry("400x300")

#status da conexao 

status_label = tk.Label(app, text="Tentando conectar ao Arduino", font=("Arial", 12))
status_label.grid(row=4, column=0, columnspan=3, pady=20)

# botoes para comandos 
btn_decolar = tk.Button(app, text="Decolar (t)", command=lambda: enviar_comando("takeoff"))
btn_pousar = tk.Button(app, text="Pousar (l)", command=lambda: enviar_comando("land"))
btn_frente = tk.Button(app, text="Frente (i)", command=lambda:("forward"))
btn_tras = tk.Button(app, text="Tras (k)", command=lambda:("backward"))
btn_esquerda = tk.Button(app, text="Esquerda (a)", command=lambda:("left"))
btn_direita = tk.Button(app, text="Direita (d)", command=lambda:("right"))
btn_subir = tk.Button(app, text="Subir (w)", command=lambda:("up"))
btn_descer = tk.Button(app, text="Descer (s)", command=lambda:("down"))


# Layout

btn_subir.grid(row=0, column=1, padx=10, pady=10)
btn_esquerda.grid(row=1, column=0, padx=10, pady=10)
btn_frente.grid(row=1, column=1, padx=10, pady=10)
btn_direita.grid(row=1, column=2, padx=10, pady=10)
btn_tras.grid(row=2, column=1, padx=10, pady=10)
btn_pousar.grid(row=3, column=1, padx=10, pady=10)
btn_decolar.grid(row=3, column=0, padx=10, pady=10)
btn_descer.grid(row=3, column=2, padx=10, pady=10)

# tentando conectar ao arduino 
arduino = conectar_arduino()

# associar as teclas aos comandos
app.bind('<KeyPress>', tecla_pressionada)
app.bind('<KeyRelease>', tecla_soltada)

# iniciar a interface grafica

app.mainloop()


# fechar a conexao com o arduino ao sair

if arduino and arduino.is_open:
    arduino.close()