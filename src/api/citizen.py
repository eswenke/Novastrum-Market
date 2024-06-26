from fastapi import APIRouter, Depends
from src.api import auth
from src import database as db
import sqlalchemy
from pydantic import BaseModel
import time

cit_id = -1

router = APIRouter(
    prefix="/citizen",
    tags=["citizen"],
    dependencies=[Depends(auth.get_api_key)],
)

class Citizen(BaseModel):
    username: str
    password: str # update to use hashing
    role: str
    planet: str
    

@router.post("/create")
def new_user(cit: Citizen):

    # If a user already exists nothing is inserted

    begin = time.time() 

    with db.engine.begin() as connection:
        # First, check if the username already exists
        existing_citizen = connection.execute(sqlalchemy.text(
            """
            SELECT id FROM citizens WHERE name = :name
            """
        ), {"name": cit.username}).fetchone()

        # If the username does not exist, insert the new citizen
        if existing_citizen is None:
            id = connection.execute(sqlalchemy.text(
                """
                INSERT INTO citizens (name, password, role, planet) VALUES (:name, :password, :role, :planet)
                RETURNING id
                """
            ), {"name": cit.username, "password": cit.password, "role": cit.role, "planet": cit.planet}).scalar_one()
        else:
            return "ERROR: Username already exists. Choose a new username."
        
        connection.execute(sqlalchemy.text(
                """
                INSERT INTO inventory (citizen_id, quantity, type) VALUES (:citizen_id, 100, 'voidex')
                """
            ), {"citizen_id": id})
        
    end = time.time() 
    print(f"Total runtime of the program is {1000 * (end - begin)} ms") 

    return "OK: User successfully created. Log into account."

@router.post("/login")
def login(username: str, password: str):
    global cit_id
    global role

    begin = time.time() 

    with db.engine.begin() as connection:
        cit_id = connection.execute(sqlalchemy.text(
            """
            SELECT id
            FROM citizens
            WHERE name LIKE :name AND password LIKE :password
            LIMIT 1
            """
            ), [{"name": username, "password": password}]).scalar()
        
        if cit_id == None:
            return "ERROR: Incorrect username or password."
        
        role = connection.execute(sqlalchemy.text(
            """
            SELECT role
            FROM citizens
            WHERE name LIKE :name AND password LIKE :password
            LIMIT 1
            """
            ), [{"name": username, "password": password}]).scalar()
    print(cit_id)

    end = time.time() 
    print(f"Total runtime of the program is {1000 * (end - begin)} ms") 

    return f"OK: Successfully logged in. Welcome to the NovaStrum Market, {username}!"

@router.post("/logout")
def logout():
    global cit_id

    begin = time.time() 

    if cit_id == -1:
        return "ERROR: Cannot logout, not logged in"
    else:
        cit_id = -1

        end = time.time() 
        print(f"Total runtime of the program is {1000 * (end - begin)} ms") 

        return "OK: Successfully logged out."