# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkpts.endpoint import endpoint_data

class GetJMeterSampleMetricsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'PTS', '2020-10-20', 'GetJMeterSampleMetrics')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_ReportId(self): # String
		return self.get_query_params().get('ReportId')

	def set_ReportId(self, ReportId):  # String
		self.add_query_param('ReportId', ReportId)
	def get_SamplerId(self): # Integer
		return self.get_query_params().get('SamplerId')

	def set_SamplerId(self, SamplerId):  # Integer
		self.add_query_param('SamplerId', SamplerId)
	def get_EndTime(self): # Long
		return self.get_query_params().get('EndTime')

	def set_EndTime(self, EndTime):  # Long
		self.add_query_param('EndTime', EndTime)
	def get_BeginTime(self): # Long
		return self.get_query_params().get('BeginTime')

	def set_BeginTime(self, BeginTime):  # Long
		self.add_query_param('BeginTime', BeginTime)
