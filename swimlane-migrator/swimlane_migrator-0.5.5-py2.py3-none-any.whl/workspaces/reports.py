import json, sys
from copy import copy
from swimlane_migrator.usergroups.groups import groups
from swimlane_migrator.utils import find_in_list

class report(object):

    def __init__(self, config):
        self.mode = config['mode']
        self.groups = groups(copy(config))

        self.logger = config.pop('logger', None)
        self.swimlane_source = config.pop('swimlane_source', None)
        self.swimlane_target = config.pop('swimlane_target', None)

        if self.swimlane_source is None:
            raise  Exception('You must provide a swimlane_source object')

        if self.swimlane_target is None:
            raise  Exception('You must provide a swimlane_target object')

        self.remove_keys = ['createdDate', 'modifiedDate', 'createdByUser', 'modifiedByUser']

        self.migratedReports = []


    def addReport(self, swimlane_server, report):
        report_response = swimlane_server.swimlane.request(
            'post',
            '/reports',
            json = report
        )

        return json.loads(report_response.text)

    def updateReport(self, swimlane_server, report_id, report):
        report_response = swimlane_server.swimlane.request(
            'put',
            '/reports/{}'.format(report_id),
            json = report
        )

        return json.loads(report_response.text)

    def getReportsByApp(self, swimlane_server, appID):
        report_response = swimlane_server.swimlane.request(
            'get',
            '/reports/app/{}'.format(appID)
        )

        return json.loads(report_response.text)

    def getReportsByWorkspace(self, swimlane_server, workspaceID):
        report_response = swimlane_server.swimlane.request(
            'get',
            '/reports/workspace/{}'.format(workspaceID)
        )

        return json.loads(report_response.text)

    def getReportsByApp(self, swimlane_server, appID):
        report_response = swimlane_server.swimlane.request(
            'get',
            '/reports/app/{}'.format(appID)
        )

        return json.loads(report_response.text)

    def getReportByID(self, swimlane_server, reportID):
        report_response = swimlane_server.swimlane.request(
            'get',
            '/reports/{}'.format(reportID)
        )

        return json.loads(report_response.text)

    def getReports(self, swimlane_server):
        report_response = swimlane_server.swimlane.request(
            'get',
            '/reports'
        )

        return json.loads(report_response.text)

    def getReportDictionary(self, swimlane_server, appID):
        report_response = self.getReportsByApp(swimlane_server, appID)

        reports_dictionary = {}
        for report in report_response:
            reports_dictionary[report['name']] = report

        return reports_dictionary

    def validateApplications(self, application_list):
        new_application_list = []
        for application_id in application_list:
            source_app_name = self.swimlane_source.validateApp(byID=application_id)
            if source_app_name != False:
                target_app_id = self.swimlane_target.validateApp(byName=source_app_name)
                if target_app_id != False:
                    new_application_list.append(target_app_id)

        return new_application_list

    def fixColumns(self, columns, source_app_id, target_app_id):
        new_columns = []

        source_field_dictionary= self.swimlane_source.getFieldDictinoary(byID=source_app_id)
        target_field_dictionary= self.swimlane_target.getFieldDictinoary(byID=target_app_id)

        for column in columns:

            source_field_name = self.swimlane_source.validateField(source_field_dictionary, byID=column)
            if source_field_name == False:
                self.logger.error('Report Columns -- Source Field ID {} not found'.format(column))
                continue

            target_field_id = self.swimlane_target.validateField(target_field_dictionary, byName=source_field_name)
            if target_field_id == False:
                self.logger.error('Report Columns -- Target Field Name {} not found in {}'.format(source_field_name, target_field_dictionary))
                continue

            new_columns.append(target_field_id)

        return new_columns

    def fixSorts(self, sorts, source_app_id, target_app_id):
        new_sorts = {}
        new_sorts['$type'] = sorts['$type']

        source_field_dictionary= self.swimlane_source.getFieldDictinoary(byID=source_app_id)
        target_field_dictionary= self.swimlane_target.getFieldDictinoary(byID=target_app_id)

        for field_id, sort in list(sorts.items()):
            if field_id != '$type':

                source_field_name = self.swimlane_source.validateField(source_field_dictionary, byID=field_id)
                if source_field_name == False:
                    self.logger.error('Report Sort -- Source Field ID {} not found'.format(field_id))
                    continue

                target_field_id = self.swimlane_target.validateField(target_field_dictionary, byName=source_field_name)
                if target_field_id == False:
                    self.logger.error('Report Sort -- Target Field Name {} not found in {}'.format(source_field_name, target_field_dictionary))
                    continue

                new_sorts[target_field_id] = sort

        return new_sorts

    def fixFilters(self, filters, source_app_id, target_app_id):
        new_filter = []

        source_field_dictionary= self.swimlane_source.getFieldDictinoary(byID=source_app_id)
        target_field_dictionary= self.swimlane_target.getFieldDictinoary(byID=target_app_id)

        for report_filter in filters:
            if 'fieldId' in report_filter:
                source_field_name = self.swimlane_source.validateField(source_field_dictionary, byID=report_filter['fieldId'])
                if source_field_name == False:
                    self.logger.error('Report Filter -- Source Field ID {} not found'.format(report_filter['fieldId']))
                    continue

                target_field_id = self.swimlane_target.validateField(target_field_dictionary, byName=source_field_name)
                if target_field_id == False:
                    self.logger.error('Report Filter -- Target Field Name {} not found in {}'.format(source_field_name, target_field_dictionary))
                    continue

                report_filter['fieldId'] = target_field_id
                new_filter.append(report_filter)

            if 'value' in report_filter:
                if isinstance(report_filter['value'], dict):
                    if '$type' in report_filter['value']:
                        if report_filter['value']['$type'] == 'Core.Models.Utilities.UserGroupSelection, Core':
                            group_obj = self.groups.lookupGroup(self.swimlane_target, report_filter['value']['name'])
                            if len(group_obj) == 1:
                                report_filter['value']['id'] = group_obj[0]['id']


        return new_filter

    def fixgroupBys(self, groupBys, source_app_id, target_app_id):
        new_groupBy = []

        source_field_dictionary= self.swimlane_source.getFieldDictinoary(byID=source_app_id)
        target_field_dictionary= self.swimlane_target.getFieldDictinoary(byID=target_app_id)

        for groupBy in groupBys:
            if 'fieldId' in groupBy:
                source_field_name = self.swimlane_source.validateField(source_field_dictionary, byID=groupBy['fieldId'])
                if source_field_name == False:
                    self.logger.error('Report GroupBy -- Source Field ID {} not found'.format(groupBy['fieldId']))
                    continue

                target_field_id = self.swimlane_target.validateField(target_field_dictionary, byName=source_field_name)
                if target_field_id == False:
                    self.logger.error('Report GroupBy -- Target Field Name {} not found in {}'.format(source_field_name, target_field_dictionary))
                    continue

                groupBy['fieldId'] = target_field_id
                new_groupBy.append(groupBy)

        return new_groupBy

    def fixAggregates(self, aggregates, source_app_id, target_app_id):
        new_aggregates = []

        source_field_dictionary= self.swimlane_source.getFieldDictinoary(byID=source_app_id)
        target_field_dictionary= self.swimlane_target.getFieldDictinoary(byID=target_app_id)

        for aggregate in aggregates:
            if 'fieldId' in aggregate:
                source_field_name = self.swimlane_source.validateField(source_field_dictionary, byID=aggregate['fieldId'])
                if source_field_name == False:
                    self.logger.error('Report Aggregates -- Source Field ID {} not found'.format(aggregate['fieldId']))
                    continue

                target_field_id = self.swimlane_target.validateField(target_field_dictionary, byName=source_field_name)
                if target_field_id == False:
                    self.logger.error('Report Aggregates -- Target Field Name {} not found in {}'.format(source_field_name, target_field_dictionary))
                    continue

                aggregate['fieldId'] = target_field_id
                new_aggregates.append(aggregate)

        return new_aggregates

    def fixPermissions(self, permissions):
        new_permissions = {}

        for key, permission in list(permissions.items()):
            if key != '$type':
                if permission['type'] == 'Role':
                    target_role_id = self.swimlane_target.validateRole(byName=permission['name'])
                    permission['id'] = target_role_id
                    new_permissions[target_role_id] = permission
            else:
                new_permissions[key] = permission

        return new_permissions

    def repairReport(self, report_obj):
        source_app_id = None
        if len(report_obj['applicationIds']) > 0:
            source_app_id = report_obj['applicationIds'][0]

            report_obj['applicationIds'] = self.validateApplications(report_obj['applicationIds'])
            if len(report_obj['applicationIds']) > 0:
                target_app_id = report_obj['applicationIds'][0]

                report_obj['columns'] = self.fixColumns(report_obj['columns'], source_app_id, target_app_id)
                report_obj['sorts'] = self.fixSorts(report_obj['sorts'], source_app_id, target_app_id)
                report_obj['filters'] = self.fixFilters(report_obj['filters'], source_app_id, target_app_id)
                report_obj['groupBys'] = self.fixgroupBys(report_obj['groupBys'], source_app_id, target_app_id)
                report_obj['aggregates'] = self.fixAggregates(report_obj['aggregates'], source_app_id, target_app_id)
                report_obj['permissions'] = self.fixPermissions(report_obj['permissions'])
            else:
                self.logger.critical('Report {} was unable to migrate, no applications assigned to report'.format(report_obj['name']))
                return None

        return report_obj


    def migrateReports(self, mode,byWorkspace = None, byApp = None,):

        source_reports = None
        target_reports = None

        if byWorkspace is not None:
            source_reports = self.getReportsByWorkspace(self.swimlane_source, byWorkspace['source'])
            target_reports = self.getReportsByWorkspace(self.swimlane_target, byWorkspace['target'])

        if byApp is not None:
            source_reports = self.getReportsByApp(self.swimlane_source, byApp['source'])
            target_reports = self.getReportsByApp(self.swimlane_target, byApp['target'])


        if source_reports is None and target_reports is None:
            raise Exception('Unable to load reports by Workstation ID: {} '.format(byWorkspace))

        self.logger.info('Count of Source Reports: {}'.format(len(source_reports)))

        for report in source_reports:
            if report['id'] not in self.migratedReports:
                self.logger.info('### Working on Report {}'.format(report['name']))
                self.migratedReports.append(report['id'])
                target_report = copy(report)
                target_report = self.repairReport(target_report)
                if target_report is not None:
                    target_report_key = find_in_list(target_reports, 'name', report['name'], self.logger)
                    if target_report_key is None:
                        for key in self.remove_keys:
                            if key in target_report:
                                target_report.pop(key)
                        if mode == 'Live':
                            try:
                                new_report = self.addReport(self.swimlane_target, target_report)
                            except Exception as e:
                                self.logger.critical('Failed to add Report "{}" Error: {}'.format(target_report['name'], e))
                    else:
                        update_report = target_reports[target_report_key]
                        update_report['applicationIds'] = copy(target_report['applicationIds'])
                        update_report['columns'] = copy(target_report['columns'])
                        update_report['sorts'] = copy(target_report['sorts'])
                        update_report['filters'] = copy(target_report['filters'])
                        update_report['groupBys'] = copy(target_report['groupBys'])
                        update_report['aggregates'] = copy(target_report['aggregates'])
                        update_report['permissions'] = copy(target_report['permissions'])
                        if mode == "Live":
                            try:
                                self.updateReport(self.swimlane_target, update_report['id'], update_report)
                            except Exception as e:
                                self.logger.critical('Failed to Update Report "{}" Error: {}'.format(update_report['name'], e))
