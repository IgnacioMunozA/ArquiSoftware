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



def upd_productos(nombre, nuevo_nombre, precio):
    con = sqlite3.connect('db/vise0.db')
    cursor= con.cursor()
    query0=f"""SELECT COUNT(*) FROM productos WHERE nombre = '{nombre}'"""
    count = cursor.execute(query0).fetchone()
    if count[0] > 0:
        query1=f"""SELECT * FROM productos WHERE nombre = '{nombre}'"""
        count = cursor.execute(query1).fetchone()
        print(count)
        if nuevo_nombre == '':
            nuevo_nombre = nombre
        if precio == '':
            precio = count[2]
        cursor.execute("UPDATE productos SET nombre = ?, precio = ? WHERE nombre = ?", (nuevo_nombre, precio, nombre))
        rows = f"Cambios realizados exitosamente. \n"
        con.commit()
        con.close()   
        return rows
    else :
        rows = "Producto inexistente, no se puede completar la acción. \n" 
        return  rows  


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitserv4"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = upd_productos(data['nombre'], data['nuevo_nombre'], data['precio'])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)