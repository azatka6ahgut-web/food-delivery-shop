from sqlalchemy.orm import Session

from . import models

INITIAL_PRODUCTS = [
    {"name": "Молоко 3.2%, 1л", "description": "Свежее пастеризованное молоко", "price": 89.0, "category": "dairy", "image_url": "", "stock_quantity": 50},
    {"name": "Хлеб бородинский", "description": "Ржаной хлеб, 400г", "price": 65.0, "category": "bakery", "image_url": "", "stock_quantity": 40},
    {"name": "Яблоки Гала, 1кг", "description": "Свежие яблоки", "price": 129.0, "category": "fruits", "image_url": "", "stock_quantity": 60},
    {"name": "Куриное филе, 1кг", "description": "Охлаждённое куриное филе", "price": 349.0, "category": "meat", "image_url": "", "stock_quantity": 30},
    {"name": "Сыр Российский, 200г", "description": "Твёрдый сыр", "price": 159.0, "category": "dairy", "image_url": "", "stock_quantity": 25},
    {"name": "Гречка, 900г", "description": "Крупа гречневая ядрица", "price": 99.0, "category": "grocery", "image_url": "", "stock_quantity": 70},
    {"name": "Бананы, 1кг", "description": "Спелые бананы", "price": 79.0, "category": "fruits", "image_url": "", "stock_quantity": 80},
    {"name": "Вода питьевая, 1.5л", "description": "Негазированная вода", "price": 45.0, "category": "drinks", "image_url": "", "stock_quantity": 100},
]


def seed_products(db: Session) -> None:
    if db.query(models.Product).count() > 0:
        return
    for item in INITIAL_PRODUCTS:
        db.add(models.Product(**item))
    db.commit()
