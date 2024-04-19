import streamlit as st, time
from utils import st_def, ut_openai

st_def.st_logo(title = "Welcome 👋 to Summary!", page_title="Summary",)
st_def.st_summary()
openai_api_key= st_def.st_sidebar()
#------------------------------------------------------------------------
def init():
    if 'page_text' not in st.session_state:   
        st.error('Read PDF before continue ... ')
        return False
    elif not openai_api_key:
        st.error("Please add your OpenAI API key to continue.")
        return False
    else: 
        return True


def combine_chunks(summaries):
    chunks = []         # combine chunks of "summaries" array into one string of max 4000 characters
    summary = ""

    for sum in summaries:
        if len(sum) + len(summary) > 4000:
            chunks.append(summary)
            summary = ""
        summary += sum

    if len(chunks) == 0:        chunks.append(summary)
    return chunks

        
def main():
    if not init(): return

    page_text_array = st.session_state['page_text']         # array, store pages. len(text) is pages.
    print("Summarizing text..."+str(len(page_text_array)))

    combined_summaries = combine_chunks(page_text_array)
    print("Found " + str(len(combined_summaries)) + " chunks to summarize.")

    iterations = 1
    while True:
        if len(combined_summaries) <= 1:    break

        summaries_of_summaries = []
        # print summaries
        for i, summary in enumerate(combined_summaries):
            prompt =f"""
                Your task is to extract relevant information from a text on the page of a book. This information will be used to create a book summary.
                Extract relevant information from the following text, which is delimited with triple backticks.\
                Be sure to preserve the important details.
                Text: ```{combined_summaries[i]}```
            """
            #    st.write(f"Summarizing {i + 1} of {len(combined_summaries)}, iteration {iterations}...")
            st.markdown(f'<span style="color:blue">Summarizing {i + 1} of {len(combined_summaries)}, iteration {iterations}...</span>', unsafe_allow_html=True)
            sum_page = ut_openai.aichat(openai_api_key=openai_api_key, messages = [{"role": "user",   "content": prompt},])
            summaries_of_summaries.append(sum_page)
            st.text(sum_page)
            time.sleep(2)  #You can query the model only 3 times in a minute for free, so we need to put some delay

        st.write('summaries_of_summaries')
        st.write(summaries_of_summaries)
        combined_summaries = combine_chunks(summaries_of_summaries)
        st.text('combined_summaries')
        st.text(combined_summaries)
        iterations += 1

    # summarize last chunk
    
    with st.spinner("Summarizing last chunk..."):
        final_summary = ut_openai.aichat(openai_api_key=openai_api_key, messages = [{"role": "user",   "content": combined_summaries[0]},])
    st.header("Final Summary")
    st.write(final_summary)
    st.success("🚨Cheers!")


if __name__ == "__main__":
    main()

