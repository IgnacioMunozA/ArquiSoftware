import requests

def menu():
    print("1. Añadir producto")
    print("2. Ver productos")
    print("3. Ver usuarios")
    print("4. Deshabilitar producto")
    print("5. Salir")
    return int(input("Seleccione una opción: "))

def add_product():
    name = input("Nombre del producto: ")
    product_data = {"id": int(input("ID del producto: ")), "name": name, "status": "active"}
    response = requests.post('http://localhost:5000/products', json=product_data)
    print(f"Respuesta: {response.json()}")

def view_products():
    response = requests.get('http://localhost:5000/products')
    print(f"Productos: {response.json()}")

def view_users():
    response = requests.get('http://localhost:5000/users')
    print(f"Usuarios: {response.json()}")

def disable_product():
    product_id = int(input("ID del producto a deshabilitar: "))
    response = requests.put(f'http://localhost:5000/products/{product_id}', json={"status": "inactive"})
    print(f"Respuesta: {response.json()}")

def main():
    while True:
        user_choice = menu()
        if user_choice == 1:
            add_product()
        elif user_choice == 2:
            view_products()
        elif user_choice == 3:
            view_users()
        elif user_choice == 4:
            disable_product()
        elif user_choice == 5:
            print("Adiós!")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    main()
