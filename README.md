# AI-powered Receipt Bot

The application is designed to process electronic and scanned receipts. 
It sendsthese images to an LLM model, which extracts detailed information from the receipts. 
Then, it stores this information in a database. 

The app has two main parts: uploading and processing receipt images, and displaying the extracted data.

The `process_image(image)` function takes an uploaded image, encodes it, and then sends a request to OpenAI’s API with the encoded image and the instructions on what information to extract.

The response from OpenAI’s API, which includes the extracted data in JSON format, is then processed. 

The function extracts the relevant data from this JSON and inserts it into the MySQL database.

The database insertion involves two steps: first, inserting the receipt headerinformation, and then inserting details about each line item on the receipt.

