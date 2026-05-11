import streamlit as st
from brain import load_library, find_relevant_papers, ask_llm

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(
    page_title="Literature Brain",
    page_icon="🧠",
    layout="wide"
)

# ------------------------
# LOAD DATA
# ------------------------
@st.cache_data
def load_data():
    return load_library()

papers = load_data()

# ------------------------
# SIDEBAR
# ------------------------
with st.sidebar:
    st.title("🧠 Literature Library")

    st.markdown("---")

    st.write(f"📚 Papers loaded: **{len(papers)}**")

    st.markdown("### Controls")

    max_papers = st.slider("Context size", 1, 10, 3)

    show_sources = st.checkbox("Show sources", value=True)

    st.markdown("---")
    st.markdown("Built by Russ locally  \nwith Ollama + LLaMA")
    
    st.markdown("### System Status")
    
    st.success("LLM connected")
    
    st.info(f"{len(papers)} papers loaded")

# ------------------------
# MAIN HEADER
# ------------------------
st.title("🧠 Literature Brain")
st.caption("Ask questions across your research library")

# ------------------------
# CHAT HISTORY
# ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------------------------
# INPUT BOX
# ------------------------
query = st.chat_input("Ask the Brain about your library...")

if query:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    # Get relevant papers
    relevant = find_relevant_papers(query, papers)[:max_papers]

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Pondering..."):
            answer = ask_llm(query, relevant)
            st.write(answer)

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            # Show sources
            if show_sources:
                st.markdown("### 📄 Sources")
                for p in relevant:
                    st.markdown(f"- 📄 **{p.get('source_file', 'unknown')}**")