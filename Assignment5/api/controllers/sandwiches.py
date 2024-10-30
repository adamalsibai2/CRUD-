from sqlalchemy.orm import Session
from fastapi import HTTPException

# Adjust the import statements according to your project structure
from ..models import models, schemas


def create(db: Session, sandwich: schemas.SandwichCreate):
    db_sandwich = models.Sandwich(
        name=sandwich.name,
        description=sandwich.description,
        price=sandwich.price
    )
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich


def read_all(db: Session):
    return db.query(models.Sandwich).all()


def read_one(db: Session, sandwich_id: int):
    return db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()


def update(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate):
    db_sandwich = read_one(db, sandwich_id=sandwich_id)
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    update_data = sandwich.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sandwich, key, value)

    db.commit()
    return db_sandwich


def delete(db: Session, sandwich_id: int):
    db_sandwich = read_one(db, sandwich_id=sandwich_id)
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    db.delete(db_sandwich)
    db.commit()
    return {"detail": "Sandwich deleted"}


