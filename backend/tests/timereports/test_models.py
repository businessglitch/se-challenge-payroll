import datetime
from backend.blueprints.timereport.models import TimeReport


class TestTimeReport(object):
    def test_total_pay(self):
        """ Total pay is correctly calculated """
        
        hours = 10
        job_group = 'A'
        total = TimeReport.get_total_pay(hours,job_group)

        assert total == 200

    def test_get_payperiod(self):
        """ Payperiod values are correctly generated"""

        date = datetime.datetime.strptime('14/11/2016', "%d/%m/%Y")
        startDate = datetime.datetime(date.year, date.month, 1).strftime("%Y-%m-%d")
        endDate = datetime.datetime(date.year, date.month, 15).strftime("%Y-%m-%d")

        assert (startDate, endDate) == TimeReport.get_payperiod(date)
