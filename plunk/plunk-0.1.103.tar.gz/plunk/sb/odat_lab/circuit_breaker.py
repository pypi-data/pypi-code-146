from py2store import myconfigs
from plunk.sb.odat_lab.guns import Dacc

# DFLT_CHUNKER = partial(fixed_step_chunker, chk_size=2048)

config_filename = 'circuit_breaker.json'
DFLT_LOCAL_SOURCE_DIR = myconfigs.get_config_value(config_filename, 'local_source_dir')


def mk_dacc(root_dir=DFLT_LOCAL_SOURCE_DIR):
    return Dacc(root_dir=root_dir)


if __name__ == '__main__':
    dacc = mk_dacc()
    # print(list(dacc.wfs.keys()))
    print(next(dacc.chk_tag_gen()))
