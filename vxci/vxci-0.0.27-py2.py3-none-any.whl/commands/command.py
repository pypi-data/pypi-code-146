import gzip
import logging
import click
from os import environ, path
from glob import glob

from vxbase import logger

from vxci import __version__, common
from vxci.checkers import check_all
from vxci.common import check_credentials, prepare, resume_log, notify_orchest, generate_coverage_reports
from vxci.coverage import push_coverage_result
from vxci.image import push_image
import signal
import sys

_logger = logging.getLogger(__name__)

signal.signal(signal.SIGTERM, common.reciveSignal)
signal.signal(signal.SIGINT, common.reciveSignal)


@click.group()
@click.pass_context
@click.option('--log_level', default="INFO",
              help='Set the log level, default to INFO, possible values: INFO, DEBUG, WARNING, ERROR')
@click.option('--log_file', default=None,
              help='File where the los will be stored, default to None')
def cli(ctx, log_level, log_file):
    # ctx.command.config = ctx.parent.command.config
    # parent = ctx.parent.params
    logger.setup_logger("vxci", log_level, log_file)
    _logger.info("VxCi: (ver: %s).", __version__)
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())


@cli.command()
@click.option('--private_deploy_key',
              default=environ.get('PRIVATE_DEPLOY_KEY', False),
              help="Env var: PRIVATE_DEPLOY_KEY.")
@click.option('--ignore_checks',
              default=environ.get('IGNORE_CHECKS', False),
              help="Env var: IGNORE_CHECKS.")
def check_keys(private_deploy_key, ignore_checks):
    """Checks if the .ssh folder exists, creates it and add the private key
    if necessary"""
    _logger.info('Check keys command')
    if not ignore_checks:
        check_all()
    config = prepare(private_deploy_key=private_deploy_key)
    check_credentials(config)


@cli.command()
@click.option('--ci_commit_ref_name', default=environ.get('CI_COMMIT_REF_NAME'),
              help=("The branch or tag name for which project is built."
                    " Env var: CI_COMMIT_REF_NAME."))
@click.option('--ci_pipeline_id', default=environ.get('CI_PIPELINE_ID'),
              help=("The unique id of the current pipeline that GitLab CI"
                    " uses internally. Env var: CI_PIPELINE_ID."))
@click.option('--ci_repository_url', default=environ.get('CI_REPOSITORY_URL'),
              help=("The URL to clone the Git repository."
                    " Env var: CI_REPOSITORY_URL."))
@click.option('--base_image', default=environ.get('BASE_IMAGE'),
              help="Env var: BASE_IMAGE.")
@click.option('--odoo_repo', default=environ.get('ODOO_REPO'),
              help=("Env var: ODOO_REPO."))
@click.option('--odoo_branch', default=environ.get('ODOO_BRANCH'),
              help=("Env var: ODOO_BRANCH."))
@click.option('--version', default=environ.get('VERSION'),
              help=("Env var: VERSION."))
@click.option('--install', default=environ.get('MAIN_APP'),
              help=("Env var: MAIN_APP."))
@click.option('--ci_job_id', default=environ.get('CI_JOB_ID'),
              help=("The unique id of the current job that GitLab CI uses internally."
                    " Env var: CI_JOB_ID."))
@click.option('--psql_image', default=False,
              help=("Override the default postgresql image to use for the tests"
                    "(Notice that this will override the PSQL_VERSION too)"))
@click.option('--image_repo_url', default=environ.get('IMAGE_REPO_URL', "quay.io/vauxoo"),
              help=("The URL where the image repository is located."
                    " Env var: IMAGE_REPO_URL."))
@click.option('--push_image', is_flag=True,
              help="If set it will push the image when on the main branch after the tests")
@click.option('--git_commit_sha', default=environ.get('CI_COMMIT_SHA'),
              help=("'git rev-parse HEAD' of the main repository."
                    "Env var: CI_COMMIT_SHA."))
def build_image(**kwargs):
    config = common.prepare(**kwargs)

    if config.get('push_image'):
        if not config.get('orchest_registry', False) or not config.get('orchest_token', False):
            _logger.error('To push the image you need to set ORCHEST_REGISTRY and ORCHEST_TOKEN env vars')
            sys.exit(1)

    common.clean_containers(config)
    common.pull_images([config['base_image'], ])
    common.run_build_image(config)
    is_latest = False

    if config.get('push_image'):
        # TODO: if we decide to build and push every image, just move the _IMAGE_TAG outside the if
        if not common.is_dev_repo(config):
            tag_latest = 'latest'
            if config.get('docker_image_repo'):
                tag_latest = '%s-%s-latest' % (config['main_app'], config['version'])
            common.push_image(config, config['instance_image'], tag_latest)
            is_latest = True
        common.push_image(config, config['instance_image'], config['image_tag'])
        common.push_image(config, config['instance_image'], config['image_git_tag'])
        common.notify_orchest(config, is_latest=is_latest)
        common.save_imagename(config["ci_commit_ref_slug"], config)
    common.clear_images(config)
    sys.exit(0)


@cli.command()
@click.option('--logpath',
              default=environ.get('CI_COMMIT_REF_SLUG', '.'),
              help="Path where are saved odoo.log_* files. Env var: CI_COMMIT_REF_SLUG.")
def check_log(logpath):
    """Checks odoo log in image to analize if there are warnings
    and show them."""
    _logger.info('Check log command')
    logpaths = glob(path.join(logpath, "odoo.log.gz_*"))

    if not logpaths:
        _logger.warning('Odoo log file was not found in path: %s', logpath)
        exit(2)

    has_warnings = False
    for logpath in logpaths:
        _logger.info("Odoo log path: %s", logpath)
        with gzip.open(logpath, "rb") as flog:
            sucesss, log = resume_log(flog)

        all_warnings = log.get('warnings')
        all_warnings.extend(log.get('warnings_deprecated'))
        all_warnings.extend(log.get('warnings_trans'))
        for warning in all_warnings:
            _logger.warn(warning)
        has_warnings = has_warnings or bool(all_warnings)

    if not has_warnings:
        exit(0)
    exit(1)


@cli.command()
@click.option('--ci_commit_ref_name', default=environ.get('CI_COMMIT_REF_NAME'),
              help=("The branch or tag name for which project is built."
                    " Env var: CI_COMMIT_REF_NAME."))
@click.option('--ci_pipeline_id', default=environ.get('CI_PIPELINE_ID'),
              help=("The unique id of the current pipeline that GitLab CI"
                    " uses internally. Env var: CI_PIPELINE_ID."))
@click.option('--ci_repository_url', default=environ.get('CI_REPOSITORY_URL'),
              help=("The URL to clone the Git repository."
                    " Env var: CI_REPOSITORY_URL."))
@click.option('--base_image', default=environ.get('BASE_IMAGE'),
              help=("Env var: BASE_IMAGE."))
@click.option('--odoo_repo', default=environ.get('ODOO_REPO'),
              help=("Env var: ODOO_REPO."))
@click.option('--odoo_branch', default=environ.get('ODOO_BRANCH'),
              help=("Env var: ODOO_BRANCH."))
@click.option('--version', default=environ.get('VERSION'),
              help=("Env var: VERSION."))
@click.option('--install', default=environ.get('MAIN_APP'),
              help=("Env var: MAIN_APP."))
@click.option('--ci_job_id', default=environ.get('CI_JOB_ID'),
              help=("The unique id of the current job that GitLab CI uses internally."
                    " Env var: CI_JOB_ID."))
@click.option('--psql_image', default=False,
              help=("Override the default postgresql image to use for the tests"
                    "(Notice that this will override the PSQL_VERSION too)"))
@click.option('--image_repo_url', default=environ.get('IMAGE_REPO_URL', "quay.io/vauxoo"),
              help=("The URL where the image repository is located."
                    " Env var: IMAGE_REPO_URL."))
@click.option('--allow_deprecated', is_flag=True,
              help="Don't fail if a deprecated method is found")
def test_image(**kwargs):
    config = common.prepare(**kwargs)

    common.pull_images([config['instance_image'],
                        config['postgres_image']])

    res = common.run_image_tests(config)
    if not res:
        common.clear_images(config)
        sys.exit(1)
    common.clear_images(config)
    sys.exit(0)


@cli.command()
@click.option('--ci_commit_ref_name', default=environ.get('CI_COMMIT_REF_NAME'),
              help=("The branch or tag name for which project is built."
                    " Env var: CI_COMMIT_REF_NAME."))
@click.option('--ci_pipeline_id', default=environ.get('CI_PIPELINE_ID'),
              help=("The unique id of the current pipeline that GitLab CI"
                    " uses internally. Env var: CI_PIPELINE_ID."))
@click.option('--ci_repository_url', default=environ.get('CI_REPOSITORY_URL'),
              help=("The URL to clone the Git repository."
                    " Env var: CI_REPOSITORY_URL."))
@click.option('--base_image', default=environ.get('BASE_IMAGE'),
              help=("Env var: BASE_IMAGE."))
@click.option('--odoo_repo', default=environ.get('ODOO_REPO'),
              help=("Env var: ODOO_REPO."))
@click.option('--odoo_branch', default=environ.get('ODOO_BRANCH'),
              help=("Env var: ODOO_BRANCH."))
@click.option('--version', default=environ.get('VERSION'),
              help=("Env var: VERSION."))
@click.option('--install', default=environ.get('MAIN_APP'),
              help=("Env var: MAIN_APP."))
@click.option('--ci_job_id', default=environ.get('CI_JOB_ID'),
              help=("The unique id of the current job that GitLab CI uses internally."
                    " Env var: CI_JOB_ID."))
@click.option('--psql_image', default=False,
              help=("Override the default postgresql image to use for the tests"
                    "(Notice that this will override the PSQL_VERSION too)"))
@click.option('--image_repo_url', default=environ.get('IMAGE_REPO_URL', "quay.io/vauxoo"),
              help=("The URL where the image repository is located."
                    " Env var: IMAGE_REPO_URL."))
@click.option('--push_image', is_flag=True,
              help="If set it will push the image when on the main branch after the tests")
@click.option('--allow_deprecated', is_flag=True,
              help="Don't fail if a deprecated method is found")
def test_images(**kwargs):
    config = common.prepare(**kwargs)
    if config.get('push_image', False):
        if not config.get('orchest_registry', False) or not config.get('orchest_token', False):
            _logger.error('To push the image you need to set ORCHEST_REGISTRY and ORCHEST_TOKEN env vars')
            sys.exit(1)

    common.pull_images([config['base_image'],
                        config['postgres_image']])

    common.run_build_image(config)

    res = common.run_image_tests(config)
    if not res:
        common.clear_images(config)
        sys.exit(1)
    is_latest = False
    if config.get('push_image', False):
        # TODO: if we decide to build and push every image, just move the _IMAGE_TAG outside the if
        if config['ci_commit_ref_name'] == config['version']:
            common.push_image(config, config['instance_image'], 'latest')
            is_latest = True
        common.push_image(config, config['instance_image'], config['image_tag'])
        common.notify_orchest(config, is_latest=is_latest)
    common.clear_images(config)
    sys.exit(0)


@cli.command()
@click.option('--ci_commit_ref_name', default=environ.get('CI_COMMIT_REF_NAME'),
              help=("The branch or tag name for which project is built."
                    " Env var: CI_COMMIT_REF_NAME."))
@click.option('--ci_pipeline_id', default=environ.get('CI_PIPELINE_ID'),
              help=("The unique id of the current pipeline that GitLab CI"
                    " uses internally. Env var: CI_PIPELINE_ID."))
@click.option('--ci_repository_url', default=environ.get('CI_REPOSITORY_URL'),
              help=("The URL to clone the Git repository."
                    " Env var: CI_REPOSITORY_URL."))
@click.option('--base_image', default=environ.get('BASE_IMAGE'),
              help=("Env var: BASE_IMAGE."))
@click.option('--odoo_repo', default=environ.get('ODOO_REPO'),
              help=("Env var: ODOO_REPO."))
@click.option('--odoo_branch', default=environ.get('ODOO_BRANCH'),
              help=("Env var: ODOO_BRANCH."))
@click.option('--version', default=environ.get('VERSION'),
              help=("Env var: VERSION."))
@click.option('--install', default=environ.get('MAIN_APP'),
              help=("Env var: MAIN_APP."))
@click.option('--ci_job_id', default=environ.get('CI_JOB_ID'),
              help=("The unique id of the current job that GitLab CI uses internally."
                    " Env var: CI_JOB_ID."))
@click.option('--psql_image', default=False,
              help=("Override the default postgresql image to use for the tests"
                    "(Notice that this will override the PSQL_VERSION too)"))
@click.option('--image_repo_url', default=environ.get('IMAGE_REPO_URL', "quay.io/vauxoo"),
              help=("The URL where the image repository is located."
                    " Env var: IMAGE_REPO_URL."))
@click.option('--allow_deprecated', is_flag=True,
              help="Don't fail if a deprecated method is found")
def test_repo(**kwargs):
    config = common.prepare(**kwargs)

    common.pull_images([config['instance_image'],
                        config['postgres_image']])
    res = common.run_image_tests(config, True)
    if not res:
        common.clear_images(config)
        sys.exit(1)
    common.clear_images(config)
    sys.exit(0)


@cli.command()
def push_coverage():
    _logger.warning("Deprecated command ' - vxci push_coverage'. "
                    "Use\n - source variables.sh\n - vxci push_coverage_combine")
    push_status = push_coverage_result()
    exit(not push_status)


@cli.command()
@click.option('--ci_commit_ref_name', default=environ.get('CI_COMMIT_REF_NAME'),
              help=("The branch or tag name for which project is built."
                    " Env var: CI_COMMIT_REF_NAME."))
@click.option('--ci_pipeline_id', default=environ.get('CI_PIPELINE_ID'),
              help=("The unique id of the current pipeline that GitLab CI"
                    " uses internally. Env var: CI_PIPELINE_ID."))
@click.option('--ci_repository_url', default=environ.get('CI_REPOSITORY_URL'),
              help=("The URL to clone the Git repository."
                    " Env var: CI_REPOSITORY_URL."))
@click.option('--base_image', default=environ.get('BASE_IMAGE'),
              help="Env var: BASE_IMAGE.")
@click.option('--odoo_repo', default=environ.get('ODOO_REPO'),
              help=("Env var: ODOO_REPO."))
@click.option('--odoo_branch', default=environ.get('ODOO_BRANCH'),
              help=("Env var: ODOO_BRANCH."))
@click.option('--version', default=environ.get('VERSION'),
              help=("Env var: VERSION."))
@click.option('--install', default=environ.get('MAIN_APP'),
              help=("Env var: MAIN_APP."))
@click.option('--ci_job_id', default=environ.get('CI_JOB_ID'),
              help=("The unique id of the current job that GitLab CI uses internally."
                    " Env var: CI_JOB_ID."))
@click.option('--psql_image', default=False,
              help=("Override the default postgresql image to use for the tests"
                    "(Notice that this will override the PSQL_VERSION too)"))
@click.option('--image_repo_url', default=environ.get('IMAGE_REPO_URL', "quay.io/vauxoo"),
              help=("The URL where the image repository is located."
                    " Env var: IMAGE_REPO_URL."))
@click.option('--push_image', is_flag=True,
              help="If set it will push the image when on the main branch after the tests")
@click.option('--git_commit_sha', default=environ.get('CI_COMMIT_SHA'),
              help=("'git rev-parse HEAD' of the main repository."
                    "Env var: CI_COMMIT_SHA."))
def push_coverage_combine(**kwargs):
    config = common.prepare(**kwargs)
    report_status, msg = generate_coverage_reports(config)

    if report_status:
        green_pattern = "\033[1;32m\033[1;49m%s\033[0m"
        _logger.info(green_pattern, "Coverage succeeded!")
    else:
        red_pattern = "\033[1;31m\033[1;49m%s\033[0m"
        _logger.error(red_pattern, msg)

    push_status = push_coverage_result()
    exit(not (report_status and push_status))


@cli.command()
@click.option('--ci_project_name', default=environ.get('CI_PROJECT_NAME'),
              help=("The project name that is currently being built."
                    " Env var: CI_PROJECT_NAME."))
@click.option('--CI_COMMIT_SHA', default=environ.get('CI_COMMIT_SHA'),
              help=("The commit revision for which project is built."
                    " Env var: CI_COMMIT_SHA."))
@click.option('--CI_COMMIT_REF_NAME', default=environ.get('CI_COMMIT_REF_NAME'),
              help=("The branch or tag name for which project is built."
                    " Env var: CI_COMMIT_REF_NAME."))
@click.option('--CI_REPOSITORY_URL', default=environ.get('CI_REPOSITORY_URL'),
              help=("The URL to clone the Git repository."
                    " Env var: CI_REPOSITORY_URL."))
@click.option('--base_image', default=environ.get('BASE_IMAGE'),
              help=("Env var: BASE_IMAGE."))
@click.option('--odoo_repo', default=environ.get('ODOO_REPO'),
              help=("Env var: ODOO_REPO."))
@click.option('--odoo_branch', default=environ.get('ODOO_BRANCH'),
              help=("Env var: ODOO_BRANCH."))
@click.option('--image_repo_url', default=environ.get('IMAGE_REPO_URL', "quay.io/vauxoo"),
              help=("The URL where the image repository is located."
                    " Env var: IMAGE_REPO_URL."))
@click.option('--orchest_registry', default=environ.get('ORCHEST_REGISTRY'),
              help=("Env var: ORCHEST_REGISTRY."))
@click.option('--orchest_token', default=environ.get('ORCHEST_TOKEN'),
              help=("Env var: ORCHEST_TOKEN."))
def upload_image(**kwargs):
    customer = environ.get('CUSTOMER', environ.get('CI_PROJECT_NAME'))
    version_tag = environ.get('VERSION').replace('.', '')
    image_name = '{customer}_{ver}'.format(
        customer=customer.replace(' ', '').replace(',', '_'),
        ver=version_tag
    )

    environ.update({'_IMAGE_NAME': image_name})
    image_sha = build_image()
    tags = [image_sha]
    is_latest = False
    if environ.get('CI_COMMIT_REF_NAME') == environ.get('VERSION'):
        tags.append('latest')
        is_latest = True
    customer_img = '{customer}{ver}'.format(customer=customer.strip(),
                                            ver=version_tag)
    image_repo = '{url}/{image}'.format(url=environ.get('IMAGE_REPO_URL'),
                                        image=customer_img)
    environ.update({'_IMAGE_REPO': image_repo})
    push_image(tags)
    notify_orchest(image_sha, is_latest=is_latest)
    sys.exit(0)
