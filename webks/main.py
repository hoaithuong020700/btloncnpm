from flask import render_template, redirect, request, session, jsonify
from webks import app, login, utils
from flask_login import login_user
from webks.admin import *
import hashlib, os, json
from webks import decorator
from webks.models import User


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()
        if user:
            login_user(user=user)

    return redirect("/admin")


@app.route('/login', methods=['post'])
def login_usr():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')

        user = utils.check_login(username=username,
                                 password=password)
        if user:
            login_user(user=user)

    return room_list()


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@app.route("/room_list")
def room_list():
    cate_id = request.args.get('RoomCatalog_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    rooms = utils.read_rooms(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('room_list.html', rooms=rooms)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')
        if password == confirm:
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            username = request.form.get('username')
            #f = request.files["avatar"]
            #avatar_path = 'imgs/upload/%s' % f.filename
            #f.save(os.path.join(app.root_path, 'static/', avatar_path))
            if utils.register_user(firstname=firstname, lastname=lastname, email=email, username=username,
                                   password=password): #, avatar=avatar_path):
                return redirect('/')
            else:
                err_msg = "Hệ thống đang bị lỗi! Vui lòng thực hiện sau!"
        else:
            err_msg = "Mật khâu không khớp!"

    return render_template('customer/register.html', err_msg=err_msg)


#chuc nang them 1 sp vao gio hang tu Room
@app.route('/api/cart', methods=['post'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}   #tao ra gio hang rong

    cart = session['cart']

    #data = request.json
    #lay du lieu tu js/main.js
    data = json.loads(request.data)
    id = str(data.get("id"))
    room_number = data.get("room_number")
    price = data.get("price", 0)

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else: #chua co sp trong gio hang
        cart[id] = {
            "id": id,
            "room_number": room_number,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    quantity, amount = utils.cart_stats(cart)

    return jsonify({
        "total_quantity": quantity,
        "total_amount": amount
    })


#@app.route('/payment')
#def payment():
    #quantity, amount = utils.cart_stats(session.get('cart'))
    #cart_info = {
        #"total_quantity": quantity,
        #"total_amount": amount
    #}
    #return render_template('customer/payment.html', cart_info=cart_info)


@app.route('/api/pay', methods=['post'])
@decorator.login_required
def pay():
    if utils.add_receipt(session.get('cart')):
        del session['cart']  #thanh toan xong se xoa gio hang

        return jsonify({
            "message": "Add receipt successful!",
            "err_code": 200
        })

    return jsonify({
        "message": "Failed"
    })


@app.route('/cart')
def cart():
    quantity, amount = utils.cart_stats(session.get('cart'))
    cart_info = {
        "total_quantity": quantity,
        "total_amount": amount
    }
    return render_template('cart.html', cart_info=cart_info)


@app.route("/rooms/<int:room_id>")
def room_detail(room_id):
    room = utils.get_room_by_id(room_id=room_id)

    return render_template('room_detail.html',
                           room=room)


@app.route("/checkout")
def check_out():
    quantity, amount = utils.cart_stats(session.get('cart'))
    cart_info = {
        "total_quantity": quantity,
        "total_amount": amount
    }
    return render_template('checkout.html', cart_info=cart_info)


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/detail")
def detail():
    return render_template('room_detail.html')


if __name__ == "__main__":
    app.run(debug=True)
