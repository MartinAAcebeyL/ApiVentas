run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	python manage.py test

coverage:
	coverage run --source='.' manage.py test
	coverage report
	coverage html

createsuperuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

flush:
	python manage.py flush

seed_products_categories_stocks:
	python manage.py seed_categories