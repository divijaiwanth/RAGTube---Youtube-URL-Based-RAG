from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM

#Free embeddings
embeddings = HuggingFaceEmbeddings()

def create_vector_db(video_id: str) -> FAISS:
    # Step 1: Get transcript
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    text = " ".join([t.text for t in transcript])

    #Step 2: Convert to Document
    documents = [Document(page_content=text)]

    # Step 3: Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(documents)

    # Step 4: Store in FAISS
    db = FAISS.from_documents(docs, embeddings)

    return db

def get_response_from_query(db: FAISS, query: str) -> str:
    docs = db.similarity_search(query,k=2)
    docs_page_content = " ".join([doc.page_content for doc in docs])

    llm = OllamaLLM(model="mistral", temperature=0.9)
    prompt = PromptTemplate.from_template(
        template=""" Your are a helpfull youtube assistant that can answe 
        question about videos based on the video's transcript. Use the following extracted parts 
        of the video transcript to answer the question. If you don't know the answer, 
        say you don't know.\n\n{docs}\n\nQuestion: {question}\nAnswer:"""
    )
    chain = prompt | llm
    response = chain.invoke({"question": query, "docs": docs_page_content})
    response = response.replace("\n", "")
    return response