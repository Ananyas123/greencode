import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    n = data.get('elements', 1000)
    was_bad = data.get('is_nested_loop', True)
    
    # Logic: O(n^2) vs O(n)
    original_ops = n**2 if was_bad else n
    green_ops = n
    
    # 0.00001g CO2 per operation (demo estimate)
    saved_co2 = (original_ops - green_ops) * 0.00001
    
    return jsonify({
        "carbon_saved_grams": round(saved_co2, 4),
        "efficiency_boost": "99.9%" if was_bad else "0%",
        "message": f"Successfully saved {round(saved_co2, 2)}g of CO2!"
    })

if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port=5000)