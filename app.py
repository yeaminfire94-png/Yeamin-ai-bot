import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Config for Mobile Optimization
st.set_page_config(
    page_title="AI Trading Signal Analyzer",
    page_icon="📈",
    layout="centered"
)

# Custom CSS for Mobile Friendly UI & Style
st.markdown("""
    <style>
    .main {
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        padding: 12px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 AI Trading Signal Analyzer")
st.caption("ক্যান্ডেলস্টিক স্ক্রিনশট অ্যানালাইসিস ও সিগন্যাল প্রেডিকশন টুল")

# Gemini API Key Setup
api_key = st.sidebar.text_input("Gemini API Key দিন:", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("অনুগ্রহ করে সাইডবারে Gemini API Key প্রবেশ করান।")

# 1. Broker Selection
brokers = ["Quotex", "Pocket Option", "Binomo", "IQ Option", "Binola", "Olymp Trade"]
selected_broker = st.selectbox("🎯 ব্রোকার নির্বাচন করুন:", brokers)

# 2. OTC Currency Pairs
otc_pairs = [
    "EUR/USD (OTC)", "EUR/GBP (OTC)", "EUR/JPY (OTC)", 
    "USD/BRL (OTC)", "USD/INR (OTC)", "USD/PKR (OTC)", 
    "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)",
    "NZD/USD (OTC)", "USD/BDT (OTC)"
]
selected_pair = st.selectbox("💱 OTC পেয়ার নির্বাচন করুন:", otc_pairs)

# Initialize Session State for Image Handling
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

st.write("---")

# 3. Screenshot Upload Mechanism
uploaded_file = st.file_uploader(
    "📸 চার্টের স্ক্রিনশট আপলোড করুন (JPG, PNG)", 
    type=["jpg", "jpeg", "png"],
    key="file_uploader"
)

if uploaded_file is not None:
    st.session_state.uploaded_image = Image.open(uploaded_file)

# Display Image & Cross/Delete Button
if st.session_state.uploaded_image is not None:
    st.write("### 🖼️ আপলোডকৃত চার্ট:")
    
    # Image Display
    st.image(st.session_state.uploaded_image, use_container_width=True)
    
    # Remove/Cross Button
    if st.button("❌ স্ক্রিনশট সরিয়ে ফেলুন (Remove Image)"):
        st.session_state.uploaded_image = None
        st.rerun()

# 4. Generate Signal Button
st.write("---")
if st.button("🚀 Analyze Chart & Get Signal"):
    if not api_key:
        st.error("❌ Gemini API Key দেওয়া হয়নি!")
    elif st.session_state.uploaded_image is None:
        st.warning("⚠️ অনুগ্রহ করে প্রথমে একটি চার্টের স্ক্রিনশট আপলোড করুন।")
    else:
        with st.spinner("🤖 AI চার্ট বিশ্লেষণ করছে, অপেক্ষা করুন..."):
            try:
                # Initialize Gemini Model
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Detailed Prompt for Chart Analysis
                prompt = f"""
                You are a professional Binary Options Trading Signal Analyzer for broker {selected_broker} and pair {selected_pair}.
                Analyze the provided chart image carefully:
                1. Identify key Support and Resistance levels.
                2. Identify candlestick patterns (e.g., Hammer, Engulfing, Doji, Pinbar).
                3. Determine current trend momentum.
                
                Based on technical analysis, provide a response in clear Bangla with:
                - Signal Direction: UP (CALL) or DOWN (PUT)
                - Signal Probability/Confidence (e.g., 85%)
                - Suggested Timeframe (e.g., 1 Min / 2 Min)
                - Detailed Technical Reason for this prediction.
                
                Format the response cleanly with markdown headers and emojis.
                Add a standard disclaimer at the bottom stating trading involves financial risk.
                """
                
                # Generate AI Analysis
                response = model.generate_content([prompt, st.session_state.uploaded_image])
                
                st.success("✅ বিশ্লেষণ সম্পন্ন হয়েছে!")
                st.markdown("### 📊 AI সিগন্যাল রেজাল্ট:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"একটি ত্রুটি ঘটেছে: {str(e)}")
