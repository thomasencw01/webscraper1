from flask import Flask, render_template
import pandas as pd
from your_scrape_module import save_combined_data  # Import the save_combined_data function from scrape.py

app = Flask(__name__)

@app.route("/")
def index():
    # Save combined data from both sources
    save_combined_data()

    # Read combined data
    combined_data = pd.read_excel('funding_opportunities_combined.xlsx')

    # Convert Source URLs to clickable links
    combined_data['Source'] = combined_data['Source'].apply(lambda x: f'<a href="{x}" target="_blank">Source</a>')

    # Generate HTML table
    table = combined_data.to_html(classes='table table-striped', index=False, escape=False)  # escape=False allows HTML links

    return render_template('index.html', table=table)

if __name__ == "__main__":
    app.run(debug=True)
