from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth 

db = SQLAlchemy()
jwt = JWTManager()
oauth = OAuth()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)
    
    print(app.config.get("GOOGLE_CLIENT_ID"))
    print(app.config.get("GOOGLE_CLIENT_SECRET"))
    
    oauth.register(
        name = "google",
        client_id = app.config["GOOGLE_CLIENT_ID"],
        client_secret = app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
                     'scope': 'openid email profile https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read'
               }
    )


    blacklist = set()
    app.blacklist = blacklist

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header,jwt_payload):
        jti = jwt_payload["jti"]
        return jti in app.blacklist

    from app.routes import main
    app.register_blueprint(main)
    return app