import socket
import sys

def bus_format(data, service_name=''):
    full_data = service_name + data
    transformed_data_len = len(full_data)
    str_data_length = f'{transformed_data_len:05d}'

    formatted_message = str_data_length + full_data
    return formatted_message

def send_transaction(service_code, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server_address = ('localhost', 5000)
        #print(f'connecting to {server_address[0]} port {server_address[1]}')
        sock.connect(server_address)
        
        if service_code == '00001':
            message = bus_format(data, service_code)
            sock.sendall(message.encode())
            amount_received = 0
            amount_expected = int(sock.recv(5))
            while amount_received < amount_expected:
                resp_data = sock.recv(amount_expected - amount_received)
                amount_received += len(resp_data)   
            sock.close()
            return resp_data   
                

        
            
        
