def install_chrome_commands(chrome_version=None):
    """Get a list of commands to install chrome based on "chrome_version"
    It could be
        - "current": Latest version from google page (by default if it is not defined)
        - "OS": Deprecated but for now installing the latest version
        - "{Empty}": It will use latest
        - "{version}": It will install this pinned version
    Require to run "apt update" before to run these commands
    Note, you can use this method directly calling:
        python -c "import tools_test;print('\n'.join(tools_test.install_chrome_commands()))"
    """
    if not chrome_version or chrome_version == "OS":
        chrome_version = "current"
    chrome_filename = "google-chrome-stable_%s_amd64.deb" % chrome_version
    chrome_url = (
        "https://dl.google.com/linux/direct/%s" % chrome_filename
        if chrome_version == "current"
        else "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/%s" % chrome_filename
    )
    cmds = [
        "wget %s -O /tmp/chrome.deb" % chrome_url,
        # Get dependencies
        "dpkg -i /tmp/chrome.deb",
        # Install those dependencies
        "apt install -f",
        # Second time with dependencies already installed
        "dpkg -i /tmp/chrome.deb",
        "rm /tmp/chrome.deb",
    ]
    return cmds
