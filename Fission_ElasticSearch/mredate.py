from flask import request, current_app
from datetime import datetime

def main():
    try:
        data = request.get_json(force=True)
        date = data['date']
        date_object = datetime.fromisoformat(date)
        formatted_date = date_object.strftime("%Y-%m-%dT%H:%M:%SZ")
        return str(formatted_date)
    except KeyError:
        current_app.logger.error('No date found in the request data')
        return "No date found in request"
    except Exception as e:
        current_app.logger.error(f'Error: {e}')
        return f"Error processing date: {str(e)}"