import streamlit as st
import base64
import requests
import mysql.connector
import json
from datetime import datetime

# Streamlit app title
st.title("Receipt Extractor")

var_for = """
Given the receipt image provided, extract all relevant information and structure the output as detailed JSON that matches the database schema for storing receipt headers and line items.
The receipt headers should include store name, slogan, address, store manager, phone number, transaction ID, date, time, cashier, subtotal, sales tax, total, gift card, 
charged amount, card type, authorization code, chip read, AID, issuer, policy ID, expiration date, survey message, survey website, user ID, password, and eligibility note. 
The line items should include SKU, description, details, and price for each item on the receipt. Exclude any sensitive information from the output. Format the JSON as follows:

    {
    "receipt_headers": {
        "store_name": "",
        "slogan": "",
        "address": "",
        "store_manager": "",
        "phone_number": "",
        "transaction_id": "",+
        "date": "",
        "time": "",
        "cashier": "",
        "subtotal": 0,
        "sales_tax": 0,
        "total": 0,
        "gift_card": 0,
        "charged_amount": 0,
        "card_type": "",
        "auth_code": "",
        "chip_read": "",
        "aid": "",
        "issuer": "",
        "policy_id": "",
        "expiration_date": "",
        "survey_message": "",
        "survey_website": "",
        "user_id": "",
        "password": "",
        "eligibility_note": ""
    },
    "line_items": [
        {
        "sku": "",
        "description": "",
        "details": "",
        "price": 0
        }
    ]
    }"""

# Function to encode the image
def encode_image(image):
    return base64.b64encode(image.read()).decode('utf-8')

# Function to process the uploaded image and update the database
def process_image(image):
    base64_image = encode_image(image)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": var_for
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2048
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()
    receipt_data_str = response_json['choices'][0]['message']['content']

    # Find the JSON string within the extracted content
    receipt_data_json_str = receipt_data_str.split('```json')[1].split('```')[0].strip()
    receipt_data = json.loads(receipt_data_json_str)

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert into receipt_headers
    header_insert_query = """
    INSERT INTO receipt_headers (store_name, slogan, address, store_manager, phone_number, transaction_id, date, time, cashier, subtotal, sales_tax, total, gift_card, charged_amount, card_type, auth_code, chip_read, aid, issuer, policy_id, expiration_date, survey_message, survey_website, user_id, password, eligibility_note)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    header_info = receipt_data['receipt_headers']
    line_items = receipt_data['line_items']

    # Format date, time, and expiration_date
    formatted_date = datetime.strptime(header_info['date'], '%m/%d/%y').strftime('%Y-%m-%d')
    formatted_time = datetime.strptime(header_info['time'], '%I:%M %p').strftime('%H:%M:%S')
    formatted_expiration_date = datetime.strptime(header_info['expiration_date'], '%m/%d/%Y').strftime('%Y-%m-%d')

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

    return receipt_data

# Streamlit tabs
tab1, tab2 = st.tabs(["Upload Receipt", "Display the Data"])

with tab1:
    st.header("Upload Receipt")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Receipt', use_column_width=True)

        # Process the uploaded image
        receipt_data = process_image(uploaded_file)

        # Display success message
        st.success("Message received successfully from the LLM.")

        # Display the JSON output
        st.json(receipt_data)


with tab2:
    st.header("Display the Data")

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fetch all records from the receipt_headers table, excluding the time column
    cursor.execute("SELECT store_name, slogan, address, store_manager, phone_number, transaction_id, date, cashier, subtotal, sales_tax, total, gift_card, charged_amount, card_type, auth_code, chip_read, aid, issuer, policy_id, expiration_date, survey_message, survey_website, user_id, password, eligibility_note FROM receipt_headers;")
    headers = cursor.fetchall()

    # Display the headers in a table
    st.subheader("Receipt Headers")
    st.table(headers)

    # Fetch and display all records from the line_items table
    st.subheader("Line Items")
    cursor.execute("SELECT * FROM line_items;")
    items = cursor.fetchall()
    st.table(items)

    # Close the cursor and the connection
    cursor.close()
    conn.close()