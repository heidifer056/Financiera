from sqlalchemy import Column, Integer, Date, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# Definir la clase para la tabla clientes
class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True)

    contratos = relationship("Contrato", back_populates="cliente")
    pagos = relationship("Pago", back_populates="cliente")
# Definir la clase para la tabla contratos
class Contrato(Base):
    __tablename__ = 'contratos'

    id_contrato = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))

    cliente = relationship("Cliente", back_populates="contratos")
    pagos = relationship("Pago", back_populates="contrato")
# Definir la clase para la tabla pagos
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
