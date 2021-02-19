source ../coffeeshopenv/bin/activate
cd backend/src/
export FLASK_APP=api.py;
export FLASK_ENV=development # enables debug mode
flask run --host=192.168.1.10 --reload
