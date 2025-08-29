from flask import Flask, request, jsonify, render_template
from datetime import datetime
import re
import os

app = Flask(__name__)

def process_array(data_array):
    """
    Process the input array and return the required output
    """
    try:
        odd_numbers = []
        even_numbers = []
        alphabets = []
        special_characters = []
        numbers_sum = 0
        alphabet_strings = []
        
        for item in data_array:
            item_str = str(item)
            
            # Check if it's a number
            if item_str.replace('-', '').replace('.', '').isdigit():
                num = int(float(item_str))
                if num % 2 == 0:
                    even_numbers.append(str(num))
                else:
                    odd_numbers.append(str(num))
                numbers_sum += num
            # Check if it's an alphabet (single character or word)
            elif re.match(r'^[a-zA-Z]+$', item_str):
                alphabets.append(item_str.upper())
                alphabet_strings.append(item_str)
            # Check if it's a special character
            else:
                special_characters.append(item_str)
        
        # Create concatenated string with alternating caps in reverse order
        concat_string = ""
        if alphabet_strings:
            # Join all alphabet strings and reverse
            all_chars = ''.join(alphabet_strings)
            reversed_chars = all_chars[::-1]
            
            # Apply alternating caps
            for i, char in enumerate(reversed_chars):
                if i % 2 == 0:
                    concat_string += char.upper()
                else:
                    concat_string += char.lower()
        
        return {
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": str(numbers_sum),
            "concat_string": concat_string
        }
    except Exception as e:
        raise Exception(f"Error processing array: {str(e)}")

@app.route('/bfhl', methods=['POST'])
def bfhl():
    """
    Main endpoint that processes the input array
    """
    try:
        # Get request data
        request_data = request.get_json()
        
        if not request_data or 'data' not in request_data:
            return jsonify({
                "is_success": False,
                "error": "Missing 'data' field in request"
            }), 400
        
        data_array = request_data['data']
        
        if not isinstance(data_array, list):
            return jsonify({
                "is_success": False,
                "error": "'data' must be an array"
            }), 400
        
        # Process the array
        processed_data = process_array(data_array)
        
        # Get current date for user_id
        current_date = datetime.now().strftime("%d%m%Y")
        
        # Create response
        response = {
            "is_success": True,
            "user_id": f"john_doe_{current_date}",
            "email": "john@xyz.com",
            "roll_number": "ABCD123",
            **processed_data
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "is_success": False,
            "error": str(e)
        }), 500

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with web interface
    """
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "message": "BFHL API is running",
        "endpoint": "/bfhl",
        "method": "POST"
    }), 200

@app.route('/bfhl', methods=['GET'])
def bfhl_info():
    """
    GET endpoint to show API information
    """
    return jsonify({
        "message": "BFHL API",
        "usage": "Send POST request with JSON body containing 'data' array",
        "examples": {
            "basic": ["a", "1", "334", "4", "R", "$"],
            "mixed": ["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"],
            "alphabets_only": ["A", "ABcD", "DOE"],
            "numbers_only": ["1", "2", "3", "4", "5"],
            "special_chars": ["@", "#", "$", "%", "&"],
            "negative_numbers": ["-1", "2", "a", "B", "&"],
            "empty": []
        },
        "endpoint": "/bfhl",
        "method": "POST",
        "generate_data": "/bfhl/generate",
        "method_generate": "GET"
    }), 200

@app.route('/bfhl/generate', methods=['GET'])
def generate_test_data():
    """
    Generate dynamic test data based on query parameters
    """
    try:
        import random
        import string
        
        # Get query parameters
        data_type = request.args.get('type', 'random')
        count = int(request.args.get('count', 10))
        min_length = int(request.args.get('min_length', 1))
        max_length = int(request.args.get('max_length', 5))
        
        # Limit count for safety
        count = min(count, 50)
        
        generated_data = []
        
        if data_type == 'random':
            # Generate completely random data
            for _ in range(count):
                choice = random.choice(['number', 'alphabet', 'special'])
                if choice == 'number':
                    num = random.randint(-100, 100)
                    generated_data.append(str(num))
                elif choice == 'alphabet':
                    length = random.randint(min_length, max_length)
                    word = ''.join(random.choices(string.ascii_letters, k=length))
                    generated_data.append(word)
                else:
                    special_chars = ['@', '#', '$', '%', '&', '*', '-', '+', '=', '!', '?', '^', '~']
                    generated_data.append(random.choice(special_chars))
                    
        elif data_type == 'mixed':
            # Generate balanced mixed data
            num_count = count // 3
            alpha_count = count // 3
            special_count = count - num_count - alpha_count
            
            # Numbers
            for _ in range(num_count):
                num = random.randint(-50, 50)
                generated_data.append(str(num))
            
            # Alphabets
            for _ in range(alpha_count):
                length = random.randint(min_length, max_length)
                word = ''.join(random.choices(string.ascii_letters, k=length))
                generated_data.append(word)
            
            # Special characters
            special_chars = ['@', '#', '$', '%', '&', '*', '-', '+', '=', '!', '?', '^', '~']
            for _ in range(special_count):
                generated_data.append(random.choice(special_chars))
                
        elif data_type == 'numbers':
            # Generate only numbers
            for _ in range(count):
                num = random.randint(-100, 100)
                generated_data.append(str(num))
                
        elif data_type == 'alphabets':
            # Generate only alphabets
            for _ in range(count):
                length = random.randint(min_length, max_length)
                word = ''.join(random.choices(string.ascii_letters, k=length))
                generated_data.append(word)
                
        elif data_type == 'special':
            # Generate only special characters
            special_chars = ['@', '#', '$', '%', '&', '*', '-', '+', '=', '!', '?', '^', '~']
            for _ in range(count):
                generated_data.append(random.choice(special_chars))
                
        elif data_type == 'pattern':
            # Generate pattern-based data
            for i in range(count):
                if i % 3 == 0:
                    generated_data.append(str(i))
                elif i % 3 == 1:
                    generated_data.append(chr(97 + (i % 26)))  # a-z
                else:
                    special_chars = ['@', '#', '$', '%', '&']
                    generated_data.append(special_chars[i % len(special_chars)])
        
        # Shuffle the generated data
        random.shuffle(generated_data)
        
        return jsonify({
            "is_success": True,
            "generated_data": generated_data,
            "parameters": {
                "type": data_type,
                "count": count,
                "min_length": min_length,
                "max_length": max_length
            },
            "usage": "Use this data in POST /bfhl endpoint",
            "example_request": {
                "data": generated_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "is_success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
