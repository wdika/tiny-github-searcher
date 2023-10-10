import pandas as pd


def main(args):
    input_csv = pd.read_csv(args.input_csv)

    all_languages = []
    # read languages
    languages = input_csv["languages"].tolist()
    # read languages and remove number followed by %
    for language in languages:
        if language not in ["nan", "", " "]:
            language = str(language)
            for sublanguage in language.split(" "):
                if "%" not in sublanguage and sublanguage not in ["nan", "", " ", "Other", "more", "other", "More"] \
                        and "," not in sublanguage and ":" not in sublanguage and '"' not in sublanguage \
                        and '{' not in sublanguage and '}' not in sublanguage and '[' not in sublanguage \
                        and ']' not in sublanguage and '#' not in sublanguage and not sublanguage.isdigit():
                    all_languages.append(sublanguage)

    # count languages
    languages_count = {}
    for language in all_languages:
        if language in languages_count:
            languages_count[language] += 1
        else:
            languages_count[language] = 1

    # sort languages by count
    languages_count = {k: v for k, v in sorted(languages_count.items(), key=lambda item: item[1], reverse=True)}

    # read keywords
    keywords = input_csv["keywords"].tolist()
    all_keywords = []
    for keyword in keywords:
        if keyword not in ["nan", "", " "]:
            keyword = str(keyword)
            for subkeyword in keyword.split(" "):
                if subkeyword not in ["nan", "", " ", "Other", "more", "other", "More"] \
                        and "," not in subkeyword and ":" not in subkeyword and '"' not in subkeyword \
                        and '{' not in subkeyword and '}' not in subkeyword and '[' not in subkeyword \
                        and ']' not in subkeyword and '#' not in subkeyword and not subkeyword.isdigit():
                    all_keywords.append(subkeyword)

    # count keywords
    keywords_count = {}
    for keyword in all_keywords:
        if keyword in keywords_count:
            keywords_count[keyword] += 1
        else:
            keywords_count[keyword] = 1

    # sort keywords by count
    keywords_count = {k: v for k, v in sorted(keywords_count.items(), key=lambda item: item[1], reverse=True)}

    # remove keywords with count < 2
    keywords_count = {k: v for k, v in keywords_count.items() if v > 1}

    top_languages = list(languages_count.keys())[:2]
    top_keywords = list(keywords_count.keys())[:1]
    top_repos = []
    for index, row in input_csv.iterrows():
        if any(language in str(row["languages"]) for language in top_languages):
            for keyword in top_keywords:
                if any(keyword in str(row["keywords"]) for keyword in top_keywords):
                    top_repos.append(row)

    # print len top repos / len all repos
    print(f"Found {len(top_repos)} / {len(input_csv)} repositories containing top keywords and top languages")

    # write top repos to input_csv
    top_repos = pd.DataFrame(top_repos)
    top_repos.to_csv("results/github_repositories_overall_analytical_filtered.csv", index=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="csv file to parse")
    args = parser.parse_args()
    main(args)
