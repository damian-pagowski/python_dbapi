from flask import Flask

app = Flask(__name__)

# @app is called decorator
# prenaunciation [raut]
# running app: FLASK_APP=hello_app.py flask run
# FLAG=value this is called flag, have to be declared with = without spaces
# export FLASK_ENV=development
# 

@app.route('/')
def index():
    return "hello from %s" % "APP"


if __name__ == '__main__':
    app.run()