import model
import os
import json
import re
from sqlalchemy.orm.exc import NoResultFound


recipe_filenames = os.listdir("./recipes")
ingredient_pattern = re.compile(u"([^A-Z]+)?([A-Z][^,]*)(?:, )?(.*)?")

model.db.drop_all()
model.db.create_all()

for fn in recipe_filenames:
	with open("./recipes/%s" % fn) as f:
		r_obj = json.load(f)

		r = model.Recipe(directions=r_obj["directions"],
			             cook_time=r_obj["cook_time"],
			             prep_time=r_obj["prep_time"],
			             serves=r_obj["serves"],
			             title=r_obj["title"],
			             id=fn)

		model.db.session.add(r)

		try:
			category = model.Category.query.filter_by(name=r_obj["category"]).one()
		except NoResultFound as e:
			category = model.Category(name=r_obj["category"])
			model.db.session.add(category)

		r.category = category
		
		for i in r_obj['ingredients']:
			match = ingredient_pattern.match(i)
			amount = match.group(1)
			ingredient = match.group(2)
			instructions = match.group(3)
			try:
				ing = model.Ingredient.query.filter_by(name=ingredient).one()
			except NoResultFound as e:
				ing = model.Ingredient(name=ingredient)
				model.db.session.add(ing)
			r_ing = model.RecipeIngredient(ingredient=ing,
 										   amount=amount,
 										   instructions=instructions,
 										   recipe=r)
			model.db.session.add(r_ing)

		for t in r_obj['tags']:
			try:
				tag = model.Tag.query.filter_by(name=t).one()
			except NoResultFound as e:
				tag = model.Tag(name=t)
				model.db.session.add(tag)
			r.tags.append(tag)

model.db.session.commit()


# {
#     "category": "Appetizers & Sides",
#     "cook_time": "5 - 6 Minutes",
#     "directions": "Preheat the Oven to 375\u00b0. Layer the lavash with the pear slices, pieces of Brie, prosciutto and sugar, in that order. Bake for 5-6 minutes until the Lavash is golden brown and the sugar has caramelized. Top with Baby Arugula and serve.",
#     "ingredients": [
#         "TJ's Lavash Bread (Regular or Whole Wheat)",
#         "1 TJ's Pear, thinly sliced",
#         "8 ounces (or so) TJ's Brie, cubed or torn into small pieces",
#         "2-3 slices TJ's Prosciutto, sliced thin",
#         "2-3 tablespoon TJ's Organic Brown Sugar",
#         "1 cup TJ's Wild Arugula"
#     ],
#     "prep_time": "2 Minutes",
#     "serves": "4 - 6",
#     "tags": [
#         "Baked",
#         "Party",
#         "Bread",
#         "Pizza",
#         "Fancy"
#     ],
#     "title": "Pear And Brie Fancy Flatbread"
# }