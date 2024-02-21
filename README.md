# Codacy Coverage PR Generator

## Description

This project automates the integration of Codacy coverage reporting into GitHub Actions workflows. It dynamically adds a Codacy coverage reporting step to an existing GitHub Actions workflow, creates a repository secret for the Codacy API token, and submits a pull request with these changes.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python3 and pip installed
- A Codacy account and a generated Codacy API token
- A GitHub account with access to the repository where you want to add coverage reporting
- Permissions to create secrets and pull requests in the target GitHub repository

## GitHub Token Requirements

You need a GitHub Personal Access Token (PAT) with the following permissions:
- `repo` (Full control of private repositories)
- `workflow` (Update GitHub Action workflows)

This token is used to authenticate API requests for creating secrets, fetching repository content, and opening pull requests.

## How to Setup for Development

1. Clone this repository to your local machine.
2. Navigate to the project directory and run `pip install -r requirements.txt` to install dependencies.
3. Create a `.env` file in the project root with your `CODACY_API_TOKEN` and `GITHUB_API_TOKEN`:
4. Optionally, you can add `GITHUB_OWNER` and `GITHUB_REPO` to your `.env` file to avoid being prompted each time.

## How to Run

1. Open your terminal and navigate to the project root directory.

2. Ensure all dependencies are installed by running:

   ```bash
   pip install -r requirements.txt
   python3 main.py

The application will prompt you to enter the necessary tokens (Codacy API token, GitHub API token) and repository information (GitHub owner, GitHub repository name) if they are not already set in your .env file. Follow the prompts to complete the integration process.

### Notes

The application will list all GitHub Actions workflow files found in the .github/workflows directory of the specified GitHub repository. You'll be prompted to select one for adding the Codacy coverage reporting step.
After making your selection, the script automatically creates a new branch, updates the selected workflow file with the Codacy coverage reporting step, and opens a pull request with these changes for you to review and merge.
Ensure you have at least one workflow file in the target repository and the necessary permissions to create secrets and pull requests.
