from .dashboards import dashboard
from .reports import report
from swimlane_migrator.utils import find_in_list
import json
from copy import copy
from sys import exit


class workspace(object):

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

        self.dashboard_engine = dashboard(config={'logger':self.logger, 'swimlane_source' : self.swimlane_source, 'swimlane_target' : self.swimlane_target, 'mode' : self.mode})
        self.report_engine = report(config={'logger':self.logger, 'swimlane_source' : self.swimlane_source, 'swimlane_target' : self.swimlane_target, 'mode': self.mode})


    def getWorkspace(self, swimlane_server):
        workspace_response = swimlane_server.swimlane.request(
            'get',
            '/workspaces'
        ).json()
        workspaces = list()
        for workspace in workspace_response:
            workspaces.append(swimlane_server.swimlane.request(
                'get',
                '/workspaces/{}'.format(workspace['id'])
            ).json())

        return workspaces

    def getWorkspaceByApp(self, swimlane_server, appID):
        workspace_response = swimlane_server.swimlane.request(
            'get',
            '/workspaces/app/{}'.format(appID)
        )

        return json.loads(workspace_response.text)


    def addWorkspace(self, swimlane_server, workspace):
        workspace_response = swimlane_server.swimlane.request(
            'post',
            '/workspaces',
            json = workspace
        )

        return json.loads(workspace_response.text)

    def updateWorkspace(self, swimlane_server, workspace_id, group):
        workspace_response = swimlane_server.swimlane.request(
            'put',
            '/workspaces/{}'.format(workspace_id),
            json = group
        )

        return json.loads(workspace_response.text)

    def deleteWorkspace(self, swimlane_server, workspace_id):
        workspace_response = swimlane_server.swimlane.request(
            'delete',
            '/workspaces/{}'.format(workspace_id)
        )


    def removeOrphanWorkspaces(self, swimlane_server):
        workspaces = self.getWorkspace(swimlane_server)
        for workspace in workspaces:

            for applicaiton_id in workspace['applications']:
                application_name = swimlane_server.validateApp(byID=applicaiton_id)
                if application_name == False:
                    workspace['applications'].remove(applicaiton_id)

            if len(workspace['applications']) == 0:
                self.logger.error('Removing Application {}'.format(workspace['name']))
                if self.mode == 'Live':
                    pass
                    # self.deleteWorkspace(swimlane_server, workspace['id'])
        if self.mode == 'Live':
            pass
            # self.dashboard_engine.removeOrphanDashboards(swimlane_server)

    def buildWorkspaceIDs(self, swimlane_server):
        workspaces = self.getWorkspace(swimlane_server)
        workspace_list = []
        for workspace in workspaces:
            workspace_list.append(workspace['id'])

        return workspace_list


    def migrateWorkspaces(self, byAppName = None):
        if byAppName is None:
            source_workspaces = self.getWorkspace(self.swimlane_source)
            target_workspaces = self.getWorkspace(self.swimlane_target)
        else:
            source_app_id = self.swimlane_source.validateApp(byName=byAppName)
            source_workspaces = self.getWorkspaceByApp(self.swimlane_source, source_app_id)
            target_app_id = self.swimlane_target.validateApp(byName=byAppName)
            target_workspaces = self.getWorkspace(self.swimlane_target)


        self.report_engine.migrateReports(self.mode,byApp = {'source' : source_app_id, 'target' : target_app_id})

        for workspace in source_workspaces:
            self.logger.debug('-------------------------------------------------')
            self.logger.info('Working on Workspace {}'.format(workspace['name']))
            target_workspace = {}
            for t_workspace in target_workspaces:
                if t_workspace['name'] == workspace['name']:
                    target_workspace = copy(t_workspace)

            ##Validate all application Workspace is pointing two is on target
            new_application_list = []
            self.logger.debug('## Working On Applications ##')
            for applicaiton_id in workspace['applications']:
                source_application_name = self.swimlane_source.validateApp(byID=applicaiton_id)
                if source_application_name != False:
                    target_application_id = self.swimlane_target.validateApp(byName=source_application_name)
                    if target_application_id != False:
                        if 'applications' not in target_workspace or target_application_id not in target_workspace['applications']:
                            self.logger.info('Add Application {} to Workspace'.format(source_application_name))
                            if self.mode == 'Live':
                                new_application_list.append(target_application_id)

            if len(new_application_list) == 0:
                self.logger.debug('Workspace has valid applications in target SKIPPING Migration')
                #continue

            new_permission_dict = {}
            self.logger.info('## Working On Permissions ##')
            for key, permission in list(workspace['permissions'].items()):
                if key != '$type':
                    if permission['type'] == 'Role':
                        target_role_id = self.swimlane_target.validateRole(byName=permission['name'])
                        if target_role_id != False:
                            self.logger.info('Adding Role {} to Workspace'.format(permission['name']))
                            new_permission_dict[target_role_id] = copy(permission)
                            new_permission_dict[target_role_id]['id'] = target_role_id
                    else:
                        self.logger.critical('Unhandled Permission Type: {}'.format(permission['type']))
                        exit()

            #new_dashboard_list = []

            target_workspace_id_key = find_in_list(target_workspaces, 'name', workspace['name'], self.logger)
            if target_workspace_id_key is None:
                self.logger.critical('Add New')
                for key in self.remove_keys:
                    if key in workspace:
                        workspace.pop(key)

                workspace['applications'] = new_application_list
                workspace['permissions'] = new_permission_dict
                #workspace['dashboards'] = new_dashboard_list

                if self.mode == 'Live':
                    workspace = self.addWorkspace(self.swimlane_target, workspace)
                self.report_engine.migrateReports(self.mode,byWorkspace = {'source' : workspace['id'], 'target' : workspace['id']})
                self.dashboard_engine.migrateDashboards(self.mode,workspace, workspace['id'], self.buildWorkspaceIDs(self.swimlane_target))
            else:
                target_workspace_id = target_workspaces[target_workspace_id_key]['id']

                update_workspace = target_workspaces[target_workspace_id_key]
                update_workspace['applications'] = new_application_list
                for app in target_workspace['applications']:
                    update_workspace['applications'].append(app)
                update_workspace['permissions'] = new_permission_dict

                self.updateWorkspace(self.swimlane_target, update_workspace['id'], update_workspace)
                self.dashboard_engine.migrateDashboards(self.mode,workspace, target_workspace_id, self.buildWorkspaceIDs(self.swimlane_target))








