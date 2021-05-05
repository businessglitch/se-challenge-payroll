import os
from flask import url_for
from werkzeug.datastructures import FileStorage
from backend.lib.tests import ViewTestMixin, assert_status_with_message
from backend.blueprints.timereport.models import TimeReport



class TestTimeReport(ViewTestMixin):
    def test_generate_payrollReport(self):
        """ Successfull returns a JSON object """
        response = self.client.get(url_for('page.generate_payrollReport'))
        assert_status_with_message(200, response, 'payrollReport')
    
    def test_upload_without_file(self):
        response = self.client.get(url_for('page.upload_file'))
        assert_status_with_message(405, response, 'Method Not Allowed')