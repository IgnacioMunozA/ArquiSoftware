import socket as sk
import sys
import time
import argparse

def bus_format(data, service_name=''):
    transformed_data = str(data)
    transformed_data_len = len(transformed_data)
    digits_left = 5 - len(str(transformed_data_len))
    str_data_length = ''

    for i in range(digits_left):
        str_data_length += '0'

    str_data_length += str(transformed_data_len) + \
        service_name+transformed_data

    return str_data_length

class App:
    def __init__(self,login_service, services=[])-> None:
        self.sock= sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        server_address = ('localhost', 5000)
        self.sock.connect(server_address)
        self.login_service = login_service
        self.services = services

    def send_msg(self,msg,name='g7999'):
        req = bus_format(msg,name).encode('utf-8')
        print("mensaje enviado: ",req)
        time.sleep(2)
        self.sock.sendall(req)
        return self.sock.recv(1024).decode('utf-8')

    def login(self):
        inputs={}
        for i in range(len(self.login_service['inputs'])):
            input_data = self.login_service['inputs'][i]
            key = input_data['name']
            inputs[key]=input(input_data['message'])
        res = self.send_msg(inputs,self.login_service['id'])
        return res
    
    def login_menu(self):
        while True:
            print("Bienvenido ")
            print("Menú de opciones: ")
            print("0. Salir")
            print("1. : {}".format(self.login_service['name']))
            option = input('Ingrese una opción')
            if option == '0':
                return
            elif option == '1':
                res = self.login()
                data = eval(res[12:])
                user_type = data[4]
                if res[10:12] == 'NK':
                    print("Servicio no está disponible")
                    pass
                elif data == None:
                    print("Usuario o contraseña incorrectos")
                    pass
                else:
                    print("Sesión iniciada")
                    break
            else:
                print("Opción no válida")
        self.menu(user_type)

    def menu(self, type_id):
        while True:
            print("Menú de opciones: ")
            print("0. Salir")
            available_services = [
                service for service in self.services if type_id in service['user_type']

            ]
            services={}
            for i in range(len(available_services)):
                actual_service = available_services[i]
                services[f'{i+1}'] = actual_service
                print("Opcion{}:{}".format(i+1,actual_service['name']))
            print("0. Salir")
            option = input('Ingrese una opción:')
            if option == '0':
                return
            elif option in services:
                    service = services[option]
                    inputs={}
                    for i in range(len(service['inputs'])):
                        input_data = service['inputs'][i]
                        key = input_data['name']
                        inputs[key]=input(input_data['message'])
                    res = self.send_msg(inputs,service['id'])
                    print(res)
                    if res[10:12] == 'NK':
                        print("Servicio no está disponible")
                        pass
                    else:
                        service['id']
            else:
                print("Opción no válida")



if __name__ == "__main__":
    app = App(
        login_service={
            'id': 'serv1',
            'name': 'Iniciar sesión',
            'inputs': [
                {
                    'name': 'correo',
                    'message': 'Ingrese su email'
                },
                {
                    'name': 'contrasena',
                    'message': 'Ingrese su contraseña'
                }
            ]
        },
        services=[
            {
                'id': 'serv2',
                'name': 'Ver productos',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre'
                    },
                ]
            },
            {
                'id': 'serv3',
                'name': 'Agregar producto',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre'
                    },
                    {
                        'name': 'precio',
                        'message': 'Ingrese el precio'
                    },
                    {
                        'name': 'estado',
                        'message': 'Ingrese el estado'
                    },
                    {
                        'name': 'ubicacion_bodega',
                        'message': 'Ingrese la ubicación en bodega'
                    },
                    {
                        'name': 'stock_actual',
                        'message': 'Ingrese el stock actual'
                    },
                    {
                        'name': 'stock_minimo',
                        'message': 'Ingrese el stock mínimo'
                    }
                ]
            },
            {
                'id': 'serv4',
                'name': 'Ver usuarios',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre'
                    },
                ]
            },
            {
                'id': 's5',
                'name': 'Eliminar producto',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'id',
                        'message': 'Ingrese el id del producto a eliminar'
                    },
                ]
            }
        ]
    )               


app.login_menu()


    




