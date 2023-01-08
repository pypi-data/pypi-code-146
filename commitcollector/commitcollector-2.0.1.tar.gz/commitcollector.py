import os
import subprocess
import argparse
import re
from tqdm import tqdm
from datetime import datetime

def get_jira_ticket_number(commit_message):
  # Use a regular expression to search for a JIRA ticket number
  # in the commit message. The ticket number is typically
  # formatted as "PROJECT-123" where PROJECT is the JIRA project
  # key and 123 is the ticket number.
  match = re.search(r'\b[A-Z]+-\d+\b', commit_message)
  if match:
    # Return the ticket number if it was found
    return match.group()
  else:
    # Return None if no ticket number was found
    return None

def main():

  # Get the current working directory
  repo_directory = os.getcwd()

  # Set up the command-line arguments parser
  parser = argparse.ArgumentParser()
  parser.add_argument("days", type=int, help="Number of days to filter the commit messages by")
  parser.add_argument('--jira', action='store_true', help="Use to parse and collect only the jira ticket number from the commit messages")
  parser.add_argument('--verbose', action='store_true', help="Use to make the collector more talky")
  args = parser.parse_args()

  # Get the number of days from the command-line argument
  days = args.days

  # Set the time range for the commits
  time_range = f"--since='{days} days ago'"

  # Get a list of all directories in the current working directory
  repo_list = [repo for repo in os.listdir(repo_directory) if os.path.isdir(os.path.join(repo_directory, repo))]

  # Create the output directory if it does not exist
  if not os.path.exists("output"):
    os.makedirs("output")

  # Group the commit messages by date
  messages_by_date = {}

  # Iterate through the list of repositories
  for repo in tqdm(repo_list, desc="Collecting commits 🦥 " ,colour="blue", bar_format='{desc}{bar}'):
    # Change the current working directory to the repository
    os.chdir(os.path.join(repo_directory, repo))
    if args.verbose:
      print(repo)
    # Run the `git log` command to get the commit messages, filtering only commits that you created and are within the specified time range
    output = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True)

    # Get the username from the command output
    username = output.stdout.decode("utf-8").strip()

    output = subprocess.run(["git", "log", f"--author={username}", time_range, "--format=%h", "--branches"], capture_output=True)
    # Split the output into a list of commit messages
    hashes = output.stdout.decode("utf-8").split("\n")

    for commithash in hashes:
      if commithash:
        commit_message = subprocess.run(["git", "log", "--format=%s", "-1", commithash], capture_output=True).stdout.decode("utf-8").strip()
        if args.jira:
          commit_message = get_jira_ticket_number(commit_message)
        date = subprocess.run(["git", "log", "--format=%cd", "-1", "--date=short", commithash], capture_output=True).stdout.decode("utf-8").strip()
        if date not in messages_by_date:
          messages_by_date[date] = {}
        if repo not in messages_by_date[date]:
          messages_by_date[date][repo] = []
        messages_by_date[date][repo].append(commit_message)

  # Write the commit messages to a text file
  os.chdir(repo_directory)

  with open("output/commit_messages.txt", "w") as f:
    for date, rest in sorted(messages_by_date.items(), key = lambda x:datetime.strptime(x[0], '%Y-%m-%d'), reverse=True):
      f.write(f"📅 {date}\n")
      for service, messages in rest.items():
        f.write(f"    📂 {service}\n")
        for message in messages:
          f.write(f"        {message}\n")

  print("Done 🦧")

if __name__ == '__main__':
    main()
