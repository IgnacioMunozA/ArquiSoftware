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



def new_inventory(nombre_producto, alias_bodega, estado, stock_actual, stock_minimo):
    print(alias_bodega)
    con = sqlite3.connect('db/vise0.db')
    cursor= con.cursor()
    query2=f"""SELECT COUNT(*) FROM inventario, bodega, productos WHERE bodega.id = inventario.id_bodega AND productos.id = inventario.id_producto AND productos.nombre = '{nombre_producto}' AND bodega.alias = '{alias_bodega}'"""
    query0=f"""SELECT bodega.id FROM bodega WHERE bodega.alias = '{alias_bodega}'"""
    id_bodega = cursor.execute(query0).fetchone()[0]
    query1=f"""SELECT productos.id FROM productos WHERE productos.nombre = '{nombre_producto}'"""
    id_producto = cursor.execute(query1).fetchone()[0]
    count= cursor.execute(query2).fetchone()[0]
    if count == 0:
        query=f"""INSERT INTO inventario (id_producto, id_bodega, estado, stock_actual, stock_minimo) VALUES ({id_producto}, {id_bodega}, '{estado}', {stock_actual}, {stock_minimo})"""
        cursor.execute(query)
        rows = f"Inventario registrado exitosamente. \n"
        con.commit()
        con.close()   
        return rows
    else :
        rows = "Registro de inventario ya existente, no se puede completar la acción. \n" 
        return  rows  


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitser16"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = new_inventory(data['nombre_producto'], data['alias_bodega'], data['estado'], data['stock_actual'], data['stock_minimo'])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)