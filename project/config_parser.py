class Config:
    def __init__(self, common_cfg='Common.cfg', peer_info_cfg='PeerInfo.cfg'):
        self.common_cfg = self.parse_common_cfg(common_cfg)
        self.peers = self.parse_peer_info_cfg(peer_info_cfg)

    def parse_common_cfg(self, filename):
        config = {}
        with open(filename, 'r') as file:
            for line in file:
                key, value = line.split()
                config[key] = value
        return config

    def parse_peer_info_cfg(self, filename):
        peers = {}
        with open(filename, 'r') as file:
            for line in file:
                peer_id, host, port, has_file = line.strip().split()
                peers[int(peer_id)] = {'host': host, 'port': int(port), 'has_file': int(has_file)}
        return peers
