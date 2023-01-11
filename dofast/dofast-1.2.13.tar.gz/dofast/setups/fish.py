import os

import codefast as cf

code = cf.shell('which code').strip()
open_ = cf.shell('which open').strip()
dirs_ = ['/home/x03/Dropbox', '/data/Dropbox']
DROPBOX_DIR = next((d for d in dirs_ if os.path.exists(d)), None)

fish_content = f"""
alias ll='ls -ltr'
alias la='ls -A'
alias l='ls -CF'
alias la='ls -A'
alias l='ls -CF'
alias st='time python3 /Users/alpha/bitwork/scripts/st.py'
alias em='emacs -nw'
alias dwa='aria2c --allow-overwrite=true --file-allocation=none -c -x16 -s32'
alias proxydwa='proxychains4 -q aria2c --allow-overwrite=true --file-allocation=none -c -x16 -s32'
alias mip='curl ipinfo.io'
alias i='curl ali.140714.xyz:5000/api/v1.0/ip'
alias webip='open http://ali.140714.xyz:5000/api/v1.0/ip'
alias pcurl='curl --proxy 117.ccccat.xyz:51170 '
alias rb='time ruby'
alias r='time ruby'
alias pl='time perl'
alias ppy='time proxychains4 -q /usr/local/bin/python3.7'
# alias pi='autopep8 --in-place --aggressive --aggressive'
alias pi='/data/db32/anaconda3/envs/dl2/bin/yapf --in-place '
alias p3='time python3'
alias c='cd'
alias cls="ls |perl -nE 'print if /\~|pye|rse/'|xargs rm"
alias typora="open -a typora"
alias oldsubl="/Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl"
alias p9='ping -c9 -W500 -i 0.2'
alias dw='cd ~/Downloads/'
alias tp='cd /data/Dropbox/tmp'
alias des='cd ~/Desktop/'
alias profile='/usr/bin/vim ~/.bashrc'
alias vidia='nvidia-smi'
alias vi='nvidia-smi'
alias work='cd /data/Dropbox/work/mgvgit/'
alias glab='cd ~/Dropbox/work/glab/2022'
alias serving='cd /data/Dropbox/work/serving/app/ || cd ~/Dropbox/work/serving/app/'
alias pj='cd /data/Dropbox/projects/'
alias pbcopy='xclip -selection clipboard'
alias pbpaste='xclip -selection clipboard -o'
alias xecho="echo ❌"
alias xxecho="echo ✔️"
alias flushbash='source ~/.bashrc'
alias pg='/usr/bin/proxychains4 -q /usr/bin/git'
alias gitlog='git log --graph --pretty=oneline --abbrev-commit'
alias pqgit='/usr/bin/proxychains4 git'
alias gl='git log --graph --pretty=oneline --abbrev-commit'
alias gb='git branch'
alias gd='git diff'
alias pytest='/data/db32/anaconda3/envs/dl2/bin/pytest'
alias round='python3 /data/Dropbox/work/scripts/rounded_corners.py'
alias open='{open_}'
alias gss='/usr/bin/gnome-screenshot'
alias gst='git status'
alias 39='ssh developer@39.100.200.248'
alias ai1='ssh -o ServerAliveInterval=60 liugaoang@47.92.192.123'
alias bastion='ssh liugaoang@omuxivirew-public.bastionhost.aliyuncs.com -p60022'
alias syncai1='rsync -vPrz liugaoang@47.92.192.123:/home/liugaoang/logs .'
alias 121='ssh -o ServerAliveInterval=60 developer@121.89.213.248'
alias test121='ssh -o ServerAliveInterval=60 deploy@121.89.217.31'
alias pq='/usr/bin/proxychains4 -q'
alias pipupdate='pip install dofast --upgrade; pip install codefast --upgrade'
alias mac='bash /data/Dropbox/work/scripts/sshmac.sh'
alias www='cd /var/www/html/'
alias cppfmt='clang-format-3.9'
alias lock='gnome-screensaver-command -l'
alias psoxi='/data/db32/anaconda3/envs/dl2/bin/psox -i'
alias wiki='xdg-open https://wiki.mgvai.cn/pages/viewpage.action?pageId=2397292'
alias json='google-chrome chrome-extension://pkgccpejnmalmdinmhkkfafefagiiiad/json-format/index.html'
alias jirui='google-chrome https://jirui.dev.mgvai.cn/api/conversation/detail/detail/sentences?conversation_id=1006'
alias megaview='google-chrome https://app.megaview.com/api/conversation/detail/detail/sentences?conversation_id=540'
alias pag='ps aux|grep '
alias ducks='du -cksh * | sort -hr '
alias pycharm='/snap/bin/pycharm-community'
alias bm='sli -bm '
alias editdofast='subl /data/db32/anaconda3/envs/dl2/lib/python3.8/site-packages/dofast/sli_entry.py'
alias ds='dropbox status'
alias lst='ls -lhtr'
alias lsth='ls -lhtr | tail'
alias ali='ssh -o ServerAliveInterval=60 root@47.105.143.5 -p7058'
alias tencent1='ssh -o ServerAliveInterval=60 deploy@49.232.103.120'
alias tencent2='ssh -o ServerAliveInterval=60 deploy@152.136.235.137'
alias les='less'
alias nsqs='watch -n0.5 "curl localhost:4151/stats"'
alias mdkir='mkdir'
alias gg="google-chrome https://www.google.com.hk"
alias flatten="xargs echo | tr ' ' ,"
alias pne="perl -nE"
alias brdiff='git diff --stat --color' # git branch diff
alias rust='rustfmt src/main.rs; cargo run'
alias iplc='ssh -o ServerAliveInterval=60 root@iplc-jp2.cloudiplc.com -p45621'
alias india='ssh ubuntu@india.ddot.fun -p7058'
alias lab='ssh -o ServerAliveInterval=60 gaoang@localhost -p 8888'
alias log='subl /data/Dropbox/work/mgvgit/monthly.md'
alias movie='open "http://www.dydhhy.com/tag/2022/"'
alias 225='ssh -o ServerAliveInterval=60 megaview@192.168.1.225'
alias tl='python3 {DROPBOX_DIR}/work/scripts/timeline.py'
alias subl='{code}'
alias p='python3'

# work
alias 4090='ssh ls@192.168.1.163'
alias asr='ssh deploy@121.89.207.49'
"""


def setup_fish():
    config_file = "~/.config/fish/config.fish"
    config_file = os.path.expanduser(config_file)
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            content = f.read()
        if content == fish_content:
            return
    with open(config_file, "w") as f:
        f.write(fish_content)
