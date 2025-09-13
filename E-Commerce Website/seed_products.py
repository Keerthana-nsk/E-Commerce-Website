import sqlite3

# Sample product list
products = [
    ("White Shirt", 499.0, "shirt1.jpg", "Comfortable cotton white shirt."),
    ("Running Shoes", 1299.0, "shoes1.jpg", "Durable and stylish running shoes."),
    ("Smartphone", 9999.0, "phone1.jpg", "Affordable smartphone with great features.")
]

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Insert products into the table
for name, price, image, description in products:
    cursor.execute(
        "INSERT INTO products (name, price, image, description) VALUES (?, ?, ?, ?)",
        (name, price, image, description)
    )

conn.commit()
conn.close()

print("✅ Sample products added successfully!")
