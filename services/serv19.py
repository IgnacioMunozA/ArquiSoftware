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



def delete_user(correo):
    con = sqlite3.connect('db/vise0.db')
    cursor= con.cursor()
    query2=f"""SELECT id FROM usuarios WHERE correo='{correo}'"""
    cursor.execute(query2)
    id_usuario= cursor.fetchone()[0]
    query0=f"""DELETE FROM usuarios WHERE correo = '{correo}'"""
    rows = cursor.execute(query0).fetchone()
    query1=f"""SELECT COUNT(1) FROM usuarios WHERE correo='{correo}'"""
    cursor.execute(query1)
    count= cursor.fetchone()[0]
    if count == 0:
        rows = f"Usuario {correo} eliminado exitosamente"
        query3=f"""INSERT INTO historial_usuarios (id_usuario, fecha_cambio, descripcion) VALUES ('{id_usuario}', '{time.strftime('%Y-%m-%d %H:%M:%S')}', 'Usuario {correo} eliminado')""" 
        cursor.execute(query3)
        con.commit()
        return rows
    else :
        rows = "No se pudo eliminar el usuario, no existe" 
        return  rows 


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitser19"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = delete_user(data["correo"])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)