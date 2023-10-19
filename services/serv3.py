import socket
import sqlite3
import argparse

def bus_format(data,status,service_name=''):
    data_str = str(service_name)+str(status)+ str(data)
    transformed_data_len = len(data_str)
    digits_left = 5 - len(str(transformed_data_len))
    str_data_length = '0'*digits_left
    str_data_length += str(transformed_data_len) + data_str

    return str_data_length



def new_product(nombre, precio, estado, ubicacion_bodega, stock_actual, stock_minimo):
    con = sqlite3.connect('db/vise.db')
    cursor= con.cursor()
    query1=f"""SELECT COUNT(*) FROM productos WHERE nombre='{nombre}'"""
    cursor.execute(query1)
    count= cursor.fetchone()[0]
    if count == 0:
        query=f"""INSERT INTO productos (nombre, precio, estado, ubicacion_bodega, stock_actual, stock_minimo) VALUES ('{nombre}', {precio}, '{estado}', '{ubicacion_bodega}', {stock_actual}, {stock_minimo})"""
        cursor.execute(query)
        rows = cursor.fetchall()
        con.commit()
        con.close()   
    else :
        rows = "Producto ya existe, no se puede agregar"    

    return rows

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitserv3"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = new_product(data['nombre'], data['precio'], data['estado'], data['ubicacion_bodega'], data['stock_actual'], data['stock_minimo'])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)
    

