from flask import Flask, request, jsonify
from db import SessionLocal
from models import Employee
from logger import get_logger

app = Flask(__name__)
logger = get_logger(__name__)

@app.route('/')
def index():
    logger.info("API health check endpoint accessed")
    return jsonify({"status": "healthy", "message": "Employee API is running"})

@app.route('/employees', methods=['GET'])
def get_employees():
    session = SessionLocal()
    try:
        status = request.args.get('status')
        country = request.args.get('country')
        logger.info(f"Fetching employees with filters - status: {status}, country: {country}")

        query = session.query(Employee)
        if status:
            query = query.filter(Employee.status == status)
        if country:
            query = query.filter(Employee.country == country)

        employees = query.all()
        return jsonify([{
            "id": emp.id,
            "name": emp.name,
            "status": emp.status,
            "country": emp.country
        } for emp in employees])
    except Exception as e:
        logger.error(f"Error fetching employees: {str(e)}")
        return jsonify({"error": "Internal server error"})
    finally:
        session.close()

@app.route('/employees', methods=['POST'])
def add_employee():
    session = SessionLocal()
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

        new_employee = Employee(name=name, country=country, status=status.lower())
        session.add(new_employee)
        session.commit()

        logger.info(f"Successfully added new employee: {name}")
        return jsonify({'message': 'Employee added successfully'})
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding employee: {str(e)}")
        return jsonify({"error": "Internal server error"})
    finally:
        session.close()

if __name__ == '__main__':
    logger.info("Starting Employee API server")
    app.run(host='0.0.0.0', port=5000)
