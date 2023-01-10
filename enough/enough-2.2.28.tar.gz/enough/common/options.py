import os
import yaml
from enough import settings


def set_options(parser):
    i = f'{settings.CONFIG_DIR}/inventory/group_vars/all/infrastructure.yml'
    driver = 'openstack'
    if os.path.exists(i):
        driver = yaml.safe_load(open(i).read()).get('infrastructure_driver', 'openstack')

    parser.add_argument('--driver',
                        default=driver,
                        choices=['libvirt', 'openstack'])
    parser.add_argument('--inventory', action='append')
    o = parser.add_argument_group(title='OpenStack',
                                  description='Only when --driver=openstack')
    o.add_argument(
        '--cloud',
        default='production',
        help='Name of the cloud in which resources are provisionned')
    parser.openstack_group = o
    return parser
