import os
import json
from pathlib import Path
from git import Repo, SymbolicReference
from git.exc import InvalidGitRepositoryError
import traceback

from continual.python.sdk.metadata import Metadata, MetadataManager
from continual.python.utils.utils import recursive_get


class ContextProvider:
    """Base context provider class."""

    name: str

    def log(self, metadata_manager: MetadataManager) -> Metadata:
        raise NotImplementedError()


class GitContext(ContextProvider):

    name: str = "git-context"

    def log(self, metadata_manager: MetadataManager) -> Metadata:
        if self._is_git_repo():
            try:
                git_context = self._get_git_metadata()
                if git_context is not None:
                    return metadata_manager.create(
                        id=self.name,
                        data=git_context,
                    )
                else:
                    return None
            except Exception as e:
                if metadata_manager.client.config.debug:
                    print(f"Error logging git context: {e}")
                    print(traceback.format_exc())
                return None

    def _is_git_repo(self) -> bool:
        try:
            _ = Repo(os.getcwd())
            return True
        except InvalidGitRepositoryError:
            return False

    def _get_git_metadata(self) -> dict:
        repo = Repo(os.getcwd(), search_parent_directories=True)
        repo_is_bare = repo.bare

        repository_name_local = ""
        if repo.working_tree_dir:
            repository_name_local = Path(repo.working_tree_dir).parts[-1]

        repository_name_remote_origin = ""
        repository_remote_origin_url = ""
        if repo.remotes and repo.remotes[0].name == "origin":
            # TODO: consider getting this from current branch tracking branch instead
            repository_name_remote_origin = os.path.splitext(
                os.path.basename(repo.remotes.origin.url)
            )[0]
            repository_remote_origin_url = repo.remotes.origin.url

        repository_name = (
            repository_name_remote_origin
            if repository_name_remote_origin
            else repository_name_local
        )

        branch_name = ""
        try:
            branch_name = repo.active_branch.name
        except:
            pass

        current_commit = None
        if not repo_is_bare:
            if isinstance(repo.head, SymbolicReference):
                current_commit = repo.head.commit
            else:
                current_commit = repo.head.reference.commit

        current_ref = None
        try:
            current_ref = repo.head.reference
        except:
            pass

        current_tag_name = ""
        current_tag_name_long = ""
        try:
            current_tag_name = repo.git.describe("--exact-match", "--abbrev=0")
            current_tag_name_long = repo.git.describe("--exact-match", "--long")
        except:
            pass

        reachable_tag_name = ""
        reachable_tag_name_long = ""
        try:
            reachable_tag_name = repo.git.describe("--abbrev=0")
            reachable_tag_name_long = repo.git.describe("--long")
        except:
            pass

        # consider setting untracked_files=True here
        is_dirty = repo.is_dirty()

        return dict(
            repository=dict(
                name=repository_name,
                name_local=repository_name_local,
                name_remote_origin=repository_name_remote_origin,
                is_bare=repo_is_bare,
                remote_origin_url=repository_remote_origin_url
                # default_branch_name
            ),
            branch=dict(name=branch_name),
            tags=dict(
                current=dict(
                    name=current_tag_name, name_describe=current_tag_name_long
                ),
                reachable=dict(
                    name=reachable_tag_name, name_describe=reachable_tag_name_long
                ),
            ),
            ref=dict(path=current_ref.path if current_ref is not None else ""),
            commit=dict(
                sha=current_commit.hexsha,
                message=current_commit.message,
                authored_datetime=current_commit.authored_datetime,
                author=dict(
                    name=current_commit.author.name, email=current_commit.author.email
                ),
                committed_datetime=current_commit.committed_datetime,
                committer=dict(
                    name=current_commit.committer.name,
                    email=current_commit.committer.email,
                ),
            )
            if current_commit is not None
            else None,
            head=dict(is_detached=repo.head.is_detached),
            is_dirty=is_dirty,
        )


class CicdRunnerContext(ContextProvider):
    name: str = "cicd-runner-context"

    def log(self, metadata_manager: MetadataManager) -> Metadata:
        if self._is_cicd_runner_context():
            try:
                cicd_runner_context = self._get_cicd_runner_metadata()
                if cicd_runner_context is not None:
                    return metadata_manager.create(
                        id=self.name,
                        data=cicd_runner_context,
                    )
                else:
                    return None
            except Exception as e:
                if metadata_manager.client.config.debug:
                    print(f"Error logging CI/CD runner context: {e}")
                    print(traceback.format_exc())
                return None

    def _is_cicd_runner_context(self) -> bool:
        # TODO: support other cicd runners
        return self._is_github_actions_cicd_runner_context()

    def _get_cicd_runner_metadata(self) -> dict:
        if self._is_github_actions_cicd_runner_context():
            return self._get_github_actions_metadata()
        return dict()

    # Github Actions

    def _is_github_actions_cicd_runner_context(self) -> bool:
        is_github_actions = False
        if os.environ.get("GITHUB_ACTIONS") == "true":
            is_github_actions = True

        return is_github_actions

    def _get_github_actions_metadata(self) -> dict:
        return dict(
            provider="Github Actions",
            run_id=f'{os.environ.get("GITHUB_RUN_ID")}-{os.environ.get("GITHUB_RUN_ATTEMPT")}',
            # Can't link to specific job because we don't have GITHUB_JOB_ID ( https://stackoverflow.com/questions/71240338/obtain-job-id-from-a-workflow-run-using-contexts )
            run_url=f'https://github.com/{os.environ.get("GITHUB_REPOSITORY")}/actions/runs/{os.environ.get("GITHUB_RUN_ID")}/attempts/{os.environ.get("GITHUB_RUN_ATTEMPT")}',
            data=dict(
                GITHUB_EVENT_NAME=os.environ.get("GITHUB_EVENT_NAME"),
                GITHUB_JOB=os.environ.get("GITHUB_JOB"),
                GITHUB_REF=os.environ.get("GITHUB_REF"),
                GITHUB_REPOSITORY=os.environ.get("GITHUB_REPOSITORY"),
                GITHUB_RUN_ID=os.environ.get("GITHUB_RUN_ID"),
                GITHUB_RUN_NUMBER=os.environ.get("GITHUB_RUN_NUMBER"),
                GITHUB_RUN_ATTEMPT=os.environ.get("GITHUB_RUN_ATTEMPT"),
                GITHUB_SHA=os.environ.get("GITHUB_SHA"),
                GITHUB_WORKFLOW=os.environ.get("GITHUB_WORKFLOW"),
                RUNNER_NAME=os.environ.get("RUNNER_NAME"),
            ),
        )


class GitProviderContext(ContextProvider):
    name: str = "git-provider-context"

    def log(self, metadata_manager: MetadataManager) -> Metadata:
        if self._is_git_provider_context():
            try:
                git_provider_context = self._get_git_provider_metadata()
                if git_provider_context is not None:
                    return metadata_manager.create(
                        id=self.name,
                        data=git_provider_context,
                    )
                else:
                    return None
            except Exception as e:
                if metadata_manager.client.config.debug:
                    print(f"Error logging git provider context: {e}")
                    print(traceback.format_exc())
                return None

    def _is_git_provider_context(self) -> bool:
        # TODO: support other providers
        return self._is_github_git_provider()

    def _get_git_provider_metadata(self) -> dict:
        if self._is_github_git_provider():
            return self._get_github_git_provider_metadata()
        return dict()

    # Github

    def _is_github_git_provider(self) -> bool:
        # TODO: Figure this out in more ways
        return self._is_github_git_provider_via_github_actions()

    def _is_github_git_provider_via_github_actions(self) -> bool:
        return CicdRunnerContext()._is_github_actions_cicd_runner_context()

    def _get_github_git_provider_metadata(self) -> dict:
        if self._is_github_git_provider_via_github_actions():
            return self._get_github_git_provider_metadata_via_github_actions()
        return dict()

    def _get_github_git_provider_metadata_via_github_actions(self) -> dict:
        github_actions_metadata = CicdRunnerContext()._get_github_actions_metadata()

        return dict(
            provider="Github",
            repository=dict(
                name=github_actions_metadata["data"]["GITHUB_REPOSITORY"],
                # In Github Actions GITHUB_REPOSITORY is `account_name/repo_name`
                url=f'https://github.com/{github_actions_metadata["data"]["GITHUB_REPOSITORY"]}',
            ),
        )


class SdlcReviewContext(ContextProvider):
    name: str = "sdlc-review-context"

    def log(self, metadata_manager: MetadataManager) -> Metadata:
        if self._is_sdlc_review_context():
            try:
                sdlc_review_context = self._get_sdlc_review_metadata()
                if sdlc_review_context is not None:
                    return metadata_manager.create(
                        id=self.name,
                        data=sdlc_review_context,
                    )
                else:
                    return None
            except Exception as e:
                if metadata_manager.client.config.debug:
                    print(f"Error logging SDLC review context: {e}")
                    print(traceback.format_exc())
                return None

    def _is_sdlc_review_context(self) -> bool:
        # TODO: support other providers
        return self._is_github_pr_context()

    def _get_sdlc_review_metadata(self) -> dict:
        if self._is_github_pr_context():
            return self._get_github_pr_metadata()
        return dict()

    # Github

    def _is_github_pr_context(self) -> bool:
        # TODO: Figure this out in more ways
        return self._is_github_pr_context_via_github_actions()

    def _is_github_pr_context_via_github_actions(self) -> bool:
        return CicdRunnerContext()._is_github_actions_cicd_runner_context()

    def _get_github_pr_metadata(self) -> dict:
        if self._is_github_pr_context_via_github_actions():
            return self._get_github_pr_metadata_via_github_actions()
        return dict()

    def _get_github_pr_metadata_via_github_actions(self) -> dict:
        github_actions_event = self._parse_github_actions_event()

        is_pr_context = recursive_get(github_actions_event, "pull_request")
        if not is_pr_context:
            return None

        return dict(
            provider="Github PR",
            id=str(recursive_get(github_actions_event, "pull_request", "number")),
            url=recursive_get(github_actions_event, "pull_request", "html_url"),
            state=recursive_get(github_actions_event, "pull_request", "state"),
            title=recursive_get(github_actions_event, "pull_request", "title"),
            user=dict(
                user_name=recursive_get(
                    github_actions_event, "pull_request", "user", "login"
                ),
                url=recursive_get(
                    github_actions_event, "pull_request", "user", "html_url"
                ),
                avatar_url=recursive_get(
                    github_actions_event, "pull_request", "user", "avatar_url"
                ),
            ),
            base=dict(
                branch=recursive_get(
                    github_actions_event, "pull_request", "base", "ref"
                ),
                sha=recursive_get(github_actions_event, "pull_request", "base", "sha"),
            ),
            head=dict(
                branch=recursive_get(
                    github_actions_event, "pull_request", "head", "ref"
                ),
                sha=recursive_get(github_actions_event, "pull_request", "head", "sha"),
            ),
            data=dict(
                # TODO
            ),
        )

    def _parse_github_actions_event(self) -> dict:
        # TODO: maybe get this from CicdRunnerContext()._get_github_actions_metadata() instead
        github_event_file = os.environ.get("GITHUB_EVENT_PATH")
        if github_event_file is None or not os.path.exists(github_event_file):
            return dict()

        try:
            with open(github_event_file, "r") as f:
                github_event = json.load(f)
        except:
            return dict()

        return github_event
