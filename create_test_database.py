from models import db, User, Product, Tag, TagPerProduct, Transaction
from datetime import date

def create_test_data():

    db.connect()

    db.create_tables([User, Product, Tag, TagPerProduct, Transaction])
    
    example_users = [
        {'name': 'John Doe',
        'adress': 'Fake street 1, 1234AB Fake town',
        'billing_information': 1234567891011121},
        {'name': 'Dorian Gray',
        'adress': '12 Grosvenor Square, SW1V 3JD London',
        'billing_information': 4029930298340177},
        {'name': 'Sherlock Holmes',
        'adress': '221B Baker Street, E17 8EG London',
        'billing_information': 3095884688930023},
        {'name': 'Nathalie Beijen',
        'adress': 'Gravin Adelastraat 155, 3032HC Rotterdam',
        'billing_information': 1234567891011121},
        {'name': 'Frederik Boersema',
        'adress': 'Kerkstraat 5, 7403BX Maastricht',
        'billing_information': 8843562094399046},
        {'name': 'Emilie Schuiten',
        'adress': 'Appelstraat 50, 9083VF Assen',
        'billing_information': 4033954185309427},
        {'name': 'Arsjad Mokiem',
        'adress': 'Wakkerstraat 34, 1097CE Amsterdam',
        'billing_information': 4445083202549932},
        {'name': 'Mischa Oostlander',
        'adress': 'Nieuwe Boteringestraat 77, 9712PK Groningen',
        'billing_information': 7437721565320840},
        {'name': 'Diana van Raab van Canstein',
        'adress': 'Voltaplein 11, 1082GB Amsterdam',
        'billing_information': 3405093284435139}
    ]

    for user in example_users:
        User.create(user_name=user['name'], adress=user['adress'], billing_information=user['billing_information'])
    
    example_products = [
        {'name': 'kado katoen',
        'description': 'kado katoen is herbruikbaar kadopapier, gemaakt van gerecycled textiel. Geef je cadeautjes voortaan in een zachte verpakking, die de krijger kan hergebruiken!',
        'price_per_unit': 7.50,
        'quantity': 221,
        'product_creator': 2,
        'tags': ['textiel', 'duurzaamheid', 'kado']
        },
        {'name': 'klein schaaltje',
        'description': 'klein roze/paars schaaltje gemaakt op de draaischijf. Geglazuurd met een craquelétechniek. Niet vaatwasser-bestendig.',
        'price_per_unit': 15.00,
        'quantity': 5,
        'product_creator': 4,
        'tags': ['keramiek', 'craquelé']
        },
        {'name': 't-shirt met motief',
        'description': 'vrolijk kinder t-shirt met dierenmotief. Handgemaakt van 100% katoen',
        'price_per_unit': 12.95,
        'quantity': 28,
        'product_creator': 9,
        'tags': ['textiel', 'kleding', 'kinderen & baby\'s', 'nuttig']
        },
        {'name': 'baby mutsje',
        'description': 'gebreid babymutsje van merino-wol. Verschillende kleuren en patronen beschikbaar.',
        'price_per_unit': 11.00,
        'quantity': 42,
        'product_creator': 7,
        'tags': ['textiel', 'kleding', 'kinderen & baby\'s', 'brei & haakwerk']
        },
        {'name': 'logische puzzel',
        'description': 'zelfgemaakte logische puzzel van hout.',
        'price_per_unit': 19.95,
        'quantity': 390,
        'product_creator': 3,
        'tags': ['hout', 'duurzaamheid', 'kado', 'spel']
        },
        {'name': 'rieten mand - groot',
        'description': 'rieten, gevlochten mand. Bijvoorbeeld om kranten of tijdschriften op te leggen. Verkrijgbaar in meerdere kleuren',
        'price_per_unit': 22.45,
        'quantity': 36,
        'product_creator': 5,
        'tags': ['riet', 'interieur', 'nuttig']
        },
        {'name': 'wollen sjaal',
        'description': 'wollen sjaal in vrolijke kleuren.',
        'price_per_unit': 30.00,
        'quantity': 4,
        'product_creator': 6,
        'tags': ['textiel', 'wol', 'kleding', 'brei & haakwerk', 'nuttig']
        },
        {'name': 'oorbellen',
        'description': 'oorbellen met hangers van fimoklei. Verschillende motiefjes beschikbaar',
        'price_per_unit': 14.32,
        'quantity': 50,
        'product_creator': 1,
        'tags': ['sierraad', 'fimoklei']
        },
        {'name': 'glazen onderzetters',
        'description': 'Onderzetters van gekleurd glas. Voorkom kringen op uw tafel met deze handige en mooie onderzetters',
        'price_per_unit': 5.35,
        'quantity': 81,
        'product_creator': 8,
        'tags': ['glas', 'interieur', 'nuttig']
        },
        {'name': 'glazen hanger ketting',
        'description': 'unieke handgedraaide hanger voor aan een ketting',
        'price_per_unit': 48.90,
        'quantity': 13,
        'product_creator': 8,
        'tags': ['glas', 'sierraad', 'kado']
        },
        {'name': 'katoenen rok',
        'description': 'halflange zomerrok verkrijgbaar in verschillende pasteltinten',
        'price_per_unit': 35.00,
        'quantity': 5,
        'product_creator': 9,
        'tags': ['textiel', 'kleding', 'nuttig']
        },
        {'name': 'kado katoen groot',
        'description': 'kado katoen is herbruikbaar kadopapier, gemaakt van gerecycled textiel. Deze grote versie is geschikt om bordspellen te verpakken',
        'price_per_unit': 9.50,
        'quantity': 111,
        'product_creator': 2,
        'tags': ['textiel', 'duurzaamheid', 'kado']
        },
        {'name': 'aardewerken fruitschaal',
        'description': 'handgevormde fruitschaal met wit glazuur',
        'price_per_unit': 24.80,
        'quantity': 9,
        'product_creator': 4,
        'tags': ['keramiek', 'interieur', 'nuttig']
        },
        {'name': 'set van kopjes',
        'description': 'op de draaischijf gevormde kopjes, verkocht in een set van 4',
        'price_per_unit': 20.00,
        'quantity': 11,
        'product_creator': 4,
        'tags': ['keramiek', 'nuttig']
        },
        {'name': 'babygym',
        'description': 'unieke handgemaakte babygym van hout. Geschikt voor kinderen vanaf 4 maanden om te spelen en zich te ontwikkelen.',
        'price_per_unit': 83.30,
        'quantity': 3,
        'product_creator': 3,
        'tags': ['hout', 'kinderen & baby\'s']
        },
        {'name': 'rieten fruitschaal',
        'description': 'fruitschaal van riet.',
        'price_per_unit': 5.00,
        'quantity': 6,
        'product_creator': 5,
        'tags': ['riet', 'interieur', 'nuttig']
        },
        {'name': 'grote schaal',
        'description': 'grote aardewerken schaal, bijvoorbeeld voor sla',
        'price_per_unit': 19.80,
        'quantity': 1,
        'product_creator': 4,
        'tags': ['keramiek', 'nuttig']
        },
        {'name': 'IJslandse Trui',
        'description': 'Zelfgebreide IJslandse Trui met ronde hals. Verkrijgbaar in verschillende grijs- en aarde-tinten. Gemaakt van IJslandse wol',
        'price_per_unit': 123.00,
        'quantity': 4,
        'product_creator': 7,
        'tags': ['textiel', 'wol', 'kleding', 'brei & haakwerk', 'nuttig']
        },
        {'name': 'nachtkastje',
        'description': 'simpel houten nachtkastje met lade van sloophout',
        'price_per_unit': 50.00,
        'quantity': 12,
        'product_creator': 3,
        'tags': ['hout', 'duurzaamheid', 'interieur', 'nuttig']
        }
    ]

    for product in example_products:
        Product.create(product_name=product['name'], description=product['description'], price_per_unit=product['price_per_unit'], quantity=product['quantity'], product_creator=product['product_creator'])
    
    tags = set()

    for product in example_products:
        for item in product['tags']:
            tags.add(item)
    
    for tag in tags:
        Tag.create(tag_name=tag)

    for count, product in enumerate(example_products, 1):
        product_id = count
        for tag in product['tags']:
            TagPerProduct.create(tag=tag, product=product_id)
    
    db.close()

create_test_data()