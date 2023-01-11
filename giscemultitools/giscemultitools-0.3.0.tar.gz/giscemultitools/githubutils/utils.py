class GithubUtils:
    @staticmethod
    def plain_get_commits_sha_from_merge_commit(response):
        res = {
            'commits': [
                commit['commit']['oid'] for commit in response['data']['repository']['pullRequest']['commits']['nodes']
            ],
            'pullRequest': {
                'number': response['data']['repository']['pullRequest']['number'],
                'state': response['data']['repository']['pullRequest']['state'],
                'milestone': response['data']['repository']['pullRequest']['milestone'] and response['data']['repository']['pullRequest']['milestone']['title'] or '',
                'url': response['data']['repository']['pullRequest']['url'],
                'title': response['data']['repository']['pullRequest']['title'],
                'baseRefName': response['data']['repository']['pullRequest']['baseRefName'],
            },
            'projectItems': []
        }
        for card in response['data']['repository']['pullRequest']['projectItems']['nodes']:
            pos_status = 0
            for i, node in enumerate(card['fieldValues']['nodes']):
                if node and node.get('field', {}).get('name') == 'Status':
                    pos_status = i
                    break

            res['projectItems'].append(
                {
                    'project_name': card['project']['title'],
                    'project_id': card['project']['id'],
                    'project_url': card['project']['url'],
                    'card_state': card['fieldValues']['nodes'][pos_status]['name'],
                    'field_id': card['fieldValues']['nodes'][pos_status]['id'],
                    'field_column_id': card['fieldValues']['nodes'][pos_status]['field']['id'],
                    'field_column_options': {
                        opt['name']: opt['id'] for opt in card['fieldValues']['nodes'][pos_status]['field']['options']
                    },
                    'card_id': card['id']
                }
            )

        return res

    @staticmethod
    def get_commits_sha_from_merge_commit(owner, repository, sha):
        from .objects import GHAPIRequester
        requester = GHAPIRequester(owner, repository)

        pulls = requester.get_pulls_from_sha(sha)
        pull_request_number = None
        for pr in pulls:
            if pr['merge_commit_sha'] == sha:
                pull_request_number = pr['number']
                break

        if pull_request_number is None:
            raise

        pr_info = requester.get_pull_request_projects_and_commits(pull_request_number=pull_request_number)
        pr_info = GithubUtils.plain_get_commits_sha_from_merge_commit(pr_info)

        return pr_info

    @staticmethod
    def get_pullrequest_info(owner, repository, pr_number):
        from .objects import GHAPIRequester
        requester = GHAPIRequester(owner, repository)

        pr_info = requester.get_pull_request_projects_and_commits(pull_request_number=pr_number)
        pr_info = GithubUtils.plain_get_commits_sha_from_merge_commit(pr_info)

        return pr_info

    @staticmethod
    def update_projectv2_item_field_value(owner, repository, project_id, item_id, field_column_id, value):
        from .objects import GHAPIRequester
        requester = GHAPIRequester(owner, repository)
        return requester.update_projectv2_item_field_value(project_id, item_id, field_column_id, value)
