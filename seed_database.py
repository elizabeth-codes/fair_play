#Create 10 users
import crud
import model
import server

model.connect_to_db(server.app)
model.db.create_all()

for n in range(10):
    email = f"user{n}@test.com"
    password = "test"
    print('asdfasdf')
    user = crud.create_user(email, password)
    model.db.session.add(user)

model.db.session.commit()