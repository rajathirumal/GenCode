from typing import Tuple
from github import Github

import os

import time as time_module
from datetime import datetime


ACCESS_TOKEN = open("secrets.config", "r").read()
g = Github(ACCESS_TOKEN)


def save_repos(listOfRepos) -> Tuple:
    """
    This function will save the repositories to the local machine.
    It will create a directory with the name of the repository and clone the repository into that directory.

    :param listOfRepos: List of repositories to be saved
    :return: Tuple of (number of repo provided, number of repo saved, elapsed, success rate)
    """
    repo_pull_start_time = time_module.time()
    total_repos_provided = listOfRepos.totalCount
    total_repos_saved = 0
    success_rate = 0
    DEFAULT_SAVE_PATH = "./download"
    if not os.path.exists(DEFAULT_SAVE_PATH):
        os.makedirs(DEFAULT_SAVE_PATH)

    for repo in listOfRepos:
        dirname = f"{DEFAULT_SAVE_PATH}/{repo.full_name}"
        command = f"git clone {repo.clone_url} {dirname} > /dev/null 2>&1"
        try:
            os.system(command)
            total_repos_saved += 1
        except SystemError as e:
            print(f"Error: {e}")
            print("Skipping this repository...")
            continue

    repo_pull_end_time = time_module.time()
    elapsed = repo_pull_end_time - repo_pull_start_time

    if total_repos_provided > 0:
        success_rate = (total_repos_saved / total_repos_provided) * 100
    else:
        success_rate = 0
    return (total_repos_provided, total_repos_saved, elapsed, success_rate)


def pull_repo_within(
    start_selector, end_selector, star_count=10
) -> Tuple[str, str, object]:
    query = (
        f"language:python created:{start_selector}..{end_selector} stars:>{star_count}"
    )
    listOfRepos = g.search_repositories(query)
    return listOfRepos


def user_interaction():
    batch_numer = 0
    total_repos = 0
    star_count = 20
    number_of_days = 1  # default number of days to go back
    print("This code will pull repositories for each day, Please answer when prompted.")
    print(
        "If you wish to start from a specific date, please prompt the date in YYYY-MM-DD format, else it will start from today and move backeards for 1 day."
    )
    end_date = input("Enter the date to start from (YYYY-MM-DD): ")
    if end_date:
        try:
            end_time = datetime.strptime(
                end_date, "%Y-%m-%d"
            ).timestamp()  # Compute epoch time
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            exit(1)
    else:
        # Assuming the user wants to start from today
        end_time = time_module.time()  # gives the epoch time when this line is execute

    start_time = end_time - ((number_of_days * 24) * 3600)  # 86400 seconds = 1 day

    while True:
        start_selector = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d")
        end_selector = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d")
        repos = pull_repo_within(start_selector, end_selector, star_count)
        if repos.totalCount == 0:
            user_input = input(
                f"No repositories found for the date range {start_selector} to {end_selector} , press y to continue or any key to exit:"
            )
        else:
            user_input = input(
                f"We are about to pull {repos.totalCount} repositories from {start_selector} to {end_selector}, do you want to continue? (y/n): "
            )
        if user_input == "y":
            if repos.totalCount != 0:
                batch_numer += 1
                print("Hold on while we pull the repositories ...")
                (
                    provided_repo_count_batch,
                    saved_repo_count_batch,
                    elapsed_batch,
                    success_rate_batch,
                ) = save_repos(repos)
                total_repos += repos.totalCount
                print(
                    "====================== Current bacth metrics ======================"
                )
                print(f"Metrics for this batch: {batch_numer}")
                print(f"Repositories pulled from {start_selector} to {end_selector}")
                print(
                    f"Number of repos with stars >{star_count} : {provided_repo_count_batch}"
                )
                print(f"Total repositories saved: {saved_repo_count_batch}")
                print(f"Elapsed time: {elapsed_batch} seconds")
                print(f"Success rate: {success_rate_batch}%")
                print(
                    "==================================================================="
                )
            end_time = start_time
            start_time = start_time - ((number_of_days * 24) * 3600)
        else:
            print("Thanks for using this code, have a nice day!")
            break

    print(f"Total repositories pulled: {total_repos}")


if __name__ == "__main__":
    user_interaction()
