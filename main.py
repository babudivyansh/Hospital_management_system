"""
@Author: Divyansh Babu

@Date: 2024-03-08 14:37

@Last Modified by: Divyansh Babu

@Last Modified time: 2024-03-09 11:46

@Title : Hospital Management app using Sanic and Mongodb.
"""
from sanic import Sanic
from Routes.doctors import app as dr
from Routes.departments import app as di
from Routes.patient import app as pr


app = Sanic(__name__)

app.blueprint(dr)
app.blueprint(di)
app.blueprint(pr)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
