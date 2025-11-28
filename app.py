from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/language_trend')
def language_trend():
    df = pd.read_csv("final_data_stackoverflow_questions.csv")

    # Ensure Year is string
    df['Year'] = df['Year'].astype(str)

    # Count total questions per year
    total_questions_per_year = df.groupby('Year').size().to_dict()

    # Count total mentions of each language per year
    grouped = df.groupby(['Year', 'Language']).size().reset_index(name='Count')

    # Normalize by total questions (like per capita calculation)
    grouped['Percentage'] = grouped.apply(lambda row: (row['Count'] / total_questions_per_year[row['Year']]) * 1000, axis=1)

    # Pivot to reshape for graphing
    pivot = grouped.pivot(index='Language', columns='Year', values='Percentage').fillna(0)

    # Get the top 10 languages based on total count
    top_languages = pivot.sum(axis=1).sort_values(ascending=False).head(10).index.tolist()
    filtered = pivot.loc[top_languages]

    # Format result for JSON
    result = []
    for lang in filtered.index:
        row = {"language": lang}
        for year in ['2022', '2023', '2024']:
            row[year] = round(filtered.at[lang, year], 2)
        result.append(row)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

