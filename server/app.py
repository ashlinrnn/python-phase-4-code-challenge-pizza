#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>" 

@app.route('/restaurants') 
def restaurants():
    restaurants = [restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in Restaurant.query.all() ] 

    response = make_response( 
        restaurants, 
        200
    ) 
    return response 

@app.route('/restaurants/<int:id>', methods = ['GET'])
def restaurant_by_id(id): 
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()

    if restaurant: 
        return restaurant.to_dict(), 200 
    return{"error": "Restaurant not found"}, 404  

@app.route('/restaurants/<int:id>', methods = ['DELETE']) 
def delete_restaurant(id): 
    restaurant = Restaurant.query.filter(Restaurant.id == id).first() 
    if not restaurant: 
        return {"error": "Restaurant not found"}, 404 
    db.session.delete(restaurant) 
    db.session.commit() 

    return {}, 204 

@app.route('/pizzas') 
def pizzas():  
   
    pizzas = [pizza.to_dict(only=("id", "ingredients", "name")) for pizza in Pizza.query.all()] 
     
    response = make_response( 
         pizzas, 
         200
     ) 
    return response  

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    
  
    price = data.get('price')
    if not price or not (1 <= price <= 30):
        return {"errors": ["validation errors"]}, 400

   
    if not Restaurant.query.get(data.get('restaurant_id')) or \
       not Pizza.query.get(data.get('pizza_id')):
        return {"errors": ["validation errors"]}, 400


    new_rp = RestaurantPizza(
        price=price,
        pizza_id=data.get('pizza_id'),
        restaurant_id=data.get('restaurant_id')
    )
    
    db.session.add(new_rp)
    db.session.commit()

   
    return new_rp.to_dict(), 201

    
    
   


if __name__ == "__main__":
    app.run(port=5555, debug=True)
