import streamlit as st
import ai_copilot

def get_suggestions(context: dict, last_user_message: str = None) -> list:
    """
    Generates dynamic suggestion chips based on the current page and last message.
    """
    page = context.get('page', 'overview')
    
    if page == "equity":
        return [
            "🔍 Explain this page",
            "📊 Explain Sharpe ratio",
            "📉 What is Max Drawdown?",
            "⚖️ Benchmarking vs SPY"
        ]
    elif page == "strategy":
        return [
            "⚡ How does crossover work?",
            "📈 Strategy vs Buy & Hold",
            "🛡️ Risk-adjusted returns",
            "🔧 Tuning parameters"
        ]
    elif page == "portfolio":
        return [
            "🧩 How to diversify?",
            "✨ Max Sharpe vs Min Vol",
            "💹 Efficient Frontier?",
            "🔍 Concentration risk"
        ]
    
    return [
        "🚀 Platform Tour",
        "📈 Best asset for 1Y?",
        "🔬 How to optimize?",
        "❔ Ask a question"
    ]

def render_chat_drawer():
    """
    Renders the persistent floating chat drawer.
    Uses custom CSS injected via utils.py.
    """
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi, I'm Fin! I'm your personal AI analyst. How can I help you today?"}
        ]

    # Handle force_msg (from Analyst Note CTA)
    if 'force_msg' in st.session_state and st.session_state.force_msg:
        msg = st.session_state.force_msg
        st.session_state.force_msg = None # Clear it
        context = st.session_state.get('ai_context', {})
        response = ai_copilot.generate_response(msg, context)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    if st.session_state.show_chat:
        # Wrap everything in a container to try and minimize the "black box" slot
        # but the actual drawer is fixed via CSS.
        with st.container():
            st.markdown('<div class="chat-drawer">', unsafe_allow_html=True)
            
            # Chat Header
            c_header = st.container()
            with c_header:
                st.markdown("""
                <div class="chat-header">
                    <div style="display:flex; align-items:center; justify-content:space-between; width:100%;">
                        <div style="display:flex; align-items:center; gap:12px;">
                            <div class="chat-logo">F</div>
                            <div>
                                <div style="font-weight:700; font-size:1rem; color:#F9FAFB;">Fin Copilot</div>
                                <div style="font-size:0.7rem; color:#6B7280; font-weight:500;">Institutional AI Analyst</div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                # Close button is hard to do inside the HTML and make it trigger python
                # So we use a streamlit button at the top right of the drawer (conceptual)
                # But since it's a fixed drawer, we'll just put a 'Close' button inside the flow
            
            # History
            chat_container = st.container(height=380, border=False)
            with chat_container:
                # To prevent duplicates, we only render the history once.
                # Streamlit chat_message handles this well within the loop.
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
            
            # Suggested Prompts (Chips)
            st.markdown("<div style='padding:0 20px; margin-bottom:12px;'>", unsafe_allow_html=True)
            context = st.session_state.get('ai_context', {})
            suggestions = get_suggestions(context)
            
            col1, col2 = st.columns(2)
            suggestion_clicked = None
            
            for i, sug in enumerate(suggestions):
                target_col = col1 if i % 2 == 0 else col2
                if target_col.button(sug, key=f"sug_btn_{i}", use_container_width=True):
                    suggestion_clicked = sug
            st.markdown("</div>", unsafe_allow_html=True)

            # Input area
            c_footer = st.container()
            with c_footer:
                user_input = st.chat_input("Ask Fin anything...")
                
                final_query = suggestion_clicked if suggestion_clicked else user_input
                
                if final_query:
                    # Append user message
                    st.session_state.chat_history.append({"role": "user", "content": final_query})
                    # Generate response
                    response = ai_copilot.generate_response(final_query, context)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()

            # Actions Row
            c1, c2 = st.columns([2, 1])
            if c1.button("Clear History", key="clear_chat_btn", use_container_width=True):
                st.session_state.chat_history = [
                    {"role": "assistant", "content": "Chat history cleared. How can I help you now?"}
                ]
                st.rerun()
            if c2.button("Close", key="close_chat_btn", use_container_width=True):
                st.session_state.show_chat = False
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
