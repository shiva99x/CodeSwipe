from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for using Flask sessions

# Sample user data (15 users) with random scores assigned
users = [
    {"id": 1, "name": "Alisson", "tech_stack": "Python, Flask", "project": "AI Chatbot", "points": random.randint(0, 1199)},
    {"id": 2, "name": "Bob", "tech_stack": "JavaScript, React", "project": "Web Dashboard", "points": random.randint(0, 1199)},
    {"id": 3, "name": "Charlie", "tech_stack": "Java, Spring Boot", "project": "API Framework", "points": random.randint(0, 1199)},
    {"id": 4, "name": "David", "tech_stack": "C++, Qt", "project": "Cross-platform App", "points": random.randint(0, 1199)},
    {"id": 5, "name": "Eve", "tech_stack": "Ruby, Rails", "project": "E-commerce Platform", "points": random.randint(0, 1199)},
    {"id": 6, "name": "Frank", "tech_stack": "Go, Kubernetes", "project": "Microservices Architecture", "points": random.randint(0, 1199)},
    {"id": 7, "name": "Grace", "tech_stack": "Swift, iOS", "project": "iOS Music App", "points": random.randint(0, 1199)},
    {"id": 8, "name": "Hannah", "tech_stack": "PHP, Laravel", "project": "Blog Platform", "points": random.randint(0, 1199)},
    {"id": 9, "name": "Isaac", "tech_stack": "TypeScript, Node.js", "project": "API Server", "points": random.randint(0, 1199)},
    {"id": 10, "name": "Jack", "tech_stack": "HTML, CSS, JavaScript", "project": "Portfolio Website", "points": random.randint(0, 1199)},
    
]

# Hardcoded questions with points
questions = [
    {"question": "What is the difference between a list and a tuple in Python?", "points": 5},
    {"question": "Explain the concept of RESTful APIs.", "points": 5},
    {"question": "How does a binary search algorithm work?", "points": 5}
]

# Home route
@app.route('/')
def index():
    # Reset session when visiting the home page
    session.pop('matches', None)  # Clear matches from the session
    session['matches'] = []  # Initialize matches as an empty list
    session['user_points'] = 0  # Initialize points to 0
    return render_template('index.html')

# Swipe route
@app.route('/swipe/<int:user_id>', methods=['GET', 'POST'])
def swipe(user_id):
    if user_id > len(users):  # Stop when no more users are left to swipe
        return redirect(url_for('connect'))

    user = users[user_id - 1]
    if request.method == 'POST':
        action = request.form['action']
        if action == 'right':  # Right swipe for connecting
            matches = session.get('matches', [])
            matches.append(user)  # Store the match in session
            session['matches'] = matches  # Update session data
        return redirect(url_for('swipe', user_id=user_id + 1))  # Move to the next user
    
    return render_template('swipe.html', user=user)

# Connections route
@app.route('/connect')
def connect():
    matches = session.get('matches', [])  # Get matches from the session
    return render_template('connect.html', matches=matches, user=None)  # Pass user as None or the current user if needed

# Challenges route to show daily questions and add points
@app.route('/challenges', methods=['GET', 'POST'])
def challenges():
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer:  # If the user answered a question
            # Award points for answering correctly (assuming all answers are correct for now)
            session['user_points'] += 5  # Add 5 points for each question solved

            # Update the current user's total score
            user_id = 1  # Example: assuming the first user is logged in (update with your authentication logic)
            users[user_id - 1]['points'] += 5

            return redirect(url_for('challenges'))  # Redirect to the challenges page to show updated score

    return render_template('challenges.html', questions=questions, points=session.get('user_points', 0))

# User Profile route
@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return "User  not found", 404
    return render_template('profile.html', user=user)



if __name__ == '__main__':
    app.run(debug=True)
