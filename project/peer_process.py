import socket
import threading
import time
from config_parser import Config
from file_manager import split_file, merge_file
from message_handler import send_choke_message, send_unchoke_message
from log_handler import setup_logger, log_event

class Peer:
    def __init__(self, peer_id, config):
        self.peer_id = peer_id
        self.config = config
        self.host = config.peers[peer_id]['host']
        self.port = config.peers[peer_id]['port']
        self.has_file = config.peers[peer_id]['has_file']
        self.bitfield = [0] * self.get_total_pieces()  # Initialize bitfield based on file size
        self.logger = setup_logger(peer_id)

    def get_total_pieces(self):
        file_size = int(self.config.common_cfg['FileSize'])
        piece_size = int(self.config.common_cfg['PieceSize'])
        return (file_size + piece_size - 1) // piece_size

    def start_server(self):
        # Start TCP server to listen for incoming connections
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Peer {self.peer_id} listening on port {self.port}")
        log_event(self.logger, f"Peer {self.peer_id} is listening on port {self.port}")

        while True:
            client_socket, addr = server.accept()
            print(f"Peer {self.peer_id} received connection from {addr}")
            log_event(self.logger, f"Peer {self.peer_id} received connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        # Handle handshake and other messages here
        try:
            handshake = client_socket.recv(32).decode()  # Receive handshake message
            print(f"Peer {self.peer_id} received handshake: {handshake}")
            log_event(self.logger, f"Peer {self.peer_id} received handshake: {handshake}")
            
            # Send handshake back
            handshake_response = 'P2PFILESHARINGPROJ'.ljust(18) + '0000000000' + str(self.peer_id).zfill(4)
            client_socket.send(handshake_response.encode())
            print(f"Peer {self.peer_id} sent handshake response: {handshake_response}")
            log_event(self.logger, f"Peer {self.peer_id} sent handshake response: {handshake_response}")

            # Handle further communication (bitfield exchange, etc.)
            # TODO: Implement additional protocol communication
        except Exception as e:
            print(f"Error handling client for peer {self.peer_id}: {e}")
            log_event(self.logger, f"Error handling client for peer {self.peer_id}: {e}")
        finally:
            client_socket.close()

    def connect_to_peer(self, target_peer_id):
        peer_info = self.config.peers[target_peer_id]
        print(f"Trying to connect to peer {target_peer_id} on {peer_info['host']}:{peer_info['port']}")
        log_event(self.logger, f"Trying to connect to peer {target_peer_id} on {peer_info['host']}:{peer_info['port']}")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client.connect((peer_info['host'], peer_info['port']))
            print(f"Successfully connected to peer {target_peer_id}")
            log_event(self.logger, f"Successfully connected to peer {target_peer_id}")

            # Send handshake
            handshake_message = 'P2PFILESHARINGPROJ'.ljust(18) + '0000000000' + str(self.peer_id).zfill(4)
            client.send(handshake_message.encode())
            print(f"Peer {self.peer_id} sent handshake: {handshake_message}")
            log_event(self.logger, f"Peer {self.peer_id} sent handshake: {handshake_message}")

            # Receive handshake response
            response = client.recv(32).decode()
            print(f"Peer {self.peer_id} received handshake response: {response}")
            log_event(self.logger, f"Peer {self.peer_id} received handshake response: {response}")

        except ConnectionRefusedError:
            print(f"Could not connect to peer {target_peer_id}. Peer might not be running.")
            log_event(self.logger, f"Could not connect to peer {target_peer_id}. Peer might not be running.")
        except Exception as e:
            print(f"Error connecting to peer {target_peer_id}: {e}")
            log_event(self.logger, f"Error connecting to peer {target_peer_id}: {e}")
        finally:
            client.close()

    def run(self):
        # Start the server to listen for incoming connections
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        # Delay to allow other peers to start their servers
        time.sleep(5)

        # Attempt to connect to other peers based on config
        for peer_id in self.config.peers:
            if peer_id != self.peer_id:
                try:
                    self.connect_to_peer(peer_id)
                except Exception as e:
                    print(f"Error during connection attempt to peer {peer_id}: {e}")
                    log_event(self.logger, f"Error during connection attempt to peer {peer_id}: {e}")


if __name__ == "__main__":
    # Initialize config and start peer process
    config = Config()
    peer_id = int(input("Enter your peer ID: "))
    peer = Peer(peer_id, config)
    peer.run()
