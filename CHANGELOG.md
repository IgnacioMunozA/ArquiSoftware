## Registro de cambios
Inicio de registro posterior a commit número 13.

# 15/11/23 - 01

- Corregido un error de consulta en el servicio 8.
- Corregido un condicional relacionado a consultas en el servicio 10.
- Corregidos múltiples mensajes de servicios.
- Añadido CRUD de proveedores.
- Añadidos servicios de lectura, creación y gestión de inventarios.
- Añadidos UPDATE para transportistas y productos.

# 14/11/23 - 01
Nuevo modelo de datos, cambios de estructura menores y actualización de código.

- Nuevo modelo de datos para el sistema.
- Todos los servicios asociados a cambios actualizados y funcionales.
- Cambios en estructura de diccionario de servicios en app.py
    - S1: login, permanece igual.
    - S2 a S5: asignados a CRUD de productos, todas las queries se han adaptado al nuevo modelo.
        - Anterior S4 (SELECT usuarios) a asignar al rango de CRUD de usuarios.
    - Anterior S6 se extiende a S7, separando consultas a historiales por separado.
    - S8 a S11: asignados a CRUD de transportistas.
- Modelo a seguir para resto de servicios en diccionario de app.py
    - S12 a S15: reservado para CRUD de proveedores.
    - S16 a S19: reservado para CRUD de usuarios.
    - Resto: POR DEFINIR
