import pandas as pd
import re
import os
from collections import Counter


def filter_and_count_items(series, min_count=1, exclude_items=None):
    """
    Filter and count items from a pandas Series
    
    Args:
        series: Pandas Series containing strings to process
        min_count: Minimum count to include in results
        exclude_items: Set of items to exclude
    
    Returns:
        Dictionary of items and their counts, sorted by count
    """
    # Use a default empty set if exclude_items is None
    if exclude_items is None:
        exclude_items = set()
    
    # Initialize a counter for efficient counting
    counter = Counter()
    
    # Process each item in the series
    for item in series.dropna():
        # Convert to string and split by spaces
        item_str = str(item)
        
        # Use regex to extract words (handles more cases)
        words = re.findall(r'[A-Za-z0-9+#_.-]+', item_str)
        
        for word in words:
            # Skip if in exclude list, empty, or just a number
            if (word in exclude_items or 
                not word or 
                word.isdigit() or 
                len(word) <= 1):
                continue
            
            counter[word] += 1
    
    # Filter by minimum count
    result = {k: v for k, v in counter.items() if v >= min_count}
    
    # Sort by count (descending)
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))


def main(args):
    print(f"Processing {args.input_csv}...")
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Common items to exclude
    exclude_items = {
        "nan", "", " ", "Other", "more", "other", "More",
        "and", "the", "to", "of", "in", "for", "with", "by",
        "is", "on", "at", "an", "as", "from", "or", "that"
    }
    
    # Read the CSV
    input_csv = pd.read_csv(args.input_csv)
    
    # Process languages with automatic filtering
    languages_count = filter_and_count_items(
        input_csv["languages"],
        min_count=1,
        exclude_items=exclude_items
    )
    
    # Process keywords with automatic filtering
    keywords_count = filter_and_count_items(
        input_csv["keywords"],
        min_count=1,
        exclude_items=exclude_items
    )
    
    # Get top languages and keywords
    top_languages = list(languages_count.keys())[:2]
    top_keywords = list(keywords_count.keys())[:1]
    
    print(f"Top languages: {', '.join(top_languages)}")
    print(f"Top keywords: {', '.join(top_keywords)}")
    
    # Filter repositories containing top languages and keywords
    top_repos = []
    
    for _, row in input_csv.iterrows():
        languages = str(row["languages"]) if pd.notna(row["languages"]) else ""
        keywords = str(row["keywords"]) if pd.notna(row["keywords"]) else ""
        
        # Check if any top language is in the languages field
        has_top_language = any(lang in languages for lang in top_languages)
        
        # Check if any top keyword is in the keywords field
        has_top_keyword = any(keyword in keywords for keyword in top_keywords)
        
        # If both conditions are met, add to top_repos
        if has_top_language and has_top_keyword:
            top_repos.append(row)
    
    # Convert to DataFrame and save
    top_repos_df = pd.DataFrame(top_repos)
    output_path = "results/github_repositories_overall_analytical_filtered.csv"
    top_repos_df.to_csv(output_path, index=False)
    
    # Print summary
    print(f"Found {len(top_repos)} / {len(input_csv)} repositories containing top keywords and top languages")
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="CSV file to parse")
    args = parser.parse_args()
    main(args)
