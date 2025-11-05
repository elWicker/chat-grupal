import socket
import threading

SERVER_IP = input("Introduce la IP del servidor: ")
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((SERVER_IP, PORT))

nombre = input("Ingresa tu nombre por favor: ")
def recibir():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje == "NOMBRE":
                cliente.send(nombre.encode('utf-8'))
            else:
                print(mensaje)
        except:
            print("Conexión cerrada")
            cliente.close()
            break
def enviar():
    while True:
        mensaje = input("")
        if mensaje.lower() == "salir":
            cliente.close()
            break
        cliente.send(mensaje.encode('utf-8'))
threading.Thread(target=recibir).start()
threading.Thread(target=enviar).start()
