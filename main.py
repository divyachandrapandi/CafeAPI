from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


def to_dict(self):
    # Method 1.
    dictionary = {}
    # Loop through each column in the data record
    for column in self.__table__.columns:
        # Create a new dictionary entry;
        # where the key is the name of the column
        # and the value is the value of the column
        dictionary[column.name] = getattr(self, column.name)
    return dictionary

    # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
    # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all")
def all():
    cafes =db.session.query(Cafe).all()
    cafe_list =[to_dict(cafe) for cafe in cafes]
    return jsonify(cafe=cafe_list)



@app.route('/add',methods=['POST'])
def add():
    new_cafe = Cafe(name=request.form["name"],
                    map_url=request.form["map_url"],
                    img_url=request.form["img_url"],
                    location=request.form["location"],
                    seats=request.form["seats"],
                    has_toilet=bool(request.form["has_toilet"]),
                    has_wifi=bool(request.form["has_wifi"]),
                    has_sockets=bool(request.form["has_sockets"]),
                    can_take_calls=bool(request.form["can_take_calls"]),
                    coffee_price=request.form["coffee_price"]
                    )
     
    db.session.add(new_cafe)
    db.session.commit()
    print(to_dict(db.session.query(Cafe).filter_by(location='Berlin').first()))
    return jsonify(cafe={
        "response":"succesfuuly updated!!"
    })

@app.route("/update/<int:cafeid>", methods = ["GET","POST","PATCH"])
def update(cafeid):
    price_args = request.args.get("price")
    cafe = Cafe.query.get(cafeid)
    if cafe:
        cafe.coffee_price = price_args
        db.session.commit()
        return jsonify(cafe={
                "response": "succesfully updated using patch!!"
            })
    else:
        return jsonify(cafe={
            "response": "not successful "
        })
@app.route('/search', methods=["GET"])
def search_by_location():

    query_location = request.args.get("loc")
    # cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    cafes = db.session.query(Cafe).all()
    cafe_list = []
    for cafe in cafes:
        if cafe.location == query_location:
                cafe_list.append(to_dict(cafe))
    if cafe_list:
        return jsonify(cafe=cafe_list)
    else:
        return jsonify(error={
            "Not Found": "Sorry we dont have any cafe in your location"
        })

@app.route("/delete/<cafeid>", methods=["DELETE"])
def delete(cafeid):
    cafe = Cafe.query.get(cafeid)
    api_key = request.args.get("api-key")
    if cafe:
        if api_key =="TopSecretAPIKey":
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={
                "response":"Successfully deleted"
            })
        else:
            return jsonify(response={
                "response": "Sorry! not allowed please check api-key"
            })
    else:
        return jsonify(response={
            "response": "The cafe with this id is not found!"
        })

@app.route('/random')
def random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=to_dict(random_cafe))
    # return jsonify(cafe={
    #     #Omit the id from the response
    #     # "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #
    #     #Put some properties in a sub-category
    #     "amenities": {
    #       "seats": random_cafe.seats,
    #       "has_toilet": random_cafe.has_toilet,
    #       "has_wifi": random_cafe.has_wifi,
    #       "has_sockets": random_cafe.has_sockets,
    #       "can_take_calls": random_cafe.can_take_calls,
    #       "coffee_price": random_cafe.coffee_price,
    #     }
    # }, encode="utf-8")

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
