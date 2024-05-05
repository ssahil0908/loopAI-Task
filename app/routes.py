from flask import Blueprint, jsonify
from app.utils import generate_report
from app.models import Report

main_bp = Blueprint('main', __name__)

@main_bp.route('/trigger_report', methods=['POST'])
def trigger_report():
    report_id = generate_report()  # Trigger report generation
    return jsonify({'report_id': report_id})

@main_bp.route('/get_report/<report_id>', methods=['GET'])
def get_report(report_id):
    report = Report.query.filter_by(report_id=report_id).first()
    if report:
        # Return the report data
        report_data = {
            'store_id': report.store_id,
            'uptime_last_hour': report.uptime_last_hour,
            'uptime_last_day': report.uptime_last_day,
            'uptime_last_week': report.uptime_last_week,
            'downtime_last_hour': report.downtime_last_hour,
            'downtime_last_day': report.downtime_last_day,
            'downtime_last_week': report.downtime_last_week
        }
        return jsonify({'status': 'Complete', 'report_data': report_data})
    else:
        return jsonify({'status': 'Running'})


