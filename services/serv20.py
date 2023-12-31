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



def update_user(correo,nuevo_correo,nuevo_tipo):
    con = sqlite3.connect('db/vise0.db')
    cursor= con.cursor()
    query0=f"""SELECT COUNT(*) FROM usuarios WHERE correo = '{correo}'"""
    count = cursor.execute(query0).fetchone()
    if count[0] > 0:
        query1=f"""SELECT * FROM usuarios WHERE correo = '{correo}'"""
        count = cursor.execute(query1).fetchone()
        print(count)
        if nuevo_correo == '':
            nuevo_correo = correo
        if nuevo_tipo == '':
            nuevo_tipo = count[4]
        query0=f"""UPDATE usuarios SET correo = '{nuevo_correo}', rol = '{nuevo_tipo}' WHERE correo = '{correo}'"""

        query3=f"""INSERT INTO historial_usuarios (id_usuario, fecha_cambio, descripcion) VALUES ('{count[0]}', '{time.strftime('%Y-%m-%d %H:%M:%S')}', 'Usuario {correo} modificado.')"""
        cursor.execute(query3)
        rows = cursor.execute(query0).fetchall()

        rows = f"Cambios realizados exitosamente. \n"
        con.commit()
        con.close()   
        return rows
    else :
        rows = "Usuario inexistente, nada que actualizar. \n" 
        return  rows  

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitser20"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = update_user(data["correo"], data["nuevo_correo"],data["nuevo_tipo"])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)