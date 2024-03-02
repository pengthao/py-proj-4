from flask import Blueprint, render_template, redirect, url_for, session, request
from project.cart.forms import EditForm



cart_blueprint = Blueprint('cart', __name__,template_folder='templates/cart')

@cart_blueprint.route('/view_cart')
def view_cart():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    
    melon_list = []
    order_total = 0.00
    for melons in session['cart']:
        print(f'melons in session cart {melons}')
        melon_list.append(melons)
        melons['subtotal'] = melons['quantity'] * melons['price']
        order_total += melons['subtotal']

    print(f'melon list {melon_list}')

    return render_template('cart.html', melon_list=melon_list, order_total=order_total, form=EditForm())

@cart_blueprint.route("/empty-cart")
def empty_cart():
   session['cart'] = []
   print(session['cart'])
   return redirect(url_for('cart.view_cart'))

@cart_blueprint.route('/edit_cart/<melon_id>', methods=['GET', 'POST'])
def edit_cart(melon_id):

    form = EditForm()

    if request.method == "POST":
        if form.validate_on_submit():
            print("Validation is successful.")

            for mel in session['cart']:
                if mel['melon_id'] == melon_id:
                    mel['quantity'] = int(form.quantity.data)
                    mel['subtotal'] = mel['price'] * mel['quantity']
                    session.modified = True
            return redirect(url_for('cart.view_cart'))
    return render_template('view_cart.html', form=form, melon_id=melon_id)