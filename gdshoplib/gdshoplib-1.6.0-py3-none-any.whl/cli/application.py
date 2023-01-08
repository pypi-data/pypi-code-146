from multiprocessing import Pool

import typer
from rich import print

from gdshoplib import Platform, Product
from gdshoplib.apps.platforms.base import BasePlatformManager
from gdshoplib.packages.cache import KeyDBCache
from gdshoplib.services.notion.database import Database
from gdshoplib.services.notion.notion import Notion

app = typer.Typer()


@app.command()
def sku_set():
    for page in Product.query(
        params={
            "filter": {
                "and": [
                    {"property": "Наш SKU", "rich_text": {"is_empty": True}},
                    {"property": "Цена (eur)", "number": {"is_not_empty": True}},
                ]
            }
        },
    ):
        sku = page.generate_sku()
        while not Product.query(filter={"sku": sku}):
            sku = page.generate_sku()

        page.notion.update_prop(
            page.id, params={"properties": {"Наш SKU": [{"text": {"content": sku}}]}}
        )
        print(Product(page.id).sku)


@app.command()
def price_update():
    for product in Product.query():
        price = product.price.now
        product.notion.update_prop(
            product.id, params={"properties": {"Текущая цена": {"number": price}}}
        )
        if product.kit:
            product.notion.update_prop(
                product.id,
                params={
                    "properties": {"Цена комплекта": {"number": product.price.kit}}
                },
            )
        product.notion.update_prop(
            product.id,
            params={
                "properties": {
                    "Текущая скидка": {"number": product.price.current_discount}
                }
            },
        )

        print(product.sku)


def generate_description(id):
    product = Product(id)
    product.description.warm_description_blocks()
    for platform, block in product.description.description_blocks.items():
        key = platform.split(":")[-1]
        platform = Platform.get_platform(key=key)
        new_description = product.description.generate(platform.manager)
        Notion().update_block(
            block.id,
            params={"code": {"rich_text": [{"text": {"content": new_description}}]}},
        )
        print(f"{product.sku}: {platform}")


@app.command()
def description_regenerate():
    with Pool(3) as p:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            p.apply_async(generate_description, (product["id"],))
        p.close()
        p.join()


def description_check_action(id):
    product = Product(id)
    for platform_manager in BasePlatformManager.__subclasses__():
        block = product.description.get_description_block(
            platform_key=platform_manager.KEY
        )
        print(f'{product.sku} {platform_manager}: {block.check if block else "None"}')


@app.command()
def description_check():
    with Pool(3) as p:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            p.apply_async(description_check_action, (product["id"],))
        p.close()
        p.join()


@app.command()
def cache_clean():
    KeyDBCache().clean(r"[blocks|pages|databases]*")


def cache_warm_func(id):
    product = Product(id)
    product.price.now
    product.kit
    product.notes
    product.specifications
    product.tags
    product.media
    product.description
    product.brand.title
    product.description.warm_description_blocks()
    print(f"{product.sku}: {product.last_edited_time}")


@app.command()
def cache_warm(
    full: bool = typer.Option(True),
    single: bool = typer.Option(False),
    only_edited: bool = typer.Option(True),
):
    with Pool(3) as p:
        with Database(
            Product.SETTINGS.PRODUCT_DB, notion=Notion(caching=True)
        ) as database:
            params = {}
            if only_edited and database.get_update_time():
                print(f"Фильтрация от даты: {database.get_update_time()}")
                params = database.edited_filter()

            for product in database.pages(params=params):
                skipped = False
                if not full:
                    if KeyDBCache().exists(product["id"]):
                        print(f"{product['id']}: SKIPPED")
                        skipped = True

                if single and not skipped:
                    cache_warm_func(product["id"])
                elif not single and not skipped:
                    p.apply_async(cache_warm_func, (product["id"],))
        p.close()
        p.join()


@app.command()
def cache_count():
    print(KeyDBCache().count())


def cache_check_action(id):
    for block in Notion().get_blocks(id):
        exists = KeyDBCache().exists(block["id"])
        print(f"{block['id']}: {exists}")


@app.command()
def cache_check():
    with Pool(3) as p:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            p.apply_async(cache_check_action, (product["id"],))
        p.close()
        p.join()


def warm_product_media(id):
    for media in Product(id).media:
        media.fetch()
        print(f"{media.file_key}: {media.exists()}")


@app.command()
def media_warm():
    with Pool(5) as p:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            p.apply_async(warm_product_media, (product["id"],))
        p.close()
        p.join()


@app.command()
def media_count():
    count = 0
    for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
        count += len(Product(product["id"]).media)

    print(count)


def media_check_action(id):
    accepted_formats = (
        "png",
        "jpg",
        "jpeg",
    )
    product = Product(id)
    for media in Product(product.id).media:
        accepted = media.format in accepted_formats
        print(
            f"{media.file_key}: {media.exists()} {'ACCEPTED' if accepted else 'REJECTED'}"
        )


@app.command()
def media_check():
    with Pool(3) as p:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            p.apply_async(media_check_action, (product["id"],))
        p.close()
        p.join()


def warm_platfrom_feed(key):
    feed = Platform.get_platform(key=key).feed()
    KeyDBCache()[f"feed/{key.lower()}"] = feed
    print(key)


@app.command()
def feed_warm(platform_key=None):
    if platform_key:
        warm_platfrom_feed(platform_key)
        return

    with Pool(7) as p:
        for platform in Platform():
            p.apply_async(warm_platfrom_feed, (platform.manager.KEY,))
        p.close()
        p.join()


if __name__ == "__main__":
    app()
