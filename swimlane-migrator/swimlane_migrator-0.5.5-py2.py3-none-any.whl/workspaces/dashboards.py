import json, sys
from copy import copy
from swimlane_migrator.utils import lookupLabel
from .reports import report

class  dashboard(object):

    def __init__(self, config):

        self.logger = config.pop('logger', None)
        self.swimlane_source = config.pop('swimlane_source', None)
        self.swimlane_target = config.pop('swimlane_target', None)

        if self.swimlane_source is None:
            raise  Exception('You must provide a swimlane_source object')

        if self.swimlane_target is None:
            raise  Exception('You must provide a swimlane_target object')

        self.remove_keys = ['createdDate', 'modifiedDate', 'createdByUser', 'modifiedByUser']
        self.mode = config['mode']
        self.dashboard_dictionary_source = self.getDashboardDictionary(self.swimlane_source)
        self.dashboard_dictionary_target = self.getDashboardDictionary(self.swimlane_target)

        self.report_engine = report(config={'logger':self.logger, 'swimlane_source' : self.swimlane_source, 'swimlane_target' : self.swimlane_target, 'mode': self.mode})


    def getDashboards(self, swimlane_server):
        dashboard_response = swimlane_server.swimlane.request(
            'get',
            '/dashboard'
        )

        return json.loads(dashboard_response.text)

    def getDashboard(self, swimlane_server, dashboard_id):
        dashboard_response = swimlane_server.swimlane.request(
            'get',
            '/dashboard/{}'.format(dashboard_id)
        )
        if dashboard_response.text != '':
            return json.loads(dashboard_response.text)
        return None


    def deleteDashboard(self, swimlane_server, dashboard_id):
        workspace_response = swimlane_server.swimlane.request(
            'delete',
            '/dashboard/{}'.format(dashboard_id)
        )

    def addDashboard(self, swimlane_server, dashboard):
        dashboard_response = swimlane_server.swimlane.request(
            'post',
            '/dashboard',
            json = dashboard
        )

        return json.loads(dashboard_response.text)

    def updateDashboard(self, swimlane_server, dashboard_id, dashboard):
        dashboard_response = swimlane_server.swimlane.request(
            'put',
            '/dashboard/{}'.format(dashboard_id),
            json = dashboard
        )

        return json.loads(dashboard_response.text)

    def getDashboardDictionary(self, swimlane_server):
        dashboard_response = self.getDashboards(swimlane_server)

        dashboard_dictionary = {}
        for dashboard in dashboard_response:
            dashboard_dictionary[dashboard['name']] = dashboard

        return dashboard_dictionary

    def validateDashboard(self, source, byID = None, byName = None):
        lookup_dictionary = None

        if source == 'target':
            lookup_dictionary = self.dashboard_dictionary_target

        if source == 'source':
            lookup_dictionary = self.dashboard_dictionary_source

        if lookup_dictionary is None:
            raise Exception('Invalid source "{}" provided, valid options "target" or "source"'.format(source))

        if byID is not None:
            return lookupLabel(lookup_dictionary, byValue=byID)

        if byName is not None:
            return lookupLabel(lookup_dictionary, byKey=byName)

    def removeOrphanDashboards(self, swimlane_server):
        dashboards = self.getDashboards(swimlane_server)
        for dashboard in dashboards:
            self.logger.info('Working on Dashboard: {}, which has {} workspaces'.format(dashboard['name'], len(dashboard['workspaces'])))
            if 'workspaces' in dashboard and len(dashboard['workspaces']) == 0:
                self.logger.error('Removing Dashboard {}'.format(dashboard['name']))
                self.deleteDashboard(swimlane_server, dashboard['id'])

    def fixItems(self, items):

        for item in items:
            if 'reportId' in item:
                source_report_obj = self.report_engine.getReportByID(self.swimlane_source, item['reportId'])
                if 'id' not in source_report_obj:
                    self.logger.critical('Dashboard Card Report ID {} could not be found in source'.format(item['reportId']))
                    continue

                source_app_name = self.swimlane_source.validateApp(byID=source_report_obj['applicationIds'][0])
                if source_app_name == False:
                    self.logger.critical('Dashboard Card App ID {} could not be found in source'.format(source_report_obj['applicationIds'][0]))
                    continue

                target_app_id = self.swimlane_target.validateApp(byName=source_app_name)
                if target_app_id == False:
                    self.logger.critical('Dashboard Card App Name "{}" could not be found in target'.format(source_app_name))
                    continue

                target_report_dictionary = self.report_engine.getReportDictionary(self.swimlane_target, target_app_id)
                target_report_id = lookupLabel(target_report_dictionary, byKey=source_report_obj['name'])
                if target_report_id == False:
                    self.logger.critical('Dashboard Card Report Name "{}" could not be found in target'.format(source_report_obj['name']))
                    continue

                item['reportId'] = target_report_id

        return items


    def migrateDashboards(self, mode,workspace_obj, target_workspace_id, target_workspace_list):


        for dashboard_id in workspace_obj['dashboards']:
            source_dashboard = self.getDashboard(self.swimlane_source, dashboard_id)

            if source_dashboard is None:
                self.logger.critical("Failed to find Dashboard ID {} in source".format(dashboard_id))
                continue

            target_dashboard_id = self.validateDashboard('target', byName=source_dashboard['name'])

            if target_dashboard_id == False:
                new_dashboard = copy(source_dashboard)
                new_dashboard['workspaces'] = [target_workspace_id]

                for key in self.remove_keys:
                    new_dashboard.pop(key, None)

                new_dashboard['items'] = self.fixItems(new_dashboard['items'])
                if mode == 'Live':
                    self.addDashboard(self.swimlane_target, new_dashboard)
                    self.dashboard_dictionary_target = self.getDashboardDictionary(self.swimlane_target)
            else:
                update_dashboard = self.getDashboard(self.swimlane_target, target_dashboard_id)

                for key, workspace_id in enumerate(update_dashboard['workspaces']):
                    if workspace_id not in target_workspace_list:
                        update_dashboard['workspaces'].pop(key)

                if target_workspace_id not in update_dashboard['workspaces']:
                    update_dashboard['workspaces'].append(target_workspace_id)

                update_dashboard['items'] = self.fixItems(source_dashboard['items'])
                if mode == 'Live':
                    self.updateDashboard(self.swimlane_target, target_dashboard_id, update_dashboard)
                    self.dashboard_dictionary_target = self.getDashboardDictionary(self.swimlane_target)
