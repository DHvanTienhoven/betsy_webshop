__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


from models import Tag, Transaction, db, Product, TagPerProduct
from datetime import date


def search(term):
    products = Product.select().where(Product.product_name.contains(term)).dicts()
    result =[]
    for product in products:
        result.append(product)
    return result


def list_user_products(user_id):
    products = Product.select().where(Product.product_creator == user_id).dicts()
    result = []
    for product in products:
        result.append(product)
    return result


def list_products_per_tag(tag_id):
    products = TagPerProduct.select(Product).join(Product).where(TagPerProduct.tag == tag_id).dicts()
    result = []
    for product in products:
        result.append(product)
    return result


'''
in order to add a product to the catalog more information is needed, therefore I added some extra arguments
'''
def add_product_to_catalog(user_id, prod_name, prod_description, price, prod_quantity, *tags):
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


def update_stock(product_id, new_quantity):
    product = Product.select().where(Product.product_id == product_id).get()
    product.quantity = new_quantity
    product.save()


def purchase_product(product_id, buyer_id, quantity):
    db.connect()
    price = Product.get(Product.product_id==product_id).price_per_unit
    subtotal = round(price * quantity, 2)
    Transaction.create(transaction_date=date.today(), product=product_id, quantity=quantity, customer=buyer_id, sub_total=subtotal)
    current_quantity = Product.get(Product.product_id==product_id).quantity
    new_quantity = current_quantity - quantity
    update_stock(product_id, new_quantity)
    db.close()


def remove_product(product_id):
    product_to_remove = Product.get(Product.product_id == product_id)
    product_to_remove.delete_instance()
    TagPerProduct.delete().where(TagPerProduct.product==product_id)

