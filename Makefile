migrate:
	touch .env
	python manage.py makemigrations
	python manage.py migrate

run_dev:
	python manage.py runserver  --settings=tabletop_backend.settings.development

run_prod:
	python manage.py runserver 0.0.0.0:8000

run_ut:
	coverage erase
	coverage run manage.py test
	coverage report

init_data:
	python manage.py initgroups
	python manage.py initadmin
	python manage.py initadyenuser
	python manage.py initdemouser

deploy:
	eb deploy --label `git rev-parse HEAD`

run_pylint:
	pylint --ignore=static --ignore=templates */
