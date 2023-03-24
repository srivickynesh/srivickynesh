import os
import re
import requests
from github import Github

def get_daily_quote():
    response = requests.get("https://quotes.rest/qod?category=inspire")
    if response.status_code == 200:
        json_response = response.json()
        quote = json_response['contents']['quotes'][0]['quote']
        author = json_response['contents']['quotes'][0]['author']
        return quote, author
    else:
        raise Exception("Failed to fetch quote")

def update_readme(quote, author):
    with open("README.md", "r") as file:
        content = file.read()

    new_content = re.sub(
        r'(?<=<\/p>)(.*)(?=<\/p>)',
        f'\n\n<center><p style="font-size: 1.5em; font-weight: bold; color: #1e90ff;">{quote}</p><p>- {author}</p></center>',
        content,
        flags=re.DOTALL
    )

    if content != new_content:
        with open("README.md", "w") as file:
            file.write(new_content)
        return True
    return False

if __name__ == "__main__":
    quote, author = get_daily_quote()
    if update_readme(quote, author):
        token = ${{ secrets.GITHUB_TOKEN }}
        repo = Github(token).get_repo("srivickynesh/srivickynesh")
        repo.update_file("README.md", "Update daily quote", open("README.md", "r").read(), repo.get_contents("README.md").sha)
