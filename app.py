from flask import Flask
from src import make_app


app = make_app()
app.run(host='0.0.0.0', port=5000)

