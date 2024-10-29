from flask import Blueprint, render_template
from flask_login import login_required

# Definimos la variable core_bp para poder registrarla en: src/__init__.py
core_bp = Blueprint('core', __name__)

# Definimos la ruta raíz de la app: el Home Page


@core_bp.route('/')
@login_required
def home():
    return render_template('core/home.html')


@core_bp.route('/consultas')
@login_required
def queries():
    return render_template('core/queries.html')


@core_bp.route('/crerPlantillas')
@login_required
def createTemplates():
    return render_template('core/createTemplates.html')


@core_bp.route('/asignarUA')
@login_required
def assignUA():
    return render_template('core/assignUA.html')


@core_bp.route('/borrar')
@login_required
def delete():
    return render_template('core/delete.html')