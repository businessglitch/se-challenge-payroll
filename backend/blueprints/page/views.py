import pandas as pd
import datetime
from io import StringIO, BytesIO

from flask import Blueprint, render_template, request, jsonify, abort
from backend.blueprints.timereport.models import TimeReport
from backend.lib.util_logger import log
from backend.lib.util_json import render_json

page = Blueprint('page', __name__, template_folder='templates')

@page.route('/')
def home():
    return render_template('page/home.html')

@page.route('/timereport/upload', methods=["POST"])
def upload_file():
    if request.method == "POST":
        if request.files:
            csv_file = request.files["timereport"]
            report_id = csv_file.filename.split('-')[-1].split('.')[0]
            report_id_record =  TimeReport.query.filter_by(report_id=report_id).first()
            
            print(csv_file)

            if report_id_record:
                # Return 406 NOT_ACCEPTABLE REQUEST if reportID already exists
                log.error("Failed to parse report, reportID:{} already exists".format(report_id))
                abort(406, "Report ID aleardy exists")

            records_df = pd.read_csv(StringIO(csv_file.read().decode('utf-8')))  

            for index, row in records_df.iterrows():
                params = {
                    'date': datetime.datetime.strptime(row['date'], "%d/%m/%Y"),
                    'report_id': int(report_id),
                    'employee_id': int(row['employee id']),
                    'job_group': row['job group'],
                    'hours_worked': float(row['hours worked'])
                }
                work_record = TimeReport(**params)
                work_record.save()

            log.info('Successfully parsed reportID:{}'.format(report_id))   
            return render_json(200, "Successfull parsed Report")

@page.route('/timereport/payrollReport', methods=["GET"])
def generate_payrollReport():
    """
    Generates a payrollReport based on all the data in the database

    :return: JSON response in the following format
        {
            "payrollReport": {
                "employeeReports": [
                    {
                        "employeeId": "1",
                        "payPeriod": {
                        "startDate": "2020-01-01",
                        "endDate": "2020-01-15"
                        },
                        "amountPaid": "$300.00"
                    }
                ]
            }
        }
    """
    reports_data =  TimeReport.query.order_by(TimeReport.employee_id.asc(), TimeReport.date.asc()).all()
    employees = []
    
    for i, report in enumerate(reports_data):
        total_pay = TimeReport.get_total_pay(report.hours_worked, report.job_group)

        # If the employee is not paid, no need to add entry to the report
        if total_pay == 0:
            continue
        
        startDate, endDate = TimeReport.get_payperiod(report.date)
       
        if employees and employees[-1]['employeeId'] ==  report.employee_id and employees[-1]['payPeriod']['startDate'] == startDate:
            employees[-1]['amountPaid'] += total_pay 
        else:
            # Format previous object's amountPaid to currency before pushing a new one
            if employees:
                employees[-1]['amountPaid'] = "${:.2f}".format(employees[-1]['amountPaid']) 

            employee = {
                'amountPaid': total_pay,
                'employeeId':report.employee_id,
                'payPeriod': {
                    "startDate": startDate,
                    "endDate": endDate
                }
            }

            employees.append(employee)
        
        if i == len(reports_data) -1:
            employees[-1]['amountPaid'] = "${:.2f}".format(employees[-1]['amountPaid']) 
    
    data = {
        'payrollReport': {
            'employeeReports': employees
        }
    }

    return render_json(200, data)

