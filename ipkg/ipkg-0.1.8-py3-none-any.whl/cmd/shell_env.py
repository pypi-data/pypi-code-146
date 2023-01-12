import click
from rich import print
from rich.syntax import Syntax

SHELL_ENV = """
# export IPKG_CACHE_DIR="${HOME}/.cache/ipkg"

function ipkg() {
  local sha1="$(sha1sum <<< "${*}" | awk '{ print $1 }')"
  local cache_path="${IPKG_CACHE_DIR:-"${HOME}/.cache/ipkg"}/${sha1}"
  if [[ -f ${cache_path} ]]; then
    local cache_hit=true
  fi
  if [[ ${cache_hit:-"false"} != "true" ]]; then
    command ipkg "${@}"
  fi
  if [[ -f ${cache_path} ]]; then
    source "${cache_path}"
  fi
}
"""
SHELL_ENV = SHELL_ENV.strip()


@click.command(name="shell-env")
def cmd_shell_env() -> None:
    print(Syntax(code=SHELL_ENV, lexer="shell"))
