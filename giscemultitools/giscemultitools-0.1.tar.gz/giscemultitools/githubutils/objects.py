import requests
import os
from json import loads, dumps


class RepositorySetUp(object):
    def __init__(self, owner, repository):
        self.owner = owner
        self.repository = repository


class GHAPIRequester(RepositorySetUp):
    def __init__(self, owner, repository):
        super(GHAPIRequester, self).__init__(owner, repository)
        if not os.environ.get('GITHUB_TOKEN'):
            raise EnvironmentError('Missing GITHUB_TOKEN environment variable')
        self.headers = {'Authorization': 'token {}'.format(os.environ.get('GITHUB_TOKEN'))}
        self.base_url = 'https://api.github.com/repos/{}/{}/'.format(self.owner, self.repository)
        self.graphql_url = 'https://api.github.com/graphql'

    def _request(self, url):
        r = requests.get(url, headers=self.headers)
        return loads(r.text)

    def _graphql_request(self, data):
        r = requests.post(self.graphql_url, data=data, headers=self.headers)
        return loads(r.text)

    def get_pulls_from_sha(self, sha):
        return self._request("{}commits/{}/pulls".format(self.base_url, sha))

    def get_commits_from_pr(self, pr):
        return self._request("{}pulls/{}/commits?per_page=100".format(self.base_url, pr))

    def get_pull_request_projects_and_commits(self, pull_request_number):
        # mergeCommit.oid is the hash
        query = """
            query {
                repository(owner: "%s", name: "%s") {
                    pullRequest(number: %s) {
                        baseRefName
                        number
                        state
                        url
                        title
                        milestone {
                          title
                        }

                        mergeCommit {
                            oid
                        }

                        commits(first: 250){
                            nodes {
                              commit {
                                oid
                              }
                            }
                        }

                        projectItems(first: 10) {
                            nodes {
                                project { id title number url }
                                id
                                type
                                fieldValues(last: 10) {
                                    nodes {
                                        ... on ProjectV2ItemFieldSingleSelectValue {
                                            id
                                            name
                                            field {
                                              ... on ProjectV2SingleSelectField {
                                                id
                                                name
                                                options {
                                                    name
                                                    id
                                                  }
                                              }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """ % (self.owner, self.repository, pull_request_number)
        return self._graphql_request(dumps({'query': query}))

    def update_projectv2_item_field_value(self, project_id, item_id, field_column_id, value):
        query = """
            mutation MyMutation {
              updateProjectV2ItemFieldValue(
                input: {projectId: "%s", itemId: "%s", fieldId: "%s", value: {singleSelectOptionId: "%s"}}
              ) {
                  clientMutationId
                  projectV2Item {
                    id
                  }
                }
            }

        """ % (project_id, item_id, field_column_id, value)
        return self._graphql_request(dumps({'query': query}))
