import requests
import time

def retrieve_github_file(owner, repo, filepath):
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{filepath}"
    
    response = requests.get(raw_url, stream=True)
    
    if response.status_code == 200:
        contents = response.content.decode("utf-8")
        return contents
    else:
        print(f"Failed to retrieve the file. Status code: {response.status_code}")
        return None

def list_repository_files(owner, repo):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        files = response.json()
        return [file_info['path'] for file_info in files]
    else:
        print(f"Failed to list repository files. Status code: {response.status_code}")
        return []

# Replace these with the appropriate values for the GitHub repository
owner = ""
repo = ""

while True:
    print("Select an option:")
    print("1. Retrieve all files")
    print("2. List repository files")
    option = input("Enter option number: ")

    if option == "1":
        files = list_repository_files(owner, repo)
        with open("github.txt", "a") as output_file:
            for file_path in files:
                file_content = retrieve_github_file(owner, repo, file_path)
                if file_content is not None:
                    output_file.write(f"File: {file_path}\n{file_content}\n{'='*40}\n")
        print("Data saved to github.txt")
    elif option == "2":
        files = list_repository_files(owner, repo)
        print("Repository files:")
        for idx, file_path in enumerate(files, start=1):
            print(f"{idx}. {file_path}")

        selection = int(input("Enter the number of the file to retrieve: ")) - 1
        if 0 <= selection < len(files):
            selected_file = files[selection]
            file_content = retrieve_github_file(owner, repo, selected_file)
            if file_content is not None:
                with open("github.txt", "a") as output_file:
                    output_file.write(file_content)
                print(f"Data from '{selected_file}' saved to github.txt")
        else:
            print("Invalid selection.")
    else:
        print("Invalid option.")
    
    # Wait for a specified interval before prompting again
    time.sleep(2)
