
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Lead Scoring Dashboard", layout="wide")

def calculate_lead_score(row):
    return (
        (2 * row['CumulativeTime']) +
        (2 * row['Number_of_Page_Visited']) +
        (5 * row['Unqiue_Visits']) +
        (3 * row['HighValuePageViews']) +
        (2 * row['DownloadedFilesCount']) +
        (1 * row['WhatsappOutbound']) +
        (10 * row['WhatsappInbound'])
    )

def categorize_lead(row):
    if row['lead_score'] >= 150 and row['WhatsappInbound'] >= 2:
        return 'Hot'
    elif 100 <= row['lead_score'] < 150 and row['WhatsappInbound'] >= 1:
        return 'Engaged'
    elif 60 <= row['lead_score'] < 100:
        return 'Warm'
    elif 30 <= row['lead_score'] < 60:
        return 'Curious'
    elif row['daysSinceLastWebActivity'] > 25 or row['daysSinceLastInbound'] > 25:
        return 'Dormant'
    else:
        return 'Cold'

st.title("📊 Lead Scoring & Engagement Strategy Dashboard")
st.markdown("Upload your lead data (.xlsx format). The app will score and bucket leads automatically.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")

    df.columns = df.columns.str.strip().str.replace(" ", "_")
    df['daysSinceLastInbound'] = df['daysSinceLastInbound'].fillna(999)
    df['daysSinceLastOutbound'] = df['daysSinceLastOutbound'].fillna(999)

    df['lead_score'] = df.apply(calculate_lead_score, axis=1)
    df['lead_bucket'] = df.apply(categorize_lead, axis=1)

    st.subheader("🧠 Scoring Summary")
    st.dataframe(df[['LeadId', 'lead_score', 'lead_bucket', 'CurrentStage']])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📌 Bucket Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x='lead_bucket', data=df, order=df['lead_bucket'].value_counts().index, palette="viridis", ax=ax)
        ax.set_title("Lead Buckets")
        st.pyplot(fig)

    with col2:
        st.markdown("### 📈 Lead Score Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['lead_score'], bins=20, kde=True, color='skyblue', ax=ax)
        ax.set_title("Lead Score Histogram")
        st.pyplot(fig)

    st.markdown("### 🎯 Content & Engagement Recommendations")

    strategies = {
        'Hot': '✅ Immediate personal WhatsApp/call + Send cost sheet + Site visit push',
        'Engaged': '🟡 Send walkthrough videos + clear pricing + interest form',
        'Warm': '🔵 Testimonials, short videos, ROI case studies',
        'Curious': '🟠 Light educational content, blog posts, project USP reels',
        'Cold': '⚪ Monthly newsletters, occasional offers',
        'Dormant': '🔴 Targeted reactivation message with limited-time incentive',
    }

    for bucket, recommendation in strategies.items():
        st.markdown(f"**{bucket}** → {recommendation}")

    st.markdown("---")
    st.markdown("### 🔍 Scoring Logic Explained")
    st.markdown("""
    - **+10** → Each inbound WhatsApp message  
    - **+5** → Each unique site visit  
    - **+3** → Each high-value page view (pricing, book-visit, cost sheet)  
    - **+2** → Total time spent & total page views  
    - **+2** → Each file download  
    - **+1** → Each outbound WhatsApp sent  
    """)

else:
    st.info("Upload an Excel file with columns like: `LeadId`, `CumulativeTime`, `WhatsappInbound`, `WhatsappOutbound`, `Unqiue_Visits`, etc.")
