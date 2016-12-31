test:
	py.test tests/

run:
	python -B app.py

production-run:
	touch .env && gunicorn app:app --log-file=-
