from colorama import Fore
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
            print("1. {}".format(self.login_service['name']))
            option = input('Ingrese una opción: ')
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
                service for service in self.services if type_id in service['user_type']     #Filters services to display by user role.
            ]
            services={}
            for i in range(len(available_services)):
                actual_service = available_services[i]
                services[f'{i+1}'] = actual_service                     #Creates a dictionary {str:dict}
                print("Opcion{}:{}".format(i+1,actual_service['name']))
            option = input('Ingrese una opción: ')
            if option == '0':
                break
            elif option in services:                        #Select a service.
                    service = services[option]              #Sets said service as current one.
                    inputs={}
                    for i in range(len(service['inputs'])):     #Iterates through the chosen service's inputs
                        input_data = service['inputs'][i]       #Makes input_data = chosen service's input list current iteration item ~ another dictionary {name:message}
                        key = input_data['name']
                        if key == 'na':                                 # This if conditional check the dictionary's 'name' field and checks for value 'na', a way to query 'SELECT * ...' without inputs.
                            break
                        if key == 'input_list':
                            item_dict = {}
                            while True:
                                p_name = input("Ingrese el nombre del producto a ordenar (0 para terminar): \n")
                                if p_name == '0':
                                    break
                                item_dict[p_name] = input("Ingrese la cantidad deseada: \n")

                            inputs[key] = item_dict
                        else:
                            inputs[key]=input(input_data['message'])    #Inserts current iteration's entered data into the empty dict 'inputs'.    
                    res = self.send_msg(inputs,service['id'])       #Sends all entered data ('inputs') to the bus.
                    print(res)
                    if res[10:12] == 'NK':
                        print("Servicio no está disponible.")
                        pass
                    else:
                        service['id']
            else:
                print("Opción no válida.")



if __name__ == "__main__":
    app = App(
        login_service={
            'id': 'serv1',
            'name': 'Iniciar sesión',
            'inputs': [
                {
                    'name': 'correo',
                    'message': 'Ingrese su email: \n'
                },
                {
                    'name': 'contrasena',
                    'message': 'Ingrese su contraseña: \n'
                }
            ]
        },
        services=[          #PERMISOSSSSSS
            {
                'id': 'serv2',
                'name': '\033[1;32m Ver productos\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'na',
                        'message': 'Ingrese el nombre: \n'
                    },
                ]
            },
            {
                'id': 'serv3',
                'name': '\033[1;32m Agregar producto\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre: \n'
                    },
                    {
                        'name': 'precio',
                        'message': 'Ingrese el precio: \n'
                    }
                ]
            },
            {
                'id': 'serv4',
                'name': '\033[1;32m Actualizar información de productos\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre: \n'
                    },
                    {
                        'name': 'nuevo_nombre',
                        'message': 'Ingrese el nuevo nombre: \n'
                    },
                    {
                        'name': 'precio',
                        'message': 'Ingrese nuevo precio: \n'
                    }
                ]
            },
            {
                'id': 'serv5',
                'name': '\033[1;32m Eliminar producto\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre del producto a eliminar: \n'
                    },
                ]
            },
            {
                'id': 'serv6',
                'name': '\033[1;37m Ver historial de cambios de productos\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'fecha',
                        'message': 'Ingrese una fecha para ver los cambios realizados desde esa fecha: \n' 
                    },
                ]
            },
            {
                'id': 'serv7',
                'name': '\033[1;37m Ver historial de cambios de usuarios\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'fecha',
                        'message': 'Ingrese una fecha para ver los cambios realizados desde esa fecha: \n' 
                    },
                ]
            },
            {
                'id': 'serv8',
                'name': '\033[1;33m Agregar empresa de transporte\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre: \n'
                    },
                    {
                        'name': 'telefono',
                        'message': 'Ingrese telefono de contacto: \n'
                    },
                    {
                        'name': 'correo',
                        'message': 'Ingrese el correo de contacto: \n'
                    }
                ]
            },
            {
                'id': 'serv9',
                'name': '\033[1;33m Obtener lista de empresas de transporte\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'na',
                        'message': 'Ingrese el nombre: \n'
                    }
                ]
            },
            {
                'id': 'ser10',
                'name': '\033[1;33m Eliminar una empresa de transporte\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre de la empresa: \n'
                    }
                ]
            },
            {
                'id': 'ser11',
                'name': '\033[1;33m Actualizar información de empresa de transporte\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre'
                    },
                    {
                        'name': 'nuevo_nombre',
                        'message': 'Ingrese el nuevo nombre: \n'
                    },
                    {
                        'name': 'telefono',
                        'message': 'Ingrese telefono de contacto: \n'
                    },
                    {
                        'name': 'correo',
                        'message': 'Ingrese el correo de contacto: \n'
                    }
                ]
            },
            {
                'id': 'ser12',
                'name': '\033[1;34m Agregar proveedor\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre: \n'
                    },
                    {
                        'name': 'telefono',
                        'message': 'Ingrese telefono de contacto: \n'
                    },
                    {
                        'name': 'correo',
                        'message': 'Ingrese el correo de contacto: \n'
                    }
                ]
            },
            {
                'id': 'ser13',
                'name': '\033[1;34m Obtener lista de proveedores\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'na',
                        'message': 'Ingrese el nombre: \n'
                    }
                ]
            },
            {
                'id': 'ser14',
                'name': '\033[1;34m Eliminar un proveedor\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre de la empresa: \n'
                    }
                ]
            },
            {
                'id': 'ser15',
                'name': '\033[1;34m Actualizar información de proveedor\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre: \n'
                    },
                    {
                        'name': 'nuevo_nombre',
                        'message': 'Ingrese el nuevo nombre: \n'
                    },
                    {
                        'name': 'telefono',
                        'message': 'Ingrese telefono de contacto: \n'
                    },
                    {
                        'name': 'correo',
                        'message': 'Ingrese el correo de contacto: \n'
                    }
                ]
            },
            {
                'id': 'ser16',
                'name': '\033[1;36m Crear instancia de inventario\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'nombre_producto',
                        'message': 'Ingrese el nombre del producto: \n'
                    },
                    {
                        'name': 'alias_bodega',
                        'message': 'Ingrese el alias de la bodega: \n'
                    },
                    {
                        'name': 'estado',
                        'message': 'Ingrese el estado: \n'
                    },
                    {
                        'name': 'stock_actual',
                        'message': 'Ingrese el stock actual: \n'
                    },
                    {
                        'name': 'stock_minimo',
                        'message': 'Ingrese el stock mínimo: \n'
                    }
                ]
            },
            {
                'id': 'ser17',
                'name': '\033[1;36m Gestionar inventarios\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'nombre_producto',
                        'message': 'Ingrese el nombre del producto: \n'
                    },
                    {
                        'name': 'alias_bodega',
                        'message': 'Ingrese el alias de la bodega: \n'
                    },
                    {
                        'name': 'estado',
                        'message': 'Ingrese el estado: \n'
                    },
                    {
                        'name': 'stock_actual',
                        'message': 'Ingrese el stock actual: \n'
                    },
                    {
                        'name': 'stock_minimo',
                        'message': 'Ingrese el stock mínimo: \n'
                    }
                ]
            },
            {
                'id': 'ser18',
                'name': '\033[1;36m Ver inventarios\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'na',
                        'message': 'Ver inventarios: \n' 
                    },
                ]
            },
            {
                'id': 'ser19',
                'name': '\033[1;37m Eliminar usuario\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'correo',
                        'message': 'Ingrese el correo del usuario a eliminar: \n'
                    },
                ]
            },
            {
                'id': 'ser20',
                'name': '\033[1;37m Actualizar información de usuario\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'correo',
                        'message': 'Ingrese el correo del usuario a actualizar: \n'
                    },
                    {
                        'name': 'nuevo_correo',
                        'message': 'Ingrese el nuevo correo: \n'
                    },
                    {
                        'name': 'nuevo_tipo',
                        'message': 'Ingrese el nuevo tipo de usuario: \n'
                    }
                ]
            },
            {
                'id': 'ser21',
                'name': '\033[1;37m Crear nuevo usuario\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'correo',
                        'message': 'Ingrese el correo del usuario a crear: \n'
                    },
                    {
                        'name': 'tipo',
                        'message': 'Ingrese el tipo de usuario: \n'
                    },
                    {
                        'name': 'contrasena',
                        'message': 'Ingrese la contraseña: \n'
                    },
                    {
                        'name': 'nombre',
                        'message': 'Ingrese el nombre: \n'
                    }
                ]
            },
            {
                'id': 'ser22',
                'name': '\033[1;30m Cambiar contraseña\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'correo',
                        'message': 'Ingrese el correo del usuario a cambiar contraseña: \n'
                    },
                    {
                        'name': 'contrasena',
                        'message': 'Ingrese su contraseña: \n'
                    },
                    {
                        'name': 'nueva_contrasena',
                        'message': 'Ingrese la nueva contraseña: \n'
                    }
                ]
            },
            {
                'id': 'ser23',
                'name': '\033[1;30m Recuperar contraseña\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'correo',
                        'message': 'Ingrese el correo del usuario a recuperar contraseña: \n'
                    },
                ]
            },
            {
                'id': 'ser24',
                'name': '\033[1;31m Crear un nuevo pedido\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'transportista',
                        'message': 'Ingrese el nombre de la empresa de transporte: \n'
                    },
                    {
                        'name': 'proveedor',
                        'message': 'Ingrese el nombre del proveedor: \n'
                    },
                    {
                        'name': 'bodega',
                        'message': 'Ingrese alias de bodega que recibirá el pedido: \n'
                    },
                    {
                        'name': 'input_list',
                        'message': 'Ingresar productos'
                    },
                ]
            },
            {
                'id': 'ser25',
                'name': '\033[1;31m Obtener un pedido\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'order_id',
                        'message': 'Ingrese el id del pedido: \n'
                    },
                ]
            },
            {
                'id': 'ser26',
                'name': '\033[1;31m Obtener detalle de pedido\033[0m',
                'user_type': ['Admin', 'Empleado'],
                'inputs': [
                    {
                        'name': 'na',
                        'message': 'Obtener todos los pedidos: \n'
                    },
                ]
            },
            {
                'id': 'ser27',
                'name': '\033[1;37m Eliminar registro de historial de productos\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'fecha',
                        'message': 'Ingrese fecha del registro a eliminar: \n'
                    },
                ]
            },
            {
                'id': 'ser28',
                'name': '\033[1;37m Eliminar registro de historial de usuarios\033[0m',
                'user_type': ['Admin'],
                'inputs': [
                    {
                        'name': 'fecha',
                        'message': 'Ingrese fecha del registro a eliminar: \n'
                    },
                ]
            }

        ]
    )               


app.login_menu()
