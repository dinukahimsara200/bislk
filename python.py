#!/usr/bin/env python3
"""
Simple CLI Tool for Business Directory Database
DBMS Mini Project - Insert data into businesses table
"""

import mysql.connector
from mysql.connector import Error
import sys

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',      # Default XAMPP username
    'password': '',      # Default XAMPP password (empty)
    'database': 'bislk_db'
}

def connect_db():
    """Connect to MySQL database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✓ Connected to database successfully!\n")
        return conn
    except Error as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPlease check:")
        print("  - XAMPP/MySQL is running")
        print("  - Database 'bislk_db' exists")
        print("  - Username/password is correct")
        sys.exit(1)

def show_menu():
    """Display main menu"""
    print("=" * 40)
    print("   BUSINESS DIRECTORY - CLI TOOL")
    print("=" * 40)
    print("1. Add new business")
    print("2. Exit")
    print("=" * 40)

def get_input(prompt, required=True, allow_empty=False):
    """Get user input with validation"""
    while True:
        value = input(prompt).strip()
        if not value and required and not allow_empty:
            print("  → This field is required. Please enter a value.")
            continue
        return value if value else None

def get_number_input(prompt, required=True):
    """Get numeric input with validation"""
    while True:
        value = input(prompt).strip()
        if not value:
            if required:
                print("  → This field is required.")
                continue
            return None
        try:
            return int(value)
        except ValueError:
            print("  → Please enter a valid number.")

def get_decimal_input(prompt, required=False):
    """Get decimal input for coordinates"""
    while True:
        value = input(prompt).strip()
        if not value:
            if required:
                print("  → This field is required.")
                continue
            return None
        try:
            return float(value)
        except ValueError:
            print("  → Please enter a valid number (e.g., 6.8935520).")

def show_categories():
    """Display available categories"""
    print("\nAvailable Categories:")
    print("  1: Restaurants")
    print("  2: Hotels")
    print("  3: Salons")
    print("  4: Spas")
    print("  5: Gyms")

def add_business(conn):
    """Add new business to database"""
    print("\n" + "=" * 40)
    print("   ADD NEW BUSINESS")
    print("=" * 40)

    # Get user input
    name = get_input("Business Name: ")
    address = get_input("Address: ")
    city = get_input("City: ")

    print("\nLocation (optional - press Enter to skip):")
    latitude = get_decimal_input("Latitude (e.g., 6.8935520): ", required=False)
    longitude = get_decimal_input("Longitude (e.g., 79.8507210): ", required=False)

    print("\nContact Information:")
    phone = get_input("Phone (optional): ", required=False)
    email = get_input("Email (optional): ", required=False)
    website = get_input("Website (optional): ", required=False)

    show_categories()
    category_id = get_number_input("Category ID (1-5): ")

    owner_id = get_number_input("Owner ID (optional): ", required=False)

    # Prepare SQL query
    query = """
        INSERT INTO businesses 
        (name, address, city, latitude, longitude, phone, email, website, category_id, owner_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (name, address, city, latitude, longitude, phone, email, website, category_id, owner_id)

    # Execute query
    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

        print("\n" + "=" * 40)
        print(f"✓ SUCCESS! Business added with ID: {cursor.lastrowid}")
        print("=" * 40)

        cursor.close()

    except Error as e:
        print(f"\n✗ Error inserting data: {e}")
        print("Please check:")
        print("  - Category ID exists (1-5)")
        print("  - Owner ID exists (if provided)")

def main():
    """Main program loop"""
    print("\nStarting Business Directory CLI...\n")

    # Connect to database
    conn = connect_db()

    while True:
        show_menu()
        choice = input("Enter your choice (1-2): ").strip()

        if choice == '1':
            add_business(conn)
        elif choice == '2':
            print("\nGoodbye! Closing connection...")
            conn.close()
            print("✓ Database connection closed.")
            break
        else:
            print("\nInvalid choice. Please enter 1 or 2.\n")

if __name__ == "__main__":
    main()