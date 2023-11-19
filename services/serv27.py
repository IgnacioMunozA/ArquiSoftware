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



def del_history_p(fecha):
    con = sqlite3.connect('db/vise0.db')
    cursor= con.cursor()
    query1=f"""DELETE FROM historial_productos WHERE fecha_cambio = '{fecha}'"""
    cursor.execute(query1)
    count= cursor.fetchone()
    print(count)
    con.commit()
    if count != None:
        con.close()
        return "Registro eliminado exitosamente."
    else :
        rows = "Registro inexistente, nada que borrar." 
        return  rows  


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitser27"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = del_history_p(data['fecha'])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)