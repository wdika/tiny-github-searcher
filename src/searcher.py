import time

import requests
from pathlib import Path


def search_code(keywords):
    # search GitHub api for repositories containing the keyword
    repos = []
    for keyword in keywords:
        print(f"Searching for {keyword}...")

        url = f"https://api.github.com/search/repositories?q={keyword}"
        response = requests.get(url)

        if response.status_code == 403:
            print("Rate limited. Waiting 5 minutes...")
            time.sleep(300)
            response = requests.get(url)

        response.raise_for_status()
        data = response.json()

        # find how many repositories were found
        num_repos = data["total_count"]
        print(f"Found {num_repos} repositories containing {keyword}")

        # find how many pages of results there are
        num_pages = num_repos // 30

        # get urls for each page of results
        for page in range(1, num_pages + 1):
            print(f"Processing page {page}...")

            url = f"https://api.github.com/search/repositories?q={keyword}&page={page}"
            response = requests.get(url)
            # try to avoid getting rate limited
            if response.status_code == 403:
                print("Rate limited. Waiting 5 minutes...")
                time.sleep(300)
                response = requests.get(url)

            if response.status_code == 422:
                # continue to the next keyword
                break

            response.raise_for_status()

            data = response.json()

            if len(data) == 0:
                break

            for repo in data["items"]:
                html_url = repo["html_url"]
                repos.append(html_url)

    # write unique urls to file
    with open("results/github_repositories_overall.csv", "w") as f:
        for repo in repos:
            f.write(repo + "\n")


def main(args):
    # create results directory if it doesn't exist
    Path("results").mkdir(exist_ok=True)

    search_code(args.keywords)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("keywords", nargs="+")
    args = parser.parse_args()
    main(args)
