import streamlit as st
from brain import load_library, find_relevant_papers, ask_llm, build_embeddings

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
papers = build_embeddings(papers)

# ------------------------
# SIDEBAR
# ------------------------
with st.sidebar:
    st.title("🧠 Literature Brain")

    st.markdown("Turn documents into structured intelligence.")

    st.markdown("---")

    # Library stats
    st.subheader("📚 Library")
    st.metric("Papers Loaded", len(papers))

    # Controls
    st.subheader("⚙️ Settings")
    max_papers = st.slider("Context size", 1, 10, 3)
    show_sources = st.checkbox("Show sources", value=True)

    # Clear chat button
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # Status
    st.subheader("🟢 System")
    st.success("LLM connected")

    st.caption("Built locally with Ollama + LLaMA")

# ------------------------
# MAIN HEADER
# ------------------------
st.title("🧠 Literature Brain")

st.markdown(
    "Ask questions across your research library and get synthesized insights."
)

st.markdown("---")

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
    relevant = find_relevant_papers(query, papers, top_k=max_papers)
    # STEP 3 (debug)
    with st.expander("🔍 Debug (click to expand)"):
    st.write(relevant)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking..."):
            answer = ask_llm(query, relevant)

        st.write(answer)

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        # Collapsible sources (cleaner UI)
        if show_sources and relevant:
            with st.expander("📄 Sources"):
                for p in relevant:
                    st.markdown(f"- **{p.get('source_file', 'unknown')}**")

            # Show sources
            if show_sources:
                st.markdown("### 📄 Sources")
                for p in relevant:
                    st.markdown(f"- 📄 **{p.get('source_file', 'unknown')}**")