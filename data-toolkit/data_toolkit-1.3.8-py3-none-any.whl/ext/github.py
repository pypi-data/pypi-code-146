# pip install github3.py
import github3
import pandas as pd
import sys, os
import subprocess as sp
import json

def init():
    git_config = sp.run(["git","config","-l"], capture_output=True).stdout
    split_config = git_config.decode().split("\n")
    git_dict = {s[0]:s[1] for s in [ s.split('=') for s in split_config[:-11] ]}

    gh_username = git_dict['user.email']
    gh_password = git_dict['user.token']

    return gh_username, gh_password

def find_forks(repo_url: str):
    gh_username, gh_password = init()

    user, repo = repo_url.split('/')[-2:]

    g = github3.login(gh_username, gh_password)
    r = g.repository(user, repo)
    total_list = list(r.forks(sort='commits', number=r.fork_count))
    data = [ (i,i.updated_at,
            i.pushed_at, i.updated_at == i.created_at) for i in total_list ]
    df = pd.DataFrame(data,columns=['name','updated_at','pushed_at','ever_changed'])

    df = df.sort_values('ever_changed')
    print(df.ever_changed.value_counts())
    return df

def fork_status(repo_url: str):
    cmd = 'for branch in `git branch -r | grep -v HEAD`;do echo -e `git show --format="%ci %cr" $branch | head -n 1` \\t$branch; done | sort -r\n'
    os.system(cmd)

def find_contributors(repo_url: str):
    from .sshconf import SshConfig
    # gh_username, gh_password = init()

    user, repo = repo_url.split('/')[-2:]
    f = open('/Users/jakub/.gitconfig').read().splitlines()
    c = SshConfig(f)

    g = github3.login(gh_username, gh_password)
    r = g.repository(user, repo) 

def dir_diff(cwd: str, action = 'status') -> json:
    # get all dirs in cwd
    output = []
    all_directories = os.listdir(cwd)

    # check that all are directories
    dirs_only = [ d for d in all_directories if len(d.split('.'))==1 and d!='swap2' ]

    for dir in dirs_only:
        cwd = os.path.abspath(dir)
        try:
            git_stash = sp.run(["git",action], cwd=cwd, capture_output=True)
        except NotADirectoryError:
            print('Not a directory:', cwd)
        output.append([cwd, git_stash.stdout.decode()])

    diff_df = pd.DataFrame(output, columns=['dir',action])
    if action == 'status':
        # remove if up to master
        diff_df = diff_df[~diff_df.status.str.contains('On branch master')]
        
        # remove if main
        diff_df = diff_df[~diff_df.status.str.contains('On branch main')]
        
        # drop rows with empty ('') status
        diff_df = diff_df[diff_df.status != '']
        
        # create column up to date with True/False
        diff_df['up_to_date'] = diff_df.status.str.contains('up to date')
        diff_df = diff_df.sort_values(by='up_to_date')
        diff_df.reset_index(inplace=True)
        
        return diff_df
        
    else:
        non_empty_diffs = diff_df.loc[diff_df['diff'].str.len() > 0]
        dict_diffs = non_empty_diffs.to_dict(orient='index')

        # map 'dir' value to key in dict_diffs
        dict_diffs = {v['dir']:v['diff'] for k,v in dict_diffs.items()}

    return dict_diffs

def see_if_merged(repo_url: str):
    # see if branches have been merged to master
    cmd = 'git branch -r --merged master'
    output = sp.run([cmd], cwd=repo_url, shell=True, capture_output=True).stdout.decode().splitlines()
    branches = [ o.split('\t') for o in output ]
    df = pd.DataFrame(branches, columns=['branch'])
    df['branch'] = df['branch'].str.replace('origin/','').str.strip()
    
    df['merged'] = True
    
    return df

def find_branches(cwd: str, remote: bool, remove: bool) -> pd.DataFrame:
    # get branches in this git repo and their last commit
    if remote: cmd = 'for branch in `git branch -r | grep -v HEAD`;do echo -e `git show --format="%ci %cr" $branch | head -n 1` \\t$branch; done | sort -r\n'
    else: cmd = 'for branch in `git branch | grep -v HEAD`;do echo -e `git show --format="%ci %cr" $branch | head -n 1` \\t$branch; done | sort -r\n'
    output = sp.run([cmd], cwd=cwd, shell=True, capture_output=True).stdout.decode().splitlines()
    branches = [ o.split('\t') for o in output ]
    df = pd.DataFrame(branches, columns=['to_parse'])
    # split line '-e 2022-11-14 22:58:45 +0000 5 days ago torigin/f/file_cai'
    # to datetime and branch name
    
    df[['e','year','month','day_time','branch']] = df.to_parse.str.split('[+|-]', expand=True)
    # split day_time to day and time
    df[['day','time','None']] = df.day_time.str.split(' ', expand=True)
     
    # remove 'e' column
    df.drop('e', axis=1, inplace=True)
    df.drop('None', axis=1, inplace=True)

    # remove 'e' from the start of year column
    df['year'] = df.year.str[2:]
    
    # remove 'torigin/' from branch name
    if remote: df['branch'] = df.branch.str.replace('torigin/','').str[4:]
    else: df['branch'] = df.branch.str.replace('tf/','f/')
    df['timedelta'] = df.branch.str.split(' ').str[:-1].str.join(' ')
    df['branch'] = df.branch.str.split(' ').str[-1]
    
    # convert to datetime
    df['datetime'] = pd.to_datetime(df['year'] + ' ' + df['month'] + ' ' + df['day'] + ' ' + df['time'])
    
    # remove redundant columns
    df = df[['branch','datetime','timedelta']]
    
    merged_df = see_if_merged(cwd)
    df = df.merge(merged_df, on='branch', how='left')
    
    # drop None in branch column
    df = df[df['branch'].notna()]
    
    # sort by datetime
    df = df.sort_values(by='datetime', ascending=False)
    
    # if remove is True, remove branches that have been merged to master
    if remove=="True": df = df[df['merged'] != True]
    
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)
    
    return df