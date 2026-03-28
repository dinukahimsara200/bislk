"""
app.py — BisLK Flask Application Entry Point
Run with:  python app.py
Access at: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from db import get_db
from datetime import datetime, timedelta
from functools import wraps
import math

# ─────────────────────────────────────────────
#  App & Config
# ─────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = 'bislk_dev_secret_2025'   # change to os.urandom(24) in production

# ── XAMPP MySQL defaults ──────────────────────
app.config['DB_HOST']     = 'localhost'
app.config['DB_USER']     = 'root'
app.config['DB_PASSWORD'] = ''             # XAMPP default: no password
app.config['DB_NAME']     = 'bislk_db'

bcrypt = Bcrypt(app)


# ─────────────────────────────────────────────
#  CUSTOM JINJA FILTER — format MySQL TIME
# ─────────────────────────────────────────────
@app.template_filter('format_time')
def format_time_filter(t):
    if t is None:
        return '—'
    if isinstance(t, timedelta):
        total = int(t.total_seconds())
        h     = total // 3600
        m     = (total % 3600) // 60
        period = 'AM' if h < 12 else 'PM'
        h12    = h % 12 or 12
        return f'{h12:02d}:{m:02d} {period}'
    if hasattr(t, 'strftime'):
        return t.strftime('%I:%M %p')
    return str(t)


# ─────────────────────────────────────────────
#  AUTH DECORATORS
# ─────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please sign in to continue.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated


def owner_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('owner_id'):
            flash('Please sign in as a business owner to continue.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────────────
#  Context processor
# ─────────────────────────────────────────────
@app.context_processor
def inject_globals():
    try:
        with get_db() as (conn, cur):
            cur.execute("SELECT * FROM categories ORDER BY name")
            categories = cur.fetchall()
    except Exception:
        categories = []

    return dict(
        nav_categories  = categories,
        current_year    = datetime.now().year,
        current_user    = {
            'id':   session.get('user_id'),
            'name': session.get('user_name'),
        } if session.get('user_id') else None,
        current_owner   = {
            'id':   session.get('owner_id'),
            'name': session.get('owner_name'),
        } if session.get('owner_id') else None,
    )


# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────
@app.route('/')
def home():
    with get_db() as (conn, cur):
        cur.execute("SELECT * FROM categories ORDER BY name")
        categories = cur.fetchall()

        cur.execute("""
            SELECT * FROM vw_business_ratings
            WHERE review_count > 0
            ORDER BY avg_rating DESC, review_count DESC
            LIMIT 6
        """)
        top_rated = cur.fetchall()

        if top_rated:
            ids = tuple(b['business_id'] for b in top_rated)
            fmt = ','.join(['%s'] * len(ids))
            cur.execute(f"""
                SELECT business_id, image_url FROM business_images
                WHERE business_id IN ({fmt}) AND is_primary = 1
            """, ids)
            img_map = {r['business_id']: r['image_url'] for r in cur.fetchall()}
            for b in top_rated:
                b['primary_image'] = img_map.get(b['business_id'], '/static/img/placeholder.jpg')

    return render_template('home.html', categories=categories, top_rated=top_rated)


# ─────────────────────────────────────────────
#  SEARCH
# ─────────────────────────────────────────────
@app.route('/search')
def search():
    q           = request.args.get('q', '').strip()
    category_id = request.args.get('category_id', '')
    city        = request.args.get('city', '').strip()

    conditions, params = [], []

    if q:
        conditions.append("(b.name LIKE %s OR b.description LIKE %s OR b.address LIKE %s)")
        params += [f'%{q}%', f'%{q}%', f'%{q}%']
    if category_id:
        conditions.append("b.category_id = %s")
        params.append(category_id)
    if city:
        conditions.append("b.city LIKE %s")
        params.append(f'%{city}%')

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    with get_db() as (conn, cur):
        cur.execute(f"""
            SELECT b.business_id, b.name, b.city, b.address, b.phone,
                   c.name AS category, c.icon AS category_icon,
                   COALESCE(vbr.avg_rating, 0)    AS avg_rating,
                   COALESCE(vbr.review_count, 0)  AS review_count,
                   img.image_url AS primary_image
            FROM businesses b
            JOIN categories c ON b.category_id = c.category_id
            LEFT JOIN vw_business_ratings vbr ON b.business_id = vbr.business_id
            LEFT JOIN business_images img
                   ON b.business_id = img.business_id AND img.is_primary = 1
            {where}
            ORDER BY avg_rating DESC, b.name ASC
        """, params)
        results = cur.fetchall()

        cur.execute("SELECT DISTINCT city FROM businesses ORDER BY city")
        cities = [r['city'] for r in cur.fetchall()]

        cur.execute("SELECT * FROM categories ORDER BY name")
        categories = cur.fetchall()

    return render_template('search.html',
                           results=results, query=q,
                           selected_category=category_id, selected_city=city,
                           cities=cities, categories=categories,
                           result_count=len(results))


# ─────────────────────────────────────────────
#  CATEGORY LISTING
# ─────────────────────────────────────────────
@app.route('/category/<slug>')
def category(slug):
    with get_db() as (conn, cur):
        cur.execute("SELECT * FROM categories WHERE slug = %s", (slug,))
        cat = cur.fetchone()
        if not cat:
            flash('Category not found.', 'danger')
            return redirect(url_for('home'))

        cur.execute("""
            SELECT b.business_id, b.name, b.city, b.address,
                   COALESCE(vbr.avg_rating, 0)   AS avg_rating,
                   COALESCE(vbr.review_count, 0) AS review_count,
                   img.image_url AS primary_image
            FROM businesses b
            LEFT JOIN vw_business_ratings vbr ON b.business_id = vbr.business_id
            LEFT JOIN business_images img
                   ON b.business_id = img.business_id AND img.is_primary = 1
            WHERE b.category_id = %s
            ORDER BY avg_rating DESC
        """, (cat['category_id'],))
        businesses = cur.fetchall()

    return render_template('search.html',
                           results=businesses, query='',
                           selected_category=str(cat['category_id']),
                           selected_city='', cities=[], categories=[],
                           result_count=len(businesses), page_title=cat['name'])


# ─────────────────────────────────────────────
#  BUSINESS DETAIL
# ─────────────────────────────────────────────
@app.route('/business/<int:business_id>')
def business_detail(business_id):
    with get_db() as (conn, cur):
        cur.execute("""
            SELECT b.*, c.name AS category_name, c.slug AS category_slug,
                   COALESCE(vbr.avg_rating, 0)   AS avg_rating,
                   COALESCE(vbr.review_count, 0) AS review_count
            FROM businesses b
            JOIN categories c ON b.category_id = c.category_id
            LEFT JOIN vw_business_ratings vbr ON b.business_id = vbr.business_id
            WHERE b.business_id = %s
        """, (business_id,))
        business = cur.fetchone()

        if not business:
            flash('Business not found.', 'danger')
            return redirect(url_for('home'))

        cur.execute("""
            SELECT * FROM business_images
            WHERE business_id = %s ORDER BY is_primary DESC
        """, (business_id,))
        images = cur.fetchall()

        cur.execute("""
            SELECT r.*, u.full_name AS reviewer_name
            FROM reviews r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.business_id = %s
            ORDER BY r.created_at DESC
        """, (business_id,))
        reviews = cur.fetchall()

        extension = None
        slug = business['category_slug']
        if slug == 'restaurants':
            cur.execute("SELECT * FROM restaurants WHERE business_id = %s", (business_id,))
            extension = cur.fetchone()
        elif slug == 'hotels':
            cur.execute("SELECT * FROM hotels WHERE business_id = %s", (business_id,))
            extension = cur.fetchone()
        elif slug == 'salons':
            cur.execute("SELECT * FROM salons WHERE business_id = %s", (business_id,))
            extension = cur.fetchone()

        cur.execute("""
            SELECT rating, COUNT(*) AS count
            FROM reviews WHERE business_id = %s
            GROUP BY rating ORDER BY rating DESC
        """, (business_id,))
        rating_breakdown = {row['rating']: row['count'] for row in cur.fetchall()}

        already_reviewed = False
        if session.get('user_id'):
            cur.execute("""
                SELECT 1 FROM reviews
                WHERE user_id = %s AND business_id = %s LIMIT 1
            """, (session['user_id'], business_id))
            already_reviewed = cur.fetchone() is not None

    return render_template('business.html',
                           business=business, images=images, reviews=reviews,
                           extension=extension, rating_breakdown=rating_breakdown,
                           already_reviewed=already_reviewed)


# ─────────────────────────────────────────────
#  NEARBY BUSINESSES
# ─────────────────────────────────────────────
@app.route('/nearby')
def nearby():
    lat_raw = request.args.get('lat')
    lon_raw = request.args.get('lon')

    user_lat = user_lon = user_city = None
    if session.get('user_id'):
        try:
            with get_db() as (conn, cur):
                cur.execute(
                    "SELECT city, latitude, longitude FROM users WHERE user_id = %s",
                    (session['user_id'],))
                u = cur.fetchone()
                if u and u['latitude'] and u['longitude']:
                    user_lat  = float(u['latitude'])
                    user_lon  = float(u['longitude'])
                    user_city = u['city']
        except Exception:
            pass

    if not lat_raw or not lon_raw:
        return render_template('nearby.html', searched=False, results=[],
                               lat=user_lat, lon=user_lon,
                               user_city=user_city, radius=5.0)

    try:
        lat    = float(lat_raw)
        lon    = float(lon_raw)
        radius = float(request.args.get('radius', 5.0))
        radius = max(0.5, min(radius, 50.0))
    except ValueError:
        flash('Invalid coordinates. Please try again.', 'danger')
        return redirect(url_for('nearby'))

    with get_db() as (conn, cur):
        cur.execute("""
            SELECT b.business_id, b.name, b.city, b.address,
                   c.name AS category, c.slug AS category_slug, c.icon AS category_icon,
                   COALESCE(vbr.avg_rating,   0) AS avg_rating,
                   COALESCE(vbr.review_count, 0) AS review_count,
                   img.image_url AS primary_image,
                   ROUND(6371 * 2 * ASIN(SQRT(
                     POWER(SIN(RADIANS(b.latitude  - %s) / 2), 2) +
                     COS(RADIANS(%s)) * COS(RADIANS(b.latitude)) *
                     POWER(SIN(RADIANS(b.longitude - %s) / 2), 2)
                   )), 2) AS distance_km
            FROM businesses b
            JOIN  categories c ON b.category_id = c.category_id
            LEFT JOIN vw_business_ratings vbr ON b.business_id = vbr.business_id
            LEFT JOIN business_images img
                   ON b.business_id = img.business_id AND img.is_primary = 1
            WHERE b.latitude IS NOT NULL AND b.longitude IS NOT NULL
            HAVING distance_km <= %s
            ORDER BY distance_km ASC
            LIMIT 20
        """, (lat, lat, lon, radius))
        results = cur.fetchall()

    return render_template('nearby.html', searched=True, results=results,
                           lat=lat, lon=lon, user_city=user_city,
                           radius=radius, result_count=len(results))


# ─────────────────────────────────────────────
#  SIGN UP
# ─────────────────────────────────────────────
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('user_id') or session.get('owner_id'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        role      = request.form.get('role', 'user')
        full_name = request.form.get('full_name', '').strip()
        email     = request.form.get('email', '').strip().lower()
        password  = request.form.get('password', '')
        confirm   = request.form.get('confirm_password', '')
        phone     = request.form.get('phone', '').strip() or None

        city      = request.form.get('city', '').strip() or None
        latitude  = request.form.get('latitude', '').strip() or None
        longitude = request.form.get('longitude', '').strip() or None
        try:
            latitude  = float(latitude)  if latitude  else None
        except ValueError:
            latitude  = None
        try:
            longitude = float(longitude) if longitude else None
        except ValueError:
            longitude = None

        if not all([full_name, email, password, confirm]):
            flash('All fields except phone are required.', 'danger')
            return render_template('signup.html', role=role)

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html', role=role)

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('signup.html', role=role)

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            with get_db() as (conn, cur):
                if role == 'owner':
                    cur.execute("SELECT 1 FROM owners WHERE email = %s", (email,))
                    if cur.fetchone():
                        flash('An owner account with that email already exists.', 'danger')
                        return render_template('signup.html', role=role)
                    cur.execute("""
                        INSERT INTO owners (full_name, email, password_hash, phone)
                        VALUES (%s, %s, %s, %s)
                    """, (full_name, email, pw_hash, phone))
                else:
                    cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
                    if cur.fetchone():
                        flash('A user account with that email already exists.', 'danger')
                        return render_template('signup.html', role=role)
                    cur.execute("""
                        INSERT INTO users (full_name, email, password_hash, phone,
                                           city, latitude, longitude)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (full_name, email, pw_hash, phone, city, latitude, longitude))

            flash(f'Account created! Please sign in as a{"n owner" if role == "owner" else " user"}.', 'success')
            return redirect(url_for('login', tab=role))

        except Exception as e:
            flash(f'Registration error: {str(e)}', 'danger')

    role = request.args.get('tab', 'user')
    return render_template('signup.html', role=role)


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id') or session.get('owner_id'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        role     = request.form.get('role', 'user')
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        next_url = request.form.get('next', '')

        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('login.html', role=role, next=next_url)

        try:
            with get_db() as (conn, cur):
                if role == 'owner':
                    cur.execute("SELECT * FROM owners WHERE email = %s", (email,))
                else:
                    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                account = cur.fetchone()

            if not account or not bcrypt.check_password_hash(account['password_hash'], password):
                flash('Incorrect email or password.', 'danger')
                return render_template('login.html', role=role, next=next_url)

            session.clear()
            if role == 'owner':
                session['owner_id']   = account['owner_id']
                session['owner_name'] = account['full_name']
                session['role']       = 'owner'
            else:
                session['user_id']   = account['user_id']
                session['user_name'] = account['full_name']
                session['role']      = 'user'
            flash(f'Welcome back, {account["full_name"]}!', 'success')

            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('home'))

        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')

    role     = request.args.get('tab', 'user')
    next_url = request.args.get('next', '')
    return render_template('login.html', role=role, next=next_url)


# ─────────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────────
@app.route('/logout', methods=['POST'])
def logout():
    name = session.get('user_name') or session.get('owner_name', '')
    session.clear()
    flash(f'You have been signed out. See you soon, {name}!', 'info')
    return redirect(url_for('home'))


# ─────────────────────────────────────────────
#  ADD BUSINESS
# ─────────────────────────────────────────────
@app.route('/business/add', methods=['GET', 'POST'])
@owner_required
def add_business():
    with get_db() as (conn, cur):
        cur.execute("SELECT * FROM categories ORDER BY name")
        categories = cur.fetchall()

    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        address     = request.form.get('address', '').strip()
        city        = request.form.get('city', '').strip()
        latitude    = request.form.get('latitude') or None
        longitude   = request.form.get('longitude') or None
        phone       = request.form.get('phone', '').strip()
        email       = request.form.get('email', '').strip()
        website     = request.form.get('website', '').strip()
        description = request.form.get('description', '').strip()
        category_id = request.form.get('category_id')
        image_url   = request.form.get('image_url', '').strip()
        owner_id    = session['owner_id']

        if not all([name, address, city, category_id]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('add_business.html', categories=categories)

        try:
            with get_db() as (conn, cur):
                cur.execute("""
                    INSERT INTO businesses
                        (name, address, city, latitude, longitude,
                         phone, email, website, description,
                         category_id, owner_id, is_verified)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0)
                """, (name, address, city, latitude, longitude,
                      phone, email, website, description, category_id, owner_id))
                new_id = cur.lastrowid

                if image_url:
                    cur.execute("""
                        INSERT INTO business_images (business_id, image_url, is_primary)
                        VALUES (%s, %s, 1)
                    """, (new_id, image_url))

                cur.execute("SELECT slug FROM categories WHERE category_id = %s", (category_id,))
                cat_row = cur.fetchone()
                slug = cat_row['slug'] if cat_row else ''

                if slug == 'restaurants':
                    cur.execute("""
                        INSERT INTO restaurants
                            (business_id, cuisine_type, price_range, has_delivery, seating_capacity)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (new_id,
                          request.form.get('cuisine_type', 'Sri Lankan'),
                          request.form.get('price_range', '$$'),
                          1 if request.form.get('has_delivery') else 0,
                          request.form.get('seating_capacity') or None))
                elif slug == 'hotels':
                    cur.execute("""
                        INSERT INTO hotels
                            (business_id, star_rating, total_rooms, has_pool,
                             check_in_time, check_out_time)
                        VALUES (%s,%s,%s,%s,%s,%s)
                    """, (new_id,
                          request.form.get('star_rating', 3),
                          request.form.get('total_rooms') or None,
                          1 if request.form.get('has_pool') else 0,
                          request.form.get('check_in_time', '14:00'),
                          request.form.get('check_out_time', '12:00')))
                elif slug == 'salons':
                    cur.execute("""
                        INSERT INTO salons
                            (business_id, services, gender_served, by_appointment)
                        VALUES (%s,%s,%s,%s)
                    """, (new_id,
                          request.form.get('services', ''),
                          request.form.get('gender_served', 'Unisex'),
                          1 if request.form.get('by_appointment') else 0))

            flash(f'"{name}" was added successfully!', 'success')
            return redirect(url_for('business_detail', business_id=new_id))

        except Exception as e:
            flash(f'Error adding business: {str(e)}', 'danger')

    return render_template('add_business.html', categories=categories)


# ─────────────────────────────────────────────
#  SUBMIT REVIEW
# ─────────────────────────────────────────────
@app.route('/review/add', methods=['POST'])
@login_required
def add_review():
    business_id = request.form.get('business_id')
    rating      = request.form.get('rating')
    title       = request.form.get('title', '').strip()
    body        = request.form.get('body', '').strip()
    user_id     = session['user_id']

    if not all([business_id, rating]):
        flash('Rating is required.', 'danger')
        return redirect(url_for('business_detail', business_id=business_id))

    try:
        with get_db() as (conn, cur):
            cur.execute("""
                INSERT INTO reviews (user_id, business_id, rating, title, body)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, business_id, rating, title, body))
        flash('Your review was submitted. Thank you!', 'success')
    except Exception:
        flash('Could not submit review — you may have already reviewed this business.', 'warning')

    return redirect(url_for('business_detail', business_id=business_id))


# ─────────────────────────────────────────────
#  REPORTS
# ─────────────────────────────────────────────
@app.route('/reports')
def reports():
    """
    Four balanced analytics reports using simple, explainable SQL.
    Only uses: JOIN, GROUP BY, COUNT, AVG — no subqueries.

      1. Latest Business Registrations  (table only)
      2. Total Reviews per Category     (table + doughnut chart)
      3. Average Rating per Category    (table + bar chart)
      4. Platform Activity by City      (table + bar chart)
    """
    with get_db() as (conn, cur):

        # ── Report 1: Latest 10 business registrations ──────────────────────
        cur.execute("""
            SELECT b.business_id, b.name, b.city,
                   c.name AS category, b.created_at
            FROM businesses b
            JOIN categories c ON b.category_id = c.category_id
            ORDER BY b.created_at DESC
            LIMIT 10
        """)
        latest_businesses = cur.fetchall()

        # ── Report 2: Total reviews per category ────────────────────────────
        cur.execute("""
            SELECT c.name          AS category,
                   COUNT(r.review_id) AS total_reviews
            FROM categories c
            JOIN businesses b ON b.category_id = c.category_id
            JOIN reviews r    ON r.business_id  = b.business_id
            GROUP BY c.name
            ORDER BY total_reviews DESC
        """)
        reviews_per_category = cur.fetchall()

        # ── Report 3: Average rating per category ────────────────────────────
        cur.execute("""
            SELECT c.name                   AS category,
                   ROUND(AVG(r.rating), 1)  AS avg_rating
            FROM categories c
            JOIN businesses b ON b.category_id = c.category_id
            JOIN reviews r    ON r.business_id  = b.business_id
            GROUP BY c.name
            ORDER BY avg_rating DESC
        """)
        avg_rating_per_category = cur.fetchall()

        # ── Report 4: Platform activity by city ─────────────────────────────
        cur.execute("""
            SELECT b.city,
                   COUNT(DISTINCT b.business_id) AS total_businesses,
                   COUNT(r.review_id)            AS total_reviews
            FROM businesses b
            LEFT JOIN reviews r ON b.business_id = r.business_id
            GROUP BY b.city
            ORDER BY total_businesses DESC
        """)
        city_activity = cur.fetchall()

        # ── Report 5: User map points (lat/lon per user) ─────────────────────
        cur.execute("""
            SELECT city, latitude, longitude
            FROM users
            WHERE latitude IS NOT NULL
              AND longitude IS NOT NULL
        """)
        user_map_points = [
            {
                'city':      row['city'] or 'Unknown',
                'latitude':  float(row['latitude']),
                'longitude': float(row['longitude']),
            }
            for row in cur.fetchall()
        ]

        # ── Report 5: User count per city (sidebar table) ────────────────────
        cur.execute("""
            SELECT city,
                   COUNT(*) AS user_count
            FROM users
            WHERE latitude IS NOT NULL
              AND longitude IS NOT NULL
            GROUP BY city
            ORDER BY user_count DESC
        """)
        user_city_counts = cur.fetchall()

        # ── Total Users Query (NEW) ──────────────────────────────────────────
        cur.execute("SELECT COUNT(*) AS count FROM users")
        total_users_result = cur.fetchone()
        total_users = total_users_result['count'] if total_users_result else 0

    return render_template('reports.html',
                           latest_businesses=latest_businesses,
                           reviews_per_category=reviews_per_category,
                           avg_rating_per_category=avg_rating_per_category,
                           city_activity=city_activity,
                           user_map_points=user_map_points,
                           user_city_counts=user_city_counts,
                           total_users=total_users)                           


# ─────────────────────────────────────────────
#  ER DIAGRAM
# ─────────────────────────────────────────────
@app.route('/er-diagram')
def er_diagram():
    return render_template('er_diagram.html')


# ─────────────────────────────────────────────
#  SQL QUERIES PAGE
# ─────────────────────────────────────────────
@app.route('/sql-queries')
def sql_queries():
    return render_template('sql_queries.html')


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)