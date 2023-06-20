#Create 10 users
import datetime
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
        #user_id = n
        user = crud.create_user(email, password)
        model.db.session.add(user)

    model.db.session.commit()



    # task_id = 11
    task_name = "wash the dishes"
    task_description = "load dishwasher & hand wash bigger dishes"
    # general_task = crud.create_general_task(task_id, task_name, task_description)
    general_task = crud.create_general_task(task_name, task_description)
    model.db.session.add(general_task)
    model.db.session.commit()

    for n in range(10):
        #assigned_task_id = n
        was_on_time = True
        active_status = True
        assigned_to = n 
        completed_date = datetime.datetime(2023, 6, 14)
        # task_id = 0
        print('booasdfuasd: ', general_task.task_id)
        task_id = general_task.task_id 
        assigned_task = crud.create_assigned_task(was_on_time, active_status, assigned_to, completed_date, task_id)
        model.db.session.add(assigned_task)
    model.db.session.commit()




    

