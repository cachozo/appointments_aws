from flask import Flask

app = Flask(__name__)


app.secret_key = "Esta es mi llave super secreta"