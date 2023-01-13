from lib.http import Http, HTTPException
from lib.util import log, get_dict_value


class GithubClient:
    '''github api'''
    # 下面定义了一个类属性
    token = 'token'
    http = None

    def __init__(self, http, token):
        self.token = token
        self.http = http

    def create_pull_request(self, title, body, url, src_branch, target_branch):
        '''
        https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28

        curl \
          -X POST \
          -H "Accept: application/vnd.github+json" \
          -H "Authorization: Bearer <YOUR-TOKEN>"\
          -H "X-GitHub-Api-Version: 2022-11-28" \
          https://api.github.com/repos/OWNER/REPO/pulls \
          -d '{"title":"Amazing new feature","body":"Please pull these awesome changes in!","head":"octocat:new-feature","base":"master"}'
        '''
        # 根据url 找出owner/repo_name
        repo_path = url.strip().replace("https://github.com/", "").replace(".git", "")
        if repo_path.endswith("/"):
            repo_path = repo_path[0, len(repo_path) - 1]

        log(f'repo: {repo_path}')
        arr = repo_path.split("/")
        owner = arr[0]
        repo = arr[1]
        api = f"https://api.github.com/repos/{repo_path}/pulls"
        try:
            res = self.http.post(api, data={
                "title": title,
                "body": body,
                "head": f"{owner}:{src_branch}",
                "base": target_branch,
                "maintainer_can_modify": True
            }, headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28"
            }, res_is_standard=False, res_is_json=True)
            pull_id = res['id']
            return f"https://github.com/{repo_path}/pull/{pull_id}"
        except HTTPException as e:
            errors = get_dict_value(e, 'errors', [])
            only_ignore_error = True
            for err in errors:
                message = get_dict_value(err, 'message')
                if message.startswith("No commits between "):
                    log(f"提交PR失败：{message}")
                    continue
                else:
                    only_ignore_error = False
            if not only_ignore_error:
                raise e
