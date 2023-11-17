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



def get_inventory():
    con = sqlite3.connect('db/vise0.db')
    cursor= con.cursor()
    query0=f"""SELECT productos.nombre, bodega.alias, inventario.estado, inventario.stock_actual, inventario.stock_minimo FROM inventario, bodega, productos WHERE bodega.id = inventario.id_bodega AND productos.id = inventario.id_producto"""
    rows = cursor.execute(query0).fetchall()
    con.commit()
    con.close()
    return rows 


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitser18"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = get_inventory()
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)