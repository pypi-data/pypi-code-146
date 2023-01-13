import sys
import argparse
import configparser
from pathlib import Path
import subprocess as sub
from os import environ as env
from argparse import RawDescriptionHelpFormatter


def get_version():
	try:
		with open(resource_path('VERSION')) as f:
			version = f.read()
	except FileNotFoundError:
		# this should never happen in a built application
		# only if there is no VERSION file while developing locally
		version = 'n/a'
	return version


class SSOSessionError(Exception):
	pass


def resource_path(relative_path):
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = Path(sys._MEIPASS)
	except Exception:
		base_path = Path(__file__).parent.absolute()

	return Path.joinpath(base_path, relative_path)


def load_config():
	aws_config = Path('~/.aws/config').expanduser()
	config = configparser.ConfigParser()
	config.read(aws_config)
	profiles = {}
	for section in config.sections():
		_section = section.split('profile ')[-1]
		profiles[_section] = {}
		for option in config.options(section):
			profiles[_section][option] = config.get(section, option)
	return profiles


def write_profiles(kconfig):
	if kconfig is None:
		return
	profiles_path = resource_path('profiles')
	profiles = kconfig['profiles']
	awsconfig = configparser.ConfigParser(allow_no_value=True)
	for profile in profiles:
		awsconfig.add_section(f'profile {profile}')
		for key, value in profiles[profile].items():
			awsconfig.set(profile, key, value)
	with open(profiles_path, 'w') as f:
		awsconfig.write(f)


def execute(cmd, capture=True):
	print(f"executing command: {cmd}")
	return sub.run(
		cmd,
		shell=True,
		check=True,
		capture_output=capture,
		env=env
	)


def sso_login(profile):
	command = f'aws sso login --profile {profile}'
	execute(command, capture=False)


def update_kubeconfig(cluster_name, alias, profile):
	command = (
		f'aws eks update-kubeconfig '
		f'--name {cluster_name} '
		f'--profile {profile} '
		f'--alias {alias}'
	)
	try:
		p = execute(command)
		print(p.stdout.strip().decode())
	except sub.CalledProcessError as ex:
		msg = ex.stderr.strip().decode()
		handled_errors = (
			'Error loading SSO Token:',
			'The SSO session associated'
		)
		# check if the error message startswith any of the known errors
		if msg.startswith(handled_errors):
			raise SSOSessionError(msg)
		else:
			print(ex.stderr.decode())
			raise ex


def manage_profiles(command):
	print('manage profiles')
	print(f"command: {command}")
	if command is None:
		print('no profile command given - display profiles overview')
		profiles_path = resource_path('profiles')
		print(f"profiles_path: {profiles_path}")
		with open(profiles_path) as f:
			content = f.read()
		print(f'available profiles:')
		print(content)
	if command == 'add':
		print('add a new profile')
	if command == 'list':
		print('display profiles overview')


def login(cluster_name, cluster_alias, profile, sso_region):
	print(f'login to cluster: {cluster_name}')
	try:
		update_kubeconfig(cluster_name, cluster_alias, profile)
	except SSOSessionError:
		sso_login(f'sso-{sso_region}')
		update_kubeconfig(cluster_name, cluster_alias, profile)


def print_section(section, items):
	print(f"[{section}]")
	for key, value in items:
		print(f'{key} = {value}')


def print_config(config):
	for section in config.sections():
		print_section(section, config.items(section))
		print()


def confirm(msg, skip=False):
	if skip:
		return True
	answer = input(msg)
	return answer.lower() in ['y', 'yes']


def bootstrap(dry=False, skip_confirm=False):
	print('bootstrap')
	aws_config_dir = Path('~/.aws/').expanduser()
	aws_config = Path('~/.aws/config').expanduser()
	current_config = configparser.ConfigParser(allow_no_value=True)
	if aws_config.exists():
		current_config.read(aws_config)
	else:
		aws_config_dir.mkdir(parents=True)
		aws_config.touch()
	profiles_path = resource_path('profiles')
	baked_config = configparser.ConfigParser()
	baked_config.read(profiles_path)
	for section in baked_config.sections():
		if current_config.has_section(section):
			print_section(section, baked_config.items(section))
			print()
			print_section(section, current_config.items(section))
			print()
			if confirm(f"Overwrite '{section}' [y/n] ? ", skip=skip_confirm):
				try:
					current_config.add_section(section)
				except configparser.DuplicateSectionError:
					pass
				for key, value in baked_config.items(section):
					current_config.set(section, key, value)
				print(f"section {section} added")
			print()
		else:
			print_section(section, baked_config.items(section))
			print()
			if confirm(f"Add '{section}' [y/n] ? ", skip=skip_confirm):
				try:
					current_config.add_section(section)
				except configparser.DuplicateSectionError:
					pass
				for key, value in baked_config.items(section):
					current_config.set(section, key, value)
				print(f"section {section} added")
			print()
	print('----------------------------------------------------------')
	print_config(current_config)
	print('----------------------------------------------------------')
	if not dry:
		if confirm(f"Write config to {aws_config} [y/n] ? ", skip=skip_confirm):
			with open(str(aws_config), 'w') as f:
				current_config.write(f)
			print(f"config written to {aws_config}")

	print('bootstrap complete')


def print_clusters(config):
	clusters = []
	for name, data in config.items():
		if 'cluster_name' in data:
			clusters.append(name.rsplit('-', 1)[:-1][0])
	for cluster in set(clusters):
		print(cluster)


def print_completion(shell):
	if shell in ['bash', 'zsh']:
		with open(resource_path(f'autocomplete.{shell}')) as f:
			completion = f.read()
		print(completion)
	else:
		print('Unsupported shell')
		sys.exit(1)


def main():
	parser = argparse.ArgumentParser(
		prog = 'klogin',
		description = 'Log in to GenuityScience kubernetes clusters',
		epilog = 'Example usage:\nklogin platform-dev admin',
		formatter_class=RawDescriptionHelpFormatter
	)
	parser.add_argument(
		'-v',
		'--version',
		default=False,
		action='store_true',
		dest='show_version',
		help='Show version'
	)
	cluster = parser.add_argument_group(
		'cluster',
		'''
		Choose a cluster to login to
		Example: klogin platform-dev
		'''
	)
	cluster.add_argument('-r', '--region', nargs='?')
	parser.add_argument("first", nargs='?', help='<cluster-name>/<command>')
	profiles = parser.add_argument_group(
		'profiles',
		'''
		Manage profiles
		Example: klogin profile add
		'''
	)
	profiles.add_argument(
		'-d',
		'--dry',
		nargs='?',
		default=False,
		help='Dry run initialization'
	)
	profiles.add_argument(
		'-y',
		'--yes',
		default=False,
		dest='skip_confirm',
		action='store_true',
		help='Skip confirmation and add/overwrite all profiles on init'
	)
	parser.add_argument("second", nargs='?', help='<role>/<command>')
	args = parser.parse_args()
	# if no arguments are provided we exit and show the help message
	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)
	if args.show_version:
		print(f'version: {get_version()}')
		sys.exit(0)
	if args.first in ['complete']:
		print_completion(args.second)
		sys.exit(0)
	if args.first in ['init']:
		bootstrap(args.dry, args.skip_confirm)
		sys.exit(0)
	config = load_config()
	if args.first in ['clusters']:
		print_clusters(config)
		sys.exit(0)
	if args.first in ['profile', 'profiles']:
		manage_profiles(args.second)
		sys.exit(0)
	else:
		cluster_alias = args.first
		role = args.second or 'ro'
		# construct the profile name, <cluster_alias>-<rolename>
		# for cluster platform-dev and role admin: platform-dev-admin 
		# for cluster gor-dev and role ro: gor-dev-ro
		profile = f'{cluster_alias}-{role}'
		cluster_name = config[profile]['cluster_name']
		sso_region = config[profile]['sso_region']
		login(cluster_name, cluster_alias, profile, sso_region)


if __name__ == '__main__':
	main()
