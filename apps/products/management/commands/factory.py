from apps.products.models import Category, Product, Stock, HistoryPrice
from faker import Faker
import random


fake = Faker()


def create_history_price(price, product):
    """Create fake history prices"""
    return HistoryPrice(product=product, price=price).save()


def create_product(amount: int = 10):
    """Create fake products"""

    def create_single_product():
        price = fake.pydecimal(2, 2, True)
        product = Product(
            name=fake.name(),
            description=fake.text(),
            weight=random.randint(1, 10),
            price=price,
            minimum_stock=random.randint(1, 50),
        )
        random_category = random.choice(Category.objects.all())
        product.category = random_category
        product.save()
        create_history_price(price, product)
        return product

    if amount == 1:
        return create_single_product()

    for _ in range(amount):
        create_single_product()


def create_category(amount: int = 5):
    """Create fake categories"""
    CATEGORIES = [
        "Celulares",
        "Computadoras",
        "Televisores",
        "Relojes",
        "Audifonos",
    ]

    def create_single_category():
        category = CATEGORIES.pop(random.randint(0, len(CATEGORIES) - 1))
        return Category(name=category, description=fake.text()).save()

    if amount == 1:
        return create_single_category()

    for _ in range(amount):
        create_single_category()


def create_stock(amount: int = 10):
    """Create fake stock"""

    def create_single_stock():
        stock = Stock(
            quantity=random.randint(500, 1000),
            current_quantity=random.randint(1, 500),
        )
        randon_product = random.choice(Product.objects.all())
        stock.save()
        stock.product.set([randon_product])
        return stock

    if amount == 1:
        return create_single_stock()

    for _ in range(amount):
        create_single_stock()