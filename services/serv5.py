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



def delete_product(nombre):
    con = sqlite3.connect('db/vise.db')
    cursor= con.cursor()
    query1=f"""SELECT COUNT(*) FROM productos WHERE nombre='{nombre}'"""
    cursor.execute(query1)
    count= cursor.fetchone()[0]
    query2=f"""SELECT id FROM productos WHERE nombre='{nombre}'"""
    cursor.execute(query2)
    id_producto= cursor.fetchone()[0]
    
    if count > 0:
        query=f"""DELETE FROM productos WHERE nombre='{nombre}'"""
        cursor.execute(query)
        rows = f"Producto {nombre} eliminado exitosamente "
        query3=f"""INSERT INTO historialcambios (id_producto, fecha_cambio, detalles_cambio) VALUES ({id_producto}, '{time.strftime('%Y-%m-%d %H:%M:%S')}', 'Producto {nombre} eliminado')"""
        cursor.execute(query3)
        con.commit()
        con.close()   
        return rows
    else :
        rows = "Producto no existe, no se puede eliminar" 
        return  rows  


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitserv5"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = delete_product(data['nombre'])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)