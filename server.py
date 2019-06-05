import os
from flask import Flask, request, Response, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
db = SQLAlchemy(app)


class Serializable(object):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Recipe(db.Model, Serializable):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    prep_time = db.Column(db.String(80))
    cook_time = db.Column(db.String(80))
    directions = db.Column(db.Text())
    serves = db.Column(db.String(10))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship("Category",
                               backref=db.backref('recipes', lazy='dynamic'))

    tags = db.relationship("Tag",
                    secondary="recipe_tags",
                    backref="recipes")

    recipe_ingredients = db.relationship("RecipeIngredient", backref="recipe")

    def __repr__(self):
        return '<Recipe %r, %r>' % (self.id, self.title)


class RecipeIngredient(db.Model, Serializable):
    __tablename__ = 'recipe_ingredients'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    amount = db.Column(db.String(120))
    instructions = db.Column(db.String(120))

    def __repr__(self):
        return '<Recipe %r Ingredient %r>' % (self.recipe.title, self.ingredient.name)


class Ingredient(db.Model, Serializable):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    recipe_ingredients = db.relationship("RecipeIngredient", backref="ingredient")

    def __repr__(self):
        return '<Ingredient %r>' % self.name



class Category(db.Model, Serializable):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Category %r>' % self.name


class Tag(db.Model, Serializable):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Tag %r>' % self.name



@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/recipes')
def recipes():
	recipes = []
	recipe_files = os.listdir('./recipes/')
	for recipe_id in recipe_files:
		with open('./recipes/%s' % recipe_id) as f:
			try:
				recipe = json.load(f)
				recipes.append(recipe)
			except ValueError as e:
				print "empty recipe id: ", recipe_id
	return jsonify(data=recipes)

@app.route('/ingredients')
def ingredients():
	ingredients = Ingredient.query.all()
	ingredients = [i.to_dict() for i in ingredients]
	return jsonify(data=ingredients)


@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
	recipe = Recipe.query.get(recipe_id)
	if recipe:
		return jsonify(data=recipe.to_dict())
	else:
		return Response("No Recipe Found", status=404, mimetype='application/json')

@app.route('/recipe/<int:recipe_id>/edit', methods=["GET", "POST"])
def edit_recipe(recipe_id):
	return Response(str(request.form.get('boobs')))


if __name__ == '__main__':
	app.run(debug=True)
