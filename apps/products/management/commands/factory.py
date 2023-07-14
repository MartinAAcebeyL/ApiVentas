from apps.products.models import Category, Product, Stock, HistoryPrice
from faker import Faker
import random


fake = Faker()


def create_history_price(price, product):
    """Create fake history prices"""
    return HistoryPrice.objects.create(
        product=product,
        price=price
    )


def create_product(amount: int = 10):
    """Create fake products"""
    def create_single_product():
        price = fake.pydecimal(2, 2, True)
        product = Product.objects.create(
            category=random.choice(Category.objects.all()),
            name=fake.name(),
            description=fake.text(),
            weight=random.randint(1, 10),
            price=price
        )
        product.save()
        create_history_price(price, product).save()
        return product

    if amount == 1:
        product = create_single_product().save()
        return product

    for _ in range(amount):
        create_single_product().save()


def create_category(amount: int = 10):
    """Create fake categories"""
    CATEGORIES = [
        "Celulares",
        "Computadoras",
        "Televisores",
        "Relojes",
        "Audifonos",
    ]

    def create_single_category():
        category = CATEGORIES.pop(random.randint(0, len(CATEGORIES)-1))
        return Category.objects.create(
            name=category,
            description=fake.text()
        )

    if amount == 1:
        category = create_single_category().save()
        return category

    for _ in range(amount):
        create_single_category().save()


def create_stock(amount: int = 10):
    """Create fake stock"""

    def create_single_stock():
        return Stock.objects.create(
            product=random.choice(Product.objects.all()),
            quantity=random.randint(1, 1000)
        )

    if amount == 1:
        stock = create_single_stock().save()
        return stock

    for _ in range(amount):
        create_single_stock().save()
