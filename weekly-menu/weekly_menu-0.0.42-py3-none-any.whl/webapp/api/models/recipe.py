from .. import mongo

from .base_document import BaseDocument


class RecipeIngredient(mongo.EmbeddedDocument):
    quantity = mongo.FloatField()
    unitOfMeasure = mongo.StringField(max_length=10)
    required = mongo.BooleanField()
    freezed = mongo.BooleanField()
    ingredient = mongo.ReferenceField('Ingredient', required=True)


class RecipePreparationStep(mongo.EmbeddedDocument):
    description = mongo.StringField(max_length=1000)


class RelatedRecipe(mongo.EmbeddedDocument):
    id = mongo.ObjectIdField()


class Recipe(BaseDocument):
    name = mongo.StringField(required=True)
    description = mongo.StringField()
    preparation = mongo.StringField()  # TODO will be a list of strings
    preparationSteps = mongo.EmbeddedDocumentListField(
        'RecipePreparationStep', default=None)
    note = mongo.StringField()
    availabilityMonths = mongo.ListField(mongo.IntField(
        min_value=1, max_value=12), max_length=12, default=None)
    ingredients = mongo.EmbeddedDocumentListField(
        'RecipeIngredient', default=None)
    servs = mongo.IntField(min_value=1)
    estimatedCookingTime = mongo.IntField(min_value=1)
    estimatedPreparationTime = mongo.IntField(min_value=1)
    rating = mongo.IntField(min_value=1, max_value=3)
    cost = mongo.IntField(min_value=1, max_value=3)
    difficulty = mongo.StringField()
    recipeUrl = mongo.StringField()
    imgUrl = mongo.StringField()
    videoUrl = mongo.StringField()
    section = mongo.StringField()
    relatedRecipes = mongo.EmbeddedDocumentListField(
        'RelatedRecipe', default=None)
    tags = mongo.ListField(
        mongo.StringField(), default=None
    )

    meta = {
        'collection': 'recipes'
    }

    def __repr__(self):
        return "<Recipe '{}'>".format(self.name)
