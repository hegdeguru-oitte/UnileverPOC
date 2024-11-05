# config/styles.py
COLORS = {
    'background': '#FFFFFF',
    'text': '#333333',
    'card_background': '#F8F9FA',
    'primary': '#007BFF',
    'accent': '#E74C3C',
    'success': '#28A745',
    'warning': '#FFC107',
    'muted': '#6C757D'
}

CSS_STYLES = f"""
<style>
    /* Global Styles */
    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
    }}
    
    /* Header Styles - Reduced size and added sophistication */
    .main-header {{
        padding: 1.5rem;
        color: {COLORS['text']};
        text-align: center;
        font-size: 1.5rem;
        letter-spacing: 0.5px;
    }}
    
    /* Streamlit's default headers adjustment */
    .css-10trblm {{
        font-size: 1.4rem !important;
        margin-bottom: 1rem !important;
    }}
    
    .css-1629p8f h1 {{
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }}
    
    .css-1629p8f h2 {{
        font-size: 1.4rem !important;
        font-weight: 500 !important;
        color: {COLORS['text']};
    }}
    
    .css-1629p8f h3 {{
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        color: {COLORS['muted']};
    }}
    
    /* Card Styles - More subtle shadows and transitions */
    .card {{
        background-color: {COLORS['card_background']};
        padding: 1.25rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
        color: {COLORS['text']};
        transition: all 0.2s ease;
    }}
    
    .card:hover {{
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    
    /* Button Styles - More sophisticated with subtle hover effects */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: {COLORS['text']};
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: none;
        width: auto !important;
        display: inline-block;
        margin: 0 auto;
        transition: all 0.2s ease;
        opacity: 0.9;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['primary']};
        opacity: 1;
        transform: translateY(-1px);
    }}
    
    /* Incident Header - More subtle and professional */
    .incident-header {{
        background-color: {COLORS['card_background']};
        color: {COLORS['text']};
        padding: 1.25rem;
        border-radius: 8px;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        border-left: 4px solid {COLORS['primary']};
    }}
    
    /* Info Box Styles - Refined styling */
    .info-box {{
        background-color: {COLORS['card_background']};
        padding: 1.25rem;
        border-radius: 6px;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    /* Container Styles */
    .custom-container {{
        max-width: 1100px;
        margin: 0 auto;
        padding: 0 1rem;
    }}
    
    /* File Uploader - More subtle styling */
    .stFileUploader {{
        padding: 1rem;
        border-radius: 8px;
        background-color: {COLORS['card_background']};
        color: {COLORS['text']};
        border: 1px dashed rgba(255,255,255,0.2);
    }}
    
    /* Text Input Fields */
    .stTextInput > div > div {{
        padding: 0.5rem;
        color: {COLORS['text']};
        background-color: {COLORS['card_background']};
        border-radius: 6px;
    }}
    
    /* Success/Warning Messages */
    .stSuccess, .stWarning {{
        padding: 0.75rem;
        border-radius: 6px;
        margin: 1rem 0;
    }}

    /* Container Padding */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }}
    
    /* Markdown styling */
    .stMarkdown {{
        font-size: 1rem;
        padding: 0.5rem 0;
    }}
    
    /* Report container styling */
    .report-container {{
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }}
    
    /* Header styling for H3 elements */
    h3 {{
        color: #2C3E50;
        padding-bottom: 0.5rem;
    }}
    
    /* Summary container styling */
    .summary-container {{
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }}
    
    /* Incident title styling */
    .incident-title {{
        color: #2C3E50;
        font-size: 1.5rem;
        margin: 0;
    }}
</style>
"""
