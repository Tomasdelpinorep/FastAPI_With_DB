import json
from typing import Optional

from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Person(BaseModel):
    name: str
    age: int
    gender: str


PEOPLE = []


@app.get('/people/{p_id}', status_code=200)
def get_person(p_id: int, db:Session = Depends(get_db)):
    person = db.query(models.PersonDB).filter(models.PersonDB.id == p_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    else:
        return person

# @app.get("/search", status_code=200)
# def get_people_by_age_and_name(age: Optional[int] = Query(None, title="Age", description="The age to filter for"),
#                                name: Optional[str] = Query(None, title="Name", description="The name to filter for")):
#     people1 = [p for p in people if p['age'] == age]
#
#     if name is None:
#         if age is None:
#             return people
#         else:
#             return people1
#     else:
#         people2 = [p for p in people if name.lower() in p['name'].lower()]
#         if age is None:
#             return people2
#         else:
#             combined = [p for p in people1 if p in people2]
#             return combined


@app.post("/addPerson", status_code=201)
def add_person(person: Person, db: Session = Depends(get_db)):

    person_model = models.PersonDB()
    person_model.gender = person.gender
    person_model.age = person.age
    person_model.name = person.name

    db.add(person_model)
    db.commit()

    return person


# @app.put("/edit/{p_id}", status_code=200)
# def edit_person(person: Person):
#     new_person = {
#         "id": person.id,
#         "name": person.name,
#         "age": person.name,
#         "gender": person.gender
#     }
#
#     person_list = [p for p in people if p['id'] == person.id]
#     if len(person_list) > 0:
#         people.remove(person_list[0])
#         people.append(new_person)
#
#         with open('people.json', 'w') as file:
#             json.dump(people, file)
#
#         return new_person
#     else:
#         return HTTPException(status_code=404, detail=f"Person with id {person.id} does not exist.")


# @app.delete("/delete/{p_id}", status_code=204)
# def delete_person(p_id: int):
#     person = [p for p in people if p['id'] == p_id]
#     if len(person) > 0:
#         people.remove(person[0])
#
#         with open("people.json", "w") as file:
#             json.dump(people, file)
#     else:
#         return HTTPException(status_code=404, detail=f"Person with id {p_id} does not exist.")
