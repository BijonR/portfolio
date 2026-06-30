from flask import Flask, render_template, send_from_directory, request, jsonify
import os, urllib.request, json
import requests

app = Flask(__name__)

# ===== SUPABASE — VISITOR COUNTER =====
SUPABASE_URL = "https://wdrfsxatfbwlhoxlkdtx.supabase.co/rest/v1"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkcmZzeGF0ZmJ3bGhveGxrZHR4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4MTAyNzcsImV4cCI6MjA5ODM4NjI3N30.10ams_FSawEHPQegYODPtwACN3BBixzcA1-Q95ixltE"

SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

portfolio_data = {
    "name": "Bijon Kanti Roy",
    "tagline": "Data Analyst | Aspiring ML Engineer",
    "bio": "I'm a Data Analyst working in the healthcare sector in Bangladesh, with a passion for turning complex data into actionable insights. With hands-on experience in SQL, Python, Power BI, and supply chain analytics, I'm on a mission to bridge the gap between data analysis and machine learning — ultimately contributing to AI-driven healthcare systems. Currently pursuing an M.Sc. in AI or Data Science in Germany to accelerate that journey.",
    "location": "Rangpur, Bangladesh",
    "email": "bijonroy720@gmail.com",
    "github": "https://github.com/BijonR",
    "linkedin": "https://www.linkedin.com/in/bijonkantiroy/",

    # Skills: category → list of {name, level, icon_url}
    # Icons from https://skillicons.dev (free, no API key needed)
    "skills": {
        "Data & Analytics": [
            {"name": "SQL",         "level": 80, "icon": "https://skillicons.dev/icons?i=mysql"},
            {"name": "Excel",       "level": 70, "icon": "https://img.icons8.com/color/96/microsoft-excel-2019--v1.png"},
            {"name": "Power BI",    "level": 70, "icon": "https://img.icons8.com/color/96/power-bi.png"},
            {"name": "Tableau",     "level": 75, "icon": "https://img.icons8.com/color/96/tableau-software.png"},
        ],
        "Programming": [
            {"name": "Python",      "level": 85, "icon": "https://skillicons.dev/icons?i=python"},
            {"name": "Pandas",      "level": 80, "icon": "https://img.icons8.com/color/96/pandas.png"},
            {"name": "NumPy",       "level": 78, "icon": "https://img.icons8.com/color/96/numpy.png"},
            {"name": "Matplotlib",  "level": 72, "icon": "https://img.icons8.com/color/96/matplotlib.png"},
        ],
        "ML & AI": [
            {"name": "Scikit-learn","level": 65, "icon": "https://img.icons8.com/color/96/scikit-learn.png"},
            {"name": "TensorFlow",  "level": 45, "icon": "https://skillicons.dev/icons?i=tensorflow"},
            {"name": "Statistics",  "level": 78, "icon": "https://img.icons8.com/color/96/statistics.png"},
        ],
        "Tools & Systems": [
            {"name": "Git",         "level": 68, "icon": "https://skillicons.dev/icons?i=git"},
            {"name": "GitHub",      "level": 68, "icon": "https://skillicons.dev/icons?i=github"},
            {"name": "Flask",       "level": 72, "icon": "https://skillicons.dev/icons?i=flask"},
            {"name": "MySQL",       "level": 88, "icon": "https://skillicons.dev/icons?i=mysql"},
        ],
    },

    "projects": [
        {
            "name": "School Management System",
            "description": "Backend development of a full-featured School Management System as a final-year project. Handles student records, attendance, academic results, and administrative workflows.",
            "tech": ["PHP", "MySQL", "Backend Development"],
            "github": "https://github.com/BijonR",
            "live": None,
        },
    ],

    "experience": [
        {
            "role": "Data Analyst",
            "company": "National Healthcare Services",
            "period": "January 2024 – Present",
            "points": [
                "Operational data analysis and KPI dashboard development using Power BI and Tableau",
                "Database design and management with MySQL for healthcare records",
                "Inventory optimization and demand forecasting using Python",
                "Supply chain coordination and reporting for medical supplies",
            ],
        },
        {
            "role": "Business Data Analyst - Part Time",
            "company": "National Healthcare Services",
            "period": "January 2023 – December 2023",
            "points": [
                "Operational data analysis and KPI dashboard development using Power BI and Tableau",
                "Database design and management with MySQL for healthcare records",
                "Inventory optimization and demand forecasting using Python",
                "Supply chain coordination and reporting for medical supplies",
            ],
        }
    ],

    "education": [
        {
            "degree": "B.Sc. in Computer Science & Engineering",
            "institution": "Daffodil International University",
            "period": "January 2019 – February 2023",
            "details": "CGPA: 3.65 / 4.00  |  VPD: 1.5 (German Scale)",
        },
        {
            "degree": "M.Sc. in Data Science",
            "institution": "Catholic University of Eichstaett-Ingolstadt",
            "period": "Winter 2026/27",
            "details": "In Progress",
        }
    ],

    "certifications": [
        {"name": "Data Science Foundations - Level 1", "issuer": "IBM",       "year": "2025"},
        {"name": "Google Analytics Certification",     "issuer": "Skillshop", "year": "2025"},
    ],

    "publications": [],
    "research": [],
    "problem_solving": [],
    "blog": [],
}


@app.route("/")
def index():
    return render_template("index.html", data=portfolio_data)


@app.route("/download-cv")
def download_cv():
    cv_dir = os.path.join(app.static_folder, "files")
    cv_file = "Bijon_Kanti_Roy_CV.pdf"
    if os.path.exists(os.path.join(cv_dir, cv_file)):
        return send_from_directory(cv_dir, cv_file, as_attachment=True)
    return "<h2 style='font-family:monospace;color:#9b5de5;text-align:center;margin-top:4rem'>CV coming soon!</h2>", 200


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    system = f"""You are Bijon's AI assistant on his portfolio website.
Bijon Kanti Roy is a Data Analyst at National Healthcare Services in Bangladesh.
He has a B.Sc. in CSE from Daffodil International University (CGPA 3.665/4.00, VPD 1.5 German scale).
He is skilled in Python, SQL, Power BI, Tableau, Excel, and is learning ML/AI.
He is applying for M.Sc. programs in Germany (AI/Data Science).
Answer questions about Bijon briefly and professionally. If asked something unrelated, say you can only answer questions about Bijon."""

    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 300,
        "system": system,
        "messages": [{"role": "user", "content": user_msg}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            reply = data["content"][0]["text"]
    except Exception as e:
        reply = "Sorry, I'm having trouble connecting right now. Please try again later."
    return jsonify({"reply": reply})


@app.route("/visit", methods=["POST"])
def track_visit():
    """Called once per page load — only counts once per visitor per day using a cookie."""
    from flask import make_response
    from datetime import datetime, timedelta

    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    already_visited = request.cookies.get("visited_date") == today_str

    try:
        # Always fetch current count first
        get_resp = requests.get(
            f"{SUPABASE_URL}/visitor_stats?id=eq.1&select=total_visits",
            headers=SUPABASE_HEADERS,
            timeout=5
        )
        rows = get_resp.json()
        current = rows[0]["total_visits"] if rows else 0

        if not already_visited:
            new_count = current + 1
            requests.patch(
                f"{SUPABASE_URL}/visitor_stats?id=eq.1",
                headers=SUPABASE_HEADERS,
                json={"total_visits": new_count},
                timeout=5
            )
            current = new_count

        resp = make_response(jsonify({"total_visits": current}))

        if not already_visited:
            # Cookie expires at midnight UTC
            tomorrow = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            resp.set_cookie("visited_date", today_str, expires=tomorrow)

        return resp
    except Exception as e:
        print("Visitor counter error:", e)
        return jsonify({"total_visits": None})


if __name__ == "__main__":
    app.run(debug=True)
