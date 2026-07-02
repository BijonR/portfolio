from flask import Flask, render_template, send_from_directory, request, jsonify
import os, urllib.request, json
import requests
import xml.etree.ElementTree as ET
import re

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

def fetch_medium_posts(username, limit=6):
    try:
        feed_url = f"https://medium.com/feed/@{username}"
        resp = requests.get(feed_url, timeout=8)
        root = ET.fromstring(resp.content)
        channel = root.find('channel')
        posts = []
        for item in channel.findall('item')[:limit]:
            content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
            thumb = None
            if content is not None and content.text:
                match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content.text)
                if match:
                    thumb = match.group(1)
            posts.append({
                "title":     item.find('title').text,
                "link":      item.find('link').text,
                "date":      item.find('pubDate').text[:16],
                "thumbnail": thumb,
                "tags":      [c.text for c in item.findall('category')][:3],
            })
        return posts
    except Exception as e:
        print("Medium RSS error:", e)
        return []

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
            {"name": "SQL",         "level": 90, "icon": "https://skillicons.dev/icons?i=mysql"},
            {"name": "Excel",       "level": 85, "icon": "https://img.icons8.com/color/96/microsoft-excel-2019--v1.png"},
            {"name": "Power BI",    "level": 82, "icon": "https://img.icons8.com/color/96/power-bi.png"},
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
            "category": "Software Development",
        },
        {
            "name": "Healthcare KPI Dashboard",
            "description": "Interactive KPI dashboard for National Healthcare Services tracking supply chain performance, inventory levels, and operational metrics using Power BI and Python.",
            "tech": ["Power BI", "Python", "SQL", "Excel"],
            "github": None,
            "live": None,
            "category": "Data Analysis & Visualization",
        },
        {
            "name": "Medical Supply Demand Forecasting",
            "description": "Demand forecasting model for medical supplies using Python. Reduced overstock and stockout incidents by predicting future inventory needs based on historical data.",
            "tech": ["Python", "Pandas", "NumPy", "Scikit-learn"],
            "github": None,
            "live": None,
            "category": "Machine Learning & AI",
        },
        {
            "name": "Healthcare Supply Chain Analytics",
            "description": "End-to-end supply chain data analysis for a healthcare provider. Identified bottlenecks, reduced costs, and improved delivery timelines through data-driven insights.",
            "tech": ["SQL", "Python", "Tableau", "Excel"],
            "github": None,
            "live": None,
            "category": "Healthcare & Domain Projects",
        },
        {
            "name": "Student Score Statistical Analysis",
            "description": "10-page statistical report analyzing student scores dataset using Welch t-tests, ANOVA, Tukey HSD, Cohen's d, and eta-squared. Produced for TU Dortmund application.",
            "tech": ["Python", "Statistics", "ANOVA", "Research"],
            "github": None,
            "live": None,
            "category": "Research & Academic",
        },
    ],

    "project_categories": [
        {"name": "All",                          "icon": "⚡"},
        {"name": "Data Analysis & Visualization","icon": "📊"},
        {"name": "Machine Learning & AI",        "icon": "🤖"},
        {"name": "Software Development",         "icon": "💻"},
        {"name": "Healthcare & Domain Projects", "icon": "🏥"},
        {"name": "Research & Academic",          "icon": "🔬"},
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
        }
    ],

    "education": [
        {
            "degree": "B.Sc. in Computer Science & Engineering",
            "institution": "Daffodil International University",
            "period": "January 2019 – February 2023",
            "details": "CGPA: 3.665 / 4.00  |  VPD: 1.5 (German Scale)",
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
    blog_posts = fetch_medium_posts("BijonR", limit=6)
    return render_template("index.html", data=portfolio_data, blog_posts=blog_posts)


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
    """Called once per page load — increments and returns the visitor count."""
    try:
        get_resp = requests.get(
            f"{SUPABASE_URL}/visitor_stats?id=eq.1&select=total_visits",
            headers=SUPABASE_HEADERS,
            timeout=5
        )
        rows = get_resp.json()
        current = rows[0]["total_visits"] if rows else 0
        new_count = current + 1

        requests.patch(
            f"{SUPABASE_URL}/visitor_stats?id=eq.1",
            headers=SUPABASE_HEADERS,
            json={"total_visits": new_count},
            timeout=5
        )
        return jsonify({"total_visits": new_count})
    except Exception as e:
        print("Visitor counter error:", e)
        return jsonify({"total_visits": None})


@app.route("/visit-count", methods=["GET"])
def get_visit_count():
    """Just reads the current count without incrementing."""
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/visitor_stats?id=eq.1&select=total_visits",
            headers=SUPABASE_HEADERS,
            timeout=5
        )
        rows = resp.json()
        count = rows[0]["total_visits"] if rows else 0
        return jsonify({"total_visits": count})
    except Exception as e:
        print("Visitor counter error:", e)
        return jsonify({"total_visits": None})


if __name__ == "__main__":
    app.run(debug=True)
