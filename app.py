from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <h2>Fashion Authenticity Checker</h2>
    <form method="POST" action="/verify_item">
      <input name="brand" placeholder="Enter Brand" required />
      <input name="model" placeholder="Enter Model" required />
      <button type="submit">Verify</button>
    </form>
    {% if result %}
      <h3>Result:</h3>
      <p>{{ result }}</p>
    {% endif %}
    """, result=None)

@app.route('/verify_item', methods=['POST'])
def verify():
    brand = request.form['brand']
    model = request.form['model']

    try:
        response = requests.get("http://brand_service:5001/brands")
        if response.status_code == 200:
            data = response.json()
            for item in data:
                if item['brand'].lower() == brand.lower() and item['model'].lower() == model.lower():
                    return render_template_string("""
                    <h2>✅ Item is Authentic!</h2>
                    <a href="/">Go back</a>
                    """)
            return render_template_string("""
            <h2>❌ Item NOT found. Might be Fake.</h2>
            <a href="/">Go back</a>
            """)
        else:
            return "Error fetching brand data", 500
    except Exception as e:
        return f"Error: {str(e)}", 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)   
