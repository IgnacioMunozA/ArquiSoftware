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



def historial(fecha):
    con = sqlite3.connect('db/vise.db')
    cursor= con.cursor()
    query=f"""SELECT DATE(h.fecha_cambio),p.nombre ,h.detalles_cambio  FROM historialcambios h, productos p WHERE DATE(fecha_cambio) >= DATE('{fecha}') AND h.id_producto = p.id"""
    cursor.execute(query)
    rows = cursor.fetchall()
    con.commit()
    con.close()
    if(len(rows)==0):
        return "No hay cambios realizados desde la fecha ingresada"
    else:
        return rows
    

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitserv6"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = historial(data['fecha'])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)