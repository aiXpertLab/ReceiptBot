import os, mysql.connector, streamlit as st
from datetime import datetime

def mysql_conn():
    conn = mysql.connector.connect(
                host="mysql-omni-omni.b.aivencloud.com",
                port='21906',
                user="avnadmin",
                password= os.environ.get('MYSQL_PWD'),
                database = 'defaultdb',            )
    cursor = conn.cursor()
    return cursor, conn

def mysql_check():
    cursor, conn = mysql_conn()
    cursor.execute("SHOW TABLES;")
    # cursor.execute("DESCRIBE receipt_headers_allvarchar;")
    cursor.close()
    conn.close()


def mysql_create_receipt_table():
    cursor, conn = mysql_conn()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipt_headers (
            receipt_id INT AUTO_INCREMENT PRIMARY KEY,
            store_name VARCHAR(255),                slogan VARCHAR(255),                address VARCHAR(255),                store_manager VARCHAR(255),                phone_number VARCHAR(50),
            transaction_id VARCHAR(255),                date DATE,                time TIME,                cashier VARCHAR(255),                subtotal DECIMAL(10,2),
            sales_tax DECIMAL(10,2),            total DECIMAL(10,2),            gift_card DECIMAL(10,2),            charged_amount DECIMAL(10,2),            card_type VARCHAR(50),
            auth_code VARCHAR(50),                chip_read VARCHAR(50),                aid VARCHAR(50),                issuer VARCHAR(255),                policy_id VARCHAR(50),
            expiration_date DATE,                survey_message TEXT,                survey_website VARCHAR(255),                user_id VARCHAR(255),                password VARCHAR(255),                eligibility_note TEXT            )
        """)
    # Create line_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS line_items (
            line_item_id INT AUTO_INCREMENT PRIMARY KEY,
            receipt_id INT,                sku VARCHAR(255),                description VARCHAR(255),                details TEXT,                price DECIMAL(10,2),
            FOREIGN KEY (receipt_id) REFERENCES receipt_headers(receipt_id)            )
        """)
    conn.commit()
    cursor.close()
    conn.close()


def mysql_create_receipt_table_allvarchar():
    cursor, conn = mysql_conn()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipt_headers_allvarchar (
            receipt_id INT AUTO_INCREMENT PRIMARY KEY,
            store_name VARCHAR(255),                slogan VARCHAR(255),                address VARCHAR(255),                store_manager VARCHAR(255),                phone_number VARCHAR(50),
            transaction_id VARCHAR(255),                date VARCHAR(50),                time VARCHAR(50),                cashier VARCHAR(255),                subtotal DECIMAL(10,2),
            sales_tax DECIMAL(10,2),            total DECIMAL(10,2),            gift_card DECIMAL(10,2),            charged_amount DECIMAL(10,2),            card_type VARCHAR(50),
            auth_code VARCHAR(50),                chip_read VARCHAR(50),                aid VARCHAR(50),                issuer VARCHAR(255),                policy_id VARCHAR(50),
            expiration_date VARCHAR(50),                survey_message TEXT,                survey_website VARCHAR(255),                user_id VARCHAR(255),                password VARCHAR(255),                eligibility_note TEXT            )
        """)
    # Create line_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS line_items_allvarchar (
            line_item_id INT AUTO_INCREMENT PRIMARY KEY,
            receipt_id INT,     sku VARCHAR(255),   description VARCHAR(255),   details TEXT,   price DECIMAL(10,2),
            FOREIGN KEY (receipt_id) REFERENCES receipt_headers(receipt_id))
        """)
    conn.commit()
    cursor.close()
    conn.close()

def mysql_insert_receipt(receipt_data):
    cursor, conn = mysql_conn()
    # Insert into receipt_headers
    header_insert_query = """
        INSERT INTO receipt_headers (store_name, slogan, address, store_manager, phone_number, transaction_id, date, time, cashier, subtotal, sales_tax, total, gift_card, charged_amount, card_type, auth_code, chip_read, aid, issuer, policy_id, expiration_date, survey_message, survey_website, user_id, password, eligibility_note)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    header_info = receipt_data['receipt_headers']
    line_items = receipt_data['line_items']
    # Format date, time, and expiration_date
    formatted_date = datetime.strptime(header_info['date'], '%m/%d/%Y').strftime('%Y-%m-%d')
    formatted_time = datetime.strptime(header_info['time'], '%I:%M %p').strftime('%H:%M:%S')
    # formatted_expiration_date = datetime.strptime(header_info['expiration_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
    formatted_expiration_date = datetime.strptime(header_info['expiration_date'], '%m/%d/%Y').strftime('%Y-%m-%d') if header_info['expiration_date'] else '01/01/2023'
    formatted_expiration_date = datetime.strptime(header_info['expiration_date'], '%m/%d/%Y') if header_info['expiration_date'] else datetime.strptime('01/01/1000', '%m/%d/%Y')
    
    # Prepare header values
    header_values = (
        header_info['store_name'],
        header_info['slogan'],
        header_info['address'],
        header_info['store_manager'],
        header_info['phone_number'],
        header_info['transaction_id'],
        formatted_date,
        formatted_time,
        header_info['cashier'],
        header_info['subtotal'],
        header_info['sales_tax'],
        header_info['total'],
        header_info['gift_card'],
        header_info['charged_amount'],
        header_info['card_type'],
        header_info['auth_code'],
        header_info['chip_read'],
        header_info['aid'],
        header_info['issuer'],
        header_info['policy_id'],
        formatted_expiration_date,
        header_info['survey_message'],
        header_info['survey_website'],
        header_info['user_id'],
        header_info['password'],
        header_info['eligibility_note']
    )

    # Insert header values
    cursor.execute(header_insert_query, header_values)
    receipt_id = cursor.lastrowid

    # Prepare and insert line items
    line_item_insert_query = """
    INSERT INTO line_items (receipt_id, sku, description, details, price)
    VALUES (%s, %s, %s, %s, %s)
    """

    for item in line_items:
        price = float(item['price'])
        line_item_values = (
            receipt_id,
            item['sku'],
            item['description'],
            item.get('details', ''),
            price
        )

        cursor.execute(line_item_insert_query, line_item_values)

    # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    
    