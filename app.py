import streamlit as st
from urllib.parse import urlparse, parse_qs
from video_info import get_video_info
from utils import get_transcript
from gemini_utils import summarize_text, generate_quiz



page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://static.vecteezy.com/system/resources/thumbnails/008/311/935/small/the-illustration-graphic-consists-of-abstract-background-with-a-blue-gradient-dynamic-shapes-composition-eps10-perfect-for-presentation-background-website-landing-page-wallpaper-vector.jpg");
    background-size: cover;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)



# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title= "YouTube AI summarizer",
    page_icon="🎥",
    layout="wide"
)

st.title("📺 YouTube video  Summarizer and Quiz Generator")
st.caption("Paste a YouTube video URL to generate an AI summary and quiz.")


# ---------------------------
# Session State
# ---------------------------
if "summary" not in st.session_state:
    st.session_state.summary = None

if "quiz" not in st.session_state:
    st.session_state.quiz = None


# ---------------------------
# URL Input
# ---------------------------
youtube_url = st.text_input("Paste a YouTube Video URL")


# ---------------------------
# Extract Video ID
# ---------------------------
def extract_video_id(url):

    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    if parsed_url.hostname in ("youtube.com", "www.youtube.com"):

        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]

    return None


# ---------------------------
# Main App
# ---------------------------
if youtube_url:

    video_id = extract_video_id(youtube_url)

    if video_id:

        # ---------------------------
        # Video Information
        # ---------------------------
        try:

            video_info = get_video_info(youtube_url)

            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(
                    video_info["thumbnail"],
                    use_container_width=True
                )

            with col2:
                st.subheader(video_info["title"])
                st.caption(f"👤 {video_info['channel']}")

            st.divider()

        except Exception:
            st.warning("Couldn't load video information.")

        # ---------------------------
        # Transcript
        # ---------------------------
        transcript = get_transcript(video_id)

        if transcript:

            st.subheader("📄 Transcript Preview")

            st.text_area(
                "Transcript",
                transcript,
                height=300
            )

            # ---------------------------
            # Summary Button
            # ---------------------------
            if st.button("Generate Summary"):

                with st.spinner("Generating Summary..."):

                    st.session_state.summary = summarize_text(
                        transcript[:12000]
                    )

                    st.session_state.quiz = None

            # ---------------------------
            # Display Summary
            # ---------------------------
            if st.session_state.summary:

                st.divider()

                st.subheader("📄 AI Summary")

                st.write(st.session_state.summary)

                st.divider()

                # ---------------------------
                # Quiz Settings
                # ---------------------------
                st.subheader("🧠 Generate Quiz")

                difficulty = st.selectbox(
                    "Difficulty",
                    ["Easy", "Medium", "Hard"]
                )

                num_questions = st.selectbox(
                    "Number of Questions",
                    [3, 5, 7, 10]
                )

                if st.button("Generate Quiz"):

                    with st.spinner("Creating Quiz..."):

                        st.session_state.quiz = generate_quiz(
                            transcript[:12000],
                            difficulty,
                            num_questions
                        )

if st.session_state.quiz:

    st.subheader("📝 Quiz")

    # Display all questions
    for i, question in enumerate(st.session_state.quiz["quiz"], start=1):

        st.write(f"### Question {i}")

        st.radio(
            question["question"],
            question["options"],
            key=f"q{i}"
        )

    # ONE submit button after ALL questions
    if st.button("Submit Quiz"):

        score = 0
        total = len(st.session_state.quiz["quiz"])

        st.header("🎉 Quiz Results")

        for i, question in enumerate(st.session_state.quiz["quiz"], start=1):

            user_answer = st.session_state.get(f"q{i}")

            correct_answer = question["answer"]

            if user_answer == correct_answer:

                score += 1
                st.success(f"✅ Question {i}: Correct")

            else:

                st.error(f"❌ Question {i}: Incorrect")

                st.write(f"Your Answer: {user_answer}")
                st.write(f"Correct Answer: {correct_answer}")

            st.write(question["explanation"])
            st.divider()

        percentage = score / total

        st.subheader(f"🏆 Score: {score}/{total}")

        st.progress(percentage)