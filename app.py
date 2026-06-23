import streamlit as st
import pandas as pd
import os
import plotly.express as px
import base64
import random
from datetime import datetime
from therapist_ai import get_therapy_response

# 1. Page Configuration
st.set_page_config(
    page_title="AI Mental Health Therapist",
    page_icon="🧠",
    layout="wide"
)

# Ensure directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# 2. Helper Functions
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

def show_gif(gif_path, width=300):
    if os.path.exists(gif_path):
        with open(gif_path, "rb") as file:
            contents = file.read()
            data_url = base64.b64encode(contents).decode("utf-8")
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" width="{width}">',
            unsafe_allow_html=True
        )
    else:
        st.info(f"✨ [GIF Placeholder: {gif_path}]")

# 3. Custom Enhanced Dark Theme CSS
bg_image = get_base64("assets/bg.jpg")
bg_style = f'url("data:image/jpg;base64,{bg_image}")' if bg_image else "none"

st.markdown(f"""
<style>
/* Main app background matching Dark Theme */
.stApp {{
    background-image: linear-gradient(
        rgba(10, 15, 30, 0.85),
        rgba(10, 15, 30, 0.95)
    ), {bg_style};
    background-color: #0A0F1D;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;
}}

/* Text Colors */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {{
    color: #F1F5F9 !important;
}}

/* Glassmorphic Metric Containers */
[data-testid="metric-container"] {{
    background: rgba(30, 41, 59, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(12px);
}}

/* Custom Gradient Buttons */
div.stButton > button {{
    background: linear-gradient(90deg, #1E40AF, #6D28D9);
    color: #FFFFFF !important;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    border: none;
    transition: all 0.3s ease;
}}

div.stButton > button:hover {{
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4);
}}

/* Sidebar Styling */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #070A13, #0F172A);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}}

section[data-testid="stSidebar"] * {{
    color: #E2E8F0 !important;
}}

/* Download Button Specific Tweaks */
div.stDownloadButton > button {{
    color: #FFFFFF !important;
    background: #10B981 !important;
    font-weight: bold;
    border-radius: 12px;
}}
</style>
""", unsafe_allow_html=True)

# 4. Header Notification and Clock
st.info("🔔 Hello Samridhi! Don't forget to log your mood today. 😊")

col_header1, col_header2 = st.columns([4, 1])
with col_header2:
    st.write("📅", datetime.now().strftime("%d %B %Y"))
    st.write("🕒", datetime.now().strftime("%I:%M %p"))

# 5. Sidebar Navigation
with st.sidebar:
    st.markdown("# 🧠 MindCare AI")
    st.write("Your Mental Wellness Partner")
    st.markdown("---")
    st.markdown("### 👤 Samridhi")
    st.write("Welcome Back! 👋")
    st.markdown("---")
    
    st.button("🏠 Dashboard")
    st.button("📈 Mood History")
    st.button("📊 Analytics")
    st.button("📅 Calendar View")
    st.button("🤖 Therapist Chat")
    st.button("💡 Tips & Resources")
    st.button("🏆 Achievements")
    st.button("👤 Profile")
    
    st.markdown("---")
    st.info(
        "💜 Your mental health is a priority.\n\n"
        "Your happiness is essential.\n\n"
        "Self-care is not selfish."
    )
    st.button("📄 Download Report")

# 6. Main Dashboard Header
st.markdown("""
<h1 style="text-align:center; font-size:50px; color:white; margin-bottom: 0px;">
AI Mental Wellness Dashboard
</h1>
""", unsafe_allow_html=True)
st.caption("<p style='text-align:center;'>Mood Tracking • Analytics • Mental Wellness Support</p>", unsafe_allow_html=True)
st.write("")

# 7. Mood Selector Grid
st.subheader("Select Your Current Mood")
st.info("🧠 Track your emotions and monitor mental wellness trends.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    happy = st.button("😊 Happy")
    sad = st.button("😔 Sad")
with col2:
    angry = st.button("😠 Angry")
    anxious = st.button("😰 Anxious")
with col3:
    stressed = st.button("😩 Stressed")
    excited = st.button("🤩 Excited")
with col4:
    tired = st.button("😴 Tired")
    confident = st.button("😎 Confident")

mood = None
if happy: mood = "😊 Happy"
elif sad: mood = "😔 Sad"
elif angry: mood = "😠 Angry"
elif anxious: mood = "😰 Anxious"
elif stressed: mood = "😩 Stressed"
elif excited: mood = "🤩 Excited"
elif tired: mood = "😴 Tired"
elif confident: mood = "😎 Confident"

# Load existing history data safely
csv_path = "data/mood_history.csv"
if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    updated_data = pd.read_csv(csv_path)
else:
    updated_data = pd.DataFrame(columns=["Date", "Mood"])

# 8. Action on Mood Selection
if mood:
    try:
        response = get_therapy_response(mood)
    except Exception:
        response = "Stay strong and take care of yourself!"

    st.success(f"Detected Mood: {mood}")
    
    if mood == "😊 Happy":
        st.balloons()
        st.success("🥳 Great! Keep spreading positivity.")
        if os.path.exists("assets/happy.gif"):
            st.image("assets/happy.gif", width=300)
    elif mood == "😔 Sad":
        st.snow()
        st.warning("💙 It's okay to feel sad. Better days are coming.")
        show_gif("assets/sad.gif")
    elif mood == "😠 Angry":
        st.error("😌 Take a deep breath and relax.")
        st.info("🫁 Try 5 deep breaths right now.")
        if os.path.exists("assets/angry.gif"):
            st.image("assets/angry.gif", width=300)
    elif mood == "😰 Anxious":
        st.info("🫂 You are safe. Focus on your breathing.")
        st.warning("🌿 Take a few moments to relax.")
        show_gif("assets/anxiety.gif")
    elif mood == "😩 Stressed":
        st.warning("☕ Take a short break and drink some water.")
        st.info("🎵 Listening to calm music may help.")
        show_gif("assets/stressed.gif")
    elif mood == "🤩 Excited":
        st.balloons()
        st.success("🚀 Channel your energy into something productive!")
        show_gif("assets/excited.gif")
    elif mood == "😴 Tired":
        st.info("😴 Your body needs rest. Take care.")
        st.warning("🛌 Try to get 7-8 hours of sleep.")
        show_gif("assets/tired.gif")
    elif mood == "😎 Confident":
        st.success("💪 Amazing! Believe in yourself and keep going.")
        st.info("🎯 This is a great time to work on your goals.")
        if os.path.exists("assets/confident.gif"):
            st.image("assets/confident.gif", width=300)

    st.markdown("---")

    # Save new log to history
    new_entry = pd.DataFrame({
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "Mood": [mood]
    })
    updated_data = pd.concat([updated_data, new_entry], ignore_index=True)
    updated_data.to_csv(csv_path, index=False)

# 9. Dashboard Analytics and Data Visualization
if not updated_data.empty:
    st.subheader("📈 Mood History")
    st.bar_chart(updated_data["Mood"].value_counts())
    
    most_common = updated_data["Mood"].mode()[0] if not updated_data["Mood"].mode().empty else "N/A"
    
    st.markdown("### 📊 Dashboard Summary")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.metric(label="📋 Total Entries", value=len(updated_data))
    with col_m2:
        st.metric(label="😊 Most Common Mood", value=most_common)
    with col_m3:
        st.metric(label="👥 Unique Moods", value=updated_data["Mood"].nunique())
        
    positive_moods_list = ["😊 Happy", "😎 Confident", "🤩 Excited", "💪 Motivated", "🤗 Grateful", "🥰 Loved", "🥳 Energetic"]
    positive_count = updated_data[updated_data["Mood"].isin(positive_moods_list)].shape[0]
    score = (positive_count / len(updated_data)) * 100 if len(updated_data) > 0 else 0
    
    with col_m4:
        st.metric(label="💚 Wellness Score", value=f"{score:.0f}%")
        
    st.markdown("### 🔍 Search Mood History")
    search_mood = st.selectbox("Filter by Mood", ["All"] + list(updated_data["Mood"].unique()))
    filtered_data = updated_data if search_mood == "All" else updated_data[updated_data["Mood"] == search_mood]
    st.dataframe(filtered_data, use_container_width=True)
    
    # Pie Chart
    mood_counts = updated_data["Mood"].value_counts()
    fig = px.pie(values=mood_counts.values, names=mood_counts.index, hole=0.5, title="🥧 Mood Distribution")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend Chart
    st.subheader("📈 Mood Trend")
    trend_data = updated_data.copy()
    trend_data["Count"] = range(1, len(trend_data) + 1)
    st.line_chart(trend_data.set_index("Date")["Count"])
    
    # Progress Bar Score
    st.markdown("### 💚 Wellness Score Tracking")
    st.progress(int(score))
    st.metric("Mental Wellness Level", f"{score:.0f}%")
    
    if score >= 80: st.success("🌟 Excellent Mental Wellness")
    elif score >= 60: st.info("😊 Good Mental Wellness")
    elif score >= 40: st.warning("⚠️ Needs Some Attention")
    else: st.error("🚨 High Stress Detected")
    
    # Achievements Badges
    st.markdown("### 🏆 Achievements")
    badges = []
    if len(updated_data) >= 1: badges.append("🥇 First Mood Logged")
    if len(updated_data) >= 5: badges.append("🏅 5 Entries Completed")
    if len(updated_data) >= 10: badges.append("🎖️ Consistent Tracker")
    if positive_count >= 5: badges.append("🌟 Positive Thinker")
    if positive_count >= 10: badges.append("👑 Wellness Master")
    
    for badge in badges:
        st.success(badge)
        
    # Advanced Analytics
    st.markdown("### 📊 Advanced Analytics")
    negative_count = len(updated_data) - positive_count
    col_an1, col_an2 = st.columns(2)
    with col_an1:
        st.metric("😊 Positive Entries", positive_count)
    with col_an2:
        st.metric("😔 Other Entries", negative_count)
        
    # AI Insights
    st.markdown("### 🧠 AI Insights")
    st.info(f"""
    📊 Total Mood Entries: {len(updated_data)}
    😊 Most Frequent Mood: {most_common}
    🎯 Unique Moods Tracked: {updated_data['Mood'].nunique()}
    """)
    
    st.markdown("### 🔥 Mood Streak")
    st.metric("Current Streak", f"{positive_count} Positive Entries")
    
    # Self-Care Plans Block
    st.markdown("### 🧘 Personalized Self-Care Plan")
    plans = {
        "😊 Happy": ["🎉 Celebrate small wins", "📸 Capture a happy memory", "🤝 Spend time with loved ones"],
        "😔 Sad": ["🎵 Listen to calming music", "📞 Call a friend", "🌳 Take a short walk"],
        "😰 Anxious": ["🫁 5 minutes deep breathing", "🧘 Meditation", "📝 Write your thoughts"],
        "😩 Stressed": ["☕ Take a break", "💧 Drink water", "🚶 Walk for 10 minutes"],
        "😎 Confident": ["🎯 Set a new goal", "📚 Learn something new", "💪 Challenge yourself"],
        "😴 Tired": ["😴 Take proper rest", "💧 Drink enough water", "🛌 Sleep 7-8 hours", "📵 Avoid screens before sleep"],
        "🤩 Excited": ["🎯 Focus your energy on goals", "📚 Learn something new", "🚀 Start a productive task"]
    }
    if mood in plans:
        for item in plans[mood]:
            st.success(item)
            
    # Daily Wellness Tip
    st.markdown("### 🌤 Daily Wellness Tip")
    daily_tips = [
        "Drink at least 8 glasses of water today 💧",
        "Take a 10-minute walk 🚶",
        "Practice deep breathing for 2 minutes 🌬️",
        "Write 3 things you're grateful for 🙏",
        "Get at least 7 hours of sleep 😴",
        "Avoid excessive screen time 📱"
    ]
    st.info(random.choice(daily_tips))
    
    # Mental Health Tips Contextual
    st.markdown("### 🌈 Mental Health Tips")
    tips = {
        "😊 Happy": "Keep spreading positivity and maintain your healthy habits.",
        "😔 Sad": "Talk to someone you trust and engage in activities you enjoy.",
        "😠 Angry": "Take deep breaths and try a short walk before reacting.",
        "😰 Anxious": "Practice mindfulness and focus on the present moment.",
        "😩 Stressed": "Take breaks, hydrate yourself, and avoid multitasking.",
        "🤩 Excited": "Channel your energy into productive activities.",
        "😴 Tired": "Prioritize sleep and give yourself time to rest.",
        "😎 Confident": "Use your confidence to achieve today's goals."
    }
    if mood in tips:
        st.success(tips[mood])
        
    # Music Recommendations
    st.markdown("### 🎵 Music Recommendation")
    music = {
        "😊 Happy": "Upbeat Pop Playlist 🎶",
        "😔 Sad": "Calm Acoustic Music 🎸",
        "😠 Angry": "Relaxing Instrumental 🎹",
        "😰 Anxious": "Meditation Sounds 🌿",
        "😩 Stressed": "Lo-Fi Chill Beats 🎧",
        "🤩 Excited": "Energetic Workout Mix 🔥",
        "😴 Tired": "Sleep Sounds 😴",
        "😎 Confident": "Motivation Playlist 💪"
    }
    if mood in music:
        st.success(music[mood])
        
    # Weekly Summary Metrics
    st.markdown("### 📅 Weekly Mood Summary")
    positive_percentage = round((positive_count / len(updated_data)) * 100, 1)
    st.info(f"""
    📊 Total Entries: {len(updated_data)}
    😊 Positive Mood Percentage: {positive_percentage}%
    🏆 Most Common Mood: {most_common}
    """)
    
    st.markdown("### 🎨 Mood Status")
    if "Happy" in most_common or "Confident" in most_common:
        st.success("🟢 Overall Mood Status: Positive")
    elif "Excited" in most_common:
        st.info("🔵 Overall Mood Status: Energetic")
    elif "Sad" in most_common or "Anxious" in most_common:
        st.warning("🟡 Overall Mood Status: Needs Attention")
    else:
        st.error("🔴 Overall Mood Status: High Stress")
        
    # Goal Tracker
    st.markdown("### 🎯 Wellness Goal Tracker")
    goal = st.slider("How many positive moods do you want this week?", 1, 20, 10)
    progress = min(int((positive_count / goal) * 100), 100)
    st.progress(progress)
    st.write(f"Progress: {progress}%")
    
    st.markdown("### 🏅 Wellness Badge")
    if score >= 80: st.success("👑 Wellness Master")
    elif score >= 60: st.success("🌟 Positive Thinker")
    elif score >= 40: st.info("😊 Improving Mindset")
    else: st.warning("💪 Recovery In Progress")
    
    # Quotes block
    quotes = [
        "Believe in yourself and all that you are. 🌟",
        "Every day is a fresh start. 🌅",
        "Your mental health matters. 💚",
        "Progress is progress, no matter how small. 🌱",
        "You are stronger than you think. 💪"
    ]
    st.markdown("### 🌟 Quote of the Day")
    st.success(random.choice(quotes))
    
    st.markdown("### 💡 Daily Motivation")
    st.info('"Your mental health is a priority. Your happiness is essential."')
else:
    st.info("👋 Welcome! Please log your current mood above to populate the analytics dashboard panels.")

# 10. AI Therapist Chat Block
st.markdown("---")
st.markdown("## 🤖 AI Therapist Chat")
user_message = st.text_input("Tell me what's on your mind...")

if st.button("Send Message"):
    if user_message:
        msg = user_message.lower()
        if "stress" in msg or "stressed" in msg:
            st.success("😌 You seem stressed. Try deep breathing for 2 minutes and take a short break.")
        elif "sad" in msg:
            st.success("💙 It's okay to feel sad sometimes. Talk to someone you trust and be kind to yourself.")
        elif "happy" in msg:
            st.success("😊 That's wonderful! Keep doing what makes you happy.")
        elif "angry" in msg:
            st.success("😠 Take a pause before reacting. A short walk can help calm your mind.")
        elif "anxious" in msg:
            st.success("🫂 Focus on your breathing and try grounding yourself in the present moment.")
        else:
            st.success("🤖 Thank you for sharing. Remember to take care of yourself and prioritize your mental wellness.")
    else:
        st.warning("Please enter a message before sending.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #94A3B8; padding: 20px;'>
        Made by <b>Samridhi Pullani</b>
    </div>
    """,
    unsafe_allow_html=True
)