import requests
import re

USERNAME = "gloriouslegacy"
API_URL = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
HEADERS = {"Accept": "application/vnd.github.v3+json"}

README_FILE = "README.md"

def fetch_repos():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error fetching repos: {response.status_code}")
        return []
    return response.json()

def generate_projects_section(repos):
    lines = ["<!-- PROJECTS_START -->"]
    for repo in repos:
        name = repo.get("name")
        url = repo.get("html_url")
        desc = repo.get("description") or "No description"
        lines.append(f"- [{name}]({url}) — {desc}")
    lines.append("<!-- PROJECTS_END -->")
    return "\n".join(lines)

def update_readme(projects_section):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(r"<!-- PROJECTS_START -->.*?<!-- PROJECTS_END -->",
                         projects_section,
                         content, flags=re.DOTALL)
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    repos = fetch_repos()
    if not repos:
        print("No repositories found or error occurred.")
        return
    projects_section = generate_projects_section(repos)
    update_readme(projects_section)
    print("README.md has been updated with latest projects!")

if __name__ == "__main__":
    main()
