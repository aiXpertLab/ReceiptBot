import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

def st_sidebar():
    with st.sidebar:
        # store_link = st.text_input("Enter Your Store URL:",   value="http://hypech.com/StoreSpark", disabled=True, key="store_link")
        openai_api_key = st.text_input("OpenAI API Key (gpt-4)", key="chatbot_api_key", type="password")
        st.write("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
        add_vertical_space(2)
        st.write('Made with ❤️ by [aiXpertLab](https://hypech.com)')
    return openai_api_key
   
def st_logo(title="aiXpert!"):
    st.title(title)

    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            background-image: url(https://hypech.com/images/logo/st_receiptbot.png);
            background-size: 200px; /* Set the width and height of the image */
            background-repeat: no-repeat;
            padding-top: 80px;
            background-position: 15px 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def st_text_preprocessing_contents():
    st.markdown("""
        - Normalize Text
        - Remove Unicode Characters
        - Remove Stopwords
        - Perform Stemming and Lemmatization
    """)    


def st_read_pdf():
    st.markdown("""
Because OpenAI has a limit on the input prompt size, we would like to send the data to be summarized in parts. 
There can be multiple ways to split the text. For the sake of simplicity, we will divide the whole book on the basis of pages. 
A **better strategy** will be to split it on the basis of paragraphs. However, it will increase the number of API calls increasing the overall time.

We will store each page in a list and then summarize it.
    """)    
    st.image("./images/book.png")

def st_summary():
    st.markdown("Now we will start prompting. This is a matter of experiment to figure out the best prompt. However, there are a few basic guidelines on how to do it efficiently. In some upcoming articles, we will discuss the art of prompting in more detail. You can use the prompt for now, which has worked well for me. ")
    # st.image("./images/featureengineering.png")

def st_case_study():
        st.image("./images/NLP-Pipeline.png")
        # main_contents="""
        #     ### 🚀 Bridge the Gap: Chatbots for Every Store 🍨
        #     Tired of missing out on sales due to limited customer support options? Struggling to keep up with growing customer inquiries? Store Spark empowers you to seamlessly integrate a powerful ChatGPT-powered chatbot into your website, revolutionizing your customer service and boosting engagement. No coding required! No modifications for current site needed!
        #     ### 📄Key Features📚:
        #     -  🔍 No Coding Required: Say goodbye to developer fees and lengthy website updates. Store Spark’s user-friendly API ensures a smooth integration process.
        #     -  📰 Empower Your Business: Offer instant customer support, improve lead generation, and boost conversion rates — all with minimal setup effort.
        #     -  🍨 Seamless Integration: Maintain your existing website design and user experience. Store Spark seamlessly blends in, providing a unified customer journey.
        #     """
    
