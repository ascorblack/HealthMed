python /app/manage.py makemigrations
python /app/manage.py migrate
while true
do
  cd /app/ && gunicorn healthmed.wsgi --bind 0.0.0.0:8000
  sleep 2
done