from flask import Flask, render_template, request, jsonify
import sqlite3
import math
import random

app = Flask(__name__)

def generate_bingo_numbers():
    """Generate a set of random bingo numbers for a card"""
    # B (1-15), I (16-30), N (31-45), G (46-60), O (61-75)
    numbers = []
    ranges = [(1,15), (16,30), (31,45), (46,60), (61,75)]
    
    for start, end in ranges:
        # Get 5 random numbers for each column
        column = random.sample(range(start, end + 1), 5)
        numbers.extend(column)
    
    # Make the center spot free
    numbers[12] = "FREE"
    
    return numbers

# Database initialization
def generate_production_batch():
    """Generate a unique production batch code"""
    return f"JDR-{random.randint(100000, 999999)}"

def init_db():
    conn = sqlite3.connect('bingo_cards.db')
    c = conn.cursor()
    
    # Drop existing table if it exists
    c.execute('DROP TABLE IF EXISTS cards')
    
    # Create cards table with bingo numbers
    c.execute('''CREATE TABLE cards
                 (card_number INTEGER PRIMARY KEY,
                  serial_number TEXT,
                  production_batch TEXT,
                  bingo_numbers TEXT)''')
    
    # Generate a production batch for all cards
    production_batch = generate_production_batch()
    
    # Check if we need to generate initial cards
    c.execute('SELECT COUNT(*) FROM cards')
    count = c.fetchone()[0]
    
    if count == 0:
        print("Generating initial 63,000 bingo cards...")
        for card_num in range(1, 63001):
            serial_num = generate_serial_number(card_num)
            bingo_nums = generate_bingo_numbers()
            bingo_nums_str = ','.join(map(str, bingo_nums))
            
            c.execute('''INSERT INTO cards 
                        (card_number, serial_number, production_batch, bingo_numbers) 
                        VALUES (?, ?, ?, ?)''',
                     (card_num, serial_num, production_batch, bingo_nums_str))
            
            if card_num % 1000 == 0:
                print(f"Generated {card_num} cards...")
                conn.commit()
        
        print("Finished generating all cards.")
        conn.commit()
    
    conn.close()

def generate_serial_number(card_number):
    # Calculate page, row, and column for the card
    page = (card_number - 1) // 36
    pos_in_page = (card_number - 1) % 36
    row = pos_in_page // 6
    col = pos_in_page % 6

    # Calculate serial number based on increments
    # Serial number increments by 300 per column and 50 per row
    # Offset for pages: each page has 1751 serial numbers (max serial on a page)
    offset = page * 1751

    serial = offset + (col * 300) + (row * 50) + 1
    return f"{serial:06d}"

def get_card_range(page):
    cards_per_page = 36
    start = (page - 1) * cards_per_page + 1
    end = start + cards_per_page - 1
    return start, end

@app.route('/api/card/<serial_number>')
def get_card_by_serial(serial_number):
    conn = sqlite3.connect('bingo_cards.db')
    c = conn.cursor()
    c.execute('SELECT card_number, serial_number, production_batch, bingo_numbers FROM cards WHERE serial_number = ?', (serial_number,))
    result = c.fetchone()
    conn.close()
    if result:
        card_number, serial_num, prod_batch, bingo_nums_str = result
        bingo_numbers = [ 'FREE' if num == 'FREE' else int(num) for num in bingo_nums_str.split(',') ]
        return {
            'card_number': card_number,
            'serial_number': serial_num,
            'production_batch': prod_batch,
            'bingo_numbers': bingo_numbers
        }
    else:
        return {'error': 'Card not found'}, 404

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    # No longer handling search_serial here, search is via API now
    
    # Calculate total pages
    total_cards = 63000
    cards_per_page = 36
    total_pages = math.ceil(total_cards / cards_per_page)
    
    # Get cards for current page
    start, end = get_card_range(page)
    
    # Fetch cards data from database
    conn = sqlite3.connect('bingo_cards.db')
    c = conn.cursor()
    
    cards = []
    for i in range(6):  # 6 rows
        row = []
        for j in range(6):  # 6 columns
            card_num = start + i * 6 + j
            if card_num <= end:
                c.execute('''SELECT serial_number, production_batch, bingo_numbers 
                           FROM cards WHERE card_number = ?''', (card_num,))
                result = c.fetchone()
                if result:
                    serial_num, prod_batch, bingo_nums_str = result
                    bingo_numbers = [
                        'FREE' if num == 'FREE' else int(num) 
                        for num in bingo_nums_str.split(',')
                    ]
                    row.append({
                        'card_number': card_num,
                        'serial_number': serial_num,
                        'production_batch': prod_batch,
                        'bingo_numbers': bingo_numbers
                    })
        cards.append(row)
    
    conn.close()
    
    return render_template('index.html',
                         cards=cards,
                         page=page,
                         total_pages=total_pages)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)
