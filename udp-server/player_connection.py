class PlayerConnection:
    def __init__(self, addr, tag_id, player_id, client_socket):
        self.addr = addr
        self.tag_id = tag_id
        self.player_id = player_id
        self.client_socket = client_socket
