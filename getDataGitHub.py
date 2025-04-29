from typing import Tuple
from github import Github

import os

import logging
import time as time_module
from datetime import datetime
from Database import Database
from log_config import configure_logging


class GetDataGitHub:

    def __init__(self):
        configure_logging()
        # script variables
        self.DEFAULT_SAVE_PATH = "./download"
        # Github interface variables
        self.ACCESS_TOKEN = open("secrets.config", "r").read()
        self.git = Github(self.ACCESS_TOKEN)
        # DB variables
        self.DB_TABLE_NAME = "GetDataGitHub"
        self.db = Database("metrics.db")
        self.db.initDb(self.DB_TABLE_NAME)
        self.db.get_cursor()
        self.max_batch_id = self.db.getBatId(self.DB_TABLE_NAME)

    def save_repos(self, listOfRepos) -> Tuple:
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
        if not os.path.exists(self.DEFAULT_SAVE_PATH):
            os.makedirs(self.DEFAULT_SAVE_PATH)

        for repo in listOfRepos:
            dirname = f"{self.DEFAULT_SAVE_PATH}/{repo.full_name}"
            command = f"git clone {repo.clone_url} {dirname} > /dev/null 2>&1"
            try:
                os.system(command)
                total_repos_saved += 1
            except SystemError as e:
                logging.error(f"Error: {e}")
                logging.error("Skipping this repository...")
                continue

        repo_pull_end_time = time_module.time()
        elapsed = repo_pull_end_time - repo_pull_start_time

        if total_repos_provided > 0:
            success_rate = (total_repos_saved / total_repos_provided) * 100
        else:
            success_rate = 0
        return (total_repos_provided, total_repos_saved, elapsed, success_rate)

    def isThisDateAlreadyPulled(self, date_string):
        """Check if the given date is in REPO_START_DATE column on GetDataGitHub table"""
        dbRes = self.db.cursor.execute(
            f"SELECT COUNT(*) FROM {self.DB_TABLE_NAME} WHERE REPO_START_DATE = ?",
            (date_string,),
        )

        if dbRes.fetchone()[0] > 0:
            logging.info(
                f"Data for {date_string} already pulled. Updating the local folder with new data"
            )
            self.updateLocalFolder = True
        else:
            logging.info(f"Date {date_string} does not exist in the database.")
            self.updateLocalFolder = False

    def pull_repo_within(
        self, start_selector, end_selector, star_count=10
    ) -> Tuple[str, str, object]:

        query = f"language:python created:{start_selector}..{end_selector} stars:>{star_count}"
        return self.git.search_repositories(query)

    def user_interaction(self):
        total_repos = 0
        star_count = 20
        number_of_days = 1  # default number of days to go back
        print(
            "This code will pull repositories for each day, Please answer when prompted."
        )
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
            end_time = (
                time_module.time()
            )  # gives the epoch time when this line is execute

        start_time = end_time - ((number_of_days * 24) * 3600)  # 86400 seconds = 1 day

        while True:
            start_selector = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d")
            end_selector = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d")
            self.isThisDateAlreadyPulled(start_selector)
            repos = self.pull_repo_within(start_selector, end_selector, star_count)
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

                    print("Hold on while we pull the repositories ...")
                    (
                        provided_repo_count_batch,
                        saved_repo_count_batch,
                        elapsed_batch,
                        success_rate_batch,
                    ) = self.save_repos(repos)
                    total_repos += repos.totalCount
                    logging.debug(
                        "====================== Current bacth metrics ======================"
                    )
                    logging.debug(f"pulling repositories into {self.DEFAULT_SAVE_PATH}")
                    logging.debug(f"Metrics for this batch: {self.max_batch_id}")
                    logging.debug(
                        f"Repositories pulled from {start_selector} to {end_selector}"
                    )
                    logging.debug(
                        f"Number of repos with stars >{star_count} : {provided_repo_count_batch}"
                    )
                    logging.debug(f"Total repositories saved: {saved_repo_count_batch}")
                    logging.debug(f"Elapsed time: {elapsed_batch} seconds")
                    logging.debug(f"Success rate: {success_rate_batch}%")
                    logging.debug(
                        "==================================================================="
                    )
                end_time = start_time
                start_time = start_time - ((number_of_days * 24) * 3600)
                self.db.cursor.execute(
                    f"INSERT INTO {self.DB_TABLE_NAME} (BATCH_ID, REPO_START_DATE, REPO_END_DATE, STAR_COUNT, NUMBER_OF_REPOS, NUMBER_OF_REPOS_SAVED, ELAPSED_TIME, SUCCESS_RATE, IS_FOLDER_UPDATE_EVENT) VALUES (?, ?, ?, ?, ?, ?, ?,?, ?)",
                    (
                        self.max_batch_id,
                        start_selector,
                        end_selector,
                        star_count,
                        provided_repo_count_batch,
                        saved_repo_count_batch,
                        elapsed_batch,
                        success_rate_batch,
                        self.updateLocalFolder,
                    ),
                )
                self.db.connection.commit()
                self.max_batch_id += 1
            else:
                print("Thanks for using this code, have a nice day!")
                break

        logging.debug(f"Total repositories pulled: {total_repos}")
        self.db.close()


if __name__ == "__main__":
    githubDataCollector = GetDataGitHub()
    githubDataCollector.user_interaction()
