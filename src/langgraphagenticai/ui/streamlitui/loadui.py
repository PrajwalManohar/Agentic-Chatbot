import streamlit as st
import os
from datetime import datetime
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "api_key_valid" not in st.session_state:
            st.session_state.api_key_valid = False
        if "theme" not in st.session_state:
            st.session_state.theme = "light"

    def _apply_custom_css(self):
        """Apply custom CSS for better styling"""
        st.markdown("""
        <style>
        /* Main container styling */
        .main-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        /* Header styling */
        .header-container {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            border-radius: 15px;
            padding: 1rem;
        }
        
        /* Chat message styling */
        .chat-message {
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-left: 20%;
        }
        
        .assistant-message {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            margin-right: 20%;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            border-radius: 25px;
            border: 2px solid #e0e0e0;
            padding: 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div > select {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            padding: 0.5rem;
        }
        
        /* Status indicators */
        .status-indicator {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            font-weight: bold;
            text-align: center;
        }
        
        .status-success {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        
        .status-warning {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
        }
        
        .status-error {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
        }
        
        /* Animation for loading */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 2s infinite;
        }
        
        /* Card styling */
        .info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        
        /* Metrics styling */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)

    def _create_header(self):
        """Create an attractive header"""
        st.markdown(f"""
        <div class="header-container">
            <h1>🤖 {self.config.get_page_title()}</h1>
            <p style="font-size: 1.2rem; margin-top: 1rem;">
                Your Advanced AI Assistant powered by LangGraph
            </p>
            <p style="font-size: 0.9rem; opacity: 0.8;">
                {datetime.now().strftime("%A, %B %d, %Y")}
            </p>
        </div>
        """, unsafe_allow_html=True)

    def _create_sidebar(self):
        """Create an enhanced sidebar with better organization"""
        with st.sidebar:
            st.markdown("### ⚙️ Configuration")
            
            # LLM Configuration Section
            with st.expander("🧠 LLM Settings", expanded=True):
                llm_options = self.config.get_llm_options()
                self.user_controls["selected_llm"] = st.selectbox(
                    "Select LLM Provider", 
                    llm_options,
                    help="Choose your preferred language model provider"
                )

                if self.user_controls["selected_llm"] == 'Groq':
                    model_options = self.config.get_groq_model_options()
                    self.user_controls["selected_groq_model"] = st.selectbox(
                        "Select Model", 
                        model_options,
                        help="Choose the specific model variant"
                    )
                    
                    self.user_controls["GROQ_API_KEY"] = st.text_input(
                        "🔑 API Key",
                        type="password",
                        placeholder="Enter your Groq API key",
                        help="Your API key is encrypted and not stored"
                    )
                    
                    # API Key validation with better UX
                    if not self.user_controls["GROQ_API_KEY"]:
                        st.markdown("""
                        <div class="status-indicator status-warning">
                            ⚠️ API Key Required
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.warning("🔗 Need an API Key?")
                        st.markdown("""
                            1. Visit [Groq Console](https://console.groq.com/keys)
                            2. Create a new API key
                            3. Copy and paste it above
                            4. Keep it secure and don't share it
                            """)
                    else:
                        st.markdown("""
                        <div class="status-indicator status-success">
                            ✅ API Key Configured
                        </div>
                        """, unsafe_allow_html=True)
                        st.session_state.api_key_valid = True

            # Use Case Configuration Section
            with st.expander("🎯 Use Cases", expanded=True):
                usecase_options = self.config.get_usecase_options()
                self.user_controls["selected_usecase"] = st.selectbox(
                    "Select Use Case",
                    usecase_options,
                    help="Choose the type of AI assistance you need"
                )
                
                # Use case description
                usecase_descriptions = {
                    "Basic Chatbot": "💬 General conversation and Q&A",
                    "Code Assistant": "💻 Programming help and code review",
                    "Creative Writing": "✍️ Content creation and storytelling",
                    "Data Analysis": "📊 Data insights and visualization"
                }
                
                if self.user_controls["selected_usecase"] in usecase_descriptions:
                    st.info(usecase_descriptions[self.user_controls["selected_usecase"]])

                if self.user_controls["selected_usecase"] =="Chatbot With Web" or self.user_controls["selected_usecase"] =="AI News" :
                    os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY API KEY",type="password")

                # Validate API key
                    if not self.user_controls["TAVILY_API_KEY"]:
                        st.warning("⚠️ Please enter your TAVILY_API_KEY key to proceed. Don't have? refer : https://app.tavily.com/home")

                if self.user_controls['selected_usecase']=="AI News":
                    st.subheader("📰 AI News Explorer ")
                
                    with st.sidebar:
                        time_frame = st.selectbox(
                        "📅 Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0
                    )
                        
                    if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                        st.session_state.IsFetchButtonClicked = True
                        st.session_state.timeframe = time_frame


    def load_streamlit_ui(self):
        """Main method to load the UI"""
        # Set page config
        st.set_page_config(
            page_title=f"🤖 {self.config.get_page_title()}",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.session_state.IsFetchButtonClicked = False
        
        # Apply custom CSS
        self._apply_custom_css()
        
        # Create header
        self._create_header()
        
        # Create sidebar
        self._create_sidebar()
        
        # Add helpful tips
        if not st.session_state.messages:
            st.markdown("""
            <div class="info-card">
                <h3>🌟 Welcome to Your AI Assistant!</h3>
                <p>Here are some things you can try:</p>
                <ul>
                    <li>💬 Ask questions about any topic</li>
                    <li>💻 Get help with coding problems</li>
                    <li>✍️ Request creative writing assistance</li>
                    <li>📊 Analyze data and get insights</li>
                </ul>
                <p><strong>Tip:</strong> Configure your LLM settings in the sidebar to get started!</p>
            </div>
            """, unsafe_allow_html=True)

        return self.user_controls