'''
Script with shopify functions
Copyright 2022 Reyes Ruiz
https://github.com/Los-Vaqueros-Western-Wear/Scripts
'''
import sys
import json
import time
import os
from pathlib import Path
from com_digitalruiz_shopify_http_client import shopify_http_client
from com_digitalruiz_my_logger import my_logger

LOGGER = my_logger.set_logger(module_name=sys.argv[0], loglevel='INFO')
SHOPIFY_ADMIN_API_URL = shopify_http_client.set_shopify_admin_url()

def create_product(data):
    '''
    Creates a new shopify product
    https://shopify.dev/api/admin-rest/2022-10/resources/product#post-products
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, "products.json"])
    content = shopify_http_client.post(url, data)
    return content

def variants_create(product_id_add_variant, data):
    '''
    Creates a new product variant
    https://shopify.dev/api/admin-rest/2022-10/resources/product-variant#post-products-product-id-variants
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            "products", \
            str(product_id_add_variant), \
            "variants.json"])
    content = shopify_http_client.post(url, data)
    return content

def variant_update(data):
    '''
    Updates variant
    https://shopify.dev/api/admin-rest/2022-10/resources/product-variant#put-variants-variant-id
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            "variants", \
            str(data['variant']['id']) + ".json"])
    content = shopify_http_client.put(url, data)
    return content

def product_update(product_id, data):
    '''
    Update product
    https://shopify.dev/api/admin-rest/2022-10/resources/product#put-products-product-id
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            "products", \
            str(product_id) + ".json"\
            ])
    content = shopify_http_client.put(url, data)
    return content

def create_product_image(product_id, data):
    '''
    Creates a new product image
    https://shopify.dev/api/admin-rest/2022-10/resources/product-image#post-products-product-id-images
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            "products", \
            str(product_id), \
            "images.json"])
    content = shopify_http_client.post(url, data)
    return content


def update_product_image(product_id, image_id, data):
    '''
    Modify product image
    https://shopify.dev/api/admin-rest/2022-10/resources/product-image#put-products-product-id-images-image-id
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            "products", \
            str(product_id), \
            "images", \
            str(image_id) + ".json"])
    content = shopify_http_client.put(url, data)
    return content

def get_product_metafields(product_id):
    '''
    Gets metafields for a product
    https://shopify.dev/api/admin-rest/2022-10/resources/metafield#get-blogs-blog-id-metafields
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, 'products', str(product_id), 'metafields.json'])
    contents = shopify_http_client.get(url)
    metafields = []
    for content in contents:
        metafields = metafields + json.loads(content)['metafields']
    return metafields

def create_product_metafield(product_id, data):
    '''
    Creates a new product metafield
    https://shopify.dev/api/admin-rest/2022-10/resources/metafield#post-metafields
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            'products', \
            str(product_id), \
            'metafields.json'\
            ])
    content = shopify_http_client.post(url, data)
    if content:
        metafields = json.loads(content)
        return metafields['metafield']['id']
    return False

def update_product_metafield(metafield_id, data):
    '''
    Updates product metafield
    https://shopify.dev/api/admin-rest/2022-10/resources/metafield#put-metafields-metafield-id
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            'metafields', \
            str(metafield_id) + '.json'\
            ])
    content = shopify_http_client.put(url, data)
    if content:
        return True
    return False

def get_product_count():
    '''
    Getting number of products
    https://shopify.dev/api/admin-rest/2022-10/resources/product#get-products-count
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, "products", "count.json"])
    contents = shopify_http_client.get(url)
    count_content = json.loads(contents[0])
    if count_content:
        product_count = count_content['count']
        return product_count
    return False

def get_all_products():
    '''
    Function to return all products either from local file or get them from shopify
    and then save them to local file
    https://shopify.dev/api/admin-rest/2022-10/resources/product#get-products
    '''
    file_name = ("all_products.json")
    products = []
    if Path(file_name).is_file():
        file_modified_time = os.path.getmtime(file_name)
        time_difference = time.time() - file_modified_time
        if time_difference <= 7200:
            with open(file_name, "r", encoding='utf-8') as json_file:
                products = json.load(json_file)
                if products:
                    return products
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            "products.json"])
    contents = shopify_http_client.get(url)
    products = []
    for content in contents:
        products = products + json.loads(content)['products']
    if products:
        with open(file_name, "w", encoding='utf-8') as json_file:
            json.dump(products, json_file)
        return products
    LOGGER.critical("No products")
    return False

def adjust_inventory(inventory_item_id, add_inventory_count, location):
    '''
    Function to adjust inventory by certain quantity, default is 1
    https://shopify.dev/api/admin-rest/2022-10/resources/inventorylevel#post-inventory-levels-adjust
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, "inventory_levels", "adjust.json"])
    data = {}
    data['location_id'] = location
    data['inventory_item_id'] = inventory_item_id
    data['available_adjustment'] = add_inventory_count
    content = shopify_http_client.post(url,data)
    if content:
        LOGGER.debug(content)
        return True
    return False

def set_inventory(inventory_item_id, available, location):
    '''
    Function to set inventory level
    https://shopify.dev/api/admin-rest/2022-10/resources/inventorylevel#post-inventory-levels-set
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, "inventory_levels", "set.json"])
    data = {}
    data['location_id'] = location
    data['inventory_item_id'] = inventory_item_id
    data['available'] = available
    content = shopify_http_client.post(url,data)
    if content:
        LOGGER.debug(content)
        return True
    return False

def get_shopify_product_data(product_id):
    '''
    Function to return data object for a product
    https://shopify.dev/api/admin-rest/2022-10/resources/product#get-products-product-id
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            'products', \
            str(product_id) + \
            '.json'])
    contents = shopify_http_client.get(url)
    return json.loads(contents[0])

def get_shopify_images(product_id):
    '''
    Function to return images from shopify by product id
    https://shopify.dev/api/admin-rest/2022-10/resources/product-image#get-products-product-id-images
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            'products', \
            str(product_id), \
            'images.json'])
    contents = shopify_http_client.get(url)
    return json.loads(contents[0])

def get_products_by_collection_id(collection_id):
    '''
    Function to retrieve products by collection id
    '''
    url = '/'.join([SHOPIFY_ADMIN_API_URL, \
            'collections', \
            str(collection_id), \
            'products.json'])
    contents = shopify_http_client.get(url)
    products = []
    for content in contents:
        products = products + json.loads(content)['products']
    if products:
        return products
    return False

def __get_paginated_url(response):
    for link in response.headers['Link'].split(','):
        if 'next' in link.split(';')[1]:
            url = link.split(';')[0].strip().replace('<','').replace('>','')
            response = shopify_http_client.get(url)
            if response:
                return response
    return False

def __merge_dicts(dict_a, dict_b):
    res = dict_a | dict_b
    return res
