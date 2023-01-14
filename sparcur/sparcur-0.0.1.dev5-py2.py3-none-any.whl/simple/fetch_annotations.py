#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::fetch_annotations.py][fetch_annotations.py]]
from pathlib import Path
from hyputils import hypothesis as hyp
from sparcur.config import auth


def from_group_name_fetch_annotations(group_name):
    """ pull hypothesis annotations from remote to local """
    group_id = auth.user_config.secrets('hypothesis', 'group', group_name)
    cache_file = Path(hyp.group_to_memfile(group_id + 'sparcur'))
    get_annos = hyp.Memoizer(cache_file, group=group_id)
    get_annos.api_token = auth.get('hypothesis-api-key')  # FIXME ?
    annos = get_annos()
    return cache_file  # needed for next phase, annos are not


def from_group_name_cached_annos(group_name):
    group_id = auth.user_config.secrets('hypothesis', 'group', group_name)
    cache_file = Path(hyp.group_to_memfile(group_id + 'sparcur'))
    get_annos = hyp.AnnoReader(cache_file, group=group_id)
    annos = get_annos()
    return annos


def from_user_name_group_name_h(user_name, group_name):
    group_id = auth.user_config.secrets('hypothesis', 'group', group_name)
    h = hyp.HypothesisUtils(username=user_name, group=group_id)
    h.token = auth.user_config.secrets('hypothesis', 'api', user_name)
    return h


def main(hypothesis_group_name=None, **kwargs):
    if hypothesis_group_name is None:
        hypothesis_group_name = 'sparc-curation'

    from_group_name_fetch_annotations(hypothesis_group_name)


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main)
# fetch_annotations.py ends here
