from flask import Flask, request, jsonify
from db import execute_query, get_connection
from logger import get_logger

app = Flask(__name__)
logger = get_logger(__name__)

@app.route('/')
def index():
    logger.info("API health check endpoint accessed")
    return jsonify({"status": "healthy", "message": "Employee API is running"})

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        status = request.args.get('status')
        country = request.args.get('country')
        logger.info(f"Fetching employees with filters - status: {status}, country: {country}")

        query = "SELECT id, name, status, country FROM employees WHERE 1=1"
        params = []

        if status:
            query += " AND status = %s"
            params.append(status)
        if country:
            query += " AND country = %s"
            params.append(country)

        data = execute_query(query, params, fetch=True)
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error fetching employees: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"})
    
@app.route('/employees', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        if not data:
            logger.warning("No JSON data provided in request")
            return jsonify({'error': 'No data provided'})

        name = data.get('name')
        country = data.get('country')
        status = data.get('status')

        if not all([name, country, status]):
            logger.warning(f"Missing required fields in request: {data}")
            return jsonify({'error': 'Missing required fields: name, country, status'})

        valid_statuses = ['active', 'inactive']
        if status.lower() not in valid_statuses:
            logger.warning(f"Invalid status provided: {status}")
            return jsonify({'error': f'Status must be one of active/inactive'})

        insert_query = "INSERT INTO employees (name, country, status) VALUES (%s, %s, %s)"
        execute_query(insert_query, (name, country, status.lower()))
        logger.info(f"Successfully added new employee: {name}")
        return jsonify({'message': 'Employee added successfully'})
    except Exception as e:
        logger.error(f"Error adding employee: {str(e)}")
        return jsonify({"error": f"Internal server error"})

if __name__ == '__main__':
    logger.info("Starting Employee API server")
    app.run(host='0.0.0.0', port=5000)
