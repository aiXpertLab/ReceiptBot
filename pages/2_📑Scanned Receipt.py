import streamlit as st, base64, json, re
import mysql.connector
from datetime import datetime
from utils import ai, st_def, db
import pandas as pd


st_def.st_logo(title='👋 Scanned Recepit Extract')
# tab1, tab2, tab3,tab4 = st.tabs(["Upload", "Display", "Save", "Database"])
tab1, tab2, tab3 = st.tabs(["Upload Receipt","Camera", "Display the Data"])

uploaded_file = None
base64_image = None
model = 'gpt-4-turbo'

with tab1:
    st.image("./data/scanned_sample.png")
    st.header("Upload Receipt")
    uploaded_file = st.file_uploader("Upload scanned receipt: ", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Receipt')
        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
        st.text(base64_image)
        st.success("Load successfully. Continue to next tab: Display")

with tab2:   
    camera_file = st.camera_input("Take a picture")
    if camera_file is not None:
        st.image(camera_file, caption='Receipt from Camera')
        base64_image = base64.b64encode(camera_file.read()).decode('utf-8')
        st.text(base64_image)
        st.success("Load successfully. Continue to next tab to Display")   

with tab3:
    if not base64_image:
        st.error('Please upload or take a picture of receipt.')
    else:
        openai_api_key= st_def.st_sidebar()
        if not openai_api_key:
            st.info('Please enter OpenAI’s API key to continue extract the receipt uploaded.')
        else: 
            var_for = """Given the receipt image provided, extract all relevant information and structure the output as detailed JSON that matches the database schema for storing receipt headers and line items. The receipt headers should include store name, slogan, address, store manager, phone number, transaction ID, date, time, cashier, subtotal, sales tax, total, gift card, charged amount, card type, authorization code, chip read, AID, issuer, policy ID, expiration date, survey message, survey website, user ID, password, and eligibility note. The line items should include SKU, description, details, and price for each item on the receipt. Exclude any sensitive information from the output. Format the JSON as follows:
                {"receipt_headers": {"store_name": "",                "slogan": "",                "address": "",                "store_manager": "",
                        "phone_number": "",                "transaction_id": "",                "date": "",                "time": "",
                        "cashier": "",                "subtotal": 0,                "sales_tax": 0,                "total": 0,
                        "gift_card": 0,                "charged_amount": 0,                "card_type": "",                "auth_code": "",
                        "chip_read": "",                "aid": "",                "issuer": "",                "policy_id": "",
                        "expiration_date": "",                "survey_message": "",                "survey_website": "",                "user_id": "",
                        "password": "",                "eligibility_note": ""            },
                    "line_items": [{"sku": "",                "description": "",                "details": "",                "price": 0}]}"""    

            receipt_data_str = ai.ai_vision(var_for = var_for, openai_api_key=openai_api_key, model_v=model, base64_image=base64_image)
            # with open('re.txt', 'w') as file:
            #     file.write(receipt_data_str)
            # st.write(receipt_data_str)

            # with open('re1.txt', 'r') as file:  receipt_data_str = file.read()
            
            start_index = receipt_data_str.find("{")    # Find the starting index of the JSON data (excluding the leading ```)
            end_index = receipt_data_str.rfind("}")+1   # Find the ending index of the JSON data (excluding the trailing ```)
            json_data = receipt_data_str[start_index:end_index] # Extract the JSON data as a substring

            receipt_dict = json.loads(json_data)
            
            col1, col2 = st.columns(2)

            with col1:
                st.header("Scanned Receipt")
                st.image(uploaded_file, caption='Uploaded Receipt')

            with col2:
                st.header("Extracted Data")
                st.write(receipt_dict)
            
            # db.mysql_insert_receipt(receipt_dict)

            # Display success message
            st.success("Message received successfully from the LLM.")
