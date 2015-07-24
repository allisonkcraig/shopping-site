"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request 
from flask_debugtoolbar import DebugToolbarExtension
import jinja2

import model


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""



    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # melons = model.Melon.get_by_id()
    # return render_template("all_melons.html",
    #                        melon_list=melons)
    total = 0
    melons_in_cart = []
    if session.get('cart_dict') is not None:
        for key, value in session['cart_dict'].items():
            # raise Exception("In for loop, accessing melons by ID from our session")
            new_melon = model.Melon.get_by_id(key)
            melons_in_cart.append((new_melon, value))
            total += new_melon.price * value
    print "MELONS IN CART", melons_in_cart

    # common_name = melons_in_cart[0][0]
    # qty =
    # price_per = melons_in_cart[0][1]
    # total_price
    # TODO: Display the contents of the shopping cart.
    #   - The cart is a list in session containing melons added

    return render_template("cart.html", melon_tuple=melons_in_cart, total=total)


@app.route("/add_to_cart/<string:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """
    print "******************************", session.get('cart_dict')
    if session.get('cart_dict') == None:
        session['cart_dict'] = {}
        print "****************************** MAKING DICT"
    # TODO: Finish shopping cart functionality
    #   - use session variables to hold cart list
    session['cart_dict'][id] = session['cart_dict'].get(id, 0) + 1
    print "******************************" , session
    flash("You added a "+ model.Melon.get_by_id(id).common_name + " to your cart!")
    # return "You added sa melon"
    return redirect('/cart')
    # return render_template("cart.html", cart_list=session['cart_dict'])


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email_input = request.form.get("email")
    pword_input = request.form.get("password")

    customer = model.Customer.get_by_email(email_input)
    if customer is None:
        flash("No such email")
        return redirect("/login")
    else:
        if pword_input != customer.pword:
            flash("Incorrect password")
            return redirect("/login")
        else:
            flash("Login successful!!")
            session['logged_in_customer_email'] = email_input
            return redirect("/melons")


@app.route("/logout")
def process_logout():
    del session['logged_in_customer_email']
    del session['cart_dict']
    flash("You have been logged out")
    return redirect("/melons")

@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
    app.debug = True
    DebugToolbarExtension(app)
