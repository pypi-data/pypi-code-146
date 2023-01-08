import os
import subprocess
import argparse
import re
import random
from tqdm import tqdm
from datetime import datetime

def get_username(repo_directory):
  """Returns the username of the user in the given repository directory."""
  os.chdir(repo_directory)
  output = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True)
  return output.stdout.decode("utf-8").strip()

def get_jira_ticket_number(commit_message):
  """Returns the JIRA ticket number from the commit message, if one exists.
  The ticket number is typically formatted as "PROJECT-123" where PROJECT is the JIRA project key and 123 is the ticket number.
  """
  match = re.search(r'\b[A-Z]+-\d+\b', commit_message)
  return match.group() if match else None

def get_commits(repo_directory, username, time_range):
  """Returns a list of commit hashes for commits by the given username in the given repository directory within the given time range."""
  os.chdir(repo_directory)
  output = subprocess.run(["git", "log", f"--author={username}", time_range, "--format=%h", "--branches"], capture_output=True)
  return output.stdout.decode("utf-8").split("\n")

def get_commit_date(repo_directory, commit_hash):
  """Returns the date of the given commit hash in the given repository directory."""
  os.chdir(repo_directory)
  output = subprocess.run(["git", "log", "--format=%cd", "-1", "--date=short", commit_hash], capture_output=True)
  return output.stdout.decode("utf-8").strip()

def get_commit_message(repo_directory, commit_hash):
  """Returns the message of the given commit hash in the given repository directory."""
  os.chdir(repo_directory)
  output = subprocess.run(["git", "log", "--format=%s", "-1", commit_hash], capture_output=True)
  return output.stdout.decode("utf-8").strip()

def create_output_directory(output_directory):
  """Creates the output directory if it does not exist."""
  print(output_directory)
  if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def create_config_file(config_file_path):
  """Creates a config file at the given file path with default values."""
  parent_directory = os.path.dirname(config_file_path)
  if not os.path.exists(parent_directory):
    os.makedirs(parent_directory)
  with open(config_file_path, "w") as config_file:
    config_file.write("OUTPUT_DIRECTORY = working_directory\n")
    config_file.write("OUTPUT_FILE_NAME = commit_messages.txt\n")

def read_config_file(config_file_path):
  """Reads the config file at the given file path and returns a dictionary of the config values."""
  config = {}
  with open(config_file_path, "r") as config_file:
    for line in config_file:
      key, value = line.strip().split(" = ")
      config[key] = value
  return config

def get_random_animal_emoji():
  """Returns a random animal emoji."""
  animal_emojis = [
    "🐶","🐱","🐭","🐹","🐰","🐻","🧸","🐼","🐨","🐯","🦁","🐮","🐷","🐽","🐸","🐵","🙈","🙉","🙊",
    "🐒","🦍","🦧","🐔","🐧","🐦","🐤","🐣","🐥","🐺","🦊","🦝","🐗","🐴","🦓","🦒","🦌","🦘","🦥",
    "🦦","🦫","🦄","🐝","🐛","🦋","🐌","🪲","🐞","🐜","🦗","🪳","🕷","🦂","🦟","🪰","🦖","🪱","🐢",
    "🐍","🦎","🐙","🦑","🦞","🦀","🦐","🦪","🐠","🐟","🐡","🐬","🦈","🦭","🐳","🐋","🐊","🐆","🐅",
    "🐃","🐂","🐄","🦬","🐪","🐫","🦙","🐘","🦏","🦛","🦣","🐐","🐏","🐑","🐎","🐖","🦇","🐓","🦃",
    "🕊","🦅","🦆","🦢","🦉","🦩","🦚","🦜","🦤","🪶","🐕","🦮","🐕","🐩","🐈","🐈","🐇","🐀","🐁",
    "🐿","🦨","🦡","🦔","🐉","🐲","🦕",
  ]
  return random.choice(animal_emojis)

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

  # Check if the config file exists in the user's home directory
  home_directory = os.path.expanduser("~")
  config_file_path = os.path.join(home_directory, ".commitcollector", "config.txt")
  if os.path.exists(config_file_path):
    # Read the config file if it exists
    config = read_config_file(config_file_path)
    output_directory = config["OUTPUT_DIRECTORY"]
    if output_directory == "working_directory":
      output_directory = repo_directory
    else:
      output_directory = os.path.join(home_directory, output_directory)
    output_file_name = config["OUTPUT_FILE_NAME"]
  else:
    # Use default values if the config file does not exist
    create_config_file(config_file_path)
    output_directory = repo_directory
    output_file_name = "commit_messages.txt"

  # Create the output directory if it does not exist
  create_output_directory(output_directory)

  # Get the username of the user
  username = get_username(repo_directory)

  # Group the commit messages by date
  messages_by_date = {}

  # Iterate through the list of repositories
  for repo in tqdm(repo_list, desc=f"{get_random_animal_emoji()}: Collecting commits " ,colour="blue", bar_format='{desc}{bar}'):
    # Change the current working directory to the repository
    repo_path = os.path.join(repo_directory, repo)

    if args.verbose:
      print(repo)

    # Get a list of commit hashes
    commit_hashes = get_commits(repo_path, username, time_range)

    # Iterate through the list of commit hashes
    for commit_hash in commit_hashes:
      if commit_hash:
        # Get the commit message and date
        commit_message = get_commit_message(repo_path, commit_hash)
        if args.jira:
          commit_message = get_jira_ticket_number(commit_message)
        date = get_commit_date(repo_path, commit_hash)

        # Group the commit message by date and repo
        if date not in messages_by_date:
          messages_by_date[date] = {}
        if repo not in messages_by_date[date]:
          messages_by_date[date][repo] = []
        messages_by_date[date][repo].append(commit_message)

  # Write the commit messages to the output file
  output_file_path = os.path.join(output_directory, output_file_name)
  with open(output_file_path, "w") as output_file:
    for date, rest in sorted(messages_by_date.items(), key = lambda x:datetime.strptime(x[0], '%Y-%m-%d'), reverse=True):
      output_file.write(f"📅 {date}\n")
      for service, messages in rest.items():
        output_file.write(f"  📂 {service}\n")
        for message in messages:
          output_file.write(f"    {message}\n")
  print(f"{get_random_animal_emoji()}: Done collecting ")
  print(f"{get_random_animal_emoji()}: Output: {output_file_path}")
  print(f"{get_random_animal_emoji()}  {get_random_animal_emoji()}  {get_random_animal_emoji()}  {get_random_animal_emoji()}  {get_random_animal_emoji()}")
if __name__ == "__main__":
  main()
