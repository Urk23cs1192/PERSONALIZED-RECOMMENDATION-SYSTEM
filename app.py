from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Add your API key here if you have one
client = OpenAI(api_key="YOUR_NEW_API_KEY")

# Store latest recommendations
latest_recommendations = ""


# -----------------------------------
# DEMO RECOMMENDATIONS
# -----------------------------------

demo_recommendations = """
1. Hands-On Machine Learning
Reason: A practical choice for improving your machine learning skills through real projects and examples.

2. Deep Learning with Python
Reason: This is useful for understanding neural networks, deep learning concepts, and AI application development.

3. Kaggle Learn
Reason: Kaggle provides short interactive courses that are suitable for learning AI and data science step by step.

4. Google AI Learning Resources
Reason: These resources can help you explore modern artificial intelligence concepts and practical applications.

5. Microsoft Learn
Reason: Microsoft Learn offers structured learning paths for AI, cloud computing, Python, and other technology skills.
"""


# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------
# GENERATE RECOMMENDATIONS
# -----------------------------------

@app.route("/recommend", methods=["POST"])
def recommend():

    global latest_recommendations

    data = request.get_json()

    name = data.get("name", "")
    age = data.get("age", "")
    interest = data.get("interest", "")
    preferences = data.get("preferences", "")
    requirements = data.get("requirements", "")

    prompt = f"""
You are RecomAI, a personalized recommendation system.

User Information:

Name: {name}
Age: {age}
Interest: {interest}
Preferences: {preferences}
Requirements: {requirements}

Generate exactly 5 personalized recommendations.

Rank them from most suitable to least suitable.

For each recommendation provide:

1. Recommendation name
2. Reason why it is suitable for this user.

Use this format:

1. Recommendation Name
Reason: explanation

2. Recommendation Name
Reason: explanation

3. Recommendation Name
Reason: explanation

4. Recommendation Name
Reason: explanation

5. Recommendation Name
Reason: explanation
"""

    try:

        response = client.responses.create(
            model="gpt-4.1",
            input=prompt
        )

        latest_recommendations = response.output_text

        return jsonify({
            "success": True,
            "recommendations": latest_recommendations,
            "demo": False
        })

    except Exception as e:

        print("OpenAI API unavailable.")
        print("Using demo recommendations instead.")
        print("Error:", e)

        # Use demo recommendations
        latest_recommendations = demo_recommendations

        return jsonify({
            "success": True,
            "recommendations": latest_recommendations,
            "demo": True
        })


# -----------------------------------
# REFINE RECOMMENDATIONS
# -----------------------------------

@app.route("/refine", methods=["POST"])
def refine():

    global latest_recommendations

    data = request.get_json()

    feedback = data.get("feedback", "")

    prompt = f"""
You are RecomAI, a personalized recommendation system.

Previous recommendations:

{latest_recommendations}

User feedback:

{feedback}

Generate exactly 5 improved recommendations based on
the user's feedback.

Rank them from most suitable to least suitable.

For each recommendation provide:

1. Recommendation name
2. Reason why it matches the updated preferences.

Use this format:

1. Recommendation Name
Reason: explanation

2. Recommendation Name
Reason: explanation

3. Recommendation Name
Reason: explanation

4. Recommendation Name
Reason: explanation

5. Recommendation Name
Reason: explanation
"""

    try:

        response = client.responses.create(
            model="gpt-4.1",
            input=prompt
        )

        latest_recommendations = response.output_text

        return jsonify({
            "success": True,
            "recommendations": latest_recommendations,
            "demo": False
        })

    except Exception as e:

        print("OpenAI API unavailable.")
        print("Using refined demo recommendations.")
        print("Error:", e)

        refined_demo = f"""
1. AI Project Roadmap
Reason: Based on your feedback, this gives you a practical path for building AI projects.

2. Kaggle AI Courses
Reason: Interactive exercises make it easier to strengthen your machine learning skills.

3. TensorFlow Learning
Reason: Useful for developing and experimenting with real deep learning projects.

4. Google Cloud AI
Reason: Helps you understand how modern AI systems are developed and deployed in the cloud.

5. GitHub AI Projects
Reason: Exploring real projects can help you learn implementation techniques and discover new ideas.
"""

        latest_recommendations = refined_demo

        return jsonify({
            "success": True,
            "recommendations": latest_recommendations,
            "demo": True
        })


# -----------------------------------
# START FLASK
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True)
