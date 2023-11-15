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


def del_proveedores(nombre):
    con = sqlite3.connect('db/vise0.db')
    cursor= con.cursor()
    query0=f"""SELECT COUNT(*) FROM proveedores WHERE nombre='{nombre}'"""
    cursor.execute(query0)
    count= cursor.fetchone()[0]
    if count > 0:
        query1=f"""DELETE FROM proveedores WHERE nombre = '{nombre}'"""
        cursor.execute(query1)
        rows = f"Proveedor {nombre} eliminado exitosamente. \n"
        con.commit()
        con.close()
        return rows
    else :
        rows = "Proveedor no existe, nada que eliminar. \n" 
        return  rows 

    

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitser14"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = del_proveedores(data['nombre'])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)