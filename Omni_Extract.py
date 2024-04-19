import streamlit as st
from utils import st_def

st_def.st_logo(title='Welcome 👋 Omni Extract', page_title="Welcome!",)
st.image("./images/receipttextextraction.png")

st.markdown("""
    #### 🚀 Template-Based OCR (Optical Character Recognition) 🍨
    Description: Using pre-defined templates to extract text from receipts based on the expected layout and structure.
    
    **Limitations**:
    — Relies on consistent and standardized receipt formats, which is rarely the case in real-world scenarios.
    — Struggles with variations in receipt layouts, such as different fonts, spacing, or orientations.
    — Requires creating and maintaining a large number of templates to accommodate different receipt formats.
    — Limited flexibility and adaptability to handle new or unseen receipt formats.

        ### 📄Rule-Based Text Extraction📚:
    Description: Defining a set of rules and regular expressions to extract specific information from receipts based on patterns and keywords.
    **Limitations**:
    — Requires extensive domain knowledge and manual effort to define and maintain the rules.
    — Rules can become complex and difficult to manage as the variety of receipt formats increases.
    — Struggles with handling variations in terminology, abbreviations, or language used in receipts.
    — Limited scalability and adaptability to new receipt formats or changes in existing ones.    
        
        ### 🔍 Python Libraries for Traditional Machine Learning Approaches📰
    `scikit-learn (sklearn)`: scikit-learn is a widely used Python library for machine learning tasks.
    It provides a comprehensive set of tools for data preprocessing, feature extraction, model training, and evaluation.
    scikit-learn offers various machine learning algorithms, including Support Vector Machines (SVM), Random Forests, and more.

    `NLTK` (Natural Language Toolkit):NLTK is a popular Python library for natural language processing (NLP) tasks. It provides utilities for text preprocessing, tokenization, stemming, and feature extraction.
    NLTK can be used in conjunction with scikit-learn for text-based machine learning tasks.

    `spaCy`: spaCy is another powerful NLP library for Python.
    It offers advanced features for text preprocessing, named entity recognition, part-of-speech tagging, and more.
    spaCy can be used to extract additional features from the receipt text to enhance the machine learning models.

    **Limitations of Traditional Approaches**:
    The traditional approaches to receipt text extraction suffer from several limitations that hinder their effectiveness and scalability:

    1. Lack of Flexibility: Traditional approaches struggle to handle the wide variety of receipt formats and layouts encountered in real-world scenarios. They often rely on fixed templates or rules, making them inflexible and difficult to adapt to new or unseen receipt formats.
    2. Manual Effort and Domain Knowledge: Traditional approaches often require significant manual effort and domain expertise to define templates, rules, or features for text extraction. This process can be time-consuming and requires continuous updates and maintenance as receipt formats evolve.
    3. Limited Scalability: As the volume and variety of receipts increase, traditional approaches face challenges in scaling efficiently. Manual data entry becomes impractical, and rule-based systems become complex and difficult to manage.
    4. Sensitivity to Variations: Traditional approaches are sensitive to variations in receipt layouts, fonts, spacing, or terminology. They may struggle to accurately extract information when faced with inconsistencies or deviations from expected patterns.
    5. Lack of Contextual Understanding: Traditional approaches often lack the ability to understand the contextual meaning and relationships between different elements in a receipt. They rely on predefined patterns and fail to capture the nuances and semantics of the text.
    6. Limited Language Support: Traditional approaches may have limited support for multiple languages or may require separate models or rules for each language, making it challenging to process receipts from different regions or countries.

   # 🍨 Text Extraction App Using Streamlit and OpenAI Vision
    """)
st.image("./images/zhang.gif")
