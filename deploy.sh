#!/bin/sh
echo "START: Changes detected on master, redeploying..."
. venv/bin/activate
sudo git pull origin master
sudo pip install -r requirements.txt

cd thesite/
echo "Updating DB..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

echo "Restarting Gunicorn server..."
pkill "python -m gunicorn"
python -m gunicorn -c config/gunicorn/prod.py

echo "Restarting Nginx..."
sudo systemctl restart nginx

cd ..
echo "DONE: Changes on master applied."

