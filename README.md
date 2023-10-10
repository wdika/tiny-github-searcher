# Tiny GitHub Searcher 🚀
***

## 🧐 About

A tiny GitHub searcher using the GitHub API. No authentication required. Nothing fancy, just a tiny searcher that allows you to search for GitHub repositories given a set of keywords and returns a CSV file with the results. Simple parser and filterer included.

## 📖 How to use
1. **Clone the repository 💻**
   ```bash
   git clone https://github.com/wdika/tiny-github-searcher.git
    ```
2. **Install dependencies ⚙️**
   ```bash
   pip install -r requirements.txt
    ```
3. **Run the searcher 🏃**
    ```bash
    python src/searcher.py {keywords}
     ```
     This will take long time, since it will search for all the repositories that match the keywords given. It also halts for 5 minutes when getting a 403 error, to escape the GitHub API rate limit. Please be patient.
4. **Enjoy the results! 😃**

### 🛠️ Optional Steps
1. **Clean the results 🔍**
    ```bash
    python src/cleaner.py results/github_repositories_overall.csv
    ```
   This will clean the results file, removing duplicates and removing dead repositories (those that return a 404 error 
    when trying to access them). This will take a while, since it will try to access all the repositories that were 
    found. Please be patient.
2. **Parse the results 📝**
    ```bash
    python src/parser.py results/github_repositories_overall_clean.csv
    ```  
    This will parse the results file, extracting the _About_, _Stars_, _Forks_, _Language_ and _Keywords_ fields from every repository. This will take a while, since it will try to access all the repositories that were found. Please be patient.
3. **Filter the results 📌**
    ```bash
    python src/filterer.py results/github_repositories_overall_analytical.csv
    ```  
    This will filter the parsed results file, removing empty, nans, false characters, etc from the _About_, _Stars_, _Forks_, _Language_ and _Keywords_ fields.
4. **That's it!** You can now use the **results/github_repositories_overall_analytical_filtered.csv** file to do whatever you want.

## 🌟 Full Running Example
```bash 
./scripts/search_github_repositories.sh
```

## 📄 License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.


## 📧 Contact
If you have any question or suggestion, please do not hesitate to contact me at dimitriskarkalousos@gmail.com
