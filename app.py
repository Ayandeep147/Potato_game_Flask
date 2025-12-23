from flask import Flask, render_template, request, session

app = Flask(__name__)
# THIS IS SECRET KEY, FLASK USES IT FOR ENCRYPTION FOR SESSION SCORE 
# IF YOU HAPPEN TO REMOVE, IT WILL THROW AN ERROR
app.secret_key = "potato_secret"

# QUESTIONS AND ANSWERS TO DISPLAY ON HTML 
questions_list = [
    {
    "question": "What do you call a sheep who can sing and dance?",
    "options": [
        "Lady Ba Ba",
        "DJ Wool",
        "Baa-thoven",
        "Shearlock Holmes"],
    "answer": "Lady Ba Ba"},

    {
    "question": "Which vegetable has the best kung fu?",
    "options": [
        "Broc-lee",
        "Carrot Chop",
        "Kung Fu Cucumber",
        "Spin-achu"
    ],
    "answer": "Broc-lee"},

    {
    "question": "What’s an astronaut’s favorite part of a computer?",
    "options": [
        "The space bar",
        "The keyboard",
        "The mouse",
        "The screen"
    ],
    "answer": "The space bar"},

    {   "question": "What do you call fake spaghetti?",
        "options": [
            "Impasta",
            "Noodles.exe",
            "Almost pasta",
            "Spa-ghetti"],
        "answer": "Impasta"},
  
    {   "question": "Why don’t eggs tell jokes?",
        "options": [
            "They are shy",
            "They crack up",
            "They are serious",
            "They forgot the punchline"],
        "answer": "They crack up"}
]


# HOME PAGE ROUTE -----------------------------------------------------------------
@app.route("/")
def home():
    return render_template('home.html')

# QUESTION PAGE ROUTE -------------------------------------------------------------
@app.route("/start")
def quiz():
    session["question_index"] = 0
    session["score"] = 0

    current_question = questions_list[session["question_index"]]

    return render_template(
        'question.html',
        question_text = questions_list[0]["question"],
        options = questions_list[0]["options"],
        current_question = session["question_index"] + 1,
        total = len(questions_list))

# ANSWER RETRIEVAL AND STORAGE -----------------------------------------------------
@app.route("/answer", methods=["POST"])
def answer():
    selected = request.form.get("answer")

    # load next question
    current_question = questions_list[session["question_index"]]
    correct_answer = current_question["answer"]

    # update score if correct
    if selected == correct_answer:
        session["score"] += 1
    
    # MOVE TO NEXT QUESTION
    session["question_index"] += 1

    # check if questions are over
    if session["question_index"] >= len(questions_list):
        final_score = session['score']
        if final_score < 3:
            title_message = "😬 Uh oh… 😬"
            message = "🥔 You are not smarter than a potato"
        elif final_score == 3:
            title_message = "🤔 Hmm... 🤔"
            message = "😐 You are smart just as a potato"
        else:
            title_message = "😎 Well done... 😎"
            message = "🎉 You are smarter than a potato, well done!"
        return render_template(
            "result.html",
            total_score=final_score,
            total=len(questions_list),
            title_message=title_message,
            message=message
        )                        
    
    # load next question
    next_question = questions_list[session["question_index"]]

    return render_template(
        "question.html",
        question_text=next_question["question"],
        options=next_question["options"],
        current_question = session["question_index"] + 1,
        total = len(questions_list))

# ABOUT PAGE ROUTE ---------------------------------------------------------------
@app.route("/about")
def about():
    return render_template('about.template')

if __name__ == "__main__":
    app.run()
