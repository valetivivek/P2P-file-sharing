def send_choke_message(peer_socket):
    message = (0).to_bytes(4, 'big') + b'\x00'  # 4-byte length + 1-byte type
    peer_socket.send(message)
    print("Sent choke message")

def send_unchoke_message(peer_socket):
    message = (0).to_bytes(4, 'big') + b'\x01'  # 4-byte length + 1-byte type
    peer_socket.send(message)
    print("Sent unchoke message")

def send_interested_message(peer_socket):
    message = (0).to_bytes(4, 'big') + b'\x02'
    peer_socket.send(message)
    print("Sent interested message")

def send_not_interested_message(peer_socket):
    message = (0).to_bytes(4, 'big') + b'\x03'
    peer_socket.send(message)
    print("Sent not interested message")

def send_have_message(peer_socket, piece_index):
    message = (4).to_bytes(4, 'big') + b'\x04' + piece_index.to_bytes(4, 'big')
    peer_socket.send(message)
    print(f"Sent have message for piece {piece_index}")
