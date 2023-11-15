import sqlite3

def fetch_data_from_table(table_name):
    conn = sqlite3.connect('db/vise0.db')
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def show_data(table_name):
    rows = fetch_data_from_table(table_name)
    print(f"\nDatos de la tabla {table_name}:\n")
    
    for row in rows:
        print(row)

if __name__ == "__main__":
    # Ejemplo de cómo mostrar datos de cada tabla
    show_data('productos')
    show_data('usuarios')