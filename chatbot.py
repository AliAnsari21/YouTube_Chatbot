from youtube_transcript_api import YouTubeTranscriptApi
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

def create_conversational_chain(video_id, api_key, question):
    # Get transcript
    try:
        api = YouTubeTranscriptApi()

        # Try English first
        try:
            transcript_list = api.fetch(
                video_id,
                languages=["en"]
            )

        except Exception:

            # If English is not available,
            # try Hindi
            transcript_list = api.fetch(
                video_id,
                languages=["hi"]
            )

        transcript = " ".join(
            chunk.text
            for chunk in transcript_list
        )

    except Exception as e:

        raise Exception(
            f"Transcript error: {e}"
        )

    # Split transcript
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

    chunks = splitter.create_documents([transcript])

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # FAISS
    vector_store = FAISS.from_documents(chunks,embeddings)

    # Retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    # Groq
    llm = ChatGroq(
        groq_api_key=api_key,
        model="openai/gpt-oss-20b",
        temperature=0.2
    )

    # Prompt
    prompt = PromptTemplate(
        template="""
You are a helpful assistant.

Answer only using the provided YouTube transcript.

If the answer is not available in the transcript,
say "I don't know."

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context","question"]
    )

    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)

    # Create context
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Create final prompt
    final_prompt = prompt.invoke({"context": context_text,"question": question})

    # Generate answer
    answer = llm.invoke(final_prompt)
    return answer.content

