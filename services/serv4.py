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
    cursor = con.cursor()

    # Verificar si el producto existe
    query_existencia = f"""SELECT COUNT(*) FROM productos WHERE nombre = '{nombre}'"""
    count_existencia = cursor.execute(query_existencia).fetchone()
    
    if count_existencia[0] > 0:
        # Obtener los valores actuales del producto
        query_select_producto = f"""SELECT * FROM productos WHERE nombre = '{nombre}'"""
        producto_anterior = cursor.execute(query_select_producto).fetchone()

        # Actualizar valores con valores predeterminados si es necesario
        if nuevo_nombre == '':
            nuevo_nombre = nombre
        if precio == '':
            precio = producto_anterior[2]

        # Actualizar en la tabla productos
        cursor.execute("UPDATE productos SET nombre = ?, precio = ? WHERE nombre = ?", (nuevo_nombre, precio, nombre))

        # Insertar en la tabla historial_productos
        query_insert_historial = f"""INSERT INTO historial_productos (id_producto, fecha_cambio, descripcion) VALUES ('{producto_anterior[0]}', '{time.strftime('%Y-%m-%d %H:%M:%S')}', 'Prducto {nuevo_nombre} actualizado') """
        cursor.execute(query_insert_historial)

        rows = "Cambios realizados exitosamente.\n"
        con.commit()
        con.close()   
        return rows
    else:
        rows = "Producto inexistente, no se puede completar la acción.\n"
        return rows



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