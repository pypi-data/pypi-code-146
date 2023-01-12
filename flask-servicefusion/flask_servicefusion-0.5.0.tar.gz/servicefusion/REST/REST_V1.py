from servicefusion.REST.V1 import ( CustomerService, JobService )

class REST_V1:
    def __init__(self, servicefusion):
        self.servicefusion = servicefusion
        self.CustomerService = CustomerService(servicefusion)
        self.JobService = JobService(servicefusion)

