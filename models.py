# Models go here
from peewee import *

db = SqliteDatabase('betsy_webshop.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = AutoField()
    user_name = CharField()
    adress = CharField()
    billing_information = IntegerField()

class Product(BaseModel):
    product_id = AutoField()
    product_name = CharField()
    description = TextField()
    price_per_unit = DecimalField()
    quantity = IntegerField()
    product_creator = ForeignKeyField(User, backref="products")

class Tag(BaseModel):
    tag_name = CharField(primary_key=True)

class TagPerProduct(BaseModel):
    tag = ForeignKeyField(Tag, backref="products_per_tag")
    product = ForeignKeyField(Product, backref="tags_per_product")

class Transaction(BaseModel):
    transaction_id = AutoField()
    transaction_date = DateField()
    product_id = ForeignKeyField(Product, backref="sales")
    quantity = IntegerField()
    sub_total = DecimalField()
    customer_id = ForeignKeyField(User, backref="purchases")