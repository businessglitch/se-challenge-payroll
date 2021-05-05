import datetime
from calendar import monthrange
from backend.lib.util_sqlalchemy import ResourceMixin
from backend.extensions import db

class TimeReport(ResourceMixin,db.Model):
    __tablename__ = 'timereports'
    id = db.Column(db.Integer, primary_key=True)

    # Timereport entry details
    report_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    job_group = db.Column(db.String(5), nullable=False)
    employee_id = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(TimeReport, self).__init__(**kwargs)
    
    @classmethod
    def get_total_pay(cls, hours, job_group):
        """
        Calculates total pay based on hours worked and the job group
        
        :params: hours, job_group
        :return: (int) 
        """
        job_groups = {
            'A': 20,
            'B': 30
        }
        
        return hours * job_groups[job_group]

    @classmethod
    def get_payperiod(cls, date):
        """
        Processes date into startDate and endDate of a pay period.

        :params: date 
        :return: tuple(startDate, endDate)
        """
        if  date.day <=  15:
            startDate = datetime.datetime(date.year, date.month, 1).strftime("%Y-%m-%d")
            endDate = datetime.datetime(date.year, date.month, 15).strftime("%Y-%m-%d")
        else:
            startDate = datetime.datetime(date.year, date.month, 16).strftime("%Y-%m-%d")
            endDate = datetime.datetime(date.year, date.month, monthrange(date.year, date.month)[1]).strftime("%Y-%m-%d")

        return (startDate, endDate)