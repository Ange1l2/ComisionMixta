from config import config
from src import init_app

app_settings = config['development']
app = init_app(app_settings)

if __name__ == '__main__':
    app.run()  # Es por eso que utilizamos DEBUG y no FLASK_DEBUG
