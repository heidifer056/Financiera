#Codigo en el que se pueden probar las funciones en cmd
from sqlalchemy import String, create_engine, Column, Integer, Date, Float, Boolean, ForeignKey, text
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy_utils import create_database, database_exists

# Crear el motor de base de datos para PostgreSQL
engine = create_engine('postgresql://postgres:superusuario@localhost/financiera', echo=True)

# Verificar si la base de datos existe, si no, crearla
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

# Definir la clase para la tabla Pago
class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True)

    contratos = relationship("Contrato", back_populates="cliente")
    pagos = relationship("Pago", back_populates="cliente")

class Contrato(Base):
    __tablename__ = 'contratos'

    id_contrato = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))

    cliente = relationship("Cliente", back_populates="contratos")
    pagos = relationship("Pago", back_populates="contrato")

class Pago(Base):
    __tablename__ = 'pagos'

    id_pago = Column(Integer, primary_key=True)
    id_contrato = Column(Integer, ForeignKey('contratos.id_contrato'))
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    fecha = Column(Date)
    monto = Column(Float)
    activo = Column(Boolean)
    fecha_registro = Column(Date)

    contrato = relationship("Contrato", back_populates="pagos")
    cliente = relationship("Cliente", back_populates="pagos")

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

def mostrar_pagos_activos():

    pagos_activos = session.query(Pago).filter_by(activo=True).all()
    for pago in pagos_activos:
        print(f"ID Pago: {pago.id_pago}, ID Contrato: {pago.id_contrato}, ID Cliente: {pago.id_cliente}, Fecha: {pago.fecha}, Monto: {pago.monto}, Activo: {pago.activo}, Fecha Registro: {pago.fecha_registro}")

def insertar_pago(id_contrato, id_cliente, fecha, monto):
    # Verificar si hay pagos anteriores para este contrato
    pagos_anteriores = session.query(Pago).filter(
        Pago.id_contrato == id_contrato,
        Pago.fecha > fecha
    ).all()

    # Desactivar los pagos posteriores
    for pago in pagos_anteriores:
        pago.activo = False

    # Crear el nuevo pago
    nuevo_pago = Pago(
        id_contrato=id_contrato,
        id_cliente=id_cliente,
        fecha=fecha,
        monto=monto,
        activo=True,
        fecha_registro=datetime.now().date()
    )
    session.add(nuevo_pago)

    # Insertar nuevos registros para los pagos que ya existían
    nuevos_registros = [Pago(
        id_contrato=pago.id_contrato,
        id_cliente=pago.id_cliente,
        fecha=pago.fecha,
        monto=pago.monto,
        activo=True,
        fecha_registro=pago.fecha_registro
    ) for pago in pagos_anteriores]
    session.add_all(nuevos_registros)

    session.commit()

def mostrar_pagos_contrato(id_contrato):
    pagos_contrato = session.query(Pago).filter_by(id_contrato=id_contrato).all()
    for pago in pagos_contrato:
        print(f"ID Pago: {pago.id_pago}, ID Cliente: {pago.id_cliente}, Fecha: {pago.fecha}, Monto: {pago.monto}")

def obtener_pagos_mes_anterior():
    sql_query = """
        SELECT 
            id_contrato,
            date_trunc('month', fecha) AS mes,
            sum(monto) AS total_pagos
        FROM 
            pagos
        WHERE 
            activo = True 
            AND fecha >= date_trunc('month', current_date) - interval '1 month' 
            AND fecha < date_trunc('month', current_date)
        GROUP BY 
            id_contrato, 
            date_trunc('month', fecha)
        ORDER BY 
            id_contrato, 
            mes;
    """

    results = session.execute(text(sql_query))
    for row in results:
        print(f"ID Contrato: {row[0]}, Mes: {row[1]}, Total Pagos: {row[2]}")

if __name__ == '__main__':
    while True:
        print("Seleccione una opción:")
        print("1. Mostrar pagos activos")
        print("2. Insertar pago")
        print("3. Mostrar pagos de un contrato")
        print("4. Obtener pagos del mes anterior")
        print("5. Salir")

        option = int(input())

        if option == 1:
            mostrar_pagos_activos()
        elif option == 2:
            id_contrato = int(input("Ingrese el ID del contrato: "))
            id_cliente = int(input("Ingrese el ID del cliente: "))
            fecha = datetime.strptime(input("Ingrese la fecha (YYYY-MM-DD): "), "%Y-%m-%d").date()
            monto = float(input("Ingrese el monto: "))
            insertar_pago(id_contrato, id_cliente, fecha, monto)
        elif option == 3:
            id_contrato = int(input("Ingrese el ID del contrato: "))
            mostrar_pagos_contrato(id_contrato)
        elif option == 4:
            obtener_pagos_mes_anterior()
        elif option == 5:
            break
        else:
            print("Opción inválida")