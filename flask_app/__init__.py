from flask import Flask

app = Flask(__name__)
if app.config.get("ENV") == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config.get("ENV") == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

from flask_app import views