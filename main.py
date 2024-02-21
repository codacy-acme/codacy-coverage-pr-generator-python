import requests
from dotenv import load_dotenv
import inquirer
import ruamel.yaml
from github_connector import GitHubConnector
import os
import io


load_dotenv()

def create_codacy_repo_token(provider, remote_organization_name, repository_name, codacy_api_token):
    url = f"https://app.codacy.com/api/v3/organizations/{provider}/{remote_organization_name}/repositories/{repository_name}/tokens"
    headers = {'api-token': codacy_api_token}
    response = requests.post(url, headers=headers)
    
    if response.ok:
        return response.json()['data']['token']
    else:
        print("Error creating Codacy repository token:", response.text)
        return None

def get_token(env_var_name, prompt_message):
    token = os.getenv(env_var_name)
    if not token:
        questions = [
            inquirer.Text('token', message=prompt_message)
        ]
        answers = inquirer.prompt(questions)
        return answers['token']
    return token

if __name__ == "__main__":
    CODACY_API_TOKEN = get_token('CODACY_API_TOKEN', 'Please enter your Codacy API token:')
    GITHUB_API_TOKEN = get_token('GITHUB_API_TOKEN', 'Please enter your GitHub API token:')
    GITHUB_OWNER = get_token('GITHUB_OWNER', 'Please enter your GitHub organization name:')
    GITHUB_REPO = get_token('GITHUB_REPO', 'Please enter your GitHub repository name:')

    gh_connector = GitHubConnector(GITHUB_API_TOKEN)

    codacy_project_token = create_codacy_repo_token('gh', GITHUB_OWNER, GITHUB_REPO, CODACY_API_TOKEN)
    if (codacy_project_token):
        gh_connector.add_secret_to_repository(GITHUB_OWNER, GITHUB_REPO, 'CODACY_PROJECT_TOKEN', codacy_project_token)
        gh_actions_files =  gh_connector.content_search(GITHUB_OWNER, GITHUB_REPO, '.github/workflows')
        print(gh_actions_files)
        if not gh_actions_files:
            print('No GH Actions on this repo, please create it first')
        else:
            questions = [
                inquirer.List('selectedFile',
                    message= 'We\'ve found the following actions, to which one do you want to add coverage?',
                    choices= gh_actions_files
                )
            ]
            answer = inquirer.prompt(questions)
            selected_file = answer['selectedFile']
            print(f'You selected: {selected_file}')
            file_content = gh_connector.get_file_content(GITHUB_OWNER, GITHUB_REPO, selected_file)
            yaml = ruamel.yaml.YAML()
            yaml_obj = yaml.load(file_content)
            new_coverage_step = {
                'name': 'Upload coverage report to Codacy',
                'uses': 'codacy/codacy-coverage-reporter-action@v1',
                'with': {
                    'project-token': '${{ secrets.CODACY_PROJECT_TOKEN }}'
                }
            }

            yaml_obj['jobs']['build']['steps'].append(new_coverage_step)
            
            main_branch = gh_connector.get_default_branch_name(GITHUB_OWNER, GITHUB_REPO)

            buf = io.StringIO()
            yaml.dump(yaml_obj,buf)
            output = buf.getvalue()
            
            gh_connector.create_pr_with_yaml_change(
                GITHUB_OWNER, GITHUB_REPO, main_branch, 'add-codacy-coverage-feature-branch',
                selected_file, "Add codacy coverage gh action", "Add codacy coverage to gh action",
                "In order to add codacy coverage reporter...", output)
            