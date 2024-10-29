<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
# <i class="fa fa-file"></i> README
# Ambientes virtuales en Python
Un entorno virtual es una herramienta que ayuda a mantener separadas las dependencias de nuestros proyectos. En el caso de *Archlinux* el paquete a
instalar sería:

```bash
$ sudo pacman -S python-virtualenv
```

Para comenzar a usarlo, primero creamos una carpeta donde se alojará el proyecto, por ejemplo:

```bash
$ mkdir app
```

y en esta carpeta creamos el entorno virtual de la siguiente manera:

```bash
$ cd app
$ virtualenv "venv"  # for linux
```

Para activarlo y comenzar a trabajar con él:

```bash
$ source venv/bin/activate
$(venv) app
```

Para salir del entorno virtual bastaría con escribir:

```bash
(venv)$ deactivate
```
Para instalar un paquete utilizamos pip (p.ej. Flask )
```bash
(venv) app$ pip install flask
```

Podemos verificar los paquetes instalados con:

```bash
$ pip list
```

obtenemos algo así laprimera vez:

```bash
Package      Version                                                                           
------------ -------                                                                            
blinker      1.8.2                                                                                                          
click        8.1.7                                                                                                                                                       
Flask        3.0.3                                                                                                                                                       
itsdangerous 2.2.0
Jinja2       3.1.4
MarkupSafe   2.1.5
pip          24.1
Werkzeug     3.0.3 
```  

En resumen, tendremos dentro de la carpeta que creamos al inicio (**app**) una subcarpeta que se llamará **env** que contiene diferentes archivos y 
directorios (no tocar). Para probar si tenemos flask instalado de manera correcta creamos un archivo que se llame por ejemplo **main.py** con el sigueinte contenido.

```python 
from flask import Flask 

app = Flask(__name__)

@app.route('/') # esta será la ruta del home page
def home(): # regresa el contenido de esta función
  return "¡Esta es la página de inicio!"
```

y podemos lanzar la aplicación con:

```bash
app $ flask --app main run
```

Si todo está bien, podremos visualizar el mensaje que regresa en un navegador de internet en la dirección [https://localhost:5000](https://localhost:5000). A este archivo le modificaremos su conteido y lo ajustaremos a una estructura más organizada de acuerdo con la documentación de FLASK y debido a que se trata de un proyecto que irá creciendo conforme avancemos.


# Estructura de directorios de la aplicación
Con la idea de tener organizada nuestra aplicación, es importante realizar una estructura de carpetas en Flask. La primera carpeta se creó cuando instalamos
el ambiente virtual **venv**, la segunda carpeta a crear será **src** donde estarán las demás carpetas que pertenecen a la aplicación. Es importante además
trabajar con un sistema de control de versiones, en este caso utilizaremos **GIT** por lo que resulta necesario crear los archivos **.env** y **.gitignore**,
en el primero definiremos las variables de entorno y el segundo tendrá archivos y carpetas a los que **git** no les dará seguimiento lo que significa que no 
se subirán a **GitHub**.

En el archivo **.env** definiremos las siguientes variables de entorno:

```{bash}
FLASK_APP = main.py
FLASK_DEBUG = 1
DEBUG = True
FLASK_RUN_PORT = 5000
APP_SETTINGS = config.DevelopmentConfig
SECRET_KEY = '5407df0348c2d8a31b0339e189'
DATABASE_URL = sqlite:///db.sqlite
``` 

- FLASK_APP - Se utiliza para especificar el módulo de la aplicación.
- FLASK_DEBUG - Indica si la aplicación está en modo de desarrollo, su valor por defecto es 1 (TRUE).
- DEBUG = True - Alternativa cuando se utiliza  el método **app.run()** en vez del comando  **flask run**. 
- FLASK_RUN_PORT - Para especificar el puerto del servidos al momento de iniciar la aplicación.
- SECRET_KEY: Necesaria para firmar la cookie de sesión. También puede ser utilizada para otros aspectos de seguridad.

Para conocer otras variables de entorno podemos acceder a [pallets projects](https://flask.palletsprojects.com/en/latest/config/) o bien a la documentación oficial de Flask  o bien en [j2logo](https://j2logo.com/tutorial-flask-leccion-7-parametros-de-configuracion-proyecto/). Para que flask pueda leer las variables de entorno, resulta necesario instalar la librería **python-dotenv**,  que es una dependencia de Flask que se encarga de leer los pares KEY-VALUE que se encuentran en el archivo de entorno **.env**.

```bash
$ pip instal python-dotenv
```

Para el caso del archivo **.gitignore**, que contendrá lo que queremos excluir en **Git**, escribimos lo siguiente:

```bash
venv/             # excluye el entorno virtual
.env              # excluye las variables de entorno

__pycache__/      # Todas las carpetas de pycache
*.py[cod]         # Todos los archivos compilados de python

.pytest_cache     # Todas las carpetas de testing, si es que tenemos
```

Otro archivo a crear es **README** donde, iré documentando la manera en que se irá desarrollando la aplicación. Por el momento, la estructura de directorios de la aplicación que estamos desarrollando quedaría de la siguiente manera:

```bash
.
└── app
    ├── src
    ├── venv
    ├── .env
    ├── .gitignore
    ├── main.py
    └── README.md
```

# Creación de la aplicación
Además de **main.py**, vamos a crear otros dos archivos:

- **main.py** - que lanzará la aplicación (ya lo creamos)
- **config.py** - Donde se definirá el ambiente de trabajo de la aplicación
- **\_\_init\_\_.py** - se encargará iniciar la app con el método **init_app()**.

Los dos primero archivos se van a crear fuera de la carpeta **src** y el tercero dentro de esta carpeta, así como se muestra:

```bash
.
└── app
    ├── src
    │   └── __init.py__
    ├── venv
    ├── config.py
    ├── .env
    ├── .gitignore
    ├── main.py
    └── README.md
```

En primer lugar, escribimos el archivo de configuración **config.py** en el directorio raíz (fuera de src):

```python
from decouple import config


class Config(object):
    DEBUG = config('DEBUG')
    Testing = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True


config = {
    'development': DevelopmentConfig
}
```

Podemos observar que se hace uso de la librería **decouple** que se utiliza para separar las variables de entorno del código fuente de la aplicación, esto nos obliga a instalar las siguiente librería:

```{bash}
$ pip install python-decouple
```

Además, en el mismo archivo de configuración se ha creado la clase **Config** en la que el atributo DEBUG se define según el valor que le dimos en el
archivo donde se especifican las variables de ambiente **.env**, en este caso **DEBUG=True** dado que estamos en etapa de desarrollo. Más adelante es posible que se creen otras clases como TestingConfig y ProductionConfig, a cada una de ellas se le agregarán otros atributos conforme avance el proyecto y finalmente se crea un diccionario en el que se especifican las diferentes etapas de desarrollo de la aplicación.

Vamos a modificar el archivo **main.py** con el siguiente contenido:

```python
from config import config
from src import init_app


app_settings = config['development']
app = init_app(app_settings)

if __name__ == '__main__':
    app.run()
```

Como podemos observar, importmos la clase **config** del archivo **config.py**, se crea la variable **app_settings** con la variable de ambiente que deseamos
en este momento sería en etapa de desarrollo por lo que, del diccionario especificado seleccionamoe: **development**, así como se muestra en el código. También se crea la variable **app** con la que se lanzará la aplicación y para esto se importa la función **init_app** que se encuentra en el archivo **\_\_init\_\_.py** dentro del directorio **src**, este archivo se encargará de configurár la aplicación de acuerdo a la etapa de desarrollo que elegimos por lo que, como parámetro se envía la variable **app_settings** que definimos con anterioridad. Su contenido sería:

```python
from flask import Flask


def init_app(app_settings):
    app = Flask(__name__)
    app.config.from_object(app_settings)

    # Register Blueprints
    from src.core.views import core_bp
    app.register_blueprint(core_bp)

    return app
```

Podemos darnos cuenta que se crea la aplicación flask con la variable **app** y se configura con la etapa de desarrollo que le enviamos como parámetro. Además con la idea de organizar el proyecto, hacemos uso de Blueprint (bp). Blueprint es un objeto que permite definir las rutas (vistas), plantillas y recursos estáticos de forma modular lo que nos facilitará el mantenimiento de la aplicación conforme vaya creciendo. En este caso estamos registrando el **core_bp** que se utilizará para definir la ruta o vista principal del directorio raíz (home page) de la página. Para esto importamos la variable **core_bp** del archivo **views.py** que se encuentra en el directorio **src/core** que tampoco se han creado por lo que, debemos debemos hacerlo. 

### Uso de Blueprint
Para poder registrar cualquier Blueprint debemos crear el archivo donde se definirá la ruta. En este caso en particular, estando en el directorio **src**, 
creamos el directorio **core** y en ese directorio creamos el archivo **\_\_init\_\_.py** vacío para convertir este directorio en un paquete de Python, además creamos el archivo **views.py** donde vamos a almacenar la ruta del home.

```bash
app/src $ mkdir core
app/src $ cd core
app/src/core $ touch __init__.py views.py
```

La estructura de directorios hasta el momento quedaría de la siguiente manera:

```bash
.
└── app
    ├── src
    │   ├── core
    │   │   ├── __init__.py
    │   │   └── views.py
    │   └── __init__.py
    ├── venv
    ├── config.py
    ├── .env
    ├── .gitignore
    ├── main.py
    └── README.md
```

En el archivo **views.py** escribimos el siguiente código:

```python
from flask import Blueprint, render_template

# Definimos la variable core_bp para poder registrarla en: src/__init__.py
core_bp = Blueprint('core', __name__)

# Definimos la ruta raíz de la app: el Home Page
@core_bp.route('/')
def home(): # Esta función regresa el render de un archivo HTML no de un mensaje
    return render_template('core/home.html')
```

Como podemos observar, importamos de Flask **Blueprint** además de **render_template**, un método de Flask que se encarga de presentar una plantilla (template) en formato HTML, el cual permite generar una respuesta. Definimos la variable **core_bp** que registramos en la función **inita_app** y definimos
la ruta y una función **home()** que regresará como respuesta, el código escrito en **home.html** que vamos a crear dentro del directorio **src/tempalates**,
en los cuales trabajaremos a continuación. Dado que resulta importante conocer como organizar una aplicación de flask utilizando Blueprint, sugiero leer este
[tutorial](https://blog.ashutoshkrris.in/how-to-use-blueprints-to-organize-your-flask-apps) o bien, cualquiera que les sea útil.

## Creación de plantillas y estilos
Para esto vamos a crear las carpetas **templates**  y  **static** dentro de la carpeta **src**. La carpeta **templates** contendrá todas las plantillas en código HTML que se utilizarán en el proyecto y **static** va a contener los recursos utilizados por las plantillas como por ejemplo, los archivos de estilo CSS, los archivos JavaScript y las imágenes. Dentro de estas carpetas vamos a crear tres archivos, **layout.html**, **navbar.html** y **uagro.css**, los dos primeros dentro de la carpeta **templates** y el tercero dentro de la carpeta **static/css**. Ademas se creará la carpeta **static/images** en la que copiaremos el logo de la Comisión Mixta Paritaria de Admisión y Promoción que se utilizará en las páginas. La estructura de directorios quedaría de la sigueinte manera:

```bash
└── app
    ├── src
    │   ├── core
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── static
    │   │   ├── css
    │   │   │   └── uagro.css
    │   │   └── images
    │   │       └── logos
    │   │           └── logo.png
    │   ├── templates
    │   │   ├── core
    │   │   │   └── home.html
    │   │   ├── layout.html
    │   │   └── navbar.html
    │   └── __init.py__
    ├── venv
    ├── config.py
    ├── .env
    ├── .gitignore
    ├── main.py
    └── README.md
```

### Plantillas HTML y Estilo CSS

Comenzaremos creando la plantilla básica **layout.html** y añadimos el siguiente código:

```html
<!DOCTYPE html>
<html lang="es" data-mdb-theme="light">
    <head>
        <!-- META -->
        <meta name="description" content="">
        <meta name="author" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- BOOSTRAP 5 CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <!-- AWESOME FONTS -->
        <script src="https://kit.fontawesome.com/1f872158cd.js" crossorigin="anonymous"></script>
        <!-- CUSTOM SCSS -->
        {% block customCSS %}{% endblock %}
        <!-- TAB TITLES -->
        {% if title %}
            <title>cmixta - {{ title }}</title>
        {% else %}
            <title>cmixta Page</title>
        {% endif %}
    </head>
    <body>
        <!-- NAVIGATION BAR -->
        {% include "navigation.html" %}
        <!-- MESSAGES -->
        <div class="container">
            <br>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <div class="row">
                        <div class="col-md-4">
                        </div>
                        <div class="col-md-4">
                            {% for category, message in messages %}
                                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                                    {{message}}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>
                            {% endfor %}
                        </div>
                        <div class="col-md-4">
                        </div>
                    </div>
                {% endif %}
            {% endwith %}
            <!-- BODY CONTENT -->
            {% block content %}{% endblock %}
        </div>
        <!-- BOONDLE JAVASCRIPT BOOSTRAP 5 -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        <!-- JavaScript Code -->
        {% block js %}{% endblock %}
    </body>
</html>
```

Como podemos observar, en este código, utilizamos [**Jinja2**](https://flask.palletsprojects.com/es/main/templating/), una biblioteca de Python que permite construir plantillas para distintos formatos de salida, en este caso HTML. Esta biblioteca se encuentra ya configurada de forma automática dentro del framework Flask. El archivo **layout.html** será el archivo HTML principal que heredarán las demás plantillas que vamos a escribir. En este código he agregado compatibilidad con **Bootstrap 5**, **Awesome Fonts** así como **Flask Flashes** para mostrar alertas de Bootstrap **<!-- MESSAGES -->** en la aplicación, se incluye también la barra de navegación **<!-- NAVIGATION BAR -->**, el contenido de la página **<!-- BODY CONTENT -->** y un bloque para incluir código JavaScript **<!-- JavaScript Code -->** en caso necesario.

Añadimos también el archivo que contiene la barra de navegación de la aplicación

```html
<!-- CUSTOM CSS STYLESHEET -->
{% block customCSS %}
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/uagro.css') }}">
{% endblock %}
<!-- Navbar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-light">
    <!-- Container wrapper -->
    <div class="container-fluid">
        <!-- Navbar brand -->
        <a class="navbar-brand" href="/">
            <img src="{{ url_for('static', filename='images/logos/cmixta_logo_white_3.svg') }}" alt="">CMPAyP
        </a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <!-- LEFT LINKS -->
            <ul class="navbar-nav ms-auto d-flex flex-row mt-3 mt-lg-0">
                <li class="nav-item text-center mx-2 mx-lg-1">
                    <a class="nav-link active" aria-current="page" href="/">
                        <div>
                            <i class="fas fa-home fa-lg mb-1"></i>
                        </div>
                        Home PAGE
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

Además, vamos agregar el contenido del **<!-- BODY -->** que especificamos en el **render_template('core/home.html')** del archivo **src/core/views.py**, este archivo lo vamos a crear bajo la carpeta **src/templates/core/home.html** con el siguiente contenido:

```html
{% extends "layout.html" %}
{% block content %}
    <h3>¡Hola Mundo!</h3>
{% endblock content %}
```

Vámos a crear una hoja de estilo en cascada (CSS) en la carpeta **src/static**, en ésta vamos a definir la tipografía, los colores institucionales así como cada uno de los estilos que vamos a utilizar en toda la aplicación, ejemplo parcial de esto lo podemos observar en el siguiente código. Para este caso la tipografía a utilizar será Barlow Condensed para la barra de navegación y para Títulos, subtítulos y sub sub títulos.

```css
/* Fonts to USE  */
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

/* DEFINE UAGro COLORS */
:root {
    --blue-dark: #17243f;
    --blue-light: #153d6a;
    --red-dark: #be1522;
    --red-light: #e30613;
    --gray-dark: #9c9c9c;
    --gray-light: #c6c6c6;
    --blue-bg-dark: #172a4a;
    --blue-bg-mid: #163155;
    --blue-bg-light: #16375f;
    --black: #000;
    --white: #fff;
}

/* DEFINE TIPOGRAPHY TO USE */
*{
    font-family: Monserrat, sans-serif;
}

body {
    font-family: Montserrat, sans-serif;
    background-color: var(--white)
}
```

Si corremos la aplicación, desde la carpeta app, con estos cambios realizados: 
```bash 
(app) $ python main.py
``` 

obtendremos la siguiente imagen con la dirección: [localhost:5000](http://localhost:5000), en la que se puede observar el logo de la Comisión Mixta Paritaria de Admisión y Promoción del lado izquierdo, el enlace del Home junto con su ícono (ambos nos llevan a la raíz de la aplicación (/)) y lo que sería el contenido de la página por el momento.

![](src/static/images/app/fig_001.png)

Dado que se requiere, por cuestiones de seguridad, accesos controlado, vamos a implementar las páginas de registro, autentificación (login) y salida de la aplicación (logout).

## Creación de las páginas: Registro, Login y Logout
Para esto, primero creamos el directorio **src/accounts** y creamos dos archivos dentro de este directorio: **\_\_init\_\_.py**, archivo vacío para convertirlo en un paquete de Python y el archivo **views.py** que es donde almacenaremos todas las rutas relacionadas con la autenticación de los usuarios:

```bash
src $ mkdir accounts
src $ cd accounts
admins $ touch __init__.py views.py   
```

La estructura de directorios hasta el momento quedaría de la siguiente manera:

```bash
.
└── app
    ├── src
    │   ├── accounts
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── core
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── static
    │   │   ├── css
    │   │   │   └── uagro.css
    │   │   └── images
    │   │       └── logos
    │   │           └── logo.png
    │   ├── templates
    │   │   ├── core
    │   │   │   └── home.html
    │   │   ├── layout.html
    │   │   └── navbar.html
    │   └── __init.py__
    ├── venv
    ├── config.py
    ├── .env
    ├── .gitignore
    ├── main.py
    └── README.md
```

 Ahora creamos el Blueprint de los usuarios de la aplicación, en el archivo **src/accounts/views.py**, agregando el siguiente código:

```python
from flask import Blueprint, render_template

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/login')
def login():
    return render_template('accounts/login.html')
```

y registramos este Blueprint en el archivo **src/\_\_init\_\_.py**:

```python
from flask import Flask


def init_app(app_settings):
    app = Flask(__name__)
    app.config.from_object(app_settings)

    # Register Blueprints
    from src.core.views import core_bp
    app.register_blueprint(core_bp)
    from src.accounts.views import accounts_bp # agregamos esta línes
    app.register_blueprint(accounts_bp) # agregamos esta línes

    return app
```

Vamos también a crear la plantilla del login dentro del folder **src/templates/admins/login.html**, para esto:

```bash
templates $ mkdir accounts
templates $ cd accounts
admins $ touch login.html 
```

y escribimos el siguiente código:

```html
{% extends "layout.html" %}
{% block content %}
    <h3>Te encuentras en la página del LOGIN</h3>
{% endblock content %}
```

La estructura de directorios quedaría hasta el momento como:

```bash
.
└── app
    ├── src
    │   ├── accounts
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── core
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── static
    │   │   ├── css
    │   │   │   └── uagro.css
    │   │   └── images
    │   │       └── logos
    │   │           └── logo.png
    │   ├── templates
    │   │   ├── accounts
    │   │   │   └── login.html
    │   │   ├── core
    │   │   │   └── home.html
    │   │   ├── layout.html
    │   │   └── navbar.html
    │   └── __init.py__
    ├── venv
    ├── config.py
    ├── .env
    ├── .gitignore
    ├── main.py
    └── README.md
```

Si corremos la app nuevamente con la dirección [localhost:5000/login](http://localhost:5000/login), obtendríamos la siguiente imagen:

![](src/static/images/app/fig_002.png)

### Creando el modelo de los usuarios de la app
Antes de crear el formulario del **login** para acceder a la página, necesitamos crear el modelo de usuarios de la app que utilizaremos. Los modelos representan las tablas en la Base de Datos de nuestra aplicación. Para poder crear nuestro modelo, creamos el archivo **src/accounts/models.py**:

```bash
app $ touch src/accounts/models.py 
```

La estructura de directorios quedaría:

```bash
.
└── app
    ├── src
    │   ├── accounts
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   └── views.py
    │   ├── core
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── static
    │   │   ├── css
    │   │   │   └── uagro.css
    │   │   └── images
    │   │       └── logos
    │   │           └── logo.png
    │   ├── templates
    │   │   ├── accounts
    │   │   │   └── login.html
    │   │   ├── core
    │   │   │   └── home.html
    │   │   ├── layout.html
    │   │   └── navbar.html
    │   └── __init.py__
    ├── venv
    ├── config.py
    ├── .env
    ├── .gitignore
    ├── main.py
    └── README.md
```

Dado que estamos tratando con autenticación de usuarios que es un aspecto crucial del desarrollo web, especialmente cuando se trata de proteger las cuentas de usuario y la información confidencial, usaremos la librería **Bcrypt**, diseñado específicamente para el hash de contraseñas, es una opción popular debido a su resistencia a los ataques de fuerza bruta y su naturaleza adaptativa, necesitaremos además las librerías **SQLAlchemy** y **datetime** Aquí un breve resumen de ellas:

- [datetime](https://docs.python.org/3/library/datetime.html): Librería que proporciona clases para la manipulación de fechas y horas. La usaremos para registro de altas y bajas de usuarios
- [Flask-Bccrypt](https://flask-bcrypt.readthedocs.io/en/1.0.1/): es una extensión de Flask que proporciona utilidades de hash bcrypt para su aplicación.
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/): es una extensión para Flask que agrega compatibilidad con SQLAlchemy a la aplicación es decir, facilita la realización de tareas comunes.

Por lo tanto, resulta necesario instalarlas en nuestro entorno virtual:

```bash
app $ pip install Flask-Bcrypt Flask-SQLAlchemy datetime
```

Instaladas las librerías, creamos el contenido del archivo **src/accounts/models.py**:

```python
from datetime import datetime
from src import bcrypt, db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<email {self.email}>"
``` 

Podemos observar en el código que hemos creado un modelo de usuario heredando la clase db.Model. El modelo de usuario administrador consta de los siguientes campos:

- id: almacena la clave principal de la tabla de usuarios
- email: almacena el correo electrónico del usuario
- password: almacena la contraseña cifrada del usuario
- created_on: almacena la fecha y hora en que se creó el usuario
- is_admin: almacena si el usuario es administrador o no

En el constructor de la clase, se configuran los campos por ejemplo, en el campo password se genera el hash de la contraseña utilizando el objeto bcrypt importado desde la aplicación. Es importante observar que en la segunda línea, hacemos importaciones desde el archivo **src/\_\_init\_\_.py** por lo que resulta importante modificarlo y agregar las líneas siguientes:

```python
from flask import Flask
from flask_bcrypt import Bcrypt  # Agregamos esta línea
from flask_sqlalchemy import SQLAlchemy # Agregamos esta línea


def init_app(app_settings):
    app = Flask(__name__)
    app.config.from_object(app_settings)

    bcrypt = Bcrypt(app) # Agregamos esta línea para crear el objeto bcrypt
    db = SQLAlchemy(app) # Agregamos esta línea para crear el objeto db

    # Register Blueprints
    from src.core.views import core_bp
    app.register_blueprint(core_bp)
    from src.admins.views import admins_bp
    app.register_blueprint(admins_bp)

    return app
```

En este punto, la librería **SQLAlchemy** a través de la variable **db = SQLAlchemy(app)** exige definir la variable de entorno **'SQLALCHEMY_DATABASE_URI'** o **'SQLALCHEMY_BINDS'**, así que, agregamos esta variable de entorno en el archivo **.env** que se encuentra en él directorio raíz de la app:

```bash
FLASK_APP = main.py
FLASK_DEBUG = 1
DEBUG = True
FLASK_RUN_PORT = 5000

# Database connection
USERPASS = 'mysql+pymysql://root:cmixta2024@'
BASEDIR = '127.0.0.1:3306'
DBNAME = '/cmixta'
DATABASE_URI = USERPASS + BASEDIR + DBNAME

# o bien de esta manera, esta es la que utilizaré
DATABASE_URI = mysql+pymysql://root:cmixta2024@127.0.0.1:3306/cmixta
```

Como podemos observar en el código, para poder realizar la conexión con la base de datos, Flask necesita un conector que dependerá del manejador de la base de datos que se está utilizando, en este caso utilizaré el de mysql (puede ser el conector de mariadb) así que debemos instalar este conector:

```bash
$ pip install pymysql
```
toda vez instalado, modificamos el archivo **config.py** agregando las siguientes líneas:

```python
from decouple import config


class Config(object):
    DEBUG = config('DEBUG')
    Testing = False
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URI') # Agregar esta línea
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Agregar esta línea


class DevelopmentConfig(Config):
    DEVELOPMENT = True


config = {
    'development': DevelopmentConfig
}
```

En este caso con SQLALCHEMY_DATABASE_URI le estamos indicando a la aplicación la cadena de conexión a la base de datos y SQLALCHEMY_TRACK_MODIFICATIONS = False deshabilita el seguimiento de modificaciones de objetos, lo que permite utilizar menos memoria. Estas modificaciones nos permiten conectarnos a la base de datos que, en este ejemplo le he llamado cmixta. 

En este punto haré una pausa para instalar el manejador de base de datos que vamos a utilizar.

### Instalando la Base de Datos

En este caso utilizaremos **mariadb** y **mysql-workbench**, cabe aclarar que en la actualidad, el primero sustituye al manejador de base de datos **mysql** y el segundo solo es el ambiente gráfico del primero. Así que para instalarlo ejecutamos desde una terminal (fuera del entorno virtual de Flask):

```bash
$ sudo pacman -S mariadb mysql-workbench 
```

Toda vez instalados y antes de inicializar la base de datos(**mariadb**), la configuramos como se indica en el [Archlinix Wiki Mariabd](https://wiki.archlinux.org/title/MariaDB) o bien seguir las instrucciones de [este vídeo en youtube](https://www.youtube.com/watch?v=Fee_F1dPOuc). Desde una terminal escribimos:

```bash
$  sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
```

Toda vez realizado esto, inicializamos el manejador de base de datos y la habilitamos para que cada vez que iniciemos la computadora, se inicie de forma automática:

```bash
$  sudo systemctl start mariadb.service
$ sudo systemctl enable mariadb.service
```

para verificar si el manejador de base de datos está activo, lo podemos comprobar con:

```bash
$  sudo systemctl status mariadb.service
```

Ahora debemos configurar la seguridad, para esto ejecutamos:

```bash
$  sudo mysql_secure_installation
```

Cuando pregunte la contraseña de **root** ponemos enter, que es la configuración por default (esto es por ser la primera vez), la siguiente pregunta sería **Switch to unix_socket authentication** y tecleamos **yes**, después preguntará si queremos cambiar la contraseña de **root**, le indicamos que si y escribimos la contraseña que elijamos y preguntará nuevamente la contraseña. De ahí en adelante, elegimos que si y que no, para no complicarme tanto, a todo le di  **yes**.

En resumen, una vez inicializada la base de datos, podemos ingresar con el usuario **root** y el password definido:

```bash
$  mysql -u root -p
```

o bien:

```bash
$  mariadb -u root -p
```

nos preguntará el password que definimos, en este caso: **cmixta2024** y aparecerá el prompt de mariadb:

```bash
Warning: skipping '!includedir /etc/my.cnf.d' directive as maximum includerecursion level was reached in file /etc/my.cnf.d/my.cnf at line 10
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 17
Server version: 11.5.2-MariaDB Arch Linux

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
```

En resumen, tendremos los siguientes datos:

- username = root
- password = cmixta2024
- host = localhost
- port = 3306
- database_name = cmixta

y son precisamente los datos que utilicé anteriormente en el archivo **.env** para establecer la conexión.

### Creando la página de Registro, Inicio y Salida de la app
Toda vez instalado el manejador de base de datos, su entorno gráfico, la modificación de los archivos **.env**, **config.py** para poder realizar la conexión de nuestra aplicación flask con MySql y creado el modelo que utilizaremos para los usuarios de la app, estamos en disponibilidad de crear los formularios de **register**, **login** y **logout** de la aplicación usuarios puedan autentificarse y salir, para esto, vamos a necesitar la librería **Flask-Login** que de manera general proporciona administración de sesiones de usuario para Flask es decir, se encarga de las tareas habituales de iniciar sesión, cerrar sesión y recordar las sesiones de los usuarios durante períodos prolongados de tiempo. la instalación la hacemos de la siguiente manera:

```bash
app $ pip install Flask-Login
```

La parte más importante de Flask-Login es la clase LoginManager que permite que nuestra aplicación y Flask-Login trabajen juntos así que debemos modificar el archivo **src/\_\_init\_\_.py** añadiendo las siguientes líneas:

```python
from flask import Flask
from flask_login import LoginManager  # Agregamos esta línea
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


def init_app(app_settings):
    app = Flask(__name__)
    app.config.from_object(app_settings)

    login_manager = LoginManager(app)   # Agregamos esta línea
    login_manager.init_app(app)  # Agregamos esta línea

    bcrypt = Bcrypt(app) 
    db = SQLAlchemy(app) 

    # Register Blueprints
    from src.core.views import core_bp
    app.register_blueprint(core_bp)
    from src.admins.views import accounts_bp
    app.register_blueprint(accounts_bp)

    return app
```

Ya que hemos configurado e inicializado el administrador de inicio de sesión en la aplicación (**login_manager**), debemos regresar el **user_loader**. Esto para volver a cargar el objeto de usuario a partir de su ID almacenado en la sesión es decir, debe tomar el ID de un usuario y devolver el objeto del usuario correspondiente a ese ID. Esto lo haremos en el archivo **src/\_\_init\_\_.py** de la siguiente manera:

```python
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


def init_app(app_settings):
    app = Flask(__name__)
    app.config.from_object(app_settings)

    login_manager = LoginManager(app)
    login_manager.init_app(app)

    bcrypt = Bcrypt(app) 
    db = SQLAlchemy(app) 

    # Register Blueprints
    from src.core.views import core_bp
    app.register_blueprint(core_bp)
    from src.admins.views import accounts_bp
    app.register_blueprint(accounts_bp)

    from src.accounts.models import User # Agregamos esta línea

    @login_manager.user_loader # Agregamos esta línea
    def load_user(user_id): # Agregamos esta línea
        return User.query.filter(User.id == int(user_id)).first() # Agregamos esta línea

    return app
```

El modelo que hemos creado **src/accounts/models.py** debe implementar las siguientes propiedades y métodos:

- **is_authenticated**: esta propiedad devuelve True si el usuario está autenticado.
- **is_active**: esta propiedad devuelve True si la cuenta del usuario está activa
- **is_anonymous**: esta propiedad devuelve True si se trata de un usuario anónimo (los usuarios reales devuelven False).
- **get_id()**: este método devuelve una cadena que identifica de forma única a este usuario y se puede utilizar para cargar el usuario desde la devolución de llamada **user_loader**.

Sin embargo, no es necesario implementarlos explícitamente ya que, Flask-Login proporciona una clase **UserMixin** que contiene estas implementaciones predeterminadas para todas estas propiedades y métodos así que, solo necesita heredarlas por lo que modificamos el archivo **src/accounts/models.py**:

```python
from datetime import datetime
from flask_login import UserMixin # Agregar esta línea
from src import bcrypt, db


class User(UserMixin, db.Model): # Modificar esta línea

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<email {self.email}>"
``` 

Resulta importante observar que el archivo **models.py** importa las variables **bcrypt** y **db** desde el archivo **src/\_\_init\_\_.py** sin embargo, estas variables se encuentran dentro de una función por lo que resulta necesario hacerlas globales para que puedan ser llamadas. También es posible personalizar el proceso de inicio de sesión predeterminado en el archivo **src/\_\_init\_\_.py**. El nombre de la vista de inicio de sesión se puede configurar como LoginManager.login_view. El valor hace referencia al nombre de la función que se encargará del proceso de inicio de sesión. De igual manera, es posible personalizar la categoría de los mensajes (estas dos son opcionales):

```python
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


def init_app(app_settings):
    global bcrypt, db # Agregar esta línea
    app = Flask(__name__)
    app.config.from_object(app_settings)

    login_manager = LoginManager(app)
    login_manager.init_app(app)

    bcrypt = Bcrypt(app) 
    db = SQLAlchemy(app) 

    # Register Blueprints
    from src.core.views import core_bp
    app.register_blueprint(core_bp)
    from src.admins.views import admins_bp
    app.register_blueprint(admins_bp)

    from src.accounts.models import User

    login_manager.login_view = "accounts.login"  # Agregamos esta línea
    login_manager.login_message_category = "danger"  # Agregamos esta línea

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first() # Agregamos esta línea

    return app
```

Dado que se requiere que la autentificación se realice desde el **Home page** es decir, los usuarios no tendrán acceso a nada sin antes registrarse, agregamos un middleware **@login_required** para evitar el acceso de usuarios no autenticados, para esto, modificamos el archivo **src/core/views.py** de la siguiente manera:

```python
from flask import Blueprint, render_template
from flask_login import login_required # Agregamos esta línea

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@login_required  # Agregamos esta línea
def home():
    return render_template('core/home.html')
```

Si corremos la aplicación, se generará un **RuntimeError** indicando que la sesión no puede estar disponible debido a que no se ha establecido la variable de entorno **SECRET_KEY** para darle solución, agregamos la variable en el archivo **.env** 

```bash
FLASK_APP = main.py
FLASK_DEBUG = 1
DEBUG = True
FLASK_RUN_PORT = 5000

# Database connection
USERPASS = "mysql+pymysql://root:cmixta2024@"
BASEDIR = "127.0.0.1:3306"
DBNAME = "/cmixta"
DATABASE_URI_NO = USERPASS+BASEDIR+DBNAME

# Database connection 2 (this way is OK)
DATABASE_URI = mysql+pymysql://root:cmixta2024@127.0.0.1:3306/cmixta

SECRET_KEY = SECRET_KEY = '5407df0348c2d8a31b0339e189' # Agregar esta línea
```

y la llamamos en el archivo **config.py** de la siguiente manera:

```python
from decouple import config


class Config(object):
    DEBUG = config('DEBUG')
    Testing = False
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config('SECRET_KEY') # Agregar esta línea


class DevelopmentConfig(Config):
    DEVELOPMENT = True


config = {
    'development': DevelopmentConfig
}
```

Hasta el momento, si corremos la aplicación nuevamente, nos llevará directamente a la páginia de inicio (Home) pero con la diferencia que, aparecera el siguiente mensaje dado que le indicamos en el archivo **src/core/views.py** que se requería inicio de sesión **@login_required** antes de poder acceder a la página (Aclaración: quité el texto que había antes en **login.html**). Esta sería la imagen que nos mostraría la app:

![](src/static/images/app/fig_003.png)

### Implementado el User Login
Ahora si estamos en posibilidad de crear la página del login, para esto, vamos autilizar la librería:

- **[Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/)**:  es una integración simple de Flask y WTForms para la creación de formularios en Flask, para instalarla haríamos:

```bash
app $ pip install Flask-WTF
```

Una vez instalada esta librería, estamos en posibilidad de crear los diferentes formularios que se requieren. El primero de ellos será el de ingreso a la aplicación (login), para esto creamos el formulario en **src/accounts/forms.py** con el siguiente contenido:

```python
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
```

Como podemos observar, importamos **FlaskForm** para poder hacer el formlario y en la clase es necesario importar los campos **EmailField** y **PasswordField** para poder crear las variables **email** y **password** además, para validar esos campos resulta necesario importar las funciones o métodos **DataRequired()** y **Email()**.

La estructura de directorios hasta el momento quedaría de la siguiente manera:

```bash
.
└── app
    ├── src
    │   ├── accounts
    │   │   ├── forms.py
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   └── views.py
    │   ├── core
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── static
    │   │   ├── css
    │   │   │   └── uagro.css
    │   │   └── images
    │   │       └── logos
    │   │           └── logo.png
    │   ├── templates
    │   │   ├── accounts
    │   │   │   └── login.html
    │   │   ├── core
    │   │   │   └── home.html
    │   │   ├── layout.html
    │   │   └── navbar.html
    │   └── __init.py__
    ├── venv
    ├── config.py
    ├── .env
    ├── .gitignore
    ├── main.py
    └── README.md
```

Ahora, vamos a crear la función que manejará el proceso de ingreso a la aplicación, esto lo hacemos modificando el archivo **src/accounts/views.py** añadiendo el siguiente código:

```python
from flask import Blueprint, render_template, flash, redirect, request, url_for # Modificar esta línea
from flask_login import login_user, current_user # Añadir esta línea
from src import bcrypt, db # Añadir esta línea
from src.accounts.models import User # Añadir esta línea
from forms import LoginForm # Añadir esta línea (el .forms se utiliza porque está en el mismo directorio)


accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ya has iniciado sesión.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Correo y/o Contraseña no válida", "danger")
            return render_template("accounts/login.html", form = form)
    return render_template('accounts/login.html')
```

A continuación explico de manera breve las funciones, objetos y librerías importados en las primeras líneas del código:

- **flash()**: es una herramienta que permite mostrar mensajes temporales a los usuarios de una aplicación web.
- **redirect()**: se utiliza para redirigir a un usuario a una URL específica.
- **request**: se utiliza para acceder a la información de una petición HTTP.
- **url_for**: se utiliza para generar la URL de una vista (ruta) a partir de un nombre y argumentos.
- **login_user()**: función que registra a un usuario como conectado en una aplicación de Flask.
- **LoginForm**: Librería para crear un sistema de inicio de sesión para una aplicación.

**bcrypt**, **db** y **User** ya fueron explicados anteriormente.

La función **login()**, primero verifica si un usuario ya está autenticado usando la propiedad **is_authenticated**. Si lo está, lo redireccionamos a la página de inicio con un mensaje. Si no está autenticado, creamos una instancia del formulario de inicio de sesión. Si el método de solicitud es **GET**, simplemente generamos un archivo **login.html** con el formulario. De lo contrario, se valida el formulario.

Durante la validación, usamos el método **check_password_hash** de la biblioteca **Flask-Bcrypt** para hacer coincidir las contraseñas cifradas. Si las contraseñas coinciden, iniciamos la sesión del usuario usando el método **login_user()** y lo redireccionamos a la página de inicio. De lo contrario, mostramos el mensaje de error ('contraseña y/o password incorrecto') y generamos la misma página HTML para corregir cualquiera de los dos campos o en su caso los dos.

Dado que estamos redireccionando a la página **login.html** dentro de la carpeta **templates/accounts** que ya existe, vamos a modificarla con el siguiente código:

```html
{% extends 'layout.html' %}
<!-- CUSTOM CSS STYLESHEET -->
{% block customSCSS %}
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/uagro.css') }}">
{% endblock %}
<!-- BODY CONTENT -->
{% block content %}
    <form class="form-signin" method="POST" action=""> <!-- action="/login" -->
        {{ form.csrf_token }}
        <div class="container-main">
            <div class="row"> <!-- THE NAME MUST BE: ROW -->
                <div class="col-md-6 side-image">
                    <!-- LEFT SIDE -->
                    <img src="{{ url_for('static', filename='images/logos/escudo_uagro_white.svg') }}" alt="">
                </div>
                <div class="col-md-6 side-inputs">
                    <!-- RIGHT SIDE -->
                    <div class="input-box">
                        <img class="img-center" src="{{ url_for('static', filename='images/logos/cmixta_logo_color_text.svg') }}">
                        <header>Iniciar sesión</header>
                        <!-- LOGIN INPUT-FIELD -->
                        <!--div class="input-field"-->
                        <div class="form-floating">
                            <i class="fa-solid fa-envelope"></i>
                            {{ form.email(placeholder="email", class="form-control mb-2 shadow-none") }}
                            {{ form.email.label }}
                            {% if form.email.errors %}
                                {% for error in form.email.errors %}
                                    <div class="alert alert-danger" role="alert">
                                        {{ error }}
                                    </div>
                                {% endfor %}
                            {% endif %}
                            <!--input class="input" type="text" id="email" name="useremail" required autocomplete="off"-->
                            <!--label for="email">correo electrónico</label-->
                        </div>
                        <!--div class="input-field"-->
                        <div class="form-floating">
                            <i class="fa-solid fa-lock"></i>
                            {{ form.password(placeholder="password", class="form-control mb-2 shadow-none") }}
                            {{ form.password.label }}
                            {% if form.password.errors %}
                                {% for error in form.password.errors %}
                                    <div class="alert alert-danger" role="alert">
                                        {{ error }}
                                    </div>
                                {% endfor %}
                            {% endif %}
                            <!--input class="input" type="password" id="password" name="password" required-->
                            <!--label for="password">contraseña</label-->
                        </div>
                        <div class="input-field">
                            <input type="submit" class="submit" value="Acceder" name="">
                        </div>
                        <div class="forget-password">
                            <span><a href="/">Olvidé mi contraseña</a></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>
{% endblock %}
```

Hasta el momento, la aplicación siempre indicaŕá el mensaje **Correo y/o Contraseña no válida** debido a que nuestra base de datos no contiene datos relacionados con la aplicación así que, resulta necesario crear el registro de usuarios.

### Implementando el registro de usuarios
Para esto, vamos a modificar el formulario que se encuentra en el archivo **src/accounts/forms.py** en la que agregaremos la clase **RegistrationForm** y la función **validate()** para la validación de los datos proporcionados:

```python
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length # Agregar validaciones

from src.accounts.models import User # Agregar línea

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

# Agregamos la clase y la función
class RegisterForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True
```

En este código podemos observar que se han agregado diferentes validadores como **EqualTo** y **Length**. La clase **RegisterForm** tiene tres campos: **email**, **password** y **confirm**, la función **validation()** se llama automáticamente cuando se envía el formulario.

En la función primero realizamos la validación inicial proporcionada por FlaskForm. Si es exitosa, realizamos nuestra validación personalizada, como verificar si el usuario ya está registrado y hacer coincidir la contraseña con la contraseña confirmada, si se produce algún error, agregamos el mensaje correspondiente en los campos respectivos.

Este formulario lo usaremos en  **src/accounts/views.py** para crear una función que gestione el proceso de registro, para esto vamos a agregar el siguiente código:

```python
from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, current_user
from src import bcrypt, db
from src.accounts.models import User
from forms import RegisterForm


accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ya has iniciado sesión.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Correo y/o Contraseña no válida", "danger")
            return render_template("accounts/login.html", form = form)
    return render_template('accounts/login.html')


# Agregamos lo siguiente
@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Ya estás registrado.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Registro exitoso y ya estás en la aplicación. Bienvenido!", "success")

        return redirect(url_for("core.home"))

    return render_template("accounts/register.html", form=form)
```

En la función de **register()** podemos observar que estamos usando el Blueprint para agregar su ruta. Inicialmente, verificamos si un usuario ya está autentificado usando la propiedad **is_authenticated**, de ser así, lo redireccionamos a la página de inicio con un mensaje. Si no está autentificado, primero creamos una instancia de la clase RegisterForm. Si el método de solicitud es GET, generamos un archivo HTML con el formulario. De lo contrario, verificamos si el formulario tiene entradas válidas usando el método **validation_on_submit()**. Si las entradas son válidas, creamos una instancia de la **clase User** con el correo electrónico y la contraseña proporcionados por el usuario y la agregamos a la base de datos. Posteriormente, iniciamos sesión con el usuario usando el método **login_user()** que acepta el objeto de usuario. También mostramos un mensaje de éxito y redireccionamos al usuario a la página de inicio. 

Este formulario se usará dentro del archivo **src/templates/account/register.html** con el siguiente código:

```html
{% extends "layout.html" %}
{% block customSCSS %}
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/uagro.css') }}">
{% endblock %}
<!-- BODY CONTENT -->
{% block content %}
    <form class="form-register" method="post" action="">
        {{ form.csrf_token }}
        <div class="container-main">
            <div class="row">
                <div class="input-box">
                    <img class="img-center" src="{{ url_for('static', filename='images/logos/cmixta_logo_color_text.svg') }}">
                    <header>Registro de usuarios</header>

                    <div class="form-floating">
                        <i class="fa-solid fa-envelope"></i>
                        {{ form.email(placeholder="email", class="form-control mb-2 shadow-none") }}
                        {{ form.email.label }}
                        {% if form.email.errors %}
                            {% for error in form.email.errors %}
                                <div class="alert alert-danger" role="alert">
                                    {{ error }}
                                </div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <div class="form-floating">
                        <i class="fa-solid fa-lock"></i>
                        {{ form.password(placeholder="password", class="form-control mb-2 shadow-none") }}
                        {{ form.password.label }}
                        {% if form.password.errors %}
                            {% for error in form.password.errors %}
                                <div class="alert alert-danger" role="alert">
                                    {{ error }}
                                </div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <div class="form-floating">
                        <i class="fa-solid fa-key"></i>
                        {{ form.confirm(placeholder="Confirm Password", class="form-control mb-2 shadow-none") }}
                        {{ form.confirm.label }}
                        {% if form.confirm.errors %}
                            {% for error in form.confirm.errors %}
                                <div class="alert alert-danger" role="alert">
                                    {{ error }}
                                </div>
                            {% endfor %}
                        {% endif %}
                    </div>
                    <div class="input-field">
                        <input type="submit" class="submit" value="Registrar" name="">
                    </div>
                </div>
            </div>
        </div>
    </form>
{% endblock %}
```

Al correr la aplicación y utilizar el registro de usuarios, se genera un error: **TypeError: RegisterForm.validate() got an unexpected keyword argument 'extra_validators'**, la forma de resolverlo es modificar el archivo **src/accounts/forms.py** de la siguiente manera:

```python
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

import email_validator

from src.accounts.models import User

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, extra_validators = None): # Modificar esta línea
        initial_validation = super(RegisterForm, self).validate(extra_validators) # Modificar esta línea
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True
```

Toda vez realizada esta modificación, es posible iniciar sesión o bien agregar usuarios a la aplicación. Ahora, debemos agregar la posibilidad de salir de la aplicación para esto, agregamos a **src/accounts/views.py** la función que permite hacerlo, ver las líneas modificadas y la función agregada:

```python
from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, current_user, logout_user, login_required # Modificar esta línea
from src import bcrypt, db
from src.accounts.models import User
from forms import RegisterForm


accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ya has iniciado sesión.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Correo y/o Contraseña no válida", "danger")
            return render_template("accounts/login.html", form = form)
    return render_template('accounts/login.html')


@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Ya estás registrado.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Registro exitoso y ya estás en la aplicación. Bienvenido!", "success")

        return redirect(url_for("core.home"))

    return render_template("accounts/register.html", form=form)

# Agregar esta función
@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado tu sesión", "success")
    return redirect(url_for("accounts.login"))
```

La biblioteca Flask-Login contiene un método logout_user que elimina al usuario de la sesión. Usamos el decorador @login_required para que solo los usuarios autentificados puedan cerrar sesión.

### Olvidé la contraseña
En esta sección voy a incluir una función de cambio de contraseña para los usuarios que la olvidan (La opción se encuentra al final del archivo **login.html**) así como se muestra en el siguiente código: 

```html
<div class="forget-password">
    <span><a href="{{ url_for('accounts.forgot_password') }}">Olvidé mi contraseña</a></span>
</div>
```

Cuando esto sucede, el usuario inicia una solicitud de cambio de contraseña mediante una página web y la aplicación se encargará de enviar a su correo electrónico con un enlace al que deberá dar click para tener acceso a otra página en la que podrá cambiarla. Para esto, vamos hacer lo siguiente:

Modificar el archivo **src/accounts/forms.py** agregando la clase **forgotForm** en la que vamos a definir los datos involucrados para inicial el proceso, en este caso solamente será el correo electrónico del usuario y un botón para el envío de la solicitud de cambio de contraseña:

```python
from wtforms import EmailField, PasswordField, SubmitField  # <-- Modificar esta línea 

# Agregar esta clase
class ForgotForm(FlaskForm):
    email = EmailField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar solicitud')
```

Necesitamos además crear una página html en la que se pueda interactuar con estos datos que acabamos de definir: la captura del correo electrónico del usuario en cuentión y un botón de envío para iniciar el proceso de cambio de la cotraseña:

```html
{% extends 'layout.html' %}
<!-- CUSTOM CSS STYLESHEET -->
{% block customSCSS %}
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/uagro.css') }}">
{% endblock %}
{% block content %}
    <form class="form-reset-pw-req" method="POST" action="">
        <!-- {{ form.crsf_token }} -->
        {{ form.hidden_tag() }}
        <div class="container-main">
            <div class="row">
                <div class="input-box">
                    <img class="img-center" src="{{ url_for('static', filename='images/logos/cmixta_logo_color_text.svg') }}">
                    <header>Solicitud para cambio de contraseña</header>
                    <!-- USER EMAIL CAPTURE -->
                    <div class="form-floating">
                        {{ form.email(placeholder="email", class="form-control mb-2 shadow-none") }}
                        {{ form.email.label }}
                        {% if form.email.errors %}
                            {% for error in form.email.errors %}
                                <div class="alert alert-danger" role="alert">
                                    {{ error }}
                                </div>
                            {% endfor %}
                        {% endif %}
                    </div>
                    <!-- SUBMIT BUTTON -->
                    <div class="input-field">
                        <p>{{ form.submit() }}</p>
                    </div>
                </div>
            </div>
        </div>
    </form>
{% endblock %}
```

Ahora debemos saber que hacer con estos datos así que, debemos crear la ruta donde se alojará la página html relativa al proceso de solicitud de cambio de contraseña, así como escribir el código de la función que va a controlar este proceso. El diagrama de flujo sería el siguiente:

```mermaid
flowchart TD
    forgot(forgot password page) --> q1{is user authenticated?} 
    q1 --> |no| form[form = ForgetForm]
    q1 --> |yes| login[login page]
    form --> q2{form validate on submit?}
    q2 --> |no| forgot
    q2 --> |yes| consult[get user.email, sql user.db]
    consult --> q4{user.email == user.db?}
    q4 --> |no| msg[msg: wrong user.email]
    q4 --> |yes| send[send_email]
    send --> login
    msg --> forgot
```


Esta función primero se va asegurar que el usuario no esté autentificado, enseguida llamamos el formulario **ForgotForm** que acabamoms de crear en el proceso anterior para utilizar los datos que definimos en ella, verificamos que el formulario haya sido enviado para validar los datos introducidos (en este caso solo el email del usuario), si se verifica el formulario, se compara el correo electrónico introducido por el usuario en la plantilla html con alguno existente en la base de datos, si son iguales, el usuario de la aplicación existe y entonces, se manda un correo electrónico a esa dirección donde se enviará un enlace para poder restablecer su contraseña. Si no coinciden los correos, lo deja en la misma página para corregirlo en caso de haberlo escrito mal. El código lo vamos a incluir en el archivo **src/accounts/views.py**.  de la siguiente manera:

```python
from .forms import LoginForm, RegisterForm, ForgotForm #<-- Agregamos el formulario que acabamos de crear
import sqlalchemy as sqla #<-- Agregamos esta para poder realizar consultas a la BD

# Agregamos la ruta hacia la plantilla forgot_password.html y la función que controla el proceso de cambio de contraseña
@accounts_bp.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("accounts.home"))
    form = ForgotForm(request.form)
    if form.validate_on_submit():
        user = db.session.scalar(
            sqla.select(User).where(User.email == form.email.data) # Si el email proporcionado se encuentra en la base de datos
        )
        if user:
            print(user)
            send_password_reset_email(user) # <-- Función para enviar el email al usuario
            flash(
                'Revise su correo electrónico y siga las instrucciones para reestablecer su contraseña.')
            return redirect(url_for('accounts.login'))
        flash('El correo no está registrado, verifique que esté bien escrito.')
    return render_template("accounts/forgot_password.html", title="Solicitud: Cambio de contraseña", form=form)
```

En este código existe una función para enviar un correo al usuario para de solicitud de cambio de contraseña  (**send_password_reset_email(user)**), pero antes de escribir el código, es importante instalar la siguiente librería:

- **Flask-Mail**: facilita el envío de correos electrónicos desde la aplicación que estamos creando en Flask

para instalarla:

```bash
app $ pip install flask-mail
```

Para comprender más sobre el tema, te recomiendo el siguiente tutorial: [Tutorial Flask – Lección 14: Enviar emails con Flask](https://j2logo.com/tutorial-flask-leccion-14-enviar-emails-con-flask/).

Toda vez instalada, vamos a configurarla con un servidor de correos electrónicos, en este ejemplo lo haremos con **Gmail** (por el momento he creado una cuenta nueva, los datos de ésta se muestran a continuación). Para esto, modificaremos el archivo donde almacenamos nuestras variables de ambiente **.env** y agregamos la siguiente información:

~~~bash
# Agregamos las siguientes variables
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 465
MAIL_USERNAME = cmixtauagro@gmail.com
MAIL_PASSWORD = {cmixtauagro2024}
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = 0
~~~

y las incluimos en el archivo de configuración de la aplicación **config.py**, dado que las variables que define el puerto del mail y el debug del mail deben ser enteros debemos hacer un cast:

~~~python
class Config(object):

    # Agregar variables de Flask-Email
    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = int(config('MAIL_PORT'))  # <-- Convertimos de string a int
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    MAIL_USE_TLS = config('MAIL_USE_TLS')
    MAIL_USE_SSL = config('MAIL_SSL')
    MAIL_DEBUG = int(config('MAIL_DEBUG'))  # <-- Convertimos de string a int
~~~

Estas configuraciones nos permiten definir el servidor de Mail. Pero para utilizar el servidor de Gmail y poder enviar correos, debemos configurarlo para admitir este tipo de solicitudes desde nuestra aplicación FLASK de lo contrario, nos enfrentaremos a problemas de seguridad que Gmail tomará como medida preventiva así que, vamos a configurar nuestra cuenta de correo. Primero vamos a activar la **verificación en dos pasos**, en [este enlace](https://support.google.com/accounts/answer/185839)  obtendremos información de cómo hacerlo, esto es necesario por que debemos establecer una contraseña para utilizar **aplicaciones externas** que es el segundo paso. Para esto, desde la página de configuración - seguridad, verás el dispositivo desde el que te estás conectando, te solicitará el correo electrónico que acabas de crear y te mostrará un password de 16 dígitos que deberás de sustituir en el archivo **.env** en la variable: **MAIL_PASSWORD =**. Es importante aclarar que esta contraseña es para la aplicación flask, para revisar el correo electrónico seguiremos utilizando el primer password que definimos cuando la creamos.

Debemos tambien incluir la librería Flask-Mail en el archivo **\_\_init\_\_.py** que es donde inicia la aplicación. Para que las variables que hemos definido puedan ser reconocidas y poder enviar los correos electrónicos, es importante aclarar que se debe incluir la librería despues de que se ha configurado la aplicación, así que debe quedar de la siguiente manera:

~~~python
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail # <-- Incluir esta línea


def init_app(app_settings):
    global bcrypt, db, mail, app
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(app_settings) # <-- configuración de la app

    mail = Mail(app) # <-- aquí va la config del mail
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    bcrypt = Bcrypt(app)
    db = SQLAlchemy(app)

    # Register Blueprints
    from src.core.views import core_bp
    app.register_blueprint(core_bp)
    from src.accounts.views import accounts_bp
    app.register_blueprint(accounts_bp)

    from src.accounts.models import User

    login_manager.login_view = "accounts.login"
    login_manager.login_message_category = "danger"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    return app

~~~

#### Función send_password_reset_email(user)
Toda vez instalado y configurado todo lo referente a la librería flask-email, estamos en posibilidad de crear la función  **send_password_reset_email(user)** que se llama desde el archivo **src/accounts/views.py** en la función **forgot_password**. Podríamos crear la función en el archivo **views.py** sin embargo, para darle orden a la aplicación, la he creado en un archivo adicional en la siguiente ruta **src/accounts/email.py** en donde crearemos las funciones relacionadas con el envío de correos a los usuarios. Antes de escribir el código, es necesario entender como se envía un correo con la librería flask-mail. La forma en que se hace es creando un objeto **Message** y llamar al método **send()** de la variable **mail** que ya hemos creado en el archivo **\_\_init\_\_.py**, pasando el **mensaje** que queremos enviar como parámetro de este método.

Para crear este mensaje, necesitamos indicar el asunto, la dirección de correo del emisor y la dirección de correo del destinatario, el contenido del mensaje en texto y/o un mensaje formateado en html, todos a manera de lista, ej:

```python
message = Message(asunto, emisor, destinatario)
message.body = texto_plano_del_correo
message.html = texto_formateado_en_html
send (message)
```

Ahora si vamos a crear la función **send_password_reset_email(user)** en el archivo **src/accounts/email.py**, en la que unicamente definiremos cada uno de estos parámetros:

```python
from flask import render_template
from src import app

def send_password_reset_email(user):
    token = user.get_reset_password_token() # <-- Función a llamar
    # Función send_email()
    send_email('[CMPAyP UAGro] Solicitud de cambio de contraseña', # <-- asunto (Subject)
               sender=app.config['MAIL_USERNAME'], # <-- emisor (sender)
               recipients=[user.email], # <-- destinatario (recipients)
               text_body=render_template(
                   'accounts/email/reset_password.txt', user=user, token=token),  # <-- texto no formateado del correo
               html_body=render_template(
                   'accounts/email/reset_password.html', user=user, token=token) # <-- texto en formato html del correo
               )
```

Como podemos observar en el código, existe la variable **token** que llama a la función **get_reset_password_token()**, la función **send_mail()** para enviar el correo electrónico y la creación de los archivos: **reset_password.txt** y **reset_password.html** referentes al cuerpo del correo en texto plano y en formato html. Hablemos de estos útimos que los vamos a crear en el directorio **src/templates/accounts/email**, el primero de ellos tendría el siguiente contenido (observar que utilizamos variable de python de acuerdo con la librería jinJa2):

```bash
Estimado {{ user.email }}

De click en el siguiente enlace para cambiar su contraseña:

{{ url_for('accounts.reset_password', token=token, _external=True) }}

Si no has solicitado un cambio de contraseña, ignora este mensaje.

Atentamente,

Comisión Mixta Paritaria de Admisión y Promoción.
```

respecto al segundo archivo en formato html, el contenido sería el siguiente:

```html
<!doctype html>
<html>
    <body>
        <p>Estimado {{ user.email }},</p>
        <p>
            Para cambiar tu password
            <a href="{{ url_for('accounts.reset_password', token=token, _external=True) }}">
                da click aquí.
            </a>.
        </p>
        <p>Alternativamente, puedes copiar y pegar el siguiente enlace en la barra de navegación de tu visualizador de internet:</p>
        <p>{{ url_for('accounts.email.reset_password', token=token, _external=True) }}</p>
        <p>Si no has solicitado un cambio de password, ignora este mensaje.</p>
        <p>Atentamente,</p>
        <p>[CMPAyP] Comisión Mixta Paritaria de Admición y Promoción</p>
    </body>
</html>

```

Respecto a la variable **token**, el correo electrónico que se envía al usuario, contiene un enlace para reestablecer la contraseña y con la idea de hacer que esto sea más seguro, resulta necesario crear un token de seguridad, este token es un código aleatorio que se genera para acceder a un recurso restringido o para validar la identidad de un usuario y que tiene una duración definida. Para hacer esto utilizaremos tokens web JSON:

- **[pyjwt](https://pyjwt.readthedocs.io/en/stable/)**: librería de Python que permite codificar y decodificar tokens web JSON (JWT) de manera sencilla, dicho de otra manera, permite transmitir información segura entre las partes involucradas, ya que se pueden firmar utilizando un par de claves públicas/privadas. Esto permite estar seguro de que el remitente es quien dice ser. Así que vamos a instalar esta librería:

~~~bash
app $ pip install pyjwt
~~~

Entonces, dado que el **token** se obtiene de la función **get_reset_password_token()** y se genera para un usuario específico, debe crearse en el archivo **src/accounts/models.py** así que vamos a agregar las líneas y función siguientes:

```python
import jwt # <-- Agregar esta librería para codificar el token
from time import time # <-- Agregar esta librería para determinar el tiempo de duración del token

# Agregar esta función
def get_reset_password_token(self, expires_in=600):
    return jwt.encode(
        {'reset_password': self.id, 'exp': time() + expires_in},
        app.config['SECRET_KEY'], algorithm='HS256'
    )
```

Lo que hace la función es generar un token (código aleatorio) con base a la información del usuario, el tiempo de expiración del enlace que hemos definido en los parámetros de la función, la clave secreta definida en las variables de ambiente (**.env**) utilizando un algoritmo de firma. Para conocer y comprender un poco más sobre el tema, puedes leer el siguiente tutorial [Autenticación en Python con JSON Web tokens y Flask](https://medium.com/@diego.coder/autenticaci%C3%B3n-en-python-con-json-web-tokens-y-flask-9f486bc88782).

La función **send_mail()**, se encargará de enviar el correo al usuario utilizando los parámetros generados en la función que la llama, de acuerdo con la sintaxis anteriormente mencionada respecto al envío de correo electrónico con flask-mail. Vamos a incluir la función **send_mail()** en el mismo archivo **email.py** y se debe definir antes de la función que la llama así que, modificamos agregando la siguiente línea y función:

```python
from flask_mail import Message # <-- importamos el método Message 

# Agregamos esta función para enviar el correo utilizando los parámetros generados én la función anterior
def send_email(subject, sender, recipients, text_body, html_body):
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.html = html_body
    Thread(target=send_async_email, args=(app, message)).start()
```

El problema de envíar correos electrónicos de esta manera, es que el envío se realiza de forma síncrona es decir,  en el mismo hilo en el que se procesa la solicitud de cambio de contraseña al precional el botón en la página web, y de acuerdo con la documentación del flask-email es mejor hacerlo de manera asíncrona. Para lograr esto, vamos a crear otra función más para que el correo se ejecute en un hilo diferente, de manera que el envío del correo no bloquee el flujo de la petición. Entonces vamos a incluir una línea y la función **send_async_email()** en el mismo aechivo **email.py** pero antes de la función que la manda llamar quedando parcialmente de la siguiente manera:

```python
from threading import Thread # <-- importar esta librería para el manejo de hilos
from src import mail, app # <-- importar la app para dar seguimiento de los datos a ejecutar


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
```

Para comprender más sobre el tema del contexto de las aplicaciones flask, recomiendo leer el siguiente aŕtículo: [Deep Dive into Flask's Application and Request Contexts](https://testdriven.io/blog/flask-contexts-advanced/).

Finalmente escribimos el estilo correspondiente a la página **forgot_password.html** en el archivo: **src/static/css/uagro.css**):

```css
/** FORGOT STYLE **/
.form-forgot {
    background: var(--white);
    padding: 0 20px 0 20px;

    .container-main {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;

        .row {
            width: 550px;
            height: 350px;
            background: var(--white);
            border-radius: 10px;
            box-shadow: 5px 5px 10px 1px rgba(0, 0, 0, 0.3);

            .input-box {
                width: 550px;
                box-sizing: border-box;

                .img-center {
                    display: block;
                    width: 65%;
                    margin-left: auto;
                    margin-right: auto;
                    padding-top: 20px;
                    padding-bottom: 40px;
                }

                header {
                    font-size: 20px;
                    font-weight: 600;
                    text-align: center;
                    margin-bottom: 30px;
                }

                .form-floating {
                    display: flex;
                    flex-direction: column;
                    position: relative;
                    padding: 0 10px 0 10px;

                    i {
                        position: absolute;
                        top: 17px;
                        left: 478px;
                        font-size: 22px;
                        color: var(--gray-dark);
                        transition: 0.5s;
                    }

                    .form-control {
                        height: 45px;
                        width: 100%;
                        border: none;
                        border-bottom: 1px solid rgba(0, 0, 0, 0.2);
                        outline: none;
                        margin-bottom: 20px;
                        color: var(--black);
                    }

                    label {
                        position: absolute;
                        top: 0px;
                        left: 10px;
                        pointer-events: none;
                        color: var(--gray-dark);
                        transition: 0.5s;
                    }

                    input:focus ~ label {
                        top: -12px;
                        font-size: 15px;
                        color: var(--black);
                    }

                    input:valid ~ label {
                        top: -12px;
                        font-size: 15px;
                        color: var(--black)
                    }
                }

                .input-field {
                    display: flex;
                    flex-direction: column;
                    position: relative;
                    padding: 5px 10px 0px 10px;

                    .submit {
                        height: 45px;
                        border: none;
                        border-radius: 5px;
                        background: var(--gray-light);
                        transition: 0.4s;
                    }

                    .submit:hover {
                        background: var(--blue-dark);
                        color: var(--white);
                    }
                }
            }
        }
    }
}
```

quedando como se muestra en el imagen:

![](src/static/images/app/fig_004.png)

El correo electrónico enviado al usuario, en este ejemplo lo envié al mío (erodriguez@uagro.mx), se mostraría de la siguiente manera:

![](src/static/images/app/fig_005.png)

Necesitamos ahora crear la página para hacer el cambio de password


























