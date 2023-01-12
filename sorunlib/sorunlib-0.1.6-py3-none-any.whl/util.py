import os

from ocs import site_config
from ocs.ocs_client import OCSClient


def _load_site_config(filename=None):
    """Load a site config file, searching for default.yaml in OCS_CONFIG DIR by
    default.

    Args:
        filename (str): Path to OCS site config file

    Returns:
        ocs.site_config.SiteConfig object

    """
    if filename is None:
        assert (os.getenv('OCS_CONFIG_DIR') is not None)
        site = 'default'
        filename = os.path.join(os.getenv('OCS_CONFIG_DIR'),
                                site + '.yaml')
    cfg = site_config.SiteConfig.from_yaml(filename)

    return cfg


def _find_instances(agent_class, host=None, config=None):
    """Find all instances of an Agent Class in a config.

    Args:
        agent_class (str): Agent Class name to search for, must match Agent
            Class defined by an OCS Agent (and thus also defined in the SCF.)
        host (str): Specific host to search on, if None all hosts will be
            searched.
        config (str): Path to the OCS Site Config File. If None the default
            file in OCS_CONFIG_DIR will be used.

    Returns:
        list: List of instance-id's matching the given agent_class.

    """
    cfg = _load_site_config(config)

    if host is not None:
        hosts = {host: cfg.hosts[host]}
    else:
        hosts = cfg.hosts

    instances = []
    for _host, hostcfg in hosts.items():
        for entry in hostcfg.instances:
            if entry['agent-class'] == agent_class:
                instances.append(entry['instance-id'])

    return instances


def _find_active_instances(agent_class, config=None):
    """Find all instances of an Agent Class currently online, based on the
    Agents known by the registry.

    Args:
        agent_class (str): Agent Class name to search for, must match Agent
            Class defined by an OCS Agent (and thus also defined in the SCF.)
        config (str): Path to the OCS Site Config File. If None the default
            file in OCS_CONFIG_DIR will be used.

    Returns:
        list: List of instance-id's matching the given agent_class.

    """
    cfg = _load_site_config(config)

    reg_client = OCSClient(cfg.hub.data['registry_address'])
    _, _, session = reg_client.main.status()

    instances = []
    for entry in session['data'].values():
        if entry['agent_class'] == agent_class:
            instance_id = entry['agent_address'].split('.')[-1]
            instances.append(instance_id)

    return instances


def create_clients(config=None, test_mode=False):
    """Create all clients needed for commanding a single platform.

    Args:
        config (str): Path to the OCS Site Config File. If None the default
            file in OCS_CONFIG_DIR will be used.
        test_mode (bool): Operate in 'test mode'. Use this to find Agents that
            are meant to stand in for real agents while testing, i.e.
            SmurfFileEmulators instead of PysmurfControllers.

    Returns:
        dict: Dictionary with the ACU and SMuRF clients needed for commanding
        in the format::

            clients = {'acu': acu_client,
                       'smurf': [smurf_client1, smurf_client2, smurf_client3]}

    """
    clients = {}

    if test_mode:
        smurf_agent_class = 'SmurfFileEmulator'
    else:
        smurf_agent_class = 'PysmurfController'

    acu_id = _find_active_instances('ACUAgent', config=config)
    smurf_ids = _find_active_instances(smurf_agent_class, config=config)

    if acu_id:
        acu_client = OCSClient(acu_id[0])
        clients['acu'] = acu_client
    if smurf_ids:
        smurf_clients = [OCSClient(x) for x in smurf_ids]
        clients['smurf'] = smurf_clients

    return clients
