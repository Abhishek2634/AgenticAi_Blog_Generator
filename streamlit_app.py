import streamlit as st
import requests
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Fixed visibility and alignment
st.markdown("""
    <style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main container - dark theme */
    .main {
        padding: 2rem;
        max-width: 1000px;
        margin: 0 auto;
        background-color: #1a1a2e;
    }
    
    /* Streamlit default background override */
    .stApp {
        background-color: #1a1a2e;
    }
    
    /* Header */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .header-container h1 {
        font-size: 3rem;
        color: #667eea;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .header-container p {
        font-size: 1.1rem;
        color: #aaa;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        color: #ffffff;
        padding: 0.5rem 0;
        border-bottom: 2px solid #667eea;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Input labels - make visible */
    .stTextInput label, .stSelectbox label {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    
    /* Input fields - light background for visibility */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #2d2d44 !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: 2px solid #3a3a52 !important;
        padding: 0.75rem;
        font-size: 16px;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #888 !important;
    }
    
    /* Generate Blog button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        margin-top: 1rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: #2d2d44 !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.5rem !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        height: 46px !important;
    }
    
    .stDownloadButton>button:hover {
        background: #667eea !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Blog content - visible text */
    .blog-content {
        background: #2d2d44;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #3a3a52;
        margin: 1.5rem 0;
        color: #ffffff;
    }
    
    .blog-content h2, .blog-content h3, .blog-content h4 {
        color: #ffffff !important;
    }
    
    .blog-content p, .blog-content li, .blog-content strong {
        color: #e0e0e0 !important;
    }
    
    /* Save section - NO white background */
    .save-section {
        background: transparent;
        padding: 1.5rem 0;
        margin: 1.5rem 0;
    }
    
    .save-section h3 {
        font-size: 1.3rem;
        color: #ffffff;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Button container - perfect alignment */
    [data-testid="column"] {
        display: flex !important;
        align-items: center !important;
    }
    
    [data-testid="column"] > div {
        width: 100%;
    }
    
    /* Success message */
    .stSuccess {
        background-color: rgba(40, 167, 69, 0.1);
        color: #28a745;
        border-radius: 8px;
        border-left: 5px solid #28a745;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Info box */
    .stInfo {
        background-color: rgba(102, 126, 234, 0.1);
        color: #667eea;
        border-left: 5px solid #667eea;
        border-radius: 8px;
    }
    
    /* Error message */
    .stError {
        background-color: rgba(220, 53, 69, 0.1);
        color: #dc3545;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #2d2d44;
        color: #ffffff !important;
        border-radius: 8px;
    }
    
    .streamlit-expanderContent {
        background-color: #2d2d44;
        border-radius: 0 0 8px 8px;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: #3a3a52;
    }
    
    /* Footer text */
    .footer-text {
        text-align: center;
        color: #888;
        padding: 2rem 1rem;
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'current_blog' not in st.session_state:
    st.session_state.current_blog = None

# API URL
API_URL = "http://localhost:8000"

# Header
st.markdown("""
    <div class="header-container">
        <h1>✍️ AI Blog Generator</h1>
        <p>Generate SEO-optimized blogs with AI in multiple languages</p>
    </div>
    """, unsafe_allow_html=True)

# ===== INPUT SECTION =====
st.markdown('<p class="section-header">📝 Input</p>', unsafe_allow_html=True)

topic = st.text_input(
    "Blog Topic",
    placeholder="e.g., What is gen ai ?, Artificial Intelligence, Web Development"
)

language_option = st.selectbox(
    "Translation Language",
    ["None (English Only)", "Hindi (हिंदी)", "French (Français)"]
)

language_map = {
    "None (English Only)": None,
    "Hindi (हिंदी)": "hindi",
    "French (Français)": "french"
}

selected_lang = language_map[language_option]

generate_button = st.button("🚀 Generate Blog", use_container_width=True)

# ===== OUTPUT SECTION =====
st.markdown("---")
st.markdown('<p class="section-header">📄 Output</p>', unsafe_allow_html=True)

if generate_button:
    if not topic:
        st.error("❌ Please enter a blog topic!")
    else:
        with st.spinner("🤖 Generating your blog..."):
            try:
                payload = {"topic": topic}
                if selected_lang:
                    payload["language"] = selected_lang
                
                progress_bar = st.progress(0)
                progress_bar.progress(30)
                
                response = requests.post(f"{API_URL}/blogs", json=payload, timeout=120)
                progress_bar.progress(80)
                
                if response.status_code == 200:
                    data = response.json()
                    blog = data.get("data", {}).get("blog", {})
                    
                    progress_bar.progress(100)
                    progress_bar.empty()
                    
                    st.success("✅ Blog generated successfully!")
                    st.session_state.current_blog = blog
                    
                    # Display blog
                    with st.container():
                        st.markdown('<div class="blog-content">', unsafe_allow_html=True)
                        st.markdown(f"## {blog.get('title', 'Untitled')}")
                        st.markdown("---")
                        st.markdown(blog.get('content', ''))
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Save section - horizontally aligned buttons
                    st.markdown('<div class="save-section">', unsafe_allow_html=True)
                    st.markdown("### 💾 Save Your Blog")
                    
                    blog_text = f"# {blog.get('title', '')}\n\n{blog.get('content', '')}"
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download Markdown",
                            data=blog_text,
                            file_name=f"{topic.replace(' ', '_')}_blog.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    with col2:
                        if st.button("🔄 Generate Another", use_container_width=True):
                            st.session_state.current_blog = None
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.expander("🔍 View Raw JSON Response"):
                        st.json(data)
                
                else:
                    progress_bar.empty()
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Try a simpler topic.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to backend. Make sure FastAPI is running:\n``````")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

elif st.session_state.current_blog:
    blog = st.session_state.current_blog
    
    with st.container():
        st.markdown('<div class="blog-content">', unsafe_allow_html=True)
        st.markdown(f"## {blog.get('title', 'Untitled')}")
        st.markdown("---")
        st.markdown(blog.get('content', ''))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="save-section">', unsafe_allow_html=True)
    st.markdown("### 💾 Save Your Blog")
    
    blog_text = f"# {blog.get('title', '')}\n\n{blog.get('content', '')}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download Markdown",
            data=blog_text,
            file_name="blog.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col2:
        if st.button("🔄 Generate Another", use_container_width=True):
            st.session_state.current_blog = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Enter a topic above and click 'Generate Blog' to get started")

# Footer
st.markdown("---")
st.markdown(
    '<div class="footer-text">Built with ❤️ using <strong>LangGraph</strong> • <strong>Streamlit</strong> • <strong>FastAPI</strong></div>',
    unsafe_allow_html=True
)
