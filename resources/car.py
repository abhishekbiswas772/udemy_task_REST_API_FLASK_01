from flask_smorest import abort, Blueprint
from db import db
from flask import request, jsonify
from models import CarModel
from flask.views import MethodView
from schema import CarsSchema

DEFAULT_PAGE = 1
DEFAULT_SIZE = 10


blp = Blueprint("Cars Models", __name__, description = "All About Cars")


@blp.route('/api/cars')
class CarView(MethodView):
    def get(self):
        #make global internal variable for query item
        query = CarModel.query

        #brand based filtering
        brand = request.args.get('brand')
        if brand is not None:
            query = query.filter(CarModel.brand.ilike(f'%{brand}%'))

        #model based filtering
        model = request.args.get('model')
        if model is not None:
            query = query.filter(CarModel.model.ilike(f'%{model}%'))

        #transmission based filtering 
        transmission = request.args.get('transmission')
        if transmission is not None:
            query = query.filter(CarModel.transmission.ilike(f'%{transmission}%'))
        
        #priced_based filtering 
        price_min = request.args.get('price_min', type=float)
        if price_min is not None:
            query = query.filter(
                CarModel.price >= price_min
            )
        price_max = request.args.get('price_max', type=float)
        if price_max is not None:
            query = query.filter(
                CarModel.price <= price_max
            )

        #pagination API Implementation
        page_request = request.args.get('page', DEFAULT_PAGE, type=int)
        size_request = request.args.get('size', DEFAULT_SIZE, type=int)
        total_num_entry = query.count()
        last_page = (total_num_entry + size_request - 1) // size_request
        if page_request > last_page:
            abort(400, message = {
                "message" : "Page Not Found"
            })

        sort_order = request.args.get('sort_order', 'asc')
        sort_by = request.args.get('sort_by')
        if sort_by is not None:
            sort_attr = getattr(CarModel, sort_by, None)
            if sort_order == "desc":
                query = query.order_by(sort_attr.desc())
            else:
                query = query.order_by(sort_attr.asc())

        cars_data_paginate = query.paginate(page=page_request, per_page=size_request, error_out=False)
        cars_schema = CarsSchema(many=True)
        result = cars_schema.dump(cars_data_paginate.items)
        return jsonify({
            "data": result,
            "total_element": total_num_entry,
            "total_pages": cars_data_paginate.pages,
            "page": page_request
        }), 200
    
    @blp.arguments(CarsSchema)
    @blp.response(201, CarsSchema)
    def post(self, car_model_data):
        if(
            CarModel.query.filter(CarModel.model == car_model_data["model"]).first()
        ):
            abort(
                400,
                message = {
                    "error" : "Model Exist",
                    "message" : "This Car Model Exists"
                }
            )
        car_data = CarModel(**car_model_data)
        try:
            db.session.add(car_data)
            db.session.commit()
        except Exception as e:
            print(e)
            abort(
                500,
                message = {
                    "error" : "Insertion Failed",
                    "message" : "Cars Model Insertion Failed"
                }
            )
        return car_data
        