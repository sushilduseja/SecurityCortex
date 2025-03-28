from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import json
import datetime
from database.db_init_sqlite import init_db
from database.db_utils_sqlite import (
    get_all_policies, get_policy, create_policy, update_policy,
    get_all_risk_assessments, get_risk_assessment, create_risk_assessment,
    get_all_compliance_monitors, get_compliance_monitor,
    create_compliance_monitor, update_compliance_monitor, get_all_reports,
    get_report, create_report, get_recent_activities, log_activity)
from database.models import Policy, RiskAssessment, ComplianceMonitor, Report, Activity

# Initialize the Flask application
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Initialize the database
init_db()


# Routes for serving the SPA
@app.route('/')
@app.route('/governance')
@app.route('/risk-assessment')
@app.route('/compliance')
@app.route('/reports')
def index():
    """Serve the main application page for any valid route in the SPA"""
    return send_from_directory('static', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    # Check if path has an extension (likely a static asset)
    if '.' in path:
        return send_from_directory('static', path)
    # For non-file paths (routes), serve the index.html for client-side routing
    return send_from_directory('static', 'index.html')


# API Routes


# Dashboard metrics
@app.route('/api/dashboard/metrics', methods=['GET'])
def get_dashboard_metrics():
    """Get summary metrics for the dashboard"""
    try:
        policies = get_all_policies()
        risk_assessments = get_all_risk_assessments()
        compliance_monitors = get_all_compliance_monitors()

        # Calculate metrics
        policy_count = len(policies)

        # Calculate average risk score
        risk_scores = [ra.get('risk_score', 0) for ra in risk_assessments]
        avg_risk_score = sum(risk_scores) / len(
            risk_scores) if risk_scores else 0

        # Calculate compliance rate
        compliant_monitors = sum(1 for m in compliance_monitors
                                 if m.get('alert_level') == 'Normal')
        compliance_rate = (compliant_monitors / len(compliance_monitors)
                           ) * 100 if compliance_monitors else 0

        # Active monitors count
        active_monitors = sum(1 for m in compliance_monitors
                              if m.get('status') == 'Active')

        # Calculate deltas based on recent activities (last 7 days vs. previous period)
        recent_activities = get_recent_activities(
            100)  # Get more activities to calculate changes

        # Get timestamp from 7 days ago
        one_week_ago = (datetime.datetime.now() -
                        datetime.timedelta(days=7)).isoformat()
        two_weeks_ago = (datetime.datetime.now() -
                         datetime.timedelta(days=14)).isoformat()

        # Count recent activities by type
        recent_policy_changes = sum(1 for a in recent_activities
                                    if a.get('related_entity_type') == 'policy'
                                    and a.get('created_at', '') > one_week_ago)

        # This is a simplified approach - in a real app we would look at actual changes
        # in risk scores and compliance values over time
        risk_assessments_last_week = sum(
            1 for a in recent_activities
            if a.get('related_entity_type') == 'risk_assessment'
            and a.get('created_at', '') > one_week_ago)

        compliance_changes = sum(
            1 for a in recent_activities
            if a.get('related_entity_type') == 'compliance_monitor'
            and a.get('created_at', '') > one_week_ago)

        monitor_changes = sum(
            1 for a in recent_activities
            if a.get('related_entity_type') == 'compliance_monitor'
            and 'create' in a.get('activity_type', '').lower()
            and a.get('created_at', '') > one_week_ago)

        # Structure the response with real delta values
        metrics = {
            'policy_count': policy_count,
            'avg_risk_score': round(avg_risk_score, 1),
            'compliance_rate': round(compliance_rate, 1),
            'active_monitors': active_monitors,
            # Add deltas (changes) for each metric
            'deltas': {
                'policy_count': recent_policy_changes,
                'avg_risk_score': risk_assessments_last_week,
                'compliance_rate': compliance_changes,
                'active_monitors': monitor_changes
            }
        }

        return jsonify({'success': True, 'data': metrics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Compliance Status Chart data
@app.route('/api/charts/compliance-status', methods=['GET'])
def get_compliance_status_chart():
    """Get data for the compliance status chart"""
    try:
        monitors = get_all_compliance_monitors()

        # Count monitors by status
        status_counts = {
            'Compliant': 0,
            'Partially Compliant': 0,
            'Non-Compliant': 0,
            'Under Review': 0
        }

        for monitor in monitors:
            alert_level = monitor.get('alert_level', '')
            if alert_level == 'Normal':
                status_counts['Compliant'] += 1
            elif alert_level == 'Warning':
                status_counts['Partially Compliant'] += 1
            elif alert_level == 'Critical':
                status_counts['Non-Compliant'] += 1
            else:
                status_counts['Under Review'] += 1

        # Convert to percentages
        total = sum(status_counts.values()) or 1  # Avoid division by zero
        status_percentages = {
            k: round((v / total) * 100)
            for k, v in status_counts.items()
        }

        return jsonify({
            'success': True,
            'data': {
                'labels': list(status_percentages.keys()),
                'values': list(status_percentages.values())
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Risk Assessment Chart data
@app.route('/api/charts/risk-distribution', methods=['GET'])
def get_risk_distribution_chart():
    """Get data for the risk distribution chart"""
    try:
        assessments = get_all_risk_assessments()

        # Count models by risk level
        risk_levels = {
            'High': 0,  # 80-100
            'Medium-High': 0,  # 60-79
            'Medium': 0,  # 40-59
            'Medium-Low': 0,  # 20-39
            'Low': 0  # 0-19
        }

        for assessment in assessments:
            score = assessment.get('risk_score', 0)

            if score >= 80:
                risk_levels['High'] += 1
            elif score >= 60:
                risk_levels['Medium-High'] += 1
            elif score >= 40:
                risk_levels['Medium'] += 1
            elif score >= 20:
                risk_levels['Medium-Low'] += 1
            else:
                risk_levels['Low'] += 1

        return jsonify({
            'success': True,
            'data': {
                'labels': list(risk_levels.keys()),
                'values': list(risk_levels.values())
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Recent Activities
@app.route('/api/activities/recent', methods=['GET'])
def get_activities():
    """Get recent activities"""
    try:
        # Parse limit from request args or use default
        limit = request.args.get('limit', 10, type=int)
        activities = get_recent_activities(limit)

        # Format activities for display
        formatted_activities = []
        for activity in activities:
            # Format the timestamp
            created_at = activity.get('created_at', '')
            if created_at:
                # Convert to a more readable format
                try:
                    dt = datetime.datetime.fromisoformat(created_at)
                    formatted_date = dt.strftime('%b %d, %Y %I:%M %p')
                except:
                    formatted_date = created_at
            else:
                formatted_date = 'Unknown'

            # Format the activity
            formatted_activity = {
                'activity': activity.get('description', 'Unknown activity'),
                'date': formatted_date,
                'user': activity.get('actor', 'System'),
                'status': 'Completed',  # Default status
                'entity_type': activity.get('related_entity_type', ''),
                'entity_id': activity.get('related_entity_id', '')
            }

            # Set status based on activity type
            activity_type = activity.get('activity_type', '').lower()
            if 'error' in activity_type or 'fail' in activity_type:
                formatted_activity['status'] = 'Failed'
            elif 'warning' in activity_type or 'alert' in activity_type:
                formatted_activity['status'] = 'Alert'
            elif 'create' in activity_type or 'new' in activity_type:
                formatted_activity['status'] = 'New'

            formatted_activities.append(formatted_activity)

        return jsonify({'success': True, 'data': formatted_activities})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Governance Policies
@app.route('/api/policies', methods=['GET'])
def api_get_policies():
    """Get all governance policies"""
    try:
        policies = get_all_policies()
        return jsonify({'success': True, 'data': policies})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/policies/<int:policy_id>', methods=['GET'])
def api_get_policy(policy_id):
    """Get a specific policy by ID"""
    try:
        policy = get_policy(policy_id)
        if policy:
            return jsonify({'success': True, 'data': policy})
        else:
            return jsonify({
                'success': False,
                'error': 'Policy not found'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/policies', methods=['POST'])
def api_create_policy():
    """Create a new policy"""
    try:
        data = request.json
        policy = Policy(title=data.get('title', ''),
                        description=data.get('description', ''),
                        category=data.get('category', ''),
                        status=data.get('status', 'Draft'),
                        content=data.get('content', ''))
        policy_id = create_policy(policy)
        return jsonify({'success': True, 'data': {'id': policy_id}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/policies/<int:policy_id>', methods=['PUT'])
def api_update_policy(policy_id):
    """Update an existing policy"""
    try:
        data = request.json
        existing = get_policy(policy_id)
        if not existing:
            return jsonify({
                'success': False,
                'error': 'Policy not found'
            }), 404

        policy = Policy(id=policy_id,
                        title=data.get('title', existing['title']),
                        description=data.get('description',
                                             existing['description']),
                        category=data.get('category', existing['category']),
                        status=data.get('status', existing['status']),
                        content=data.get('content', existing['content']))
        success = update_policy(policy)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Risk Assessment endpoints
@app.route('/api/risk-assessments', methods=['GET'])
def api_get_risk_assessments():
    """Get all risk assessments"""
    try:
        assessments = get_all_risk_assessments()
        return jsonify({'success': True, 'data': assessments})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/risk-assessments/<int:assessment_id>', methods=['GET'])
def api_get_risk_assessment(assessment_id):
    """Get a specific risk assessment by ID"""
    try:
        assessment = get_risk_assessment(assessment_id)
        if assessment:
            return jsonify({'success': True, 'data': assessment})
        else:
            return jsonify({
                'success': False,
                'error': 'Risk assessment not found'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/risk-assessments', methods=['POST'])
def api_create_risk_assessment():
    """Create a new risk assessment"""
    try:
        data = request.json
        assessment = RiskAssessment(title=data.get('title', ''),
                                    model_name=data.get('model_name', ''),
                                    risk_score=data.get('risk_score', 0.0),
                                    findings=data.get('findings', ''),
                                    recommendations=data.get(
                                        'recommendations', ''),
                                    status=data.get('status', 'Pending'))
        assessment_id = create_risk_assessment(assessment)
        return jsonify({'success': True, 'data': {'id': assessment_id}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Compliance Monitoring endpoints
@app.route('/api/compliance-monitors', methods=['GET'])
def api_get_compliance_monitors():
    """Get all compliance monitors"""
    try:
        monitors = get_all_compliance_monitors()
        return jsonify({'success': True, 'data': monitors})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/compliance-monitors/<int:monitor_id>', methods=['GET'])
def api_get_compliance_monitor(monitor_id):
    """Get a specific compliance monitor by ID"""
    try:
        monitor = get_compliance_monitor(monitor_id)
        if monitor:
            return jsonify({'success': True, 'data': monitor})
        else:
            return jsonify({
                'success': False,
                'error': 'Compliance monitor not found'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/compliance-monitors', methods=['POST'])
def api_create_compliance_monitor():
    """Create a new compliance monitor"""
    try:
        data = request.json
        monitor = ComplianceMonitor(
            name=data.get('name', ''),
            description=data.get('description', ''),
            model_or_system=data.get('model_or_system', ''),
            threshold_value=data.get('threshold_value', 0.0),
            current_value=data.get('current_value', 0.0),
            status=data.get('status', 'Active'),
            alert_level=data.get('alert_level', 'Normal'))
        monitor_id = create_compliance_monitor(monitor)
        return jsonify({'success': True, 'data': {'id': monitor_id}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/compliance-monitors/<int:monitor_id>', methods=['PUT'])
def api_update_compliance_monitor(monitor_id):
    """Update an existing compliance monitor"""
    try:
        data = request.json
        existing = get_compliance_monitor(monitor_id)
        if not existing:
            return jsonify({
                'success': False,
                'error': 'Compliance monitor not found'
            }), 404

        monitor = ComplianceMonitor(
            id=monitor_id,
            name=data.get('name', existing['name']),
            description=data.get('description', existing['description']),
            model_or_system=data.get('model_or_system',
                                     existing['model_or_system']),
            threshold_value=data.get('threshold_value',
                                     existing['threshold_value']),
            current_value=data.get('current_value', existing['current_value']),
            status=data.get('status', existing['status']),
            alert_level=data.get('alert_level', existing['alert_level']))
        success = update_compliance_monitor(monitor)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Reports endpoints
@app.route('/api/reports', methods=['GET'])
def api_get_reports():
    """Get all reports"""
    try:
        reports = get_all_reports()
        return jsonify({'success': True, 'data': reports})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/reports/<int:report_id>', methods=['GET'])
def api_get_report(report_id):
    """Get a specific report by ID"""
    try:
        report = get_report(report_id)
        if report:
            return jsonify({'success': True, 'data': report})
        else:
            return jsonify({
                'success': False,
                'error': 'Report not found'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/reports', methods=['POST'])
def api_create_report():
    """Create a new report"""
    try:
        data = request.json
        report = Report(title=data.get('title', ''),
                        description=data.get('description', ''),
                        report_type=data.get('report_type', ''),
                        content=data.get('content', ''),
                        insights=data.get('insights', ''),
                        status=data.get('status', 'Draft'))
        report_id = create_report(report)
        return jsonify({'success': True, 'data': {'id': report_id}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Run the application
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
