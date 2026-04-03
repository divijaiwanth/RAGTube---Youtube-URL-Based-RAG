import streamlit as st
import langchain_helper as lch
import re

st.set_page_config(page_title="YouTube Q&A")

st.title("🎥 YouTube Video Q&A Assistant")


# Extract video ID
def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/|shorts/)([^&?/]+)", url) 
    #using regex to extract the video ID from the URL, works for both regular and shortened(shorts) YouTube URLs
    return match.group(1) if match else None


# Form (single submit)
with st.form("qa_form"):
    video_url = st.text_input("Enter YouTube Video URL")
    query = st.text_input("Ask your question")

    submit = st.form_submit_button("Submit")


# On submit
if submit:
    if not video_url or not query:
        st.error("Please enter both video URL and question")
    else:
        video_id = extract_video_id(video_url)

        if not video_id:
            st.error("Invalid YouTube URL")
        else:
            with st.spinner("Processing..."):
                vector_db = lch.create_vector_db(video_id)
                response = lch.get_response_from_query(vector_db, query)

            st.success("Done!")

            # Response display
            st.subheader("Response:")
            st.success(response)