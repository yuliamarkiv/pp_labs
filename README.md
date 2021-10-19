# pp_labs

TO Install :
1. cd pp_labs
2. poetry shell
3. poetry install
4. gunicorn --workers=4 --bind=127.0.0.1:5000 wsf:app
