lint:
	ls *.py */**.py | xargs -n1 pep8

autolint:
	ls *.py */**.py | xargs -n1 autopep8 -i

test:
	py.test tests/

run:
	python -B app.py

production-run:
	touch .env && gunicorn app:app --log-file=-

heroku:
	git push heroku master
