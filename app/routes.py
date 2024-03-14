from flask import flash, render_template, request, redirect, url_for
from app import app
from app.utils import insertar_pago
from app.utils import mostrar_pagos_activos, insertar_pago, mostrar_pagos_contrato, obtener_pagos_mes_anterior

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagos', methods=['GET'])
def pagos():
    return render_template('pagos.html')

@app.route('/insertar_pago', methods=['POST'])
def insertar_pago_route():
    id_contrato = request.form['id_contrato']
    id_cliente = request.form['id_cliente']
    fecha = request.form['fecha']
    monto = request.form['monto']

    message, success = insertar_pago(int(id_contrato), int(id_cliente), fecha, float(monto))
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')

    return redirect(url_for('pagos'))


@app.route('/pagos_activos', methods=['GET'])
def mostrar_pagos_activos_route():

    pagos_activos = mostrar_pagos_activos()
    return render_template('pagos_activos.html', pagos=pagos_activos)

@app.route('/pagos_contrato', methods=['GET'])
def mostrar_pagos_contrato_route():
    id_contrato = request.args.get('id_contrato')

    # Validar que el ID del contrato no esté vacío
    if id_contrato is None or id_contrato == '':
        pagos_activos = mostrar_pagos_activos()
        return render_template('pagos_contrato.html', pagos=pagos_activos)

    # Utiliza la sesión SQLAlchemy correcta
    pagos_contrato = mostrar_pagos_contrato(int(id_contrato))
    return render_template('pagos_contrato.html', pagos=pagos_contrato)


@app.route('/pagos_mes_anterior', methods=['GET'])
def mostrar_pagos_mes_anterior_route():
    # Utiliza la sesión SQLAlchemy correcta
    resultados = obtener_pagos_mes_anterior()
    return render_template('pagos_mes_anterior.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)