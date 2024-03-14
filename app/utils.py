from sqlalchemy import text
from app.models import Pago, Contrato, Cliente
from app import Session
from datetime import datetime

def mostrar_pagos_activos():
    # Crear una nueva sesión de SQLAlchemy
    session = Session()

    pagos_activos = session.query(Pago).filter_by(activo=True).all()

    # Cerrar la sesión después de usarla
    session.close()

    return pagos_activos

def insertar_pago(id_contrato, id_cliente, fecha, monto):
    # Crear una nueva sesión de SQLAlchemy
    session = Session()

    cliente_existente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
    
    if not cliente_existente:
        session.rollback()
        session.close()
        return "El ID del cliente no existe.", False

    contrato_existente = session.query(Contrato).filter_by(id_contrato=id_contrato).first()

    if not contrato_existente:
        session.rollback()
        session.close()
        return "El ID del contrato no existe.", False

    contrato_cliente_valido = session.query(Contrato).filter_by(id_contrato=id_contrato, id_cliente=id_cliente).first()

    if not contrato_cliente_valido:
        session.rollback()
        session.close()
        return "El ID del contrato no pertenece al ID del cliente.", False

    pagos_posterirores = session.query(Pago).filter(
        Pago.activo == True,
        Pago.id_contrato == id_contrato,
        Pago.id_cliente == id_cliente,
        Pago.fecha > fecha
    ).all()

    for pago in pagos_posterirores:
        pago.activo = False

    nuevo_pago = Pago(
        id_contrato=id_contrato,
        id_cliente=id_cliente,
        fecha=fecha,
        monto=monto,
        activo=True,
        fecha_registro=datetime.now().date()
    )
    session.add(nuevo_pago)

    nuevos_registros = [Pago(
        id_contrato=pago.id_contrato,
        id_cliente=pago.id_cliente,
        fecha=pago.fecha,
        monto=pago.monto,
        activo=True,
        fecha_registro=pago.fecha_registro
    ) for pago in pagos_posterirores ]
    session.add_all(nuevos_registros)

    # Cerrar la sesión después de usarla
    session.commit()
    session.close()

    return "Pago realizado correctamente.", True

def mostrar_pagos_contrato(id_contrato):
    # Crear una nueva sesión de SQLAlchemy
    session = Session()

    pagos_contrato = session.query(Pago).filter_by(id_contrato=id_contrato, activo=True).all()

    # Cerrar la sesión después de usarla
    session.close()

    return pagos_contrato

def obtener_pagos_mes_anterior():
    # Crear una nueva sesión de SQLAlchemy
    session = Session()

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
    pagos_mes_anterior = results.fetchall()
    
    session.close()
    
    return pagos_mes_anterior