import os
import re
import requests
from github import Github

def get_github_token():
    return os.getenv('GITHUB_TOKEN')

QUOTE_API_URL = "https://quotes.rest/qod?category=inspire"

def get_daily_quote():
    response = requests.get(QUOTE_API_URL)
    if response.ok:  # More idiomatic way to check for status code 200
        json_response = response.json()
        quote = json_response['contents']['quotes'][0]['quote']
        author = json_response['contents']['quotes'][0]['author']
        return quote, author
    else:
        response.raise_for_status()

def update_readme(quote, author):
    with open("README.md", "r", encoding='utf-8') as file:  # Specify encoding
        content = file.read()

    new_content = re.sub(
        r'(?<=<!-- START QUOTE -->)(.*)(?=<!-- END QUOTE -->)',
        f'\n\n<center><p>{quote}</p><p>- {author}</p></center>',
        content,
        flags=re.DOTALL
    )

    if content != new_content:
        with open("README.md", "w", encoding='utf-8') as file:  # Specify encoding
            file.write(new_content)
        return True
    return False

if __name__ == "__main__":
    quote, author = get_daily_quote()
    if update_readme(quote, author):
        token = get_github_token()
        if not token:
            raise Exception("GitHub token not found")
        repo = Github(token).get_repo("srivickynesh/srivickynesh")
        readme_content = open("README.md", "r", encoding='utf-8').read()
        repo.update_file(
            "README.md",
            "Update daily quote",
            readme_content,
            repo.get_contents("README.md").sha,
            branch="main"  # Specify the branch if needed
        )
