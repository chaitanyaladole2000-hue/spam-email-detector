"""
Spam Email Detection Web Application
Model  : TF-IDF + Logistic Regression (sklearn)
History: Persisted in history.db (SQLite)
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from detector_sklearn import predict_spam

app = Flask(__name__)
app.secret_key = "spam_detector_secret_key_2024"

DB_PATH = "history.db"

# ── Database setup ─────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            email      TEXT    NOT NULL,
            prediction TEXT    NOT NULL,
            confidence REAL    NOT NULL,
            is_spam    INTEGER NOT NULL,
            checked_at TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_result(result):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO history (email, prediction, confidence, is_spam, checked_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        result["email_text"],
        result["prediction"],
        result["confidence"],
        1 if result["is_spam"] else 0,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT * FROM history ORDER BY id DESC LIMIT 10
    """).fetchall()
    total = conn.execute("SELECT COUNT(*) FROM history").fetchone()[0]
    spam  = conn.execute("SELECT COUNT(*) FROM history WHERE is_spam=1").fetchone()[0]
    ham   = conn.execute("SELECT COUNT(*) FROM history WHERE is_spam=0").fetchone()[0]
    conn.close()
    return {
        "total":  total,
        "spam":   spam,
        "ham":    ham,
        "recent": [dict(r) for r in rows]
    }

def clear_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM history")
    conn.commit()
    conn.close()

# ── Routes ─────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        email_text = request.form.get("email_text", "").strip()

        if not email_text:
            flash("Please enter email content to check!", "error")
            return redirect(url_for("predict"))

        if len(email_text) < 10:
            flash("Email content is too short. Please enter more text.", "error")
            return redirect(url_for("predict"))

        result = predict_spam(email_text)

        if result["label"] == "ERROR":
            flash(result.get("message", "Prediction failed."), "error")
            return redirect(url_for("predict"))

        save_result(result)

        return render_template(
            "result.html",
            result=result,
            email_text=email_text,
            history=get_history()
        )

    return render_template("predict.html", history=get_history())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/check-again")
def check_again():
    return redirect(url_for("predict"))


@app.route("/clear-history")
def clear_history():
    clear_db()
    flash("History cleared!", "success")
    return redirect(url_for("predict"))


# ── Error handlers ─────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html", error="Page not found!"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("index.html", error="Internal server error!"), 500


# ── Startup ────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()

    sklearn_ready = os.path.exists("spam_model.pkl") and os.path.exists("vectorizer.pkl")

    print("\n" + "=" * 60)
    print("MODEL STATUS")
    print("=" * 60)
    print(f"  sklearn  : {'✓ Ready' if sklearn_ready else '✗ Missing → run train_model.py'}")
    print(f"  history  : ✓ Saved in {DB_PATH}")
    if not sklearn_ready:
        print("\n  WARNING: Model files not found! Run train_model.py first.")
    print("=" * 60 + "\n")

    app.run(debug=True, host="0.0.0.0", port=5000)