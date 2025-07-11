import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json
import time
from datetime import datetime
import asyncio
from typing import Dict, Any, Generator

class DisplayResultStreamlit:
    def __init__(self, usecase: str, graph: Any, user_message: str):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.response_placeholder = None
        self.current_response = ""

    def _create_typing_indicator(self):
        """Create a typing indicator for better UX"""
        return st.empty()

    def _simulate_typing_effect(self, text: str, placeholder) -> None:
        """Simulate typing effect for responses"""
        displayed_text = ""
        for char in text:
            displayed_text += char
            placeholder.markdown(f"**Assistant:** {displayed_text}▊")
            time.sleep(0.02)  # Adjust speed as needed
        placeholder.markdown(f"**Assistant:** {text}")

    def _format_response_content(self, content: str) -> str:
        """Format response content with better styling"""
        if not content:
            return "I'm sorry, I couldn't generate a response."
        
        # Add basic markdown formatting detection
        if '```' in content:
            # Code blocks present
            return content
        elif content.startswith('#'):
            # Headers present
            return content
        else:
            # Regular text - add some basic formatting
            return content

    def _create_response_container(self) -> st.container:
        """Create a container for the response with custom styling"""
        return st.container()

    def _handle_error(self, error: Exception) -> None:
        """Handle errors gracefully with user-friendly messages"""
        st.error(f"❌ An error occurred: {str(error)}")
        st.markdown("""
        <div style="padding: 1rem; background: #ffe6e6; border-radius: 10px; border-left: 4px solid #ff4444;">
            <h4>🔧 Troubleshooting Tips:</h4>
            <ul>
                <li>Check your API key configuration</li>
                <li>Ensure you have a stable internet connection</li>
                <li>Try a different model or use case</li>
                <li>Refresh the page if the issue persists</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)



    def _display_response_stats(self, response_time: float, token_count: int = None) -> None:
        """Display response statistics"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⏱️ Response Time", f"{response_time:.2f}s")
        
        with col2:
            st.metric("📊 Use Case", self.usecase)
    

    def _process_basic_chatbot(self) -> None:
        """Process basic chatbot interactions with enhanced UX"""
        try:
            start_time = time.time()
            
            # Create response container
            response_container = self._create_response_container()
            
            with response_container:
                # Show typing indicator
                typing_placeholder = st.empty()
                typing_placeholder.markdown("🤖 **Assistant is typing...**")
                
                # Process the graph stream
                full_response = ""
                response_placeholder = st.empty()
                
                usecase= self.usecase
                graph = self.graph
                user_message = self.user_message
                print(user_message)
                if usecase =="Basic Chatbot":
                    for event in graph.stream({'messages':("user",user_message)}):
                        print(event.values())
                        for value in event.values():
                            print(value['messages'])
                            with st.chat_message("user"):
                                st.write(user_message)
                            with st.chat_message("assistant"):
                                st.write(value["messages"].content)
                elif usecase=="Chatbot With Web":
             # Prepare state and invoke the graph
                    initial_state = {"messages": [user_message]}
                    res = graph.invoke(initial_state)
                    for message in res['messages']:
                        if type(message) == HumanMessage:
                            with st.chat_message("user"):
                                st.write(message.content)
                        elif type(message)==ToolMessage:
                            with st.chat_message("ai"):
                                st.write("Tool Call Start")
                                st.write(message.content)
                                st.write("Tool Call End")
                        elif type(message)==AIMessage and message.content:
                            with st.chat_message("assistant"):
                                st.write(message.content)
                elif usecase == "AI News":
                    frequency = self.user_message
                    with st.spinner("Fetching and summarizing news... ⏳"):
                        result = graph.invoke({"messages": frequency})
                        try:
                    # Read the markdown file
                            AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                            with open(AI_NEWS_PATH, "r") as file:
                                markdown_content = file.read()

                    # Display the markdown content in Streamlit
                            st.markdown(markdown_content, unsafe_allow_html=True)
                        except FileNotFoundError:
                            st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                
                # Clear typing indicator
                typing_placeholder.empty()
                
                # Calculate response time
                response_time = time.time() - start_time
            
                
                # Display response stats
                self._display_response_stats(response_time)
                
            
                
        except Exception as e:
            self._handle_error(e)


    
    def display_result_on_ui(self) -> None:
        """Main method to display results on UI"""
       
        # Create main response area
        st.markdown("### 💬 Chat Console")
        
        # Handle different use cases
        if self.usecase == "Basic Chatbot":
            self._process_basic_chatbot()
        else:
            # Default to basic chatbot
            self._process_basic_chatbot()
        

    def get_response_for_api(self) -> Dict[str, Any]:
        """Get response in API format for external integrations"""
        try:
            full_response = ""
            
            for event in self.graph.stream({'messages': ("user", self.user_message)}):
                for value in event.values():
                    if 'messages' in value:
                        message_content = value["messages"].content
                        if message_content:
                            full_response = message_content
            
            return {
                "success": True,
                "response": full_response,
                "usecase": self.usecase,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "usecase": self.usecase,
                "timestamp": datetime.now().isoformat()
            }