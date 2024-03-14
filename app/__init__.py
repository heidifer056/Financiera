from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists

# Crear la aplicación Flask
app = Flask(__name__, template_folder='../templates')

# Configuraciones
app.config['SECRET_KEY'] = 'tu_clave_secreta'  

# Crear el motor de base de datos para PostgreSQL
engine = create_engine('postgresql://postgres:superusuario@localhost/financiera', echo=True)

# Verificar si la base de datos existe, si no, crearla
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Importar las rutas después de crear la aplicación
from app import routes
