from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
styles = getSampleStyleSheet()
def create_pdf(report_text):

    pdf_path = "reports/AI_Product_Feedback_Report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    story = []

    story.append(
        Paragraph(
            "<b>AI Product Feedback Report</b>",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(report_text.replace("\n","<br/>"),
        styles["BodyText"])
    )

    doc.build(story)

    return pdf_path
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
model = genai.GenerativeModel("gemini-2.5-flash")
st.set_page_config(
    page_title="AI Product Feedback Analyzer",
    page_icon="📊",
    layout="wide"
)
st.title("🤖 AI Product Feedback Analyzer")
st.write(
    "Analyze Google Play Store reviews using Python, Data Analytics and AI."
)
uploaded_file = st.file_uploader(
    "📂 Upload your Reviews CSV",
    type=["csv"]
)
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    reviews = "\n".join(df["content"].astype(str).head(100))
    prompt = f"""
You are an experienced Product Manager.

Analyze these customer reviews.

Provide:

1. Executive Summary

2. Top 5 User Pain Points

3. Top 5 Positive Highlights

4. Feature Suggestions

5. Product Improvement Recommendations

Customer Reviews:

{reviews}
"""

    total_reviews = len(df)

    average_rating = round(df["score"].mean(), 2)

    def get_sentiment(rating):

        if rating >= 4:
            return "Positive"

        elif rating == 3:
            return "Neutral"

        else:
            return "Negative"

    df["Sentiment"] = df["score"].apply(get_sentiment)

    positive = len(df[df["Sentiment"] == "Positive"])
    neutral = len(df[df["Sentiment"] == "Neutral"])
    negative = len(df[df["Sentiment"] == "Negative"])

    positive_percent = round((positive / total_reviews) * 100, 2)
    negative_percent = round((negative / total_reviews) * 100, 2)

    st.success("✅ File uploaded successfully!")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Total Reviews", total_reviews)

    with col2:
        st.metric("⭐ Average Rating", average_rating)

    with col3:
        st.metric("😊 Positive", f"{positive_percent}%")

    with col4:
        st.metric("😞 Negative", f"{negative_percent}%")

    st.subheader("📄 Uploaded Dataset")

    st.dataframe(df)
    
    st.subheader("📊 Dashboard Visualizations")

rating_chart = Image.open("charts/rating_distribution.png")
sentiment_chart = Image.open("charts/sentiment_pie.png")
trend_chart = Image.open("charts/review_trend.png")
top_words_chart = Image.open("charts/top_words.png")

col1, col2 = st.columns(2)

with col1:
    st.image(
        rating_chart,
        caption="📊 Rating Distribution",
        use_container_width=True
    )

with col2:
    st.image(
        sentiment_chart,
        caption="🥧 Sentiment Distribution",
        use_container_width=True
    )

col3, col4 = st.columns(2)

with col3:
    st.image(
        trend_chart,
        caption="📈 Review Trend",
        use_container_width=True
    )

with col4:
    st.image(
        top_words_chart,
        caption="☁️ Top 10 Important Words",
        use_container_width=True
    )
    st.subheader("🤖 AI Review Analysis")

if st.button("Generate AI Insights"):

    with st.spinner("Analyzing reviews..."):

        response = model.generate_content(prompt)

ai_report = response.text

pdf_file = create_pdf(ai_report)

with open(pdf_file, "rb") as pdf:

    PDFbyte = pdf.read()

st.success("Analysis Completed!")

st.markdown(ai_report)

st.download_button(
    label="📄 Download PDF Report",
    data=PDFbyte,
    file_name="AI_Product_Feedback_Report.pdf",
    mime="application/pdf"
)