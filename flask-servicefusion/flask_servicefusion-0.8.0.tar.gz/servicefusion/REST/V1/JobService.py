from datetime import datetime, timedelta
from pytz import timezone
from servicefusion.JSONHandler import JSONHandler
from keap.REST.V1.mixins import CreateMixin, DeleteMixin


class JobService(CreateMixin, DeleteMixin):
    api_url = "jobs"
    json_handler = JSONHandler()

    def __init__(self, servicefusion):
        super().__init__(servicefusion)

    @staticmethod
    def get_datetime():
        mst = timezone('MST')
        return datetime.now(mst)

    @staticmethod
    def get_rfc_date(date=None):
        if date is None:
            # return rfc3339.rfc3339(datetime.now(), use_system_timezone=False)
            return datetime.now().strftime("%Y-%m-%dT%H:%M:%S-00:00")
        else:
            # return rfc3339.rfc3339(date, use_system_timezone=False)
            return date.strftime("%Y-%m-%dT%H:%M:%S-00:00")

    def get_job_by_id(self, job_id):
        params = {
            'expand': 'equipment, equipment.custom_fields, products, services, other_charges, labor_charges, expenses, invoices'
        }
        response = self._get(f'{self.api_url}/{job_id}', **params)
        return response

    def get_jobs(self):
        filter_date = self.get_rfc_date(date=self.get_datetime() - timedelta(hours=1))
        current_page = 1
        complete = False
        results = []

        while not complete:
            params = {
                'page': current_page,
                'per-page': '50',
                'filters[updated_date][gte]': filter_date,
                'filters[status]': 'Job Closed, Completed, Partially Completed, Scheduled, Started, Waiting - Acrylic, '
                                   'Waiting - Circ Pump, Waiting - Wifi Card, Waiting for parts, Unscheduled, Delayed, '
                                   'On The Way, Cancelled, Invoiced',
                'expand': 'notes, contact',
            }
            response = self._get('jobs', **params)
            if self.json_handler.extract_value(response, 'totalCount') > 0:
                if 'items' in response:
                    results += response.get("items")
                    if response.get("currentPage") == response.get("pageCount"):
                        complete = True
                    else:
                        current_page = current_page + 1
                        complete = False
            else:
                return None
        return results
