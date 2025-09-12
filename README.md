
Avalanche Quizzler 🎮
Avalanche Quizzler is a quiz-based dApp prototype where users can choose categories, answer questions, track scores, and claim rewards.
The backend is powered by Flask, with SQLite as the database, and the frontend is a simple HTML/CSS/JS interface.

🚀 Features
    • Category selection: Gaming, Builders, NFTs
    • Quiz engine with random questions from the database
    • Session-based score tracking
    • End screen with results
    • NFT claim page (mockup for now, extendable)

📂 Project Structure
avalanche-quizzler/
│── appp/                 # Main backend app
│   ├── __init__.py       # Flask factory + DB + session setup
│   ├── routes.py         # API endpoints
│   ├── classdata.py      # Database models
│   ├── conductor.py      # Helper logic (local file)
│   ├── logic.py          # Validation logic
│   ├── getnstoreq.py     # DB interaction layer
│   ├── static/           # Frontend assets (CSS, JS, images)
│   └── templates/        # Frontend HTML pages
│
├── run.py                # Entry point
├── config.py             # Loads env variables
├── .env                  # Environment variables (API keys, secrets)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

⚙️ Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/YOUR_USERNAME/avalanche-quizzler.git

cd avalanche-quizzler

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Environment Variables
Create a .env file in the root directory and add your keys:
SECRET_KEY=supersecretkey
GROQ_KEY=your_api_key_here
To get the groq_key you would need to go to the groq api site 
https://console.groq.com/keys
And you would only need to use this groq_key if you want to populate the tables 

5️⃣ Database Setup
By default, the app uses SQLite (app.db).
The app.db should also be pushed with the rest of the code so it should be populated.
    • If you already have the populated app.db file, just run the app.
    • To check if it is populated go to your terminal, ensure the current directory is on root and then type sqlite3 appp/avalanche.db 
    • When it opens up then type select * from gamingquestion limit 5; 
    • If you see questions there then it is populated.
    • If not, run your population script (from populate.py) to seed the database with articles, summaries, and questions.
To run populate.py:
python3 -m appp.populate
Which would run the web scraping algorithm to populate the tables, a strong internet connection is also required. But if network makes the code crash, then go to the database file using sqlite3 appp/avalanche.db and delete all the contents by delete from table_name; 
Exit by .quit and the rerun the python file

▶️ Run the App
python run.py
Then open:
👉 http://127.0.0.1:5000

🎨 Frontend Pages
    • / → Category Selection
    • /quiz → Quiz Questions
    • /results → Score Summary
    • /claim → NFT Claim Page

🛠️ Tech Stack
    • Backend: Flask, SQLAlchemy, Flask-Session
    • Database: SQLite
    • Frontend: HTML, CSS, Vanilla JS
    • Environment: dotenv for secrets
