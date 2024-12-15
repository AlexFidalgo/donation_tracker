from flask import Flask, render_template, send_file
from app.scraper import scrape_donations
from app.formatter import prepare_data
from app.database import SessionLocal, DonationEntry
import pytz
import matplotlib
matplotlib.use("Agg")  # Use a non-GUI backend
import matplotlib.pyplot as plt
import io
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    # Scrape data from the website
    donation_value, goal_value = scrape_donations()

    if donation_value and goal_value:
        # Calculate percentage dynamically
        donation_float = float(donation_value.replace("R$", "").replace(".", "").replace(",", "."))
        goal_float = float(goal_value.replace("R$", "").replace(".", "").replace(",", "."))
        percentage = (donation_float / goal_float) * 100
        percentage_str = f"{percentage:.2f}%"

        # Pass the scraped values to the template
        return render_template("index.html", 
                               donation=donation_value, 
                               goal=goal_value, 
                               percentage=percentage_str)
    else:
        # If scraping fails, display an error message
        return render_template("index.html", 
                               donation="N/A", 
                               goal="N/A", 
                               percentage="N/A")

@app.route("/graph")
def graph():
    # Query all data from the database
    session = SessionLocal()
    entries = session.query(DonationEntry).order_by(DonationEntry.execution_date.asc()).all()
    session.close()

    # Extract data for the graph
    dates = [entry.execution_date.astimezone(pytz.timezone("America/Sao_Paulo")) for entry in entries]
    totals = [float(entry.total_arrecadado.replace("R$", "").replace(".", "").replace(",", ".")) for entry in entries]

    # Generate the graph
    plt.figure(figsize=(10, 6))
    plt.plot(dates, totals, marker="o", linestyle="-", color="blue")
    plt.title("Total Arrecadado vs. Time")
    plt.xlabel("Date")
    plt.ylabel("Total Arrecadado (R$)")
    plt.grid(True)

    # Save the graph to an in-memory buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    # Serve the graph as an image
    return send_file(buffer, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)