from threading import Thread
from flask import Flask , render_template, request
import model as m
import pyttsx3
from openai import OpenAI
# import speech_recognition as sr
from bardapi import Bard
import os

app = Flask(__name__)
# response.set_cookie("__Secure-1PSID", value="your_value", secure=True)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 130)
engine.setProperty('volume', 80)

# openai.api_key = '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'
# Bard.set_api_key("AIzaSyDNBtlVYI2oRTDp1S-JQB7a8pkVLaBvuJk")
os.environ["BARD_API_KEY"] = "AIzaSyDvFxD3huha88UK64n0RqXZ77hyd99bm24"
# bard_inproxy = Bard(timeout=10)

client = OpenAI(api_key='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')

anxiety_score = 0
depression_score = 0
stress_score = 0
token = 'AIzaSyDvFxD3huha88UK64n0RqXZ77hyd99bm24'

def get_bard_analysis(anxietyscore, depressionscore, stressscore):
    prompt = f"Provide a detailed analysis for a user with Anxiety Score: {anxietyscore}, Depression Score: {depressionscore}, Stress Score: {stressscore}"
    # try:
    #     # response = Bard().ask(text=prompt)  # Pass `self` as argument
    #     response = Bard().get_answer(prompt)['content']
    #     print(response)
    #     return response
    # except Exception as e:
    #     print(f"Bard API error: {e}")
    #     return "Error: Unable to retrieve analysis from Bard API."
    
    bard = Bard(token=token)
    bard.get_answer(prompt)['content']

# def get_gpt_analysis(anxietyscore, depressionscore, stressscore):
#     # Use ChatGPT API for detailed analysis
#     prompt = f"Provide a detailed analysis for a user with Anxiety Score: {anxietyscore}, Depression Score: {depressionscore}, Stress Score: {stressscore}"
#     # response = openai.Completion.create(
#     #     model="gpt-3.5-turbo",
#     #     prompt=prompt,
#     #     max_tokens=200
#     # )
# #     completion = client.chat.completions.create(
# #   model="gpt-3.5-turbo",
# #   messages=[
# #     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
# #     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
# #   ]
# # )
# #     return completion['choices'][0]['content']
#     prompt = f"Provide a detailed analysis for a user with Anxiety Score: {anxietyscore}, Depression Score: {depressionscore}, Stress Score: {stressscore}"

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a mental health analysis assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=300  # You can adjust this value based on the desired response length
#     )

#     analysis_result = response['choices'][0]['message']['content']
#     print(analysis_result)
#     return analysis_result


def get_gpt_analysis(anxietyscore, depressionscore, stressscore):
    # Use ChatGPT API for detailed analysis
    prompt = f"Provide a detailed analysis for a user with Anxiety Score: {anxietyscore}, Depression Score: {depressionscore}, Stress Score: {stressscore}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a mental health analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300  # You can adjust this value based on the desired response length
    )

    analysis_result = response.choices[0].message.content
    print(analysis_result)
    return analysis_result

def get_analysis(anxietyscore, depressionscore, stressscore):
    # Use ChatGPT API for detailed analysis and recommendations
    prompt = f"Provide a detailed analysis and recommendations for a user with Anxiety Score: {anxietyscore}, Depression Score: {depressionscore}, Stress Score: {stressscore}. Also, suggest some music, TED Talks, and quotes."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a mental health analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500  # You can adjust this value based on the desired response length
    )

    analysis_result = response.choices[0].message.content
    print(analysis_result)
# Extracting recommendations based on a known prompt
    music_recommendations, ted_recommendations, quote_recommendations = extract_recommendations(analysis_result)
    recommendations = {'music': ['- "Happy" by Pharrell Williams', '- "Don\'t Stop Me Now" by Queen', '- "Walking on Sunshine" by Katrina and the Waves', '- "Three Little Birds" by Bob Marley', '- "I Will Survive" by Gloria Gaynor', '', 'TED Talks:', '1. "The Happy Secret to Better Work" by Shawn Achor', '2. "The Power of Vulnerability" by Brené Brown', '3. "All it takes is 10 mindful minutes" by Andy Puddicombe', '', 'Quotes:', '1. "Happiness is not something ready-made. It comes from your own actions." - Dalai Lama', '2. "The only way to do great work is to love what you do." - Steve Jobs', '3. "You are never too old to set another goal or to dream a new dream." - C.S. Lewis', '', "It is important to note that these suggestions are general recommendations and may not be suitable for everyone. If the user's mental health changes or if they develop any concerns, it is advisable to consult with a mental health professional for personalized advice and support"], 'ted_talks': ["1.The Power of Vulnerability by Brené Brown2. How to Make Stress Your Friend by Kelly McGonigal"
], 'quotes': ['1. "Happiness is not something ready-made. It comes from your own actions." - Dalai Lama', '2. "The only way to do great work is to love what you do." - Steve Jobs', '3. "You are never too old to set another goal or to dream a new dream." - C.S. Lewis', '', "It is important to note that these suggestions are general recommendations and may not be suitable for everyone. If the user's mental health changes or if they develop any concerns, it is advisable to consult with a mental health professional for personalized advice and support."]}
    # recommendations = {
    #     "music": music_recommendations,
    #     "ted_talks": ted_recommendations,
    #     "quotes": quote_recommendations
    # }
    print(recommendations)

    return analysis_result, recommendations

def extract_recommendations(analysis_result):
    # Extracting music recommendations
    music_start = analysis_result.find("Music Recommendations:")
    music_end = analysis_result.find("TED Talk Recommendations:")
    music_recommendations = [item.strip() for item in analysis_result[music_start:music_end].strip().split('\n')[1:]]

    # Extracting TED Talk recommendations
    ted_start = analysis_result.find("TED Talk Recommendations:")
    ted_end = analysis_result.find("Quotes:")
    ted_recommendations = [item.strip() for item in analysis_result[ted_start:ted_end].strip().split('\n')[1:]]

    # Extracting quote recommendations
    quote_start = analysis_result.find("Quotes:")
    quote_recommendations = [item.strip() for item in analysis_result[quote_start:].strip().split('\n')[1:]]

    return music_recommendations, ted_recommendations, quote_recommendations




def speak(audio):
    engine.say(audio)
    engine.runAndWait()

@app.route("/")
def index():
    # param = 'Hello Everyone. We help you to find if you are suffering from Anxiety/Stress/Depression and suggest measures to control it or manage it.'
    # thr = Thread(target=speak, args=[param])
    # thr.start()
    return render_template("index.html")

@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/form", methods = ["GET","POST"])
def model():
    if request.method == "POST":
        ##Anxiety Questions
        ans1 = request.form['q1']
        ans4 = request.form['q4']
        ans7 = request.form['q7']
        ans10 = request.form['q10']
        ans13 = request.form['q13']
        ans16 = request.form['q16']
        ans19 = request.form['q19']

        ##Depression Questions
        ans2 = request.form['q2']
        ans5 = request.form['q5']
        ans8 = request.form['q8']
        ans11 = request.form['q11']
        ans14 = request.form['q14']
        ans17 = request.form['q17']
        ans20 = request.form['q20']

        ##Stress Questions
        ans3 = request.form['q3']
        ans6 = request.form['q6']
        ans9 = request.form['q9']
        ans12 = request.form['q12']
        ans15 = request.form['q15']
        ans18 = request.form['q18']
        ans21 = request.form['q21']
    
        try:
            ans1 = float(ans1)
            ans2 = float(ans2)
            ans3 = float(ans3)
            ans4 = float(ans4)
            ans5 = float(ans5)
            ans6 = float(ans6)
            ans7 = float(ans7)
            ans8 = float(ans8)
            ans9 = float(ans9)
            ans10 = float(ans10)
            ans11 = float(ans11)
            ans12 = float(ans12)
            ans13 = float(ans13)
            ans14 = float(ans14)
            ans15 = float(ans15)
            ans16 = float(ans16)
            ans17 = float(ans17)
            ans18 = float(ans18)
            ans19 = float(ans19)
            ans20 = float(ans20)
            ans21 = float(ans21)
            global anxietyscore, stressscore, depressionscore
            anxietyscore = (ans1 + ans4 + ans7 + ans10 + ans13 + ans16 + ans19)*2
            depressionscore = (ans2 + ans5 + ans8 + ans11 + ans14 + ans17 + ans20)*2
            stressscore = (ans3 + ans6 + ans9 + ans12 + ans15 + ans18 + ans21)*2
            anxiety_score = anxietyscore
            depression_score = depressionscore
            stress_score = stressscore
            return render_template('result.html', result = anxietyscore, result1 = depressionscore, result2 = stressscore, calculation_success = True)
            
        except ValueError:
            return render_template(
                'form.html',
                result = "Bad Input",
                result1 = "Bad Input",
                result2 = "Bad Input",
                calculation_success = False,
                error = "Cannot perform the required calculation"
            )
    return render_template("form.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/form1", methods = ["GET","POST"])
def model1():
    if request.method == "POST":
        in1 = request.form['x1']
        in2 = request.form['x2']
        in3 = request.form['x3']
        in4 = request.form['x4']
        in5 = request.form['x5']
        in6 = request.form['x6']
        in7 = request.form['x7']
        in8 = request.form['x8']
        in9 = request.form['x9']
        in10 = request.form['x10']
        in11 = request.form['x11']
        in12 = request.form['x12']
        in13 = request.form['x13']

        try:
            in1 = float(in1)
            in2 = float(in2)
            in3 = float(in3)
            in4 = float(in4)
            in5 = float(in5)
            in6 = float(in6)
            in7 = float(in7)
            in8 = float(in8)
            in9 = float(in9)
            in10 = float(in10)
            in11 = float(in11)
            in12 = float(in12)
            in13 = float(in13)
            answer = m.anxiety_pred(in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12, in13, anxietyscore)
            answer1 = m.stress_pred(in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12, in13, stressscore)
            answer2 = m.depression_pred(in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12, in13, depressionscore)
            print(answer)
            print(answer1)
            print(answer2)
            return render_template("result1.html", my_answer = answer, my_answer1 = answer1, my_answer2 = answer2, calculation_success = True)
        except ValueError:
            return render_template("form1.html",
            my_answer = "Bad Input",
            calculation_success=False)
    return render_template("form1.html")



# @app.route("/detailed_report_gpt")
# def detailed_report():
#     # Retrieve scores from the session or database
#     anxietyscore =  anxiety_score
#     depressionscore =  depression_score
#     stressscore =  stress_score

#     # Get detailed analysis from GPT API
#     gpt_analysis = get_gpt_analysis(anxietyscore, depressionscore, stressscore)

#     return render_template("detailed_report.html", gpt_analysis=gpt_analysis)

# @app.route("/detailed_report")
# def detailed_report():
#     # Retrieve scores from the session or database
#     anxietyscore = anxiety_score
#     depressionscore = depression_score
#     stressscore = stress_score

#     # Get detailed analysis from Bard API
#     bard_analysis = get_bard_analysis(anxietyscore, depressionscore, stressscore)

#     return render_template("detailed_report.html", bard_analysis=bard_analysis)


# @app.route("/detailed_report1")
# def detailed_report():
#     # Retrieve scores from the session or database
#     anxietyscore = anxiety_score
#     depressionscore = depression_score
#     stressscore = stress_score

#     # Get detailed analysis from Bard API
#     gpt_analysis = get_gpt_analysis(anxietyscore, depressionscore, stressscore)

#     return render_template("detailed_report.html", gpt_analysis=gpt_analysis)


@app.route("/detailed_report")
def detailed_report():
    # Retrieve scores from the session or database
    anxietyscore = anxiety_score
    depressionscore = depression_score
    stressscore = stress_score

    # Get detailed analysis and recommendations from GPT API
    gpt_analysis, recommendations = get_analysis(anxietyscore, depressionscore, stressscore)

    return render_template("detailed_report.html", gpt_analysis=gpt_analysis, recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)