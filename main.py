import socket
import threading
import queue
from tkinter import *
from tkinter.scrolledtext import ScrolledText

# Configurações
HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

class SequencerServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sequence_number = 0
        self.clients = []
        self.lock = threading.Lock()
        self.message_queue = queue.Queue()
        
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Sequencer running on {self.host}:{self.port}")
        
        # Thread para aceitar conexões
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.daemon = True
        accept_thread.start()
        
        # Thread para processar mensagens
        process_thread = threading.Thread(target=self.process_messages)
        process_thread.daemon = True
        process_thread.start()
    
    def accept_connections(self):
        while True:
            client_socket, addr = self.socket.accept()
            print(f"New connection from {addr}")
            with self.lock:
                self.clients.append(client_socket)
            
            # Thread para receber mensagens deste cliente
            thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
            thread.daemon = True
            thread.start()
    
    def receive_messages(self, client_socket):
        while True:
            try:
                message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                if message:
                    with self.lock:
                        self.sequence_number += 1
                        sequenced_message = f"{self.sequence_number}:{message}"
                        self.message_queue.put(sequenced_message)
            except:
                with self.lock:
                    self.clients.remove(client_socket)
                client_socket.close()
                break
    
    def process_messages(self):
        while True:
            message = self.message_queue.get()
            with self.lock:
                for client in self.clients:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        self.clients.remove(client)
                        client.close()

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Distribuído - Sequenciador Fixo")
        
        # Configuração da interface
        self.setup_ui()
        
        # Configuração do socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def setup_ui(self):
        # Área de mensagens recebidas
        Label(self.root, text="Mensagens Recebidas (Ordem de Entrega)").pack()
        self.received_messages = ScrolledText(self.root, height=15)
        self.received_messages.pack(fill=BOTH, expand=True)
        
        # Área de envio de mensagens
        Label(self.root, text="Enviar Mensagem").pack()
        self.message_entry = Entry(self.root, width=50)
        self.message_entry.pack()
        
        self.send_button = Button(self.root, text="Enviar", command=self.send_message)
        self.send_button.pack()
        
        # Área de status
        self.status_label = Label(self.root, text="Desconectado", fg="red")
        self.status_label.pack()
        
        # Botão de conexão
        self.connect_button = Button(self.root, text="Conectar ao Sequenciador", command=self.connect_to_sequencer)
        self.connect_button.pack()
    
    def connect_to_sequencer(self):
        try:
            self.socket.connect((HOST, PORT))
            self.status_label.config(text="Conectado", fg="green")
            
            # Thread para receber mensagens do sequenciador
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
        except Exception as e:
            self.status_label.config(text=f"Erro: {str(e)}", fg="red")
    
    def send_message(self):
        message = self.message_entry.get()
        if message and hasattr(self, 'socket'):
            try:
                self.socket.send(message.encode('utf-8'))
                self.message_entry.delete(0, END)
            except Exception as e:
                self.status_label.config(text=f"Erro ao enviar: {str(e)}", fg="red")
    
    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(BUFFER_SIZE).decode('utf-8')
                if message:
                    seq_num, content = message.split(':', 1)
                    self.received_messages.insert(END, f"[Seq {seq_num}] {content}\n")
            except Exception as e:
                self.status_label.config(text=f"Desconectado: {str(e)}", fg="red")
                break

def start_server():
    server = SequencerServer(HOST, PORT)
    server.start()
    # Manter o servidor rodando
    while True:
        pass

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        start_server()
    else:
        root = Tk()
        app = ClientApp(root)
        root.mainloop()
