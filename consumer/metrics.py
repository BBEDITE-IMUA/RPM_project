from prometheus_client import Counter

RECEIVE_MESSAGE = Counter('receive_message_from_queue', 'Receive message from queue')
