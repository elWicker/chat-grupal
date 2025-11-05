import socket
import threading

HOST = ''
PORT = 5000


clientes = [] # Lista de gente que estan conectados
nombres = {}


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear socket TCP 
server.bind((HOST, PORT))
server.listen()

print(f"Servidor de chat grupal escuchando en el puerto {PORT}...")

def broadcast(mensaje, cliente_emisor=None):
    """Envía el mensaje a todos los clientes conectados excepto el emisor"""
    for cliente in clientes:
        if cliente != cliente_emisor:
            try:
                cliente.send(mensaje)
            except:
                cliente.close()
                if cliente in clientes:
                    clientes.remove(cliente)
def manejar_cliente(cliente):
    """Maneja los mensajes de un cliente"""
    nombre = cliente.recv(1024).decode('utf-8')
    nombres[cliente] = nombre
    bienvenida = f" {nombre} se unio al chat"
    print(bienvenida)
    broadcast(bienvenida.encode('utf-8'))

    while True:
        try:
            mensaje = cliente.recv(1024)
            if not mensaje:
                break
            texto = f"{nombre}: {mensaje.decode('utf-8')}"
            print(texto)
            broadcast(texto.encode('utf-8'), cliente)
        except:
            cliente.close()
            if cliente in clientes:
                clientes.remove(cliente)
                salida = f"{nombre} salio del chat"
                print(salida)
                broadcast(salida.encode('utf-8'))
            break

def recibir_conexiones():
    """Acepta nuevas conexiones de clientes"""
    while True:
        cliente, direccion = server.accept()
        print(f"Conectado con {direccion}")
        cliente.send("NOMBRE".encode('utf-8'))  # pide el nombre a la persona que se conecta
        clientes.append(cliente)
        threading.Thread(target=manejar_cliente, args=(cliente,)).start()
recibir_conexiones()
