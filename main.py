import streamlit as st
import langchain_helper as lch
import re
import time
import html

st.set_page_config(page_title="YouTube Q&A")

st.title("🎥 YouTube Video Q&A Assistant")

# Initialize session state for rate limiting
if "request_history" not in st.session_state:
    st.session_state.request_history = []

# Rate limiting constants
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_WINDOW = 5

def check_rate_limit():
    current_time = time.time()
    # Filter out requests older than the window
    st.session_state.request_history = [
        t for t in st.session_state.request_history 
        if current_time - t < RATE_LIMIT_WINDOW
    ]
    
    if len(st.session_state.request_history) >= MAX_REQUESTS_PER_WINDOW:
        return False
    
    st.session_state.request_history.append(current_time)
    return True

def sanitize_query(query: str) -> str:
    if not query:
        return ""
    # Strip leading/trailing whitespaces
    query = query.strip()
    # Replace multiple spaces/newlines with a single space
    query = re.sub(r'\s+', ' ', query)
    # Remove HTML tags
    query = re.sub(r'<[^>]+>', '', query)
    # Unescape HTML entities
    query = html.unescape(query)
    # Limit to reasonable length
    MAX_LENGTH = 500
    if len(query) > MAX_LENGTH:
        query = query[:MAX_LENGTH]
    return query

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
    elif not check_rate_limit():
        st.error(f"Rate limit exceeded. Please wait a moment before trying again. Maximum {MAX_REQUESTS_PER_WINDOW} requests per {RATE_LIMIT_WINDOW} seconds.")
    else:
        sanitized_query = sanitize_query(query)
        if not sanitized_query:
            st.error("Query contains no valid text after sanitization.")
        else:
            video_id = extract_video_id(video_url)
    
            if not video_id:
                st.error("Invalid YouTube URL")
            else:
                with st.spinner("Processing..."):
                    try:
                        vector_db = lch.create_vector_db(video_id)
                        response = lch.get_response_from_query(vector_db, sanitized_query)
            
                        st.success("Done!")
            
                        # Response display
                        st.subheader("Response:")
                        st.success(response)
                    except Exception as e:
                        st.error(f"An error occurred during processing: {e}")