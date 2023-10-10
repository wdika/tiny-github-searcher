import pandas as pd
import requests
from tqdm import tqdm


# Function to check if a GitHub URL is valid
def is_valid_github_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def main(args):
    # Read the CSV file
    df = pd.read_csv(args.input_csv, header=None)

    # Remove duplicates while keeping the original order
    seen = set()
    unique_github_urls = []
    for url in df.values:
        url = url[0]
        if url not in seen:
            seen.add(url)
            unique_github_urls.append(url)

    # Filter the list to keep only valid GitHub URLs, i.e. remove 404s
    valid_github_urls = [url for url in tqdm(unique_github_urls) if is_valid_github_url(url)]

    # Write the filtered list to a new CSV file
    df = pd.DataFrame(valid_github_urls)
    df.to_csv('results/github_repositories_overall_clean.csv', index=False, header=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="csv file to parse")
    args = parser.parse_args()
    main(args)
