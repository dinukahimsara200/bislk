-- ============================================================
--  BisLK — Sri Lankan Business Directory
--  Sample Data  (Step 3)
--  Run AFTER schema.sql
-- ============================================================

USE bislk_db;

-- ============================================================
--  1. CATEGORIES  (5 categories)
-- ============================================================
INSERT INTO categories (name, slug, description, icon) VALUES
('Restaurants',  'restaurants', 'Dining, cafes, takeaways and everything in between', 'fa-utensils'),
('Hotels',       'hotels',      'From budget guesthouses to luxury resorts',           'fa-hotel'),
('Salons',       'salons',      'Hair, beauty, grooming and wellness studios',          'fa-scissors'),
('Spas',         'spas',        'Relaxation, massage therapy and holistic treatments',  'fa-spa'),
('Gyms',         'gyms',        'Fitness centres, crossfit boxes and yoga studios',     'fa-dumbbell');


-- ============================================================
--  2. USERS  (10 users — passwords are bcrypt hashes of
--             "Password1!" for demo purposes only)
-- ============================================================
INSERT INTO users (full_name, email, password_hash, phone, joined_at) VALUES
('Kavindu Perera',    'kavindu@email.com',  '$2b$12$DEMO_HASH_kavindu_perera_001', '0771234561', '2024-01-10 09:00:00'),
('Sanduni Fernando',  'sanduni@email.com',  '$2b$12$DEMO_HASH_sanduni_fernando02', '0712345672', '2024-02-14 11:30:00'),
('Ravindu Silva',     'ravindu@email.com',  '$2b$12$DEMO_HASH_ravindu_silva_0003', '0762345683', '2024-03-05 08:15:00'),
('Ishara Jayawardena','ishara@email.com',   '$2b$12$DEMO_HASH_ishara_jayaward04',  '0751234594', '2024-04-22 14:00:00'),
('Dineth Wickrama',   'dineth@email.com',   '$2b$12$DEMO_HASH_dineth_wickrama05', '0741234505', '2024-05-01 10:45:00'),
('Nimesha Dissanayake','nimesha@email.com', '$2b$12$DEMO_HASH_nimesha_dissana06', '0771234516', '2024-06-18 16:20:00'),
('Tharaka Bandara',   'tharaka@email.com',  '$2b$12$DEMO_HASH_tharaka_bandara07', '0712345627', '2024-07-03 09:50:00'),
('Malsha Rathnayake', 'malsha@email.com',   '$2b$12$DEMO_HASH_malsha_rathnaya08', '0762345638', '2024-08-11 13:00:00'),
('Sahan Mendis',      'sahan@email.com',    '$2b$12$DEMO_HASH_sahan_mendis_009', '0751234549', '2024-09-25 17:30:00'),
('Dilani Kumari',     'dilani@email.com',   '$2b$12$DEMO_HASH_dilani_kumari_010', '0741234550', '2024-10-08 08:00:00');


-- ============================================================
--  3. BUSINESSES  (15 businesses — Colombo, Kandy, Galle)
--     category_id: 1=Restaurant 2=Hotel 3=Salon 4=Spa 5=Gym
--     owner_id references users table
-- ============================================================
INSERT INTO businesses
    (name, address, city, province, latitude, longitude, phone, email, website,
     description, category_id, owner_id, is_verified) VALUES

-- ── RESTAURANTS (category_id = 1) ─────────────────────────
('The Rice Bowl',
 '45 Galle Road, Colombo 03', 'Colombo', 'Western',
 6.8935520, 79.8507210, '0112345601', 'info@ricebowl.lk', 'https://ricebowl.lk',
 'Authentic Sri Lankan rice and curry buffet with over 20 curries daily. A local favourite since 2010.',
 1, 1, 1),

('Spice Garden Restaurant',
 '12 Kandy Road, Peradeniya, Kandy', 'Kandy', 'Central',
 7.2565890, 80.5985420, '0812345602', 'hello@spicegarden.lk', NULL,
 'Traditional Kandyan cuisine served in a lush garden setting overlooking the Mahaweli River.',
 1, 2, 1),

('The Fort Café',
 '18 Church Street, Galle Fort, Galle', 'Galle', 'Southern',
 6.0296840, 80.2166710, '0912345603', 'fortcafe@email.com', 'https://fortcafe.lk',
 'Charming café inside a 17th-century Dutch colonial building. Known for hoppers, fresh seafood and Ceylon tea.',
 1, 3, 1),

('Colombo Kitchen',
 '77 Duplication Road, Colombo 05', 'Colombo', 'Western',
 6.8807030, 79.8630140, '0112345604', 'cokitchen@email.com', NULL,
 'Contemporary Sri Lankan fusion restaurant. Think kottu reinvented and pol sambol tapas.',
 1, 4, 0),

('Lakeside Diner',
 '5 Lake Drive, Kandy', 'Kandy', 'Central',
 7.2905010, 80.6332780, '0812345605', 'lakeside@email.com', NULL,
 'Relaxed diner by Kandy Lake offering a mix of local and Western dishes at budget-friendly prices.',
 1, NULL, 0),

-- ── HOTELS (category_id = 2) ──────────────────────────────
('Grand Colombo Hotel',
 '1 Galle Face Terrace, Colombo 03', 'Colombo', 'Western',
 6.9058120, 79.8480610, '0112345606', 'reservations@grandcolombo.lk', 'https://grandcolombo.lk',
 'Five-star oceanfront luxury hotel with panoramic Indian Ocean views, a rooftop pool and award-winning restaurants.',
 2, 5, 1),

('Kandy Hills Resort',
 '28 Rajapihilla Road, Kandy', 'Kandy', 'Central',
 7.3003540, 80.6423120, '0812345607', 'info@kandyhills.lk', 'https://kandyhills.lk',
 'Boutique hill-country resort nestled in a tea estate. Private plunge pools and daily guided hikes.',
 2, 6, 1),

('Galle Fort Hotel',
 '28 Church Street, Galle Fort, Galle', 'Galle', 'Southern',
 6.0302190, 80.2168450, '0912345608', 'stay@galleforthotel.lk', 'https://galleforthotel.lk',
 'Heritage boutique hotel within the UNESCO-listed Galle Fort. Colonial architecture meets modern luxury.',
 2, 7, 1),

('City Stay Inn',
 '34 Maradana Road, Colombo 10', 'Colombo', 'Western',
 6.9208850, 79.8617320, '0112345609', 'citystay@email.com', NULL,
 'Clean, affordable 3-star hotel ideal for business travellers. Free Wi-Fi and airport shuttle included.',
 2, NULL, 0),

-- ── SALONS (category_id = 3) ──────────────────────────────
('Glamour Studio',
 '88 Havelock Road, Colombo 05', 'Colombo', 'Western',
 6.8844200, 79.8698340, '0112345610', 'glamour@email.com', NULL,
 'Premier unisex salon offering cutting, colouring, keratin treatments and bridal packages.',
 3, 8, 1),

('Tresses Hair Lounge',
 '14 Peradeniya Road, Kandy', 'Kandy', 'Central',
 7.2934780, 80.6345010, '0812345611', 'tresses@email.com', NULL,
 'Modern hair salon specialising in balayage, Japanese straightening and scalp treatments.',
 3, 9, 0),

('The Groom Room',
 '7 Light House Street, Galle Fort, Galle', 'Galle', 'Southern',
 6.0289560, 80.2172100, '0912345612', 'groomroom@email.com', NULL,
 'Upscale men-only grooming lounge. Classic wet shaves, beard sculpting and hot towel treatments.',
 3, 10, 1),

-- ── SPAS (category_id = 4) ────────────────────────────────
('Serenity Spa Colombo',
 '120 Union Place, Colombo 02', 'Colombo', 'Western',
 6.9117600, 79.8554830, '0112345613', 'serenity@email.com', 'https://serenityspa.lk',
 'Award-winning urban spa. Ayurvedic therapies, Swedish massage and a dedicated couple''s suite.',
 4, 1, 1),

-- ── GYMS (category_id = 5) ────────────────────────────────
('Iron Republic Gym',
 '55 R.A. de Mel Mawatha, Colombo 03', 'Colombo', 'Western',
 6.8959360, 79.8558020, '0112345614', 'iron@email.com', NULL,
 'High-performance fitness centre with Olympic lifting platforms, a 25m indoor track and personal trainers.',
 5, 2, 1),

('Flex Fitness Kandy',
 '9 Katugastota Road, Kandy', 'Kandy', 'Central',
 7.3072150, 80.6348780, '0812345615', 'flex@email.com', NULL,
 'Community gym with modern equipment, group classes and monthly membership plans. Open 24/7.',
 5, 3, 0);


-- ============================================================
--  4. EXTENSION TABLES
-- ============================================================

-- ── Restaurants ──────────────────────────────────────────
--  business_id 1-5 are restaurants
INSERT INTO restaurants (business_id, cuisine_type, price_range, has_delivery, seating_capacity) VALUES
(1, 'Sri Lankan',         '$$',   1, 120),
(2, 'Sri Lankan',         '$$',   0,  80),
(3, 'Sri Lankan, Seafood','$$$',  0,  45),
(4, 'Sri Lankan Fusion',  '$$$',  1,  60),
(5, 'Sri Lankan, Western','$',    0,  90);

-- ── Hotels ───────────────────────────────────────────────
--  business_id 6-9 are hotels
INSERT INTO hotels (business_id, star_rating, total_rooms, has_pool, check_in_time, check_out_time) VALUES
(6, 5, 220, 1, '15:00:00', '12:00:00'),
(7, 4,  28, 1, '14:00:00', '11:00:00'),
(8, 4,  14, 0, '14:00:00', '12:00:00'),
(9, 3,  65, 0, '13:00:00', '11:00:00');

-- ── Salons ───────────────────────────────────────────────
--  business_id 10-12 are salons
INSERT INTO salons (business_id, services, gender_served, by_appointment) VALUES
(10, 'Haircut, Colouring, Keratin, Bridal, Makeup', 'Unisex', 1),
(11, 'Haircut, Balayage, Straightening, Scalp Treatment', 'Female', 1),
(12, 'Haircut, Wet Shave, Beard Sculpting, Hot Towel', 'Male', 1);


-- ============================================================
--  5. BUSINESS IMAGES
--     Using placeholder image paths (replace with real URLs
--     once the app is deployed / images are uploaded).
-- ============================================================
INSERT INTO business_images (business_id, image_url, caption, is_primary) VALUES
-- The Rice Bowl (id=1)
(1, '/static/img/businesses/rice_bowl_1.jpg',  'Our famous rice and curry spread',   1),
(1, '/static/img/businesses/rice_bowl_2.jpg',  'Indoor dining area',                 0),
-- Spice Garden (id=2)
(2, '/static/img/businesses/spice_garden_1.jpg','Garden seating by the river',        1),
(2, '/static/img/businesses/spice_garden_2.jpg','Kandyan platter',                    0),
-- The Fort Café (id=3)
(3, '/static/img/businesses/fort_cafe_1.jpg',  'Colonial façade at dusk',            1),
(3, '/static/img/businesses/fort_cafe_2.jpg',  'Hopper breakfast set',               0),
-- Colombo Kitchen (id=4)
(4, '/static/img/businesses/colomkitchen_1.jpg','Modern interior',                   1),
-- Lakeside Diner (id=5)
(5, '/static/img/businesses/lakeside_1.jpg',   'Lake view terrace',                  1),
-- Grand Colombo Hotel (id=6)
(6, '/static/img/businesses/grand_col_1.jpg',  'Ocean-view infinity pool',           1),
(6, '/static/img/businesses/grand_col_2.jpg',  'Deluxe king room',                   0),
(6, '/static/img/businesses/grand_col_3.jpg',  'Lobby atrium',                       0),
-- Kandy Hills (id=7)
(7, '/static/img/businesses/kandyhills_1.jpg', 'Hillside villa with plunge pool',    1),
(7, '/static/img/businesses/kandyhills_2.jpg', 'Tea estate sunrise view',            0),
-- Galle Fort Hotel (id=8)
(8, '/static/img/businesses/gallefort_1.jpg',  'Colonial courtyard',                 1),
(8, '/static/img/businesses/gallefort_2.jpg',  'Heritage suite',                     0),
-- City Stay Inn (id=9)
(9, '/static/img/businesses/citystay_1.jpg',   'Standard double room',               1),
-- Glamour Studio (id=10)
(10,'/static/img/businesses/glamour_1.jpg',    'Reception and styling area',         1),
-- Tresses (id=11)
(11,'/static/img/businesses/tresses_1.jpg',    'Modern wash stations',               1),
-- The Groom Room (id=12)
(12,'/static/img/businesses/groomroom_1.jpg',  'Classic barber chairs',              1),
-- Serenity Spa (id=13)
(13,'/static/img/businesses/serenity_1.jpg',   'Treatment room with ambient lighting',1),
(13,'/static/img/businesses/serenity_2.jpg',   'Couple''s suite',                    0),
-- Iron Republic (id=14)
(14,'/static/img/businesses/ironrep_1.jpg',    'Olympic lifting platforms',          1),
(14,'/static/img/businesses/ironrep_2.jpg',    'Indoor track',                       0),
-- Flex Fitness (id=15)
(15,'/static/img/businesses/flex_1.jpg',       'Main gym floor',                     1);


-- ============================================================
--  6. REVIEWS  (33 reviews across all 15 businesses)
--     Spread across different users and ratings to produce
--     realistic averages for the reports.
-- ============================================================
INSERT INTO reviews (user_id, business_id, rating, title, body, created_at) VALUES

-- The Rice Bowl (id=1)
(2, 1, 5, 'Best rice and curry in Colombo!',
 'The variety here is unreal. Over 20 curries to choose from and every single one is authentic. Worth every rupee.',
 '2024-02-20 12:30:00'),
(3, 1, 4, 'Great food, slightly slow service',
 'Loved the dhal and the jackfruit curry especially. Service was a bit slow on weekends but the food makes up for it.',
 '2024-04-11 13:15:00'),
(5, 1, 5, 'A true Sri Lankan experience',
 'Brought my overseas cousins here and they were blown away. This is the real deal — no tourist traps.',
 '2024-07-02 14:00:00'),

-- Spice Garden (id=2)
(1, 2, 5, 'Magical setting, incredible food',
 'Sitting by the Mahaweli River eating authentic Kandyan dishes — doesn''t get better than this. The ambul thiyal was perfect.',
 '2024-03-15 19:00:00'),
(4, 2, 4, 'Lovely atmosphere',
 'The garden setting is beautiful. Food was great but portion sizes could be a little bigger for the price.',
 '2024-06-22 20:00:00'),
(6, 2, 5, 'Hidden gem in Kandy',
 'Stumbled upon this place while exploring Peradeniya. The kiri bath dessert was out of this world.',
 '2024-09-01 18:30:00'),

-- The Fort Café (id=3)
(7, 3, 5, 'Perfect spot inside Galle Fort',
 'Historic building, excellent hoppers and the best cup of Ceylon tea I''ve had. Tourist-friendly but not overpriced.',
 '2024-01-28 09:30:00'),
(8, 3, 4, 'Charming café with great vibes',
 'Love the colonial atmosphere. The egg hopper was crispy and the coconut sambol was on point.',
 '2024-05-14 10:00:00'),

-- Colombo Kitchen (id=4)
(9, 4, 3, 'Interesting concept, mixed results',
 'The fusion idea is fun and the kottu reinvention was good. Some dishes felt too experimental though.',
 '2024-08-05 20:30:00'),
(10, 4, 4, 'Creative and delicious mostly',
 'The pol sambol tapas are a must-try. A little pricey but you''re paying for the creativity.',
 '2024-09-18 19:15:00'),

-- Lakeside Diner (id=5)
(1, 5, 4, 'Great value by the lake',
 'Very affordable with a lovely view. Nothing fancy but solid Sri Lankan home cooking done well.',
 '2024-04-30 12:00:00'),
(3, 5, 3, 'Decent but nothing special',
 'Food was okay, nothing memorable. The view is the main attraction. Would go again for a casual lunch.',
 '2024-07-17 13:30:00'),

-- Grand Colombo Hotel (id=6)
(4, 6, 5, 'Absolute luxury — exceeded expectations',
 'The ocean view from the rooftop pool at sunset is something I will never forget. Staff were incredibly attentive.',
 '2024-03-22 22:00:00'),
(5, 6, 5, 'Best hotel in Colombo, no contest',
 'Stayed for our anniversary. The room, the food, the spa — everything was flawless. Worth every penny.',
 '2024-06-10 10:00:00'),
(2, 6, 4, 'Outstanding but pricey',
 'You get what you pay for here. The facilities are world-class. Only minor complaint is the parking is a bit chaotic.',
 '2024-10-03 11:30:00'),

-- Kandy Hills Resort (id=7)
(6, 7, 5, 'A dream escape in the hills',
 'Our private plunge pool overlooked a tea estate. Woke up to mist over the hills every morning. Simply stunning.',
 '2024-04-05 09:00:00'),
(7, 7, 5, 'Best resort stay in Sri Lanka',
 'The guided tea estate hike is a must. Accommodation is intimate and the staff remember your name — personal touch is rare.',
 '2024-08-19 08:30:00'),

-- Galle Fort Hotel (id=8)
(8, 8, 5, 'Heritage and luxury in one',
 'Staying inside the fort walls is a truly unique experience. The building is beautifully restored and the room was stunning.',
 '2024-02-12 20:00:00'),
(9, 8, 4, 'Wonderful boutique hotel',
 'Small but perfectly formed. Every detail is thought through. No pool but you have the ocean a short walk away.',
 '2024-07-28 15:00:00'),

-- City Stay Inn (id=9)
(10, 9, 3, 'Good value for business travel',
 'Clean rooms and the airport shuttle was punctual. Not a luxury experience but everything worked as expected.',
 '2024-05-20 08:00:00'),
(1,  9, 3, 'Functional and affordable',
 'Exactly what you''d expect from a 3-star. Good Wi-Fi, comfortable bed, nothing more nothing less.',
 '2024-09-10 10:00:00'),

-- Glamour Studio (id=10)
(2, 10, 5, 'Transformed my hair completely',
 'Came in with damaged, dull hair and left looking like a different person. The keratin treatment lasted months.',
 '2024-03-08 16:00:00'),
(4, 10, 4, 'Great salon, good atmosphere',
 'Clean, professional and the stylist actually listened to what I wanted. Will be a regular.',
 '2024-06-25 14:30:00'),

-- Tresses Hair Lounge (id=11)
(3, 11, 5, 'Finally found my balayage person!',
 'Been looking for a salon in Kandy that can do proper balayage. Tresses absolutely nailed it. Booked next appointment already.',
 '2024-04-18 15:00:00'),
(5, 11, 4, 'Lovely salon, great results',
 'The scalp treatment was so relaxing. Staff are friendly and the pricing is very reasonable for the quality.',
 '2024-08-07 16:00:00'),

-- The Groom Room (id=12)
(6, 12, 5, 'Best barbershop experience I have had',
 'The hot towel shave was incredible. Felt like a completely different person walking out. Worth every rupee.',
 '2024-05-03 11:00:00'),
(7, 12, 5, 'Proper classic barbershop in the fort',
 'Love the vintage aesthetic and the skill here is real. My beard has never looked this sharp.',
 '2024-09-22 10:30:00'),

-- Serenity Spa (id=13)
(8, 13, 5, 'A true sanctuary in the city',
 'The Ayurvedic massage was deeply therapeutic. The ambiance is perfect — I completely switched off for two hours.',
 '2024-02-29 17:00:00'),
(9, 13, 5, 'Couples suite was incredible',
 'Booked the couple''s suite for our anniversary. Thoughtful touches everywhere. Highly recommend the hot stone package.',
 '2024-07-14 18:30:00'),
(10,13, 4, 'Very good but slightly overpriced',
 'Treatment quality is excellent. Just feels a little expensive. Would appreciate a loyalty discount.',
 '2024-10-01 14:00:00'),

-- Iron Republic Gym (id=14)
(1, 14, 5, 'Best equipped gym in Colombo',
 'Finally a gym with proper Olympic platforms and bumper plates. The 25m track is a game changer for conditioning.',
 '2024-03-30 07:30:00'),
(2, 14, 4, 'Excellent gym, can get crowded',
 'Equipment quality is top tier. Gets busy between 6-8pm so try to go off-peak. Trainers are very knowledgeable.',
 '2024-08-12 06:45:00'),

-- Flex Fitness Kandy (id=15)
(3, 15, 4, 'Great community gym',
 'Monthly membership is very affordable and the equipment is well-maintained. Love that it''s open 24/7.',
 '2024-06-14 08:00:00'),
(4, 15, 3, 'Good for the price',
 'Does the job for a regular workout. Nothing fancy but it''s clean and accessible. Group classes are a nice bonus.',
 '2024-09-05 09:15:00');


-- ============================================================
--  QUICK VERIFICATION QUERIES
--  Run these after inserting data to confirm everything looks
--  correct before starting the Flask app.
-- ============================================================

-- Count rows in each table
SELECT 'users'            AS tbl, COUNT(*) AS rows_count FROM users
UNION ALL
SELECT 'categories',               COUNT(*)         FROM categories
UNION ALL
SELECT 'businesses',               COUNT(*)         FROM businesses
UNION ALL
SELECT 'business_images',          COUNT(*)         FROM business_images
UNION ALL
SELECT 'reviews',                  COUNT(*)         FROM reviews
UNION ALL
SELECT 'restaurants',              COUNT(*)         FROM restaurants
UNION ALL
SELECT 'hotels',                   COUNT(*)         FROM hotels
UNION ALL
SELECT 'salons',                   COUNT(*)         FROM salons;

-- Preview business ratings via the view
SELECT name, category, city, avg_rating, review_count
FROM vw_business_ratings
ORDER BY avg_rating DESC, review_count DESC;
