from github import Github, GithubException
import base64
from base64 import b64encode


class GitHubConnector:
    def __init__(self, token):
        self.g = Github(token)

    def get_file_content(self, owner, repo, path):
        try:
            repo = self.g.get_repo(f"{owner}/{repo}")
            file_content = repo.get_contents(path)
            return base64.b64decode(file_content.content).decode('utf-8')
        except GithubException as e:
            print(f"GitHub API Error: {e}")
            return None

    def content_search(self, owner, repo, path):
        try:
            repo = self.g.get_repo(f"{owner}/{repo}")
            contents = repo.get_contents(path)
            print(contents)
            return [content.path for content in contents]
        except GithubException as e:
            print(f"GitHub API Error: {e}")
            return None

    def add_secret_to_repository(self, owner, repo, secret_name, secret_value):
        try:
            repo = self.g.get_repo(f"{owner}/{repo}")
            repo.create_secret(secret_name,secret_value)
            print(f"Secret '{secret_name}' added to repository '{owner}/{repo}'.")
        except Exception as e:
            print(f"Failed to add secret to repository: {e}")

    def get_default_branch_name(self, owner, repo):
        try:
            repo = self.g.get_repo(f"{owner}/{repo}")
            return repo.default_branch
        except GithubException as e:
            print(f"GitHub API Error: {e}")
            return None

    def create_pr_with_yaml_change(self, owner, repo, base_branch, new_branch_name, file_path, commit_message, pr_title, pr_body, updated_yaml_content):
        try:
            repo = self.g.get_repo(f"{owner}/{repo}")
            
            # Step 1: Get the SHA of the latest commit of the base branch
            base_sha = repo.get_git_ref(f"heads/{base_branch}").object.sha

            # Step 2: Create a new branch from the base branch
            repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=base_sha)

            # Step 3: Get the SHA of the existing file to update
            file_contents = repo.get_contents(file_path, ref=base_branch)
            file_sha = file_contents.sha

            # Step 4: Update the YAML file on the new branch
            repo.update_file(file_path, commit_message, updated_yaml_content, file_sha, branch=new_branch_name)

            # Step 5: Create a pull request
            repo.create_pull(title=pr_title, body=pr_body, head=new_branch_name, base=base_branch)
            
            print('Pull request created successfully.')
        except GithubException as e:
            print(f"Error creating pull request: {e}")
