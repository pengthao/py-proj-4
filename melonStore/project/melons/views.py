from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from project.models import melon_list, Melon
from project.melons.forms import AddForm
from pprint import pprint

melons_blueprint = Blueprint('melons', __name__,template_folder='templates/melons')

@melons_blueprint.route('/all_melons')
def all_melons():

    melons = melon_list()
    for melon in melons:
        session[melon.melon_id] = melon.to_dict()
    
    return render_template('all_melons.html', melons=melons)


@melons_blueprint.route('/melon_details/<melon_id>', methods=["GET", "POST"])
def melon_details(melon_id):
    print(f'melon id {melon_id}') 
    session_melon = session.get(str(melon_id), {})
    print(f"session melon before dictionary {session_melon}")
    melon = Melon.from_dict(session_melon)


    print(f'just melon {melon}') 
    print(f"session melon {session_melon}")
    print(f"session cart {session['cart']}")
    form = AddForm()

    if request.method == "POST":
        if form.validate_on_submit():
            print("Validation is successful.")
            
            melon_update = None

            if 'cart' not in session:
                session['cart'] = []
                print('cart initialized empty list')

            print(session['cart'])

            for mel in session['cart']:
                print(f"mel for mel in cart {mel}")
                if mel['melon_id'] == melon_id:
                    mel['quantity'] += int(form.quantity.data)
                    mel['subtotal'] = mel['price'] * mel['quantity']
                    print(f'melon in session{mel}') 
                    melon_update = mel
                    print(f'melon update {melon_update}')
                    session.modified = True
                    flash(f'{melon.common_name} has been updated!')
                    break 

            if melon_update is None:
                new_melon = Melon.to_dict(melon)
                new_melon['quantity'] = int(form.quantity.data)
                new_melon['subtotal'] = new_melon['price'] * new_melon['quantity']
                print(f'melon {new_melon}') 
                session['cart'].append(new_melon)
                session.modified = True
                flash(f'{melon.common_name} has been added to cart!')
                print(f"session cart {session['cart']}")   
            return redirect(url_for('cart.view_cart'))
        
    return render_template('melon_details.html', melon=melon, form=form)