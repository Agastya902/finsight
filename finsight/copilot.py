import streamlit as st

def get_context_response(user_query: str, context: dict) -> str:
    """
    Deterministic context-aware response engine for Fin.
    Routes queries based on keywords and current app session state.
    """
    q = user_query.lower()
    page = context.get('page', 'unknown')
    asset = context.get('asset', 'N/A')
    
    # Intent: Page Explanation
    if "what is this" in q or "explain this page" in q or "summarize" in q:
        if page == "equity":
            return f"This is the **Equity Intelligence** dashboard for **{asset}**. It shows historical performance metrics, relative benchmarking, and automated risk assessments like Max Drawdown and Sharpe Ratio."
        elif page == "strategy":
            return f"You are looking at the **Algorithmic Validator**. It compares a Moving Average Crossover strategy (MA {context.get('short',50)}/{context.get('long',200)}) against a passive Buy & Hold approach for **{asset}**."
        elif page == "portfolio":
            return f"This is the **Portfolio Builder**. It uses Modern Portfolio Theory to optimize your selection of {len(context.get('tickers', []))} assets. You can see the Efficient Frontier and your optimal capital allocation here."
        else:
            return "FinSight is a premium fintech platform for equity analysis, strategy backtesting, and portfolio optimization. Navigate through the top tabs to get started."

    # Intent: Metric Explanation
    if "sharpe" in q:
        val = context.get('sharpe', 'N/A')
        return f"The **Sharpe Ratio** measures risk-adjusted return. Your current result is **{val}**. Generally, a Sharpe > 1.0 is considered good, and > 2.0 is very high. It tells you if your returns are due to smart investment or just taking too much risk."
    
    if "drawdown" in q or "drop" in q or "risk" in q:
        val = context.get('max_dd', 'N/A')
        return f"**Maximum Drawdown** represents the largest peak-to-trough decline. Currently, this is **{val}**. It's a key metric for understanding the 'pain tolerance' required for this investment or strategy."
    
    if "volatility" in q or "fluctuation" in q:
        val = context.get('vol', 'N/A')
        return f"**Volatility** (Standard Deviation) measures how much the price fluctuates. At **{val}**, this indicates the historical uncertainty or risk in the asset's price movements."

    if "diversify" in q or "advice" in q or "improve" in q:
        if page == "portfolio":
            return "To improve this portfolio, look at the correlation matrix below. You want assets with low or negative correlations to reduce overall systemic risk."
        return "Diversification is key. Consider adding assets from different sectors or asset classes (like Bonds/Gold) to your portfolio to lower your overall Beta."

    if "benchmark" in q or "compare" in q:
        bench = context.get('benchmark', 'SPY')
        return f"Benchmarking against **{bench}** allows you to see if you are actually outperforming the broader market ('Alpha') or just riding the market's natural wave ('Beta')."

    # Default catch-all
    return "I'm Fin, your AI Portfolio Analyst. I can explain the metrics on this screen, help you interpret the charts, or give you a guided tour of the platform. Try asking 'Explain Sharpe Ratio' or 'Summarize this page'."

def render_chat_drawer():
    """
    Renders the persistent floating chat drawer.
    Uses custom CSS injected via utils.py.
    """
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False
    
    # The Floating Action Button (FAB)
    # Note: The button itself is handled by CSS in utils.py applied to a specific container
    
    if st.session_state.show_chat:
        st.markdown('<div class="chat-drawer">', unsafe_allow_html=True)
        
        # Chat Header
        st.markdown("""
        <div class="chat-header">
            <div style="display:flex; align-items:center; gap:10px;">
                <div class="chat-logo">F</div>
                <div>
                    <div style="font-weight:600; font-size:0.95rem;">Fin Copilot</div>
                    <div style="font-size:0.7rem; color:#6B7280;">AI Portfolio Analyst</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # History
        chat_container = st.container(height=360, border=False)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        
        # Suggested Prompts (Chips)
        st.markdown("<div style='padding:0 20px; margin-bottom:10px;'>", unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        suggestion = None
        if s1.button("🔍 Explain this page", key="sug_1", use_container_width=True):
            suggestion = "Explain this page"
        if s2.button("📊 Explain Sharpe", key="sug_2", use_container_width=True):
            suggestion = "Explain Sharpe ratio"
        
        s3, s4 = st.columns(2)
        if s3.button("📉 Why did it drop?", key="sug_3", use_container_width=True):
            suggestion = "Why is the drawdown high?"
        if s4.button("🧩 How to diversify?", key="sug_4", use_container_width=True):
            suggestion = "How can I diversify?"
        st.markdown("</div>", unsafe_allow_html=True)

        # Input
        user_input = st.chat_input("Ask Fin anything...")
        final_query = suggestion if suggestion else user_input

        if final_query:
            st.session_state.chat_history.append({"role": "user", "content": final_query})
            # Generate deterministic response using active context
            context = st.session_state.get('ai_context', {})
            response = get_context_response(final_query, context)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
            
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = [{"role": "assistant", "content": "Chat cleared. How can I help you now?"}]
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
