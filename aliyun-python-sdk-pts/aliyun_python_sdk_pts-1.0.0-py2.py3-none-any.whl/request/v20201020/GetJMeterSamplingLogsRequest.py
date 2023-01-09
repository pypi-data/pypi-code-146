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

class GetJMeterSamplingLogsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'PTS', '2020-10-20', 'GetJMeterSamplingLogs')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_ResponseCode(self): # String
		return self.get_query_params().get('ResponseCode')

	def set_ResponseCode(self, ResponseCode):  # String
		self.add_query_param('ResponseCode', ResponseCode)
	def get_AgentId(self): # Long
		return self.get_query_params().get('AgentId')

	def set_AgentId(self, AgentId):  # Long
		self.add_query_param('AgentId', AgentId)
	def get_ReportId(self): # String
		return self.get_query_params().get('ReportId')

	def set_ReportId(self, ReportId):  # String
		self.add_query_param('ReportId', ReportId)
	def get_MinRT(self): # Integer
		return self.get_query_params().get('MinRT')

	def set_MinRT(self, MinRT):  # Integer
		self.add_query_param('MinRT', MinRT)
	def get_EndTime(self): # Long
		return self.get_query_params().get('EndTime')

	def set_EndTime(self, EndTime):  # Long
		self.add_query_param('EndTime', EndTime)
	def get_BeginTime(self): # Long
		return self.get_query_params().get('BeginTime')

	def set_BeginTime(self, BeginTime):  # Long
		self.add_query_param('BeginTime', BeginTime)
	def get_Thread(self): # String
		return self.get_query_params().get('Thread')

	def set_Thread(self, Thread):  # String
		self.add_query_param('Thread', Thread)
	def get_MaxRT(self): # Integer
		return self.get_query_params().get('MaxRT')

	def set_MaxRT(self, MaxRT):  # Integer
		self.add_query_param('MaxRT', MaxRT)
	def get_PageNumber(self): # Integer
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self, PageNumber):  # Integer
		self.add_query_param('PageNumber', PageNumber)
	def get_SamplerId(self): # Integer
		return self.get_query_params().get('SamplerId')

	def set_SamplerId(self, SamplerId):  # Integer
		self.add_query_param('SamplerId', SamplerId)
	def get_Success(self): # Boolean
		return self.get_query_params().get('Success')

	def set_Success(self, Success):  # Boolean
		self.add_query_param('Success', Success)
	def get_PageSize(self): # Integer
		return self.get_query_params().get('PageSize')

	def set_PageSize(self, PageSize):  # Integer
		self.add_query_param('PageSize', PageSize)
	def get_Keyword(self): # String
		return self.get_query_params().get('Keyword')

	def set_Keyword(self, Keyword):  # String
		self.add_query_param('Keyword', Keyword)
