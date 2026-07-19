import streamlit as st
import random
import json


# Gemini (Optional)
try:
    import google.generativeai as genai
except:
    genai = None

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="AI Sports Quiz Generator",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 AI Sports Quiz Generator")
st.write("Generate AI Sports Quiz using Google Gemini")

# -----------------------------
# LOAD API KEY
# -----------------------------


API_KEY = st.secrets["GOOGLE_API_KEY"]

model = None

if genai and API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
    except:
        model = None

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Quiz Settings")

sport = st.sidebar.selectbox(
    "🏅 Select Sport",
    [
        "Cricket",
        "Football",
        "Tennis",
    ]
)

difficulty = st.sidebar.selectbox(
    "🎯 Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

num_questions = st.sidebar.slider(
    "📝 Number of Questions",
    5,
    20,
    5
)

generate = st.sidebar.button("🚀 Generate Quiz")

# -----------------------------
# SESSION STATE
# -----------------------------
if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "score" not in st.session_state:
    st.session_state.score = 0

if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.sidebar.markdown("---")

st.sidebar.subheader("🏆 Score")

if st.session_state.submitted:
    st.sidebar.success(
        f"{st.session_state.score}/{len(st.session_state.quiz)}"
    )
else:
    st.sidebar.info("Quiz Not Submitted")

    # -----------------------------
# FALLBACK QUIZ DATA
# -----------------------------

quiz_data = {

"Cricket":{

"Easy":[

{
"question":"How many players are there in a cricket team?",
"options":["9","10","11","12"],
"answer":"11"
},

{
"question":"Who is called the God of Cricket?",
"options":["Virat Kohli","MS Dhoni","Sachin Tendulkar","Rohit Sharma"],
"answer":"Sachin Tendulkar"
},

{ 
"question":"How many runs are awarded for a boundary?",
"options":["2","4","6","8"],
"answer":"4"
},
{
    "question":"Which color ball is mostly used in Test cricket?",
    "options":["Red","White","Pink","Blue"],
    "answer":"Red"
},

{
    "question":"How many wickets does each team have?",
    "options":["8","9","10","11"],
    "answer":"10"
}

],

"Medium":[

{
"question":"Who won the ICC Cricket World Cup 2011?",
"options":["Australia","India","England","Pakistan"],
"answer":"India"
},

{
"question":"Which country invented Cricket?",
"options":["India","England","Australia","South Africa"],
"answer":"England"
},

{
"question":"How many overs are there in a T20 innings?",
"options":["10","15","20","25"],
"answer":"20"
},
{
    "question":"Which country won the first ICC Cricket World Cup?",
    "options":["India","West Indies","Australia","England"],
    "answer":"West Indies"
},

{
    "question":"What does LBW stand for?",
    "options":["Leg Before Wicket","Long Ball Wicket","Leg Behind Wicket","Long Before Wide"],
    "answer":"Leg Before Wicket"
}

],

"Hard":[

{
"question":"Who scored the first ODI double century?",
"options":["Sachin Tendulkar","Virender Sehwag","Rohit Sharma","Chris Gayle"],
"answer":"Sachin Tendulkar"
},

{
"question":"Who has the most international centuries?",
"options":["Virat Kohli","Sachin Tendulkar","Ricky Ponting","Rohit Sharma"],
"answer":"Sachin Tendulkar"
},

{
"question":"Who has won the most IPL titles as captain?",
"options":["MS Dhoni","Rohit Sharma","Virat Kohli","Hardik Pandya"],
"answer":"Rohit Sharma"
},

{
"question":"Which bowler has the highest wickets in Test cricket?",
"options":["Shane Warne","Muralitharan","Anderson","Kumble"],
"answer":"Muralitharan"
},
{
    "question":"Which country won the ICC Cricket World Cup 1983?",
    "options":["India","Australia","England","Pakistan"],
    "answer":"India"
}

]

},

# -----------------------------

"Football":{

"Easy":[

{
"question":"How many players are there in a football team?",
"options":["9","10","11","12"],
"answer":"11"
},

{
"question":"Who won FIFA World Cup 2022?",
"options":["France","Argentina","Brazil","Germany"],
"answer":"Argentina"
},

{
"question":"Which player is called GOAT by many fans?",
"options":["Messi","Ronaldo","Mbappe","Neymar"],
"answer":"Messi"
},
{
    "question":"How many minutes are played in normal football time?",
    "options":["80","90","100","120"],
    "answer":"90"
},

{
    "question":"Which body part cannot touch the ball except the goalkeeper?",
    "options":["Head","Foot","Hand","Chest"],
    "answer":"Hand"
}

],

"Medium":[

{
"question":"Which country hosted FIFA 2022?",
"options":["Russia","Brazil","Qatar","USA"],
"answer":"Qatar"
},

{
"question":"How many halves are there in football?",
"options":["1","2","3","4"],
"answer":"2"
},

{
"question":"Which club does Lionel Messi currently play for?",
"options":["Barcelona","PSG","Inter Miami","Al Nassr"],
"answer":"Inter Miami"
},
{
    "question":"How many points are awarded for a win?",
    "options":["1","2","3","4"],
    "answer":"3"
},

{
    "question":"Which country is famous for Samba Football?",
    "options":["Brazil","Germany","Spain","Italy"],
    "answer":"Brazil"
}

],

"Hard":[

{
"question":"Who won the Golden Boot in FIFA 2022?",
"options":["Messi","Mbappe","Giroud","Kane"],
"answer":"Mbappe"
},

{
"question":"Which country has won the most FIFA World Cups?",
"options":["Germany","Brazil","Italy","Argentina"],
"answer":"Brazil"
},

{
"question":"How many minutes are played in normal football time?",
"options":["80","90","100","120"],
"answer":"90"
},

{
"question":"Who is known as CR7?",
"options":["Messi","Ronaldo","Neymar","Mbappe"],
"answer":"Ronaldo"
},
{
    "question":"Which player has won the most Ballon d'Or awards?",
    "options":["Ronaldo","Messi","Cruyff","Platini"],
    "answer":"Messi"
}

]

},

# -----------------------------

"Tennis":{

"Easy":[

{
"question":"Which Grand Slam is played on grass?",
"options":["French Open","Wimbledon","US Open","Australian Open"],
"answer":"Wimbledon"
},

{
"question":"How many players play singles tennis?",
"options":["1","2","3","4"],
"answer":"2"
},

{
"question":"Love means?",
"options":["0","15","30","40"],
"answer":"0"
},
{
    "question":"What is the object used to hit the tennis ball?",
    "options":["Bat","Racket","Stick","Club"],
    "answer":"Racket"
},

{
    "question":"Which Grand Slam is played in England?",
    "options":["French Open","US Open","Australian Open","Wimbledon"],
    "answer":"Wimbledon"
}

],

"Medium":[

{
"question":"Who has won the most Grand Slam titles?",
"options":["Federer","Nadal","Djokovic","Murray"],
"answer":"Djokovic"
},

{
"question":"Tennis is played using?",
"options":["Bat","Stick","Racket","Club"],
"answer":"Racket"
},

{
"question":"Which surface is French Open played on?",
"options":["Grass","Clay","Hard","Carpet"],
"answer":"Clay"
},
{
    "question":"How many points are needed to win a normal game?",
    "options":["30","40","50","60"],
    "answer":"40"
},

{
    "question":"Which Grand Slam is played on hard court?",
    "options":["US Open","French Open","Wimbledon","None"],
    "answer":"US Open"
}

],

"Hard":[

{
"question":"How many sets are played in men's Grand Slam final?",
"options":["3","5","4","2"],
"answer":"5"
},

{
"question":"Which country hosts Wimbledon?",
"options":["USA","Australia","England","France"],
"answer":"England"
},

{
"question":"Who is called the King of Clay?",
"options":["Federer","Djokovic","Nadal","Murray"],
"answer":"Nadal"
},

{
"question":"What is the maximum points in a normal game before deuce?",
"options":["30","40","50","60"],
"answer":"40"
},
{
    "question":"Which player has won the most Wimbledon men's singles titles?",
    "options":["Federer","Djokovic","Nadal","Sampras"],
    "answer":"Federer"
}

]

}

}
# -----------------------------
# GENERATE QUIZ
# -----------------------------

if generate:

    quiz = []

    # Try Gemini AI
    if model is not None:

        prompt = f"""
Generate {num_questions} multiple choice questions on {sport}.

Difficulty : {difficulty}

Return ONLY valid JSON.

Format:

[
{{
"question":"Question",
"options":["A","B","C","D"],
"answer":"Correct Answer"
}}
]
"""

        try:

            response = model.generate_content(prompt)

            text = response.text

            text = text.replace("json","")
            text = text.replace("","")

            quiz = json.loads(text)

        except:
            quiz = []

    # -----------------------------
    # FALLBACK QUESTIONS
    # -----------------------------

    if len(quiz) == 0:

        quiz = quiz_data[sport][difficulty]

        random.shuffle(quiz)

        if num_questions < len(quiz):
            quiz = quiz[:num_questions]

    st.session_state.quiz = quiz
    st.session_state.answers = {}
    st.session_state.score = 0
    st.session_state.submitted = False

    st.success("✅ Quiz Generated Successfully!")

# -----------------------------
# DISPLAY QUESTIONS
# -----------------------------

if len(st.session_state.quiz) > 0:

    st.header("📝 Quiz")

    for i, q in enumerate(st.session_state.quiz):

        answer = st.radio(

            f"Q{i+1}. {q['question']}",

            q["options"],

            key=f"q{i}"

        )

        st.session_state.answers[i] = answer
        # -----------------------------
# SUBMIT QUIZ
# -----------------------------

if len(st.session_state.quiz) > 0:

    if st.button("✅ Submit Quiz"):

        score = 0

        for i, q in enumerate(st.session_state.quiz):

            if st.session_state.answers.get(i) == q["answer"]:
                score += 1

        st.session_state.score = score
        st.session_state.submitted = True

# -----------------------------
# SHOW SCORE
# -----------------------------

if st.session_state.submitted:

    total = len(st.session_state.quiz)

    st.success(f"🎉 Your Score : {st.session_state.score}/{total}")

    percentage = (st.session_state.score / total) * 100

    st.progress(int(percentage))

    if percentage >= 80:
        st.balloons()
        st.success("Excellent Performance 🏆")

    elif percentage >= 50:
        st.info("Good Job 👍")

    else:
        st.warning("Keep Practicing 💪")

    st.markdown("---")
    st.header("✅ Correct Answers")

    for i, q in enumerate(st.session_state.quiz):

        st.write(f"### Q{i+1}. {q['question']}")

        user = st.session_state.answers.get(i)

        st.write(f"*Your Answer:* {user}")

        st.write(f"*Correct Answer:* {q['answer']}")

        if user == q["answer"]:
            st.success("Correct ✅")
        else:
            st.error("Wrong ❌")

        st.write("---")

# -----------------------------
# RESET QUIZ
# -----------------------------

if st.sidebar.button("🔄 Reset Quiz"):

    st.session_state.quiz = []
    st.session_state.answers = {}
    st.session_state.score = 0
    st.session_state.submitted = False

    st.rerun()

# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.markdown(
"""
<div style="text-align:center">

### 🏆 AI Sports Quiz Generator

Developed using

🐍 Python

🎈 Streamlit

🤖 Google Gemini AI

</div>
""",
unsafe_allow_html=True
)
