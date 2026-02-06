from flask import Flask
from .config import Config
from .routes import auth_bp, product_bp
from .cli.product_seed_cli import product_seed

def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.cli.add_command(product_seed)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    
    return app