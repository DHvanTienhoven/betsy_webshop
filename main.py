__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import Tag, Transaction, User, db, Product, TagPerProduct
from datetime import date


def search(term: str):
    '''
    Description: This function will search for products based on a search term

    Keyword arguments: term -- search term (string, case insensitive)

    Returns: List of Dictionairies of products that contain the term
    '''
    products = Product.select().where(Product.product_name.contains(term)).dicts()
    return list(products)


def list_user_products(user_name: str):
    '''
    Description: This function will search for products based on a specific user

    Keyword arguments: user_name (string, case sensitive)

    Returns: List of Dictionairies of products made by the user
    '''
    user_id = User.get(User.user_name == user_name).user_id
    products = Product.select().where(Product.product_creator == user_id).dicts()
    return list(products)


def list_products_per_tag(tag_id: str):
    '''
    Description: This function will search for products based on a tag ID

    Keyword arguments: tag_id (string, case sensitive)

    Returns: List of Dictionairies of products with specified tag
    '''
    products = TagPerProduct.select(Product).join(Product).where(TagPerProduct.tag == tag_id).dicts()
    return list(products)


def add_product_to_catalog(user_id: int, prod_name: str, prod_description: str, price: float, prod_quantity: int, *tags):
    '''
    Description: This function will add a product to the database

    Keyword arguments: user_id (int), prod_name (string), prod_decription (string), price (float), product quantity (int), tags (string)

    Updates database to add new product
    '''
    db.connect()
    Product.create(product_name=prod_name, description=prod_description, price_per_unit=price, quantity=prod_quantity, product_creator=user_id)
    get_existing_tags = Tag.select()
    existing_tags = []
    for tag in get_existing_tags:
        existing_tags.append(tag.tag_name)
    for tag in tags:
        if tag not in existing_tags:
            Tag.create(tag_name = tag)
    product_id = len(Product.select()) + 1
    for tag in tags:
        TagPerProduct.create(tag=tag, product=product_id)
    db.close()


def update_stock(product_name: str, new_quantity: int):
    '''
    Description: this function will handle the updating of the stock if for example a user creates more products or a product is sold

    Keyword arguments: product_name (string, case sensitive) new_quantity (int)

    Updates database to update quantity of an existing product
    '''
    product_id = Product.get(Product.product_name == product_name).product_id
    product = Product.select().where(Product.product_id == product_id).get()
    product.quantity = new_quantity
    product.save()


def purchase_product(product_name: str, buyer_name: str, quantity: int):
    '''
    Description: this function will handle the purchase of a product by a user.

    Keyword arguments: product_name (string, case sensitive) buyer_name (string, case sensitive) quantity (int)

    Updates database: adds sale to Transactions record, the stock of the product will be updated to the new quantity
    '''
    product_id = Product.get(Product.product_name == product_name).product_id
    buyer_id = User.get(User.user_name == buyer_name).user_id
    db.connect()
    price = Product.get(Product.product_id==product_id).price_per_unit
    subtotal = round(price * quantity, 2)
    Transaction.create(transaction_date=date.today(), product=product_id, quantity=quantity, customer=buyer_id, sub_total=subtotal)
    current_quantity = Product.get(Product.product_id==product_id).quantity
    new_quantity = current_quantity - quantity
    update_stock(product_name, new_quantity)
    db.close()


def remove_product_from_user(product_name: str):
    '''
    Description: this function will remove a product from the database

    Keyword arguments: product_name (string, case sensitive)

    Updates database: removes product from database 
    '''
    product_to_remove = Product.get(Product.product_name == product_name)
    product_id = product_to_remove.product_id
    print(product_id)
    product_to_remove.delete_instance()
    TagPerProduct.delete().where(TagPerProduct.product==product_id)

