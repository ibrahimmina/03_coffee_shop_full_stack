import os
import http.client
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin
import json

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
db = setup_db(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    return response

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
@cross_origin()
def get_drinks():
    drinkslist = []
    drinks = Drink.query.all()
    if len(drinks) == 0:
        abort(404)
    for drink in drinks:
        drinkslist.append(drink.short())
    return jsonify({
        "success": True,
        "drinks": drinkslist
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail')
@cross_origin()
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinkslist = []
    drinks = Drink.query.all()
    if len(drinks) == 0:
        abort(404)
    for drink in drinks:
        drinkslist.append(drink.long())
    return jsonify({
        "success": True,
        "drinks": drinkslist
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',  methods=['POST'])
@cross_origin()
@requires_auth('post:drinks')
def post_drinks_detail(payload):
    request_data = request.get_json()
    if (request_data.get("title")):
        title = request_data.get("title")    
    if (request_data.get("recipe")):
        dataList = request_data.get("recipe")
        recipe = '['
        for index in range(len(dataList)):
            if (index == 0):
                recipe = recipe + '{'
            else:
                recipe = recipe + ',{'
            for key in dataList[index]:
                #print(dataList[index][key])
                if (key != "parts"):
                    recipe = recipe + '"' + key + '":"' + dataList[index][key] + '",'
                else:
                    recipe = recipe + '"' + key + '":' + str(dataList[index][key]) + '}'
        recipe = recipe + ']'
    else:
        recipe = ''
    try:
        drink = Drink(title=title, recipe=recipe)
        drink.insert()    
        return jsonify({
            "success": True,
            "drinks": drink.long()
        },200)
    except:
        db.session.rollback()
        abort(422) 
    finally:
        db.session.close()
'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>',  methods=['PATCH'])
@cross_origin()
@requires_auth('patch:drinks')
def patch_drinks_detail(payload,drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    drinkList = []
    drinkDict = {}
    if (drink != None):
        request_data = request.get_json()

        if ( request_data.get("title")):
             drink.title = request_data.get("title")
        
        if (request_data.get("recipe")):
            dataList = request_data.get("recipe")
            recipe = '['
            for index in range(len(dataList)):
                if (index == 0):
                    recipe = recipe + '{'
                else:
                    recipe = recipe + ',{'
                for key in dataList[index]:
                    #print(dataList[index][key])
                    if (key != "parts"):
                        recipe = recipe + '"' + key + '":"' + dataList[index][key] + '",'
                    else:
                        recipe = recipe + '"' + key + '":' + str(dataList[index][key]) + '}'
            recipe = recipe + ']'
            drink.recipe = recipe
        
        try:
            drink.update()  
            drinkDict = drink.long()
            drinkList.append(drinkDict)
            return jsonify({
                "success": True,
                "drinks": drinkList
            })
        except:
            db.session.rollback()
            abort(422) 
        finally:
            db.session.close()

    else:
        abort(404)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>',  methods=['DELETE'])
@cross_origin()
@requires_auth('delete:drinks')
def delete_drinks_detail(payload,drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if (drink != None):
        try:
            drink = Drink.query.get(drink_id)
            drink.delete()
            db.session.commit()
            return jsonify({
                "success": True,
                "delete":drink_id,
            },200)    
        except:
            db.session.rollback()
            return jsonify({
                "success": False,
                "delete":drink_id,
            },200)          
        finally:
            db.session.close()
    else:
        abort(404)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def notfound(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "not found"
                    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.route('/tabs/user-page')
@app.errorhandler(AuthError)
def AuthError(AuthError):
    return jsonify({
                    "success": False, 
                    "error": AuthError.status_code,
                    "message":AuthError.error["description"]
                    }), 401    
    #print (request.headers)
    #auth_header = request.headers("Authorization")
    #print (auth_header)