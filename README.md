# BFHL REST API - Full Stack

This is a REST API built with Python Flask that processes arrays and returns categorized data as per the VIT Full Stack Question requirements.

## Features

- **POST endpoint** at `/bfhl` that processes input arrays
- **Array processing** to separate even/odd numbers, alphabets, and special characters
- **Sum calculation** of all numbers in the array
- **String concatenation** with alternating caps in reverse order
- **Error handling** with graceful exception management
- **Health check** endpoints for monitoring

## API Endpoints

### 1. POST `/bfhl` - Main Processing Endpoint

**Request Body:**
```json
{
    "data": ["a", "1", "334", "4", "R", "$"]
}
```

**Response:**
```json
{
    "is_success": true,
    "user_id": "john_doe_26122024",
    "email": "john@xyz.com",
    "roll_number": "ABCD123",
    "odd_numbers": ["1"],
    "even_numbers": ["334", "4"],
    "alphabets": ["A", "R"],
    "special_characters": ["$"],
    "sum": "339",
    "concat_string": "Ra"
}
```

### 2. GET `/` - Health Check
Returns API status and basic information.

### 3. GET `/bfhl` - API Information
Returns usage instructions and examples.

## Logic Implementation

1. **Number Processing**: Identifies even/odd numbers and calculates sum
2. **Alphabet Processing**: Converts alphabets to uppercase
3. **Special Character Detection**: Identifies non-alphanumeric characters
4. **String Concatenation**: Reverses alphabet order and applies alternating caps
5. **User ID Generation**: Creates user_id in format `{full_name_ddmmyyyy}`

## Local Development

### Prerequisites
- Python 3.7+
- pip

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-name>

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The API will be available at `http://localhost:8000`

### Testing

#### Basic Testing
```bash
# Test the main endpoint
curl -X POST http://localhost:8000/bfhl \
  -H "Content-Type: application/json" \
  -d '{"data": ["a", "1", "334", "4", "R", "$"]}'

# Test health check
curl http://localhost:8000/
```

#### Dynamic Data Generation
The API now includes a dynamic data generation endpoint:

```bash
# Generate random data
curl "http://localhost:8000/bfhl/generate?type=random&count=15"

# Generate mixed data
curl "http://localhost:8000/bfhl/generate?type=mixed&count=20"

# Generate only numbers
curl "http://localhost:8000/bfhl/generate?type=numbers&count=25"

# Generate only alphabets
curl "http://localhost:8000/bfhl/generate?type=alphabets&count=30"

# Generate pattern-based data
curl "http://localhost:8000/bfhl/generate?type=pattern&count=15"
```

#### Advanced Testing Options

##### 1. **Dynamic Test Client**
```bash
# Run comprehensive dynamic tests
python3 dynamic_test_client.py
```

This generates random data patterns and tests the API with:
- Random data of different sizes
- Pattern-based data (Fibonacci, primes, vowels, etc.)
- Edge cases and boundary conditions
- Stress testing with large datasets

##### 2. **Configuration-Based Testing**
```bash
# Run predefined test scenarios
python3 config_test_runner.py
```

This uses `test_config.json` to run:
- Basic examples from the VIT question paper
- Edge cases and boundary conditions
- Different data patterns and combinations
- Mixed data type scenarios

##### 3. **Custom Test Scenarios**
You can modify `test_config.json` to add your own test scenarios:

```json
{
  "test_scenarios": {
    "my_custom_scenario": {
      "description": "My custom test scenario",
      "tests": [
        {
          "name": "Custom Test 1",
          "data": ["your", "custom", "data", "here"],
          "expected": {
            "even_numbers": [],
            "odd_numbers": [],
            "alphabets": ["YOUR", "CUSTOM", "DATA", "HERE"],
            "special_characters": [],
            "sum": "0",
            "concat_string": "HerEaTaDuMoCuYoUr"
          }
        }
      ]
    }
  }
}
```

## Deployment

### Option 1: Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Open app
heroku open
```

### Option 2: Railway
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Python app
3. Deploy with one click

### Option 3: Render
1. Connect your GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`
4. Deploy

### Option 4: Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel --python`

## Environment Variables

- `PORT`: Server port (default: 8000)

## Error Handling

The API handles various error scenarios:
- Missing or invalid request data
- Malformed JSON
- Processing errors
- Returns appropriate HTTP status codes and error messages

## Response Format

All responses include:
- `is_success`: Boolean indicating operation status
- `user_id`: Generated user ID with current date
- `email`: Static email address
- `roll_number`: Static roll number
- Processed data arrays
- Calculated sum and concatenated string

## Testing Examples

### Example A
**Input:** `["a","1","334","4","R","$"]`
**Expected Output:** Even numbers: ["334","4"], Odd numbers: ["1"], Sum: "339"

### Example B
**Input:** `["2","a","y","4","&","-","*","5","92","b"]`
**Expected Output:** Even numbers: ["2","4","92"], Odd numbers: ["5"], Sum: "103"

### Example C
**Input:** `["A","ABcD","DOE"]`
**Expected Output:** Alphabets: ["A","ABCD","DOE"], Sum: "0"

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
