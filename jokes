import sqlite3
import random
from faker import Faker

# Connect to the SQLite database
conn = sqlite3.connect('social_network.db')
c = conn.cursor()

# Create relationships table
c.execute('''CREATE TABLE IF NOT EXISTS relationships
             (id INTEGER PRIMARY KEY,
              person1 TEXT,
              person2 TEXT,
              relationship_type TEXT,
              start_date TEXT)''')

# Function to generate fake relationships
def generate_fake_relationships(num_records):
    fake = Faker()
    relationship_types = ['friend', 'family', 'colleague', 'spouse']
    for _ in range(num_records):
        person1 = fake.name()
        person2 = fake.name()
        relationship_type = random.choice(relationship_types)
        start_date = fake.date()
        c.execute("INSERT INTO relationships (person1, person2, relationship_type, start_date) VALUES (?, ?, ?, ?)",
                  (person1, person2, relationship_type, start_date))

# Generate 100 fake relationships
generate_fake_relationships(100)

# Commit changes and close connection
conn.commit()
conn.close()
