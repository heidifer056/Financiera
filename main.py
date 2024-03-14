#Codigo en el que se se pueden probar las funciones en la pagina web
from flask import Flask, render_template, request
from app import routes
from app import app
from app.models import *
from app.utils import *

if __name__ == '__main__':
    app.run(debug=True)

