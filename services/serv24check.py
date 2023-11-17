import socket
import sqlite3
import argparse
import time

# NON TESTED CODE BELLOW

def bus_format(data,status,service_name=''):
    data_str = str(service_name)+str(status)+ str(data)
    transformed_data_len = len(data_str)
    digits_left = 5 - len(str(transformed_data_len))
    str_data_length = '0'*digits_left
    str_data_length += str(transformed_data_len) + data_str

    return str_data_length



def create_order(transportista, proveedor, bodega, input_list):
    con = sqlite3.connect('db/vise0.db')
    cursor= con.cursor()
    query0=f"""SELECT transportistas.id FROM transportistas WHERE nombre = '{transportista}'"""
    transportista = cursor.execute(query0).fetchone()[0]
    query0=f"""SELECT proveedores.id FROM proveedores WHERE nombre = '{proveedor}'"""
    proveedor = cursor.execute(query0).fetchone()[0]
    query0=f"""SELECT bodega.id FROM bodega WHERE alias = '{bodega}'"""
    bodega = cursor.execute(query0).fetchone()[0]
    query1 = f"""INSERT INTO pedidos (id_proveedores, id_transportistas, id_bodega) VALUES ('{proveedor}','{transportista}','{bodega}')"""
    cursor.execute(query1)
    order_id = cursor.execute(f"""SELECT MAX(id) FROM pedidos""").fetchone()[0]

    for key, value in input_list.items():
        print("Key: ", key, " Value: ", value, " \n")
        p_id = cursor.execute(f"""SELECT id FROM productos WHERE nombre = '{key}'""").fetchone()[0]
        cursor.execute(f"""INSERT INTO orden_producto (id_producto, id_pedido, cantidad) VALUES ('{p_id}','{order_id}','{value}')""")

    rows = cursor.fetchall()
    con.commit()
    con.close()
    if(len(rows)==0):
        return "DIABLO"
    else:
        return rows
    

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitser24"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        # print(data, " \n")
        # data2 = eval(data['input_list'])
        # for key, value in data['input_list'].items():
        #     print("Key: ", key, " Value: ", value, " \n")
        ans = create_order(data['transportista'], data['proveedor'], data['bodega'], data['input_list'])
        response = bus_format("",status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)