from __future__ import annotations

from tcsoa.gen.Internal.Reports._2007_06.BOMRollup import CreateRollupTemplateInput, RollupReportResponse, GetRollupTemplateInput, RollupTemplateInput, RollupTemplateCalculationResponse, ReviseRollupReportInput, CreateRollupCalculationTemplateInput, RollupTemplateResponse, CreateRollupCalculationTemplateResponse, CreateRollupReportInput
from typing import List
from tcsoa.base import TcService


class BOMRollupService(TcService):

    @classmethod
    def getRollupTemplateCalculations(cls, input: List[RollupTemplateInput]) -> RollupTemplateCalculationResponse:
        """
        This operation gets a RollupTemplate's calculation templates. Calculation templates define which properties
        will be used as input for calculations such as sum, center of mass, product of inertia, etc.
        
        Use cases:
        - User wants to find all calculation templates associated with a RollupTemplate.
        - User wants to verify a RollupTemplate has calculation templates in order to avoid generating an empty rollup
        report.
        
        """
        return cls.execute_soa_method(
            method_name='getRollupTemplateCalculations',
            library='Internal-Reports',
            service_date='2007_06',
            service_name='BOMRollup',
            params={'input': input},
            response_cls=RollupTemplateCalculationResponse,
        )

    @classmethod
    def getRollupTemplates(cls, input: List[GetRollupTemplateInput]) -> RollupTemplateResponse:
        """
        This operation gets RollupTemplates by using one of three options:
        1.    All RollupTemplates if the input string is empty, null, or "Mode=ALL". This will find all rollup
        templates in the database.
        2.    User preference - If the input string is "Mode=USER_PREFERENCE", this operation will find the user's
        favorite RollupTemplates (defined by the preference ROLL_UP_FAVORITE_TEMPLATES).
        3.    Specific name and scope context - If input the string is "Mode=SPECIFIC:name:scope_context", this
        operation will search the database for the specific rollup template that matches the name and scope_context
        supplied. Name is the name of the template, scope_context depends on the scope - for site scope, it is the site
        ID; for group, it is the group name; for user, it is the user name.
        
        Use cases:
        - User needs to fetch RollupTemplates in order to clone them.
        - User created RollupTemplates in another session, and needs to fetch them in order to create and attach rollup
        calculation templates.
        - User wants to generate rollup reports.
        - User wants to get a RollupTemplate's calculation templates.
        - User wants to revise a rollup report.
        
        """
        return cls.execute_soa_method(
            method_name='getRollupTemplates',
            library='Internal-Reports',
            service_date='2007_06',
            service_name='BOMRollup',
            params={'input': input},
            response_cls=RollupTemplateResponse,
        )

    @classmethod
    def cloneRollupTemplates(cls, input: List[RollupTemplateInput]) -> RollupTemplateResponse:
        """
        This operation makes a copy or copies of existing RollupTemplates.
        
        Use cases:
        User wants to create a RollupTemplate (and calculation templates) similar to one that already exists.
        """
        return cls.execute_soa_method(
            method_name='cloneRollupTemplates',
            library='Internal-Reports',
            service_date='2007_06',
            service_name='BOMRollup',
            params={'input': input},
            response_cls=RollupTemplateResponse,
        )

    @classmethod
    def reviseRollupReports(cls, input: List[ReviseRollupReportInput]) -> RollupReportResponse:
        """
        This operation revises one or more rollup reports. This is used when the user would prefer to overwrite an
        existing report, instead of generating a new report and keeping the old one.
        
        Use cases:
        User has already generated a rollup report and wants to make some changes, as opposed to simply generating a
        new rollup report.
        """
        return cls.execute_soa_method(
            method_name='reviseRollupReports',
            library='Internal-Reports',
            service_date='2007_06',
            service_name='BOMRollup',
            params={'input': input},
            response_cls=RollupReportResponse,
        )

    @classmethod
    def createRollupCalculationTemplates(cls, input: List[CreateRollupCalculationTemplateInput]) -> CreateRollupCalculationTemplateResponse:
        """
        This operation creates rollup calculation templates.
        
        Use cases:
        User invokes 'createRollupCalculationTemplates' to create and attach rollup calculation templates to
        RollupTemplates.
        """
        return cls.execute_soa_method(
            method_name='createRollupCalculationTemplates',
            library='Internal-Reports',
            service_date='2007_06',
            service_name='BOMRollup',
            params={'input': input},
            response_cls=CreateRollupCalculationTemplateResponse,
        )

    @classmethod
    def createRollupTemplates(cls, input: List[CreateRollupTemplateInput]) -> RollupTemplateResponse:
        """
        The 'createRollupTemplates' operation creates one or more RollupTemplates. RollupTemplates are a container for
        one or more rollup calculation templates.
        
        Use cases:
        User wants to create RollupTemplates in order to generate rollup reports.
        """
        return cls.execute_soa_method(
            method_name='createRollupTemplates',
            library='Internal-Reports',
            service_date='2007_06',
            service_name='BOMRollup',
            params={'input': input},
            response_cls=RollupTemplateResponse,
        )

    @classmethod
    def generateRollupReports(cls, input: List[CreateRollupReportInput]) -> RollupReportResponse:
        """
        This operation creates rollup reports for the specified root BOM lines, using the specified RollupTemplates.
        
        Use cases:
        User has created a RollupTemplate with rollup calculation templates, and wants to generate a rollup report.
        """
        return cls.execute_soa_method(
            method_name='generateRollupReports',
            library='Internal-Reports',
            service_date='2007_06',
            service_name='BOMRollup',
            params={'input': input},
            response_cls=RollupReportResponse,
        )
