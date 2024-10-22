import logging
import os

def setup_logger(peer_id):
    log_filename = f'log_peer_{peer_id}.log'
    logging.basicConfig(filename=log_filename, level=logging.INFO, 
                        format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    return logging.getLogger()

def log_event(logger, message):
    logger.info(message)

# Usage:
# logger = setup_logger(peer_id)
# log_event(logger, "Peer 1001 connected to Peer 1002")
