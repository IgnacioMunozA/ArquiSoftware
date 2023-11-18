import socket
import sqlite3
import argparse
import time

# GET BY ID

def bus_format(data,status,service_name=''):
    data_str = str(service_name)+str(status)+ str(data)
    transformed_data_len = len(data_str)
    digits_left = 5 - len(str(transformed_data_len))
    str_data_length = '0'*digits_left
    str_data_length += str(transformed_data_len) + data_str

    return str_data_length



def get_order(order_id):
    con = sqlite3.connect('db/vise0.db')
    cursor = con.cursor()

    # Consulta para obtener la información de la orden
    query = f"""
        SELECT
            pedidos.id AS order_id,
            transportistas.nombre AS transportista,
            proveedores.nombre AS proveedor,
            bodega.alias AS bodega,
            productos.nombre AS productos,
            orden_producto.cantidad AS cantidad
        FROM
            pedidos
        JOIN transportistas ON pedidos.id_transportistas = transportistas.id
        JOIN proveedores ON pedidos.id_proveedores = proveedores.id
        JOIN bodega ON pedidos.id_bodega = bodega.id
        JOIN orden_producto ON pedidos.id = orden_producto.id_pedido
        JOIN productos ON orden_producto.id_producto = productos.id
        WHERE
            pedidos.id = '{order_id}'
    """

    cursor.execute(query)
    result = cursor.fetchall()

    con.close()

    if not result:
        return "Orden no encontrada"
    else:
        return result
    

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

message = b"00010sinitser25"
sock.sendall(message)
status = sock.recv(4096)[10:12].decode('utf-8')

if status == 'OK':
    print("Servicio disponible")
    while True:
        message_received= sock.recv(4096).decode('utf-8')
        client_name= message_received[5:10]
        data = eval(message_received[10:])
        ans = get_order(data['order_id'])
        response = bus_format(ans,status, str(client_name)).encode('utf-8')
        sock.send(response)
        print(response)