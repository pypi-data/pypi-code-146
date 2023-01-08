from recipe_scrapers import scrape_html, scrape_me

from weekly_menu.webapp.api.models.recipe import RecipeIngredient

from ...models import Recipe


def create_module(app, **kwargs):
    from .controllers import scraper_blueprint
    app.register_blueprint(scraper_blueprint)


def scrape_recipe_from_url(url: str):
    try:
        scraped = scrape_me(url, wild_mode=True)
    except:
        scraped = scrape_html(url)

    return {
        'title': scraped.title(),
        'image': scraped.image(),
        'servings': scraped.yields(),
        'ingredients': scraped.ingredients(),
        'nutrients': scraped.nutrients(),
        'instructions': scraped.instructions(),
        'instructions_list': scraped.instructions_list(),
        'links': scraped.links(),
    }
