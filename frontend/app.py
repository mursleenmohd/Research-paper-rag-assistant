import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Research RAG Assistant",
    layout="wide",
)

st.title("Research RAG Assistant")
st.caption("Ask questions about your research papers using RAG.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

with st.sidebar:
    st.header("Research Paper")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"],)
    if uploaded_file is not None:
        if st.button("Process PDF"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf",)}
            try:
                response = requests.post(f"{BACKEND_URL}/ingest-pdf", files=files, timeout=120,)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.uploaded = True
                    if data.get("already_indexed"):
                        st.info("This PDF is already indexed. No duplicate vectors were created.")
                    else:
                        st.success("PDF processed successfully!")
                        st.write(f"Pages: {data['pages']}")
                        st.write(f"Chunks: {data['chunks']}")
                else:
                    st.error(f"Processing failed: {response.text}")
            except requests.exceptions.RequestException:
                st.error("Could not connect to the backend.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask something about your research paper...")
if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.write(question)
    if not st.session_state.uploaded:
        answer = "Please upload and process a PDF first."
        with st.chat_message("assistant"):
            st.warning(answer)
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )
    else:
        try:
            response = requests.post(f"{BACKEND_URL}/ask",json={"query": question, "top_k": 5,}, timeout=120,)
            if response.status_code == 200:
                data = response.json()
                answer = data["answer"]
                with st.chat_message("assistant"):
                    st.write(answer)
                    st.subheader("Sources")
                    for source in data["sources"]:
                        st.write(
                            f"{source['document_name']} "
                            f"— Page {source['page_number']} "
                            f"— Chunk {source['chunk_index']}"
                        )

                st.session_state.messages.append({"role": "assistant", "content": answer,})

            else:
                with st.chat_message("assistant"):
                    st.error(f"Request failed: {response.text}")
        except requests.exceptions.RequestException:
            with st.chat_message("assistant"):
                st.error("Could not connect to the backend.")