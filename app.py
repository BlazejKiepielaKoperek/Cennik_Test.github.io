import streamlit as st
from twilio.rest import Client
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="N Studios - Kalkulator Produkcji Wideo",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for cinematic dark mode
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #050505;
        color: #ffffff;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling */
    .main-header {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #ffffff 0%, #a0a0a0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
    }
    
    .sub-header {
        color: #a0a0a0;
        font-size: 14px;
        margin-bottom: 30px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #0a0a0a;
        padding: 6px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #a0a0a0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 8px;
        padding: 16px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #d4af37;
        color: #050505;
    }
    
    /* Input styling */
    .stSelectbox, .stSlider, .stTextInput, .stNumberInput {
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #0a0a0a;
        border: 1px solid #1a1a1a;
        color: #ffffff;
    }
    
    .stTextInput > div > div > input {
        background-color: #0a0a0a;
        border: 1px solid #1a1a1a;
        color: #ffffff;
    }
    
    /* Price display styling */
    .price-display {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%);
        padding: 32px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.3);
        margin: 40px 0;
    }
    
    .price-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: rgba(0, 0, 0, 0.7);
        margin-bottom: 8px;
    }
    
    .price-amount {
        font-size: 48px;
        font-weight: 800;
        color: #050505;
        letter-spacing: -1px;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: #d4af37;
        color: #050505;
        border: none;
        border-radius: 8px;
        padding: 20px 40px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 16px;
    }
    
    .stButton > button:hover {
        background-color: #f0c040;
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.5);
    }
    
    /* Radio buttons */
    .stRadio > div {
        display: flex;
        gap: 12px;
    }
    
    .stRadio > div > label {
        background-color: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-radius: 8px;
        padding: 16px 20px;
        flex: 1;
        text-align: center;
        cursor: pointer;
    }
    
    /* Info box */
    .info-box {
        background: rgba(212, 175, 55, 0.1);
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #d4af37;
        margin-top: 20px;
    }
    
    .info-box strong {
        color: #d4af37;
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        margin-top: 20px;
    }
    
    /* Labels */
    label {
        color: #a0a0a0 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
</style>
""", unsafe_allow_html=True)

# Twilio Configuration
def send_whatsapp_notification(form_data):
    """Send WhatsApp notification using Twilio"""
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER')
        your_whatsapp = os.getenv('YOUR_WHATSAPP_NUMBER')
        
        if not all([account_sid, auth_token, twilio_whatsapp, your_whatsapp]):
            st.error("⚠️ Twilio credentials not configured in .env file")
            return False
        
        client = Client(account_sid, auth_token)
        
        # Format message
        mode = form_data['mode']
        message = f"""🎬 *NOWE ZAPYTANIE - N STUDIOS*

*Tryb:* {mode}
*Szacowana cena:* {form_data['price']} PLN

👤 *Dane kontaktowe:*
Imię: {form_data['name']}
Telefon: {form_data['phone']}
Email: {form_data['email']}

⚙️ *Konfiguracja:*
"""
        
        if mode == 'TRADYCYJNE':
            message += f"""Sprzęt: {form_data['equipment']}
Studio: {form_data['studio']}
Długość: {form_data['length']}s
Złożoność: {form_data['complexity']}
"""
        else:
            message += f"Długość: {form_data['length']}s\n"
        
        message += f"\n⏰ Data: {datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}"
        
        # Send message
        twilio_message = client.messages.create(
            body=message,
            from_=twilio_whatsapp,
            to=your_whatsapp
        )
        
        return True
        
    except Exception as e:
        st.error(f"❌ Błąd wysyłania WhatsApp: {str(e)}")
        return False

# Pricing calculations
def calculate_traditional_price(equipment, studio, length, complexity):
    """Calculate price for traditional mode"""
    equipment_prices = {
        'Sony FX3': 5000,
        'ARRI Alexa': 15000,
        'RED Komodo': 10000
    }
    
    studio_prices = {
        'Brak': 0,
        'Cyklorama': 3000,
        'Ściana LED': 8000
    }
    
    complexity_prices = {
        'Montaż': 2000,
        'VFX': 5000,
        '3D': 8000
    }
    
    total = (equipment_prices[equipment] + 
             studio_prices[studio] + 
             complexity_prices[complexity] + 
             (length * 50))
    
    return int(total)

def calculate_ai_price(length):
    """Calculate price for AI mode"""
    return int(length * 100)

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Main app
def main():
    # Header
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="main-header">N</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="main-header">KALKULATOR PRODUKCJI</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Wybierz tryb i skonfiguruj swoją produkcję wideo</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tab selection
    tab1, tab2 = st.tabs(["🎥 TRADYCYJNE", "🤖 AI REKLAMA"])
    
    # TRADITIONAL MODE TAB
    with tab1:
        st.markdown("### Konfiguracja Tradycyjna")
        
        col1, col2 = st.columns(2)
        
        with col1:
            equipment = st.selectbox(
                "Sprzęt",
                options=['Sony FX3', 'ARRI Alexa', 'RED Komodo'],
                key='equipment'
            )
            
            studio = st.selectbox(
                "Studio",
                options=['Brak', 'Cyklorama', 'Ściana LED'],
                key='studio'
            )
        
        with col2:
            complexity = st.radio(
                "Złożoność",
                options=['Montaż', 'VFX', '3D'],
                horizontal=True,
                key='complexity'
            )
        
        length_trad = st.slider(
            "Długość wideo (sekundy)",
            min_value=15,
            max_value=120,
            value=60,
            step=1,
            key='length_trad'
        )
        
        # Calculate price
        price_trad = calculate_traditional_price(equipment, studio, length_trad, complexity)
        
        # Display price
        st.markdown(f"""
        <div class="price-display">
            <div class="price-label">Szacowany Kosztorys</div>
            <div class="price-amount">{price_trad:,} <span style="font-size: 24px;">PLN</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Lead form
        st.markdown("### 📋 Dane Kontaktowe")
        
        name_trad = st.text_input("Imię i nazwisko", key='name_trad')
        phone_trad = st.text_input("Telefon", key='phone_trad')
        email_trad = st.text_input("Email", key='email_trad')
        
        if st.button("🎬 UMÓW WIZYTĘ", key='submit_trad'):
            if name_trad and phone_trad and email_trad:
                form_data = {
                    'mode': 'TRADYCYJNE',
                    'price': price_trad,
                    'name': name_trad,
                    'phone': phone_trad,
                    'email': email_trad,
                    'equipment': equipment,
                    'studio': studio,
                    'length': length_trad,
                    'complexity': complexity
                }
                
                if send_whatsapp_notification(form_data):
                    st.markdown("""
                    <div class="success-message">
                        ✓ Dziękujemy! Wkrótce się z Tobą skontaktujemy.
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
            else:
                st.error("⚠️ Proszę wypełnić wszystkie pola kontaktowe")
    
    # AI MODE TAB
    with tab2:
        st.markdown("### AI Reklama")
        
        length_ai = st.slider(
            "Długość wideo (sekundy)",
            min_value=15,
            max_value=120,
            value=60,
            step=1,
            key='length_ai'
        )
        
        st.markdown("""
        <div class="info-box">
            <p style="font-size: 14px; color: #a0a0a0; line-height: 1.6; margin: 0;">
                <strong>AI REKLAMA</strong> - Szybka, automatyczna produkcja wykorzystująca sztuczną inteligencję. 
                Idealna dla treści social media i kampanii online.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate price
        price_ai = calculate_ai_price(length_ai)
        
        # Display price
        st.markdown(f"""
        <div class="price-display">
            <div class="price-label">Szacowany Kosztorys</div>
            <div class="price-amount">{price_ai:,} <span style="font-size: 24px;">PLN</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Lead form
        st.markdown("### 📋 Dane Kontaktowe")
        
        name_ai = st.text_input("Imię i nazwisko", key='name_ai')
        phone_ai = st.text_input("Telefon", key='phone_ai')
        email_ai = st.text_input("Email", key='email_ai')
        
        if st.button("🎬 UMÓW WIZYTĘ", key='submit_ai'):
            if name_ai and phone_ai and email_ai:
                form_data = {
                    'mode': 'AI REKLAMA',
                    'price': price_ai,
                    'name': name_ai,
                    'phone': phone_ai,
                    'email': email_ai,
                    'length': length_ai
                }
                
                if send_whatsapp_notification(form_data):
                    st.markdown("""
                    <div class="success-message">
                        ✓ Dziękujemy! Wkrótce się z Tobą skontaktujemy.
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
            else:
                st.error("⚠️ Proszę wypełnić wszystkie pola kontaktowe")

if __name__ == "__main__":
    main()
