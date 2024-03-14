# Financiera
Este proyecto es una aplicación web para gestionar pagos y contratos de una empresa financiera. 

Funcionalidades
Mostrar pagos activos
Insertar un nuevo pago
Mostrar los pagos de un contrato específico
Obtener los pagos del mes anterior
Estructura del Proyecto
El proyecto sigue la siguiente estructura:

proyecto_financiera/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
│
├── templates/
│   ├── index.html
│   ├── pagos_activos.html
│   ├── pagos_contrato.html
│   ├── pagos_mes_anterior.html
│   └── pagos.html
│ 
├── Consulta_SQL.txt
├── ERD_Financiera.png
├── main.py
└── maincmd.py

app/: Contiene los archivos de la aplicación Flask.

__init__.py: Inicializa la aplicación Flask y configura las rutas.
models.py: Define las clases de modelos para la base de datos.
routes.py: Contiene las rutas y las funciones asociadas para renderizar las páginas.
utils.py: Contiene funciones útiles para la aplicación.

templates/: Contiene las plantillas HTML para las páginas web.
Consulta_SQL.txt: Contine la consulta SQL para obtener todos los pagos acumulados por fecha y contrato de los clientes en el mes anterior 
ERD_Financiera.png: Contiene el diagrama entidad-relación de la base de datos
main.py: Archivo principal para la aplicacion
maincmd.py: Programa para probar las funciones desde cmd

Configuración
Tener PostgreSQL instalado y configurado en tu máquina.
Cree una base de datos llamada "financiera" y ajusta la URL de conexión en app/__init__.py si es necesario.
Cree las tablas siguientes: 
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY
);

CREATE TABLE contratos (
    id_contrato SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES clientes(id_cliente)
);

CREATE TABLE pagos (
    id_pago SERIAL PRIMARY KEY,
    id_contrato INTEGER REFERENCES contratos(id_contrato),
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    fecha DATE,
    monto FLOAT,
    activo BOOLEAN,
    fecha_registro DATE
);

Editar el archivo config.py con la URL de la base de datos:
SQLALCHEMY_DATABASE_URL = 'postgresql://tu_usuario:tu_contraseña@localhost/tu_base_de_datos'

Uso
Ejecuta la aplicación:
python main.py
La aplicación estará disponible en http://127.0.0.1:5000/
