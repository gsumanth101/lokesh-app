# Main app function
def main():
    # Enhanced animated header with theme support
    st.markdown("""
    <div style="background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%); 
                padding: 2rem; border-radius: 25px; margin-bottom: 2rem; 
                text-align: center; color: white; 
                box-shadow: 0 15px 60px var(--shadow-medium);
                position: relative;
                overflow: hidden;
                animation: slideInUp 1s ease-out;
                backdrop-filter: blur(10px);">
        <div style="position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                    animation: shimmer 3s infinite;"></div>
        <h1 style="margin: 0; font-size: 3rem; font-weight: 800; 
                   text-shadow: 0 4px 8px rgba(0,0,0,0.3); color: white;
                   animation: fadeInUp 1.2s ease-out;
                   letter-spacing: -1px;">
            🌾 Smart Farming Assistant
        </h1>
        <p style="margin: 1rem 0 0 0; font-size: 1.3rem; opacity: 0.95; color: white;
                  animation: fadeInUp 1.4s ease-out;
                  font-weight: 500;">
            AI-Powered Agriculture Solutions for Modern Farmers
        </p>
        <div style="margin-top: 1.5rem; animation: fadeInUp 1.6s ease-out;">
            <span style="display: inline-block; padding: 0.5rem 1rem; 
                        background: rgba(255,255,255,0.2); border-radius: 20px;
                        margin: 0 0.5rem; font-size: 0.9rem; font-weight: 600;
                        animation: bounce 2s infinite;">🚀 AI-Powered</span>
            <span style="display: inline-block; padding: 0.5rem 1rem; 
                        background: rgba(255,255,255,0.2); border-radius: 20px;
                        margin: 0 0.5rem; font-size: 0.9rem; font-weight: 600;
                        animation: bounce 2s infinite 0.2s;">🌍 Multi-Language</span>
            <span style="display: inline-block; padding: 0.5rem 1rem; 
                        background: rgba(255,255,255,0.2); border-radius: 20px;
                        margin: 0 0.5rem; font-size: 0.9rem; font-weight: 600;
                        animation: bounce 2s infinite 0.4s;">📱 Real-Time</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Selection
    st.sidebar.title("🧠 Model Selection")
    selected_model = st.sidebar.selectbox(
        "Select Model",
        options=list(MODEL_OPTIONS.keys()),
        index=1  # Default to Enhanced Model
    )
    
    # Language selector in sidebar
    st.sidebar.title("🌐 Language / भाषा")
    languages = get_language_options()
    selected_language = st.sidebar.selectbox(
        "Select Language",
        options=list(languages.keys()),
        key="language_selector"
    )
    current_lang = languages[selected_language]
    
    # Store language in session state
    st.session_state.current_language = current_lang
    
    # Display language
    st.sidebar.markdown(f"**🌐 Current Language:** {selected_language}")
    st.sidebar.markdown("---")
    
    # Check if user is logged in
    if 'current_user' in st.session_state and st.session_state.is_logged_in:
        user_role = st.session_state.current_user['role']
        user_info_text = f"Logged in as: {st.session_state.current_user['name']} ({user_role.capitalize()})"
        
        # Translate user info if needed
        if current_lang != 'en':
            user_info_text = translate_text(user_info_text, current_lang)
        
        st.sidebar.write(user_info_text)
        
        logout_text = "Logout"
        if current_lang != 'en':
            logout_text = translate_text(logout_text, current_lang)
            
        if st.sidebar.button(logout_text):
            logout_user()
            st.rerun()
            
        # User is logged in - show role-based content
        user_role = st.session_state.current_user['role']
        
        if user_role == 'admin':
            show_admin_dashboard()
        elif user_role == 'farmer':
            show_farmer_dashboard()
        elif user_role == 'buyer':
            show_buyer_dashboard()
        elif user_role == 'agent':
            show_agent_dashboard()
            
    else:
        # Show the enhanced crop interface for non-logged-in users
        show_enhanced_crop_interface()
    

if __name__ == "__main__":
    main()
