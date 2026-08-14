import streamlit as st
import google.generativeai as genai
from PIL import Image

# Embedded API Key
API_KEY = "AQ.Ab8RN6JNBY3l8NJAzHQmn6NTEcvewQ2lMFvzinqM4L0oNnLfNg"

st.set_page_config(page_title="AI Trading Signal Analyzer", layout="centered")

st.title("📈 AI Trading Signal Analyzer")

brokers = ["Quotex", "Pocket Option", "Binomo", "IQ Option", "Binola", "Olymp Trade"]
selected_broker = st.selectbox("🎯 ব্রোকার সিলেক্ট করুন:", brokers)

otc_pairs = ["EUR/USD (OTC)", "EUR/GBP (OTC)", "EUR/JPY (OTC)", "USD/BRL (OTC)", "USD/INR (OTC)", "USD/PKR (OTC)"]
selected_pair = st.selectbox("💱 OTC পেয়ার সিলেক্ট করুন:", otc_pairs)

uploaded_file = st.file_uploader("📸 চার্টের স্ক্রিনশট দিন:", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("🚀 Analyze Chart"):
        try:
            genai.configure(api_key=API_KEY)
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
