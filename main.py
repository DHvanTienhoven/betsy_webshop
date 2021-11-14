__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import Tag, Transaction, User, Product, TagPerProduct
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
    Description: This function will search for made and bought products based on a specific user

    Keyword arguments: user_name (string, case sensitive)

    Returns: List of Dictionairies of products made by the user
    '''
    user_id = User.get(User.user_name == user_name).user_id
    made_products = list(Product.select().where(Product.product_creator == user_id).dicts())
    made_products = [d['product_name'] for d in made_products]
    bought_products = list(Transaction.select(Product).join(Product).where(Transaction.customer_id == user_id and Transaction.quantity > 0).dicts())
    bought_products = [d['product_name'] for d in bought_products]
    user_products = {'own products': made_products, 'bought products': bought_products}
    return user_products


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
    price = Product.get(Product.product_id==product_id).price_per_unit
    subtotal = round(price * quantity, 2)
    Transaction.create(transaction_date=date.today(), product_id=product_id, quantity=quantity, customer_id=buyer_id, sub_total=subtotal)
    current_quantity = Product.get(Product.product_id==product_id).quantity
    new_quantity = current_quantity - quantity
    update_stock(product_name, new_quantity)


def remove_bought_product_from_user(product_name: str, user_name: str):
    '''
    Description: this function will reverse a purchase based on the input. It will change the quantity in the Transaction table
    for the given user and product to 0, and restore the quantity in the product database

    Keyword arguments: product_name (string, case sensitive), user_name (string, case sensitive)

    Updates database: changes quantity in transaction table to 0. Will restore the quantity in the products table
    '''
    user_id = User.get(User.user_name == user_name).user_id
    product_id = Product.get(Product.product_name == product_name).product_id
    transaction_record = Transaction.select().where(Transaction.customer_id == user_id and Transaction.product_id == product_id).get()
    quantity = transaction_record.quantity
    current_quantity = Product.get(Product.product_id==product_id).quantity
    update_stock(product_name, quantity + current_quantity)
    transaction_record.quantity = 0
    transaction_record.save()
