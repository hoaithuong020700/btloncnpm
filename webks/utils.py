import hashlib
from webks.models import User, UserRole, Receipt, ReceiptDetail, Room
from webks import db


def check_login(username, password): #role=UserRole.ADMIN):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = User.query.filter(User.username == username,
                             User.password == password).first()
                             #User.user_role == role).first()

    return user


def read_rooms(cate_id=None, kw=None, from_price=None, to_price=None):
    rooms = Room.query

    if cate_id:
        rooms = rooms.filter(Room.RoomCatalog_id == cate_id)

    if kw:
        rooms = rooms.filter(Room.room_number.contains(kw))

    if from_price and to_price:
        rooms = rooms.filter(Room.price.__gt__(from_price), Room.price.__lt__(to_price))

    return rooms.all()


def get_room_by_id(room_id):
    return Room.query.get(room_id)


def register_user(firstname, lastname, email, username, password):#, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(firstname=firstname, lastname=lastname, email=email, username=username, password=password)
             #avatar=avatar)
             #user_role=UserRole.USER)

    db.session.add(u)
    db.session.commit()


def cart_stats(cart):
    total_amount, total_quantity = 0, 0
    if cart:
        for r in cart.values():
            total_quantity = total_quantity + r["quantity"]
            total_amount = total_amount + r["quantity"]*r["price"]

    return total_quantity, total_amount


def add_receipt(cart):
    if cart:
        receipt = Receipt(customer_id=1)
        db.session.add(receipt)

        for r in list(cart.values()):
            detail = ReceiptDetail(receipt=receipt,
                                   room_id=int(r["id"]),
                                   quantity=r["quantity"],
                                   price=r["price"])
            db.session.add(detail)

        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)

    return False
