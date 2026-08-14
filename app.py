import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Trading Signal Analyzer", layout="centered")

st.title("📈 AI Trading Signal Analyzer")

# API Key input on main page
api_key = st.text_input("আপনার Gemini API Key এখানে দিন:", type="password")

if not api_key:
    st.warning("অনুগ্রহ করে উপরে আপনার Gemini API Key দিন।")

brokers = ["Quotex", "Pocket Option", "Binomo", "IQ Option", "Binola", "Olymp Trade"]
selected_broker = st.selectbox("🎯 ব্রোকার:", brokers)

otc_pairs = ["EUR/USD (OTC)", "EUR/GBP (OTC)", "EUR/JPY (OTC)", "USD/BRL (OTC)", "USD/INR (OTC)", "USD/PKR (OTC)"]
selected_pair = st.selectbox("💱 OTC পেয়ার:", otc_pairs)

uploaded_file = st.file_uploader("📸 চার্টের স্ক্রিনশট দিন:", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("🚀 Analyze Chart"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                with st.spinner("অ্যানালাইসিস হচ্ছে..."):
                    prompt = f"""
                    You are a professional Binary Options Trading Signal Analyzer for broker {selected_broker} and pair {selected_pair}.
                    Analyze the provided chart image carefully and provide response in clear Bangla:
                    - Signal Direction: UP (CALL) or DOWN (PUT)
                    - Signal Probability/Confidence
                    - Suggested Timeframe
                    - Detailed Technical Reason
                    """
                    response = model.generate_content([prompt, image])
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"ত্রুটি: {e}")
        else:
            st.error("API Key দিন!")
