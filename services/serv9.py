import socket
import sqlite3
import argparse

def bus_format(data, service_name=''):
    transformed_data = str(data)
    transformed_data_len = len(transformed_data)
    digits_left = 5 - len(str(transformed_data_len))
    str_data_length = ''

    for i in range(digits_left):
        str_data_length += '0'

    str_data_length += str(transformed_data_len) + \
        service_name+transformed_data

    return str_data_length



def get_transportistas():
    con = sqlite3.connect('db/vise0.db')
    cursor= con.cursor()
    query0=f"""SELECT * FROM transportistas"""
    cursor.execute(query0)
    rows = cursor.fetchall()
    con.commit()
    con.close()
    print(rows)
    if(len(rows)==0):
        return None
    else:
        return rows
    

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitserv9"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible\n")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = get_transportistas()
        response = bus_format(ans, str(client_name)).encode('utf-8')
        sock.send(response)