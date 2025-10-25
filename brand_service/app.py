from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

brands = []

@app.route('/')
def index():
    return render_template_string("""
    <h2>Registered Brand Models</h2>
    <ul>
      {% for item in brands %}
        <li>{{ item['brand'] }} - {{ item['model'] }}</li>
      {% endfor %}
    </ul>
    <form method="POST" action="/brand">
      <input name="brand" placeholder="Brand Name" required />
      <input name="model" placeholder="Model Name" required />
      <button type="submit">Register Brand</button>
    </form>
    """, brands=brands)

@app.route('/brand', methods=['POST'])
def add_brand():
    brand = request.form.get('brand') or request.json.get('brand')
    model = request.form.get('model') or request.json.get('model')
    brands.append({'brand': brand, 'model': model})
    return jsonify({'message': 'Brand model registered successfully'}), 201

@app.route('/brands', methods=['GET'])
def get_brands():
    return jsonify(brands)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
