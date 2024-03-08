from flask import Flask, request, jsonify, render_template
import re

def evaluate_expression(expression):
    allowed_chars = "0123456789+-*%. "
    for char in expression:
        if char not in allowed_chars:
            raise ValueError("Invalid character in expression")
    expression = re.sub(r'(\d)([+\-*%])', r'\1 \2 ', expression)
    expression = re.sub(r'([+\-*/])(\d)', r' \1 \2', expression)
    expression = expression.replace("  ", " ")
    parts = expression.split()
    
    total = 0
    current_operator = "+"
    for part in parts:
        if part in "+-*%":
            current_operator = part
        else:
            try:
                number = float(part)
                if current_operator == "+":
                    total += number
                elif current_operator == "-":
                    total -= number
                elif current_operator == "*":
                    total *= number
                elif current_operator == "%":
                    if number == 0:
                        raise ValueError("Division by zero")
                    total /= number
            except ValueError as e:
                raise ValueError("Invalid number or operation") from e
    
    return total

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    operation = data.get('operation')
    try:
        result = evaluate_expression(operation)
        return jsonify(result=str(result))
    except ValueError as e:
        return jsonify(error=str(e)), 400


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
