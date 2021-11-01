__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


from logging import NullHandler
from models import Tag, Transaction, User, db, Product, TagPerProduct
from datetime import date

#This function will search for a product based on a search term, if the term is in the product name it will list the product.
#It's case-insensitive

def search(term: str):
    products = Product.select().where(Product.product_name.contains(term)).dicts()
    result =[]
    for product in products:
        result.append(product)
    return result

#This function will list all products for a certain user, based on their name
#It's case-sensitive

def list_user_products(user_name: str):
    user_id = User.get(User.user_name == user_name).user_id
    products = Product.select().where(Product.product_creator == user_id).dicts()
    result = []
    for product in products:
        result.append(product)
    return result

#this function will display all products with a given tag
#it's case-sensitive

def list_products_per_tag(tag_id: str):
    products = TagPerProduct.select(Product).join(Product).where(TagPerProduct.tag == tag_id).dicts()
    result = []
    for product in products:
        result.append(product)
    return result

#This function will add a product to the catalog

def add_product_to_catalog(user_id: int, prod_name: str, prod_description: str, price: float, prod_quantity: int, *tags):
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

#this function will handle the updating of the stocl if for example a user creates more products or a product is sold
#it will take the product name and new quantity as arguments and it is case-sensitive

def update_stock(product_name: str, new_quantity: int):
    product_id = Product.get(Product.product_name == product_name).product_id
    product = Product.select().where(Product.product_id == product_id).get()
    product.quantity = new_quantity
    product.save()

#This function will handle the purchase of a product by a User. It will be added to the Transactions Record and the 
# stock of the product will be updated. The product will NOT be added to the products of the buyer, as it is assumed the buyer 
# will use it and not sell it on. If they'd want to sell it, they'd have to create a new product with add_product_to_catalog. 
# it will take the name of the product, the name of the buyer and the quantity of bought products and it is case-sensitive

def purchase_product(product_name: str, buyer_name: str, quantity: int):
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

#this function will remove a product from a certain user. It is still listed in the database, but not associated with the user anymore
# the function takes the product name as its argument and it is case-sensitive

def remove_product_from_user(product_name: str):
    product_to_remove = Product.select().where(Product.product_name == product_name).get()
    product_to_remove.product_creator = None
    product_to_remove.save()

