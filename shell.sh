source ../coffeeshopenv/bin/activate
cd backend/
export FLASK_APP=api.py;
export FLASK_ENV=development # enables debug mode
flask shell
