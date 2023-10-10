import pandas as pd
import requests
from bs4 import BeautifulSoup
from numpy.core.defchararray import isdigit
from tqdm import tqdm
from pathlib import Path


def parse_repo_urls(args):
    # parse repo urls from csv and put them in a list
    df = pd.DataFrame(columns=["url", "about", "keywords", "languages", "stars", "forks"])

    with open(args.input_csv, "r") as f:
        for line in tqdm(f):
            url = line.strip()
            print(f"URL: {url}")
            response = requests.get(url, allow_redirects=False)

            soup = BeautifulSoup(response.text, "html.parser")
            soup = soup.text.replace("\n", " ")
            soup = " ".join(soup.split())

            if soup != "" and soup != " " and soup is not None:
                about = soup.split("Pull requests")
                if len(about) >= 1:
                    about = about[0]
                    if len(about) >= 1:
                        about = about.split("Skip to content")
                        if len(about) >= 1:
                            about = about[0]
                            if len(about) >= 1:
                                suffix = url.split("/")
                                if suffix[-1] != "":
                                    suffix = suffix[-1]
                                else:
                                    suffix = suffix[-2]
                                about = about.split(suffix)
                                if len(about) >= 1:
                                    about = about[-1]
                                    if len(about) >= 1:
                                        about = about.split(":")
                                        if len(about) >= 1:
                                            about = about[-1]
                                        else:
                                            about = ""
                                    else:
                                        about = ""
                                else:
                                    about = ""
                            else:
                                about = ""
                        else:
                            about = ""
                    else:
                        about = ""
                print(f"About: {about}")
                if about != "" and about != " " and about is not None:
                    stars = soup.split("Pull requests")[0].split("Notifications")[1].split("Star")[1].split(about)[0]
                else:
                    stars = soup.split("Pull requests")[0].split("Notifications")[1].split("Star")[1]
                if len(stars) > 10:
                    stars = stars.split(" ")[1]
                if " " in stars:
                    stars = stars.split(" ")[1]
                if "k" in stars:
                    stars = stars.replace("k", "00")
                    if "." in stars:
                        stars = stars.replace(".", "")
                    else:
                        stars = stars + "0"
                if stars == "":
                    stars = "0"
                if isdigit(stars):
                    stars = int(stars)
                    if about != "" and about != " " and about is not None:
                        stars = soup.split("Pull requests")
                        # check if is empty
                        if len(stars) >= 1:
                            stars = stars[0]
                            if len(stars) >= 1:
                                stars = stars.split("Notifications")
                                if len(stars) > 1:
                                    stars = stars[1]
                                    if len(stars) > 1:
                                        stars = stars.split("Star")
                                        if len(stars) >= 1:
                                            stars = stars[1]
                                            if len(stars) > 1:
                                                stars = stars.split(about)
                                                if len(stars) >= 1:
                                                    stars = stars[0]
                                                else:
                                                    stars = ""
                                            else:
                                                stars = ""
                                        else:
                                            stars = ""
                                else:
                                    stars = ""
                            else:
                                stars = ""
                        else:
                            stars = ""
                    else:
                        stars = ""
                    if " " in stars:
                        stars = stars.split(" ")[1]
                    if "k" in stars:
                        stars = stars.replace("k", "00")
                        if "." in stars:
                            stars = stars.replace(".", "")
                        else:
                            stars = stars + "0"
                    if stars == "":
                        stars = "0"
                    if isdigit(stars):
                        stars = int(stars)
                        print(f"Stars: {stars}")
                        if about != "" and about != " " and about is not None:
                            forks = \
                            soup.split("Pull requests")[0].split("Notifications")[1].split("Fork")[1].split(about)[
                                0].split("Star")[0]
                        else:
                            forks = \
                            soup.split("Pull requests")[0].split("Notifications")[1].split("Fork")[1].split("Star")[0]
                    if " " in forks:
                        forks = forks.split(" ")[1]
                    if "k" in forks:
                        forks = forks.replace("k", "00")
                        if "." in forks:
                            forks = forks.replace(".", "")
                        else:
                            forks = forks + "0"
                    if forks == "":
                        forks = "0"
                    if isdigit(forks):
                        forks = int(forks)
                    print(f"Forks: {forks}")
                else:
                    stars = 0
                    forks = 0

                if "Languages" in soup:
                    languages = soup.split("Languages")[1].split("Footer")[0]
                else:
                    languages = ""

                # to list
                languages = languages.split(" ")
                languages = [language for language in languages if language != "" and "%" not in language]

                print(f"Languages: {languages}")

                keywords = soup.split("Topics")[-1].split("Resources")[0]
                keywords = keywords.split(" ")
                keywords = [keyword for keyword in keywords if keyword != ""]
                if len(keywords) > 100:
                    keywords = ""

                print(f"Keywords: {keywords}")
            else:
                about = ""
                keywords = ""
                languages = ""
                stars = 0
                forks = 0

            df = pd.concat([df, pd.DataFrame({
                "url": [url],
                "about": [about],
                "keywords": [keywords],
                "languages": [languages],
                "stars": [stars],
                "forks": [forks]
            })], ignore_index=True)

            # save to csv
            df.to_csv("results/github_repositories_overall_analytical.csv", index=False)


def main(args):
    parse_repo_urls(args)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="csv file to parse")
    args = parser.parse_args()
    main(args)
