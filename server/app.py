#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource,reqparse

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class PlantsResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, help="Name cannot be blank", type=str)
    parser.add_argument("image", required=True, help="image cannot be blank", type=str)
    parser.add_argument("price", required=True, help="price cannot be blank", type=int)


    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
      
        args = PlantsResource.parser.parse_args()
        name = args.get('name')
        image = args.get('image')
        price = args.get('price')
        to_add = Plant(name=name, image=image, price=price)
        


        try:
            db.session.add(to_add)
            db.session.commit()
            return { 'new_plant' :{
                "id" : to_add.id,
                "name": to_add.name,
                "image": to_add.image,
                "price": to_add.price
            }}, 201
        except Exception as e:
            db.session.rollback()
            return {
                'error' : str(e)
            }, 500
        finally:
            db.session.close()


#         new_plant =Plant(
#             name=data['name'],
#             image=data['image'],
#             price=data['price']
#         )
#         db.session.add(new_plant)
#         db.session.commit()


#         return make_response(new_plant.to_dict(), 201)


api.add_resource(PlantsResource, '/plants')


# class PlantByID(Resource):

#     def get(self, id):
#         plant = Plant.query.filter_by(id=id).first().to_dict()
#         return make_response(jsonify(plant), 200)
#     def post(self,id):
#         data=request.get_json()
#         plant=Plant.query.filter_by(id=id).first()

#         for attr in data:
#             setattr(plant,attr,data[attr])
#         db.session.add(plant)
#         db.session.commit()

#         return make_response(plant.to_dict(), 200) 
    
#     def delete(self,id):
#         plant=Plant.query.filter_by(id=id).first()
#         db.session.delete(plant)
#         db.session.commit()
        

#         return make_response('',204)
    



#api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
