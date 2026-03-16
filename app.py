from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'diecast_secret_key' # For session management

# Expanded Inventory (20 Cars) with Gallery and Descriptions
products = [
    {
        "id": 1, "name": "Porsche 911 GT3", "scale": "1:24", "price": 12000, "image": "porsche.png", "category": "Sports", "specs": "Highly detailed interior, opening doors, rubber tires.",
        "gallery": ["porsche.png", "porsche_side.png", "porsche_rear.png"],
        "description": "The Porsche 911 GT3 is a high-performance homologation model of the Porsche 911 sports car. It is a line of high-performance models, which began with the 1973 911 Carrera RS. This 1:24 scale model features precision casting and authentic paint colors."
    },
    {
        "id": 2, "name": "Lamborghini Huracán", "scale": "1:18", "price": 23000, "image": "lambo.png", "category": "Supercar", "specs": "Engine detail, steerable wheels, premium gloss finish.",
        "gallery": ["lambo.png", "lambo_detail.png", "hero.png"],
        "description": "The Lamborghini Huracán is a sports car manufactured by Italian automotive manufacturer Lamborghini replacing the previous V10 offering, the Gallardo. This 1:18 scale replica features a full opening engine bay and steerable front wheels."
    },
    {
        "id": 3, "name": "Bugatti Chiron", "scale": "1:18", "price": 24800, "image": "bugatti.png", "category": "Hypercar", "specs": "Active rear wing, carbon fiber textures, luxury packaging.",
        "gallery": ["bugatti.png", "bugatti_side.png", "lambo.png"],
        "description": "The Bugatti Chiron is a mid-engine two-seater sports car developed and manufactured in Molsheim, France by Bugatti Engineering GmbH. This model highlights the active rear wing and intricate carbon fiber detailing."
    },
    {
        "id": 4, "name": "Shelby GT500", "scale": "1:24", "price": 10000, "image": "shelby.png", "category": "Muscle", "specs": "Racing stripes, chrome accents, opening hood/trunk.",
        "gallery": ["shelby.png", "shelby_engine.png", "porsche.png"],
        "description": "The Shelby GT500 is a high-performance variant of the Ford Mustang. This 1:24 scale diecast features iconic racing stripes and highly detailed chrome accents."
    },
    {
        "id": 5, "name": "Audi R8 V10 Plus", "scale": "1:24", "price": 10800, "image": "audi.png", "category": "Sports", "specs": "Quattro detailing, LED-style headlight moldings.",
        "gallery": ["audi.png", "hero.png", "lambo.png"],
        "description": "The Audi R8 is a mid-engine, 2-seater sports car, which uses Audi's trademark quattro permanent all-wheel drive system."
    },
    {
        "id": 6, "name": "Nissan GT-R (R35)", "scale": "1:64", "price": 2000, "image": "gtr.png", "category": "JDM", "specs": "Precision casting, authentic paint colors, collector box.",
        "gallery": ["gtr.png", "porsche.png", "hero.png"],
        "description": "The Nissan GT-R is a high-performance sports car and grand tourer produced by Nissan, unveiled in 2007."
    },
    {
        "id": 7, "name": "Ferrari F40", "scale": "1:18", "price": 28000, "image": "ferrari_f40.png", "category": "Classic", "specs": "Iconic pop-up lights, detailed engine bay.",
        "gallery": ["ferrari_f40.png", "lambo.png", "porsche.png"],
        "description": "The Ferrari F40 is a mid-engine, rear-wheel drive sports car built from 1987 to 1992."
    },
    {
        "id": 8, "name": "McLaren P1", "scale": "1:18", "price": 23600, "image": "mclaren_p1.png", "category": "Hypercar", "specs": "Aerodynamic sculpting, opening butterfly doors.",
        "gallery": ["mclaren_p1.png", "hero.png", "porsche.png"],
        "description": "The McLaren P1 is a limited-production mid-engine plug-in hybrid sports car."
    },
    {
        "id": 9, "name": "Ford Mustang 1967", "scale": "1:24", "price": 8800, "image": "mustang_1967.png", "category": "Classic", "specs": "Vintage interior, chrome bumpers, rubber tires.",
        "gallery": ["mustang_1967.png", "porsche.png", "lambo.png"],
        "description": "The 1967 Mustang was the first significant redesign of the original model."
    },
    {
        "id": 10, "name": "Dodge Challenger SRT", "scale": "1:24", "price": 9600, "image": "challenger.png", "category": "Muscle", "specs": "Widebody kit, detailed HEMI engine.",
        "gallery": ["challenger.png", "hero.png", "porsche.png"],
        "description": "The Dodge Challenger is a heavy-duty muscle car with legendary performance."
    },
    {
        "id": 11, "name": "BMW M4 Competition", "scale": "1:24", "price": 11200, "image": "bmw_m4.png", "category": "Sports", "specs": "Carbon roof detail, shadowline trim.",
        "gallery": ["bmw_m4.png", "hero.png", "lambo.png"],
        "description": "The BMW M4 is a high-performance version of the BMW 4 Series."
    },
    {
        "id": 12, "name": "Aston Martin DB11", "scale": "1:18", "price": 22000, "image": "aston_martin_db11.png", "category": "Luxury", "specs": "Bespoke interior, elegant metallic finish.",
        "gallery": ["aston_martin_db11.png", "hero.png", "lambo.png"],
        "description": "The Aston Martin DB11 is a grand tourer flagship."
    },
    {
        "id": 13, "name": "Mercedes-AMG GT", "scale": "1:24", "price": 11600, "image": "mercedes_amg_gt.png", "category": "Sports", "specs": "Panamericana grille, detailed cockpit.",
        "gallery": ["mercedes_amg_gt.png", "hero.png", "porsche.png"],
        "description": "The Mercedes-AMG GT is a grand tourer produced by Mercedes-AMG."
    },
    {
        "id": 14, "name": "Chevrolet Corvette C8", "scale": "1:18", "price": 20800, "image": "corvette_c8.png", "category": "Supercar", "specs": "Mid-engine detail, removable roof panel.",
        "gallery": ["corvette_c8.png", "hero.png", "porsche.png"],
        "description": "The Chevrolet Corvette (C8) is the eighth generation of the Corvette."
    },
    {
        "id": 15, "name": "Toyota Supra Mk4", "scale": "1:64", "price": 2240, "image": "supra_mk4.png", "category": "JDM", "specs": "Custom rims, aerodynamic wing.",
        "gallery": ["supra_mk4.png", "porsche.png", "hero.png"],
        "description": "The Toyota Supra is a legendary JDM icon."
    },
    {
        "id": 16, "name": "Pagani Huayra", "scale": "1:18", "price": 30400, "image": "pagani_detail.png", "category": "Hypercar", "specs": "Gullwing doors, exposed engine detail.",
        "gallery": ["pagani_detail.png", "lambo.png", "porsche.png"],
        "description": "The Pagani Huayra is a masterpiece of Italian engineering."
    },
    {
        "id": 17, "name": "Koenigsegg Jesko", "scale": "1:18", "price": 32000, "image": "jesko_detail.png", "category": "Hypercar", "specs": "Extreme downforce wings.",
        "gallery": ["jesko_detail.png", "porsche.png", "lambo.png"],
        "description": "The Koenigsegg Jesko is the ultimate track-focused hypercar."
    },
    {
        "id": 18, "name": "Volkswagen Golf GTI", "scale": "1:43", "price": 3600, "image": "golf_gti.png", "category": "Compact", "specs": "Plaid interior detail.",
        "gallery": ["golf_gti.png", "hero.png", "lambo.png"],
        "description": "The VW Golf GTI is the world's favorite hot hatch."
    },
    {
        "id": 19, "name": "Tesla Model S Plaid", "scale": "1:24", "price": 7600, "image": "tesla.png", "category": "EV", "specs": "Minimalist interior, yoke steering wheel detail.",
        "gallery": ["tesla.png", "hero.png", "porsche.png"],
        "description": "The Tesla Model S is the pinnacle of all-electric luxury."
    },
    {
        "id": 20, "name": "Rolls-Royce Cullinan", "scale": "1:18", "price": 36000, "image": "cullinan.png", "category": "Luxury", "specs": "Spirit of Ecstasy, suicide doors.",
        "gallery": ["cullinan.png", "porsche.png", "lambo.png"],
        "description": "The Rolls-Royce Cullinan is the absolute peak of luxury SUVs."
    }
]

# Mock Databases with Persistence
import json
import os

DB_FILE = 'db.json'

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"users": {}, "orders": {}, "carts": {}, "collections": {}}

def save_db():
    db_data = {
        "users": users,
        "orders": orders,
        "carts": carts,
        "collections": collections
    }
    with open(DB_FILE, 'w') as f:
        json.dump(db_data, f, indent=4)

db = load_db()
users = db.get("users", {})
orders = db.get("orders", {})
carts = db.get("carts", {})
collections = db.get("collections", {})

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def index():
    # Show all for filtering
    return render_template('index.html', products=products)

@app.route('/shop')
def shop():
    sort = request.args.get('sort', '')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    filtered_products = list(products)
    if sort == 'low-high':
        filtered_products.sort(key=lambda x: x['price'])
    elif sort == 'high-low':
        filtered_products.sort(key=lambda x: x['price'], reverse=True)
    
    # Pagination
    total_products = len(filtered_products)
    total_pages = (total_products + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = filtered_products[start:end]
    
    return render_template('shop.html', 
                          products=paginated_products, 
                          page=page, 
                          total_pages=total_pages,
                          sort=sort)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return redirect(url_for('shop'))
    
    # Suggest other products
    suggestions = [p for p in products if p['id'] != product_id][:4]
    
    return render_template('product_detail.html', product=product, suggestions=suggestions)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        password = request.form.get('password')
        
        if email in users:
            flash('Email already registered!', 'error')
            return redirect(url_for('signup'))
            
        users[email] = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'password': password
        }
        
        # Auto-sign-in
        session['user'] = email
        
        # Create empty order history for new users
        orders[email] = []
        save_db()
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('profile'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = email
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password', 'error')
            
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    email = session['user']
    user = users.get(email)
    user_orders = orders.get(email, [])
    
    return render_template('profile.html', user=user, orders=user_orders)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user' not in session:
        return {"success": False, "message": "Unauthorized"}, 401
    
    email = session['user']
    user = users.get(email)
    if not user:
        return {"success": False, "message": "User not found"}, 404

    # Update fields
    user['name'] = request.form.get('name', user['name'])
    user['phone'] = request.form.get('phone', user['phone'])
    user['address'] = request.form.get('address', user['address'])
    save_db()
    
    flash('Profile updated successfully!', 'success')
    return {"success": True, "message": "Profile updated"}

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user' not in session:
        return {"success": False, "message": "Please login first"}, 401
    
    email = session['user']
    product_id = request.json.get('product_id')
    product = next((p for p in products if p['id'] == int(product_id)), None)
    
    if not product:
        return {"success": False, "message": "Product not found"}, 404
        
    if email not in carts:
        carts[email] = []
    
    # Check if already in cart (incrementing qty not implemented for simplicity, just add)
    carts[email].append(product)
    save_db()
    return {"success": True, "message": f"{product['name']} added to cart", "count": len(carts[email])}

@app.route('/get_cart')
def get_cart():
    if 'user' not in session:
        return {"success": False, "items": []}
    
    email = session['user']
    items = carts.get(email, [])
    total = sum(item['price'] for item in items)
    return {"success": True, "items": items, "total": total}

@app.route('/add_to_collection', methods=['POST'])
def add_to_collection():
    if 'user' not in session:
        return {"success": False, "message": "Please login first"}, 401
    
    email = session['user']
    product_id = int(request.json.get('product_id'))
    
    if email not in collections:
        collections[email] = []
        
    if product_id not in collections[email]:
        collections[email].append(product_id)
        save_db()
        return {"success": True, "message": "Added to your collection"}
    else:
        return {"success": False, "message": "Already in your collection"}

@app.route('/get_collection')
def get_collection():
    if 'user' not in session:
        return {"success": False, "items": []}
    
    email = session['user']
    product_ids = collections.get(email, [])
    user_collection = [p for p in products if p['id'] in product_ids]
    return {"success": True, "items": user_collection}

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
