#Create 10 users
import os

import crud
import model
import server

os.system("dropdb fair_play")
os.system("createdb fair_play")

with server.app.app_context():
    model.connect_to_db(server.app)
    model.db.create_all()

    for n in range(10):
        email = f"user{n}@test.com"
        password = "test"
        user = crud.create_user(email, password)
        model.db.session.add(user)

    model.db.session.commit()