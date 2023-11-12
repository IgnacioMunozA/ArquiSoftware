import socket
import sqlite3
import argparse
import time

def bus_format(data,status,service_name=''):
    data_str = str(service_name)+str(status)+ str(data)
    transformed_data_len = len(data_str)
    digits_left = 5 - len(str(transformed_data_len))
    str_data_length = '0'*digits_left
    str_data_length += str(transformed_data_len) + data_str

    return str_data_length



def new_transport(nombre):
    con = sqlite3.connect('db/vise.db')
    cursor= con.cursor()
    query=f"""DELETE FROM transportes WHERE nombre = '{nombre}'"""
    cursor.execute(query)
    rows = f"Transportista {nombre} eliminado exitosamente "
    con.commit()
    con.close()
    if rows != None:
        return rows
    else :
        rows = "Transportista ya existe, no se puede agregar" 
        return  rows 

    

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitser10"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = new_transport(data['nombre'])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)