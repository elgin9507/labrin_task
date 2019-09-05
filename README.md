### After cloning this repo, run the commands in following order to start the app:


    python3 -m venv env
    
    source env/bin/acticate
    
    pip install -r requirements.txt
    
    docker-compose up -d
    
    python manage.py makemigrations && python manage.py migrate
    
    python manage.py runserver
    
    celery -A labrin_task worker -l info
