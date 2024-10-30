from flask import Blueprint, render_template
from flask_login import login_required

# Definimos la variable core_bp para poder registrarla en: src/__init__.py
core_bp = Blueprint('core', __name__)

# Definimos la ruta raíz de la app: el Home Page


@core_bp.route('/')
@login_required
def home():
    return render_template('core/home.html')
