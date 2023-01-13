import os
ali_prefix = os.getcwd()
work_dir = os.path.dirname(os.path.realpath(__file__))
dry_run = False
target_rpm_dir = '/tmp/o2_rpms'
skip_deps = False
devel = False
force_build = False
log_level='INFO'
s3_bucket='s3://system-configuration/RPMS/'
release_tag='dev'
architecture='slc8_x86-64'
tag_version=False
