# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""Analytics coverage APIs."""
import csv
import os
import shutil
import uuid
import json
import subprocess

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from yangsuite import get_logger, get_path
from ysdevices.devprofile import YSDeviceProfile
from ysfilemanager import split_user_set, YSYangSet
from yscoverage.coverage import (
    YangCoverage,
    YangCoverageInProgress,
    YangCoverageException
)
from yscoverage.dataset import dataset_for_yangset
from yscoverage.yangdiff import getdiff
from yscoverage.get2edit import GetToEdit
from yscoverage.mibyang import MIBYANGpath
from yscoverage.mappings import (
    MibYangWriter,
    process_import_data,
    show_mapping_data,
    MappingException
)


log = get_logger(__name__)


if not os.path.isfile(os.path.join(get_path('mibs_dir'), 'SNMPv2-MIB.my')):
    mib_path = get_path('mibs_dir')
    if os.path.isdir(mib_path):
        os.rmdir(mib_path)
    if os.path.isdir(os.path.join(os.path.dirname(__file__), 'mibs')):
        shutil.copytree(
            os.path.join(os.path.dirname(__file__), 'mibs'),
            mib_path
        )
    else:
        log.error('Cannot find MIB files')


@login_required
def render_main_page(request):
    """Return the main coverage.html page."""
    devices = YSDeviceProfile.list(require_feature="ssh")

    return render(request,
                  'yscoverage/coverage.html',
                  {'devices': devices})


@login_required
def getconfig(request):
    """Get running configuration from device."""
    device = request.POST.get('device')

    if not device:
        return JsonResponse({}, status=404, reason='No device')

    dev_profile = YSDeviceProfile.get(device)

    try:
        cfg = YangCoverage.get_config(dev_profile)
    except YangCoverageException as e:
        return JsonResponse({}, status=404, reason=str(e))

    return JsonResponse({'config': cfg})


def getreleases(request):
    """Get releases to choose from for model coverage."""
    if request.method == 'POST':
        ios = request.POST.get('ios')
        uri = request.POST.get(
            'uri',
            "http://yang-suite.cisco.com:8480/coverage/getreleases")

        if not ios:
            return JsonResponse({}, status=404, reason='No platform specified')

        releases = YangCoverage.get_releases(ios)

        if 'releases' in releases and not len(releases['releases']):
            # Try base server
            releases = YangCoverage.get_base_releases(uri + '?ios=' + ios)
            JsonResponse(releases)

        return JsonResponse(releases)
    else:
        ios = request.GET.get('ios', 'xe')

        releases = YangCoverage.get_releases(ios)

        return JsonResponse(releases)


@login_required
def getcoverage(request):
    """Get model coverage."""
    if request.method == 'POST':

        port = request.POST.get('port', '')
        cli = request.POST.get('cli')
        uri = request.POST.get('uri')
        timeout = request.POST.get('timeout', 120)
        convert_to_edit = request.POST.get('convert', 'true')
        edit_target = request.POST.get('target', 'running')
        coverage = ''
        xml = ''

        if not cli:
            return JsonResponse({}, status=404, reason='No config to test')

        while timeout:
            try:
                coverage, xml = YangCoverage.get_coverage(cli,
                                                          port,
                                                          uri)
                if convert_to_edit == 'true':
                    ge = GetToEdit(xml)
                    xml = ge.edit_config(edit_target)
                timeout = 0
            except YangCoverageInProgress:
                timeout -= 1
            except Exception as e:
                return JsonResponse({}, status=404, reason=str(e))

        result = {'coverage': coverage,
                  'xml': xml,
                  'average': YangCoverage.average_lines_per_second}

        return JsonResponse(result)

    else:

        return JsonResponse(YangCoverage.get_progress())


@login_required
def render_datasets_page(request):
    """Return the datasets.html page."""
    return render(request,
                  'yscoverage/dataset.html')


@login_required
def get_dataset(request):
    """Get XPath dataset for a given module and yangset."""
    model = request.POST.get('model') or request.GET.get('model')
    yangset = request.POST.get('yangset') or request.GET.get('yangset')
    addons = (request.POST.getlist('addons[]') or
              request.GET.getlist('addons[]'))
    fmt = request.POST.get('format') or request.GET.get('format')
    all_data = request.POST.get('all_data') or request.GET.get('all_data')
    if all_data == 'true':
        all_data = True
    else:
        all_data = False

    if not model:
        return JsonResponse({}, status=400, reason='No model specified.')
    if not yangset:
        return JsonResponse({}, status=400, reason='No yangset specified.')
    if not fmt:
        fmt = 'json'

    owner, setname = split_user_set(yangset)
    data = dataset_for_yangset(owner, setname, model, addons,
                               reference=request.user.username,
                               all_data=all_data)

    if fmt == 'json':
        return JsonResponse(data)
    elif fmt == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % model

        writer = csv.writer(response)
        # Add header row
        writer.writerow(data['header'])
        # Write data
        for row in data['data']:
            writer.writerow(row)
        return response
    else:
        return JsonResponse({}, status=400, reason='Unrecognized "format"')


@login_required
def get_diff(request):
    """Get diffs from two versions of a model."""
    model = request.POST.get('model') or request.GET.get('model')
    from_set = request.POST.get('fromset') or request.GET.get('fromset')
    to_set = request.POST.get('toset') or request.GET.get('toset')
    addons = (request.POST.getlist('addons[]') or
              request.GET.getlist('addons[]'))
    fmt = request.POST.get('format') or request.GET.get('format')

    if not model:
        return JsonResponse({}, status=400, reason='No model specified.')
    if not from_set:
        return JsonResponse({}, status=400, reason='No "from" yangset given.')
    if not to_set:
        return JsonResponse({}, status=400, reason='No "to" yangset given.')
    if not fmt:
        fmt = 'json'

    addons.append("nodetype")
    try:
        from_dataset = dataset_for_yangset(*split_user_set(from_set),
                                           model,
                                           addons,
                                           reference=request.user.username)
        to_dataset = dataset_for_yangset(*split_user_set(to_set),
                                         model,
                                         addons,
                                         reference=request.user.username)
    except Exception as e:
        log.error(f'Error loading the module: {e}')
        return JsonResponse({
            'message': f'Error loading the module: {e}'
        }, status=400, reason=e.msg)

    data = getdiff(from_dataset,
                   to_dataset)

    if fmt == 'json':
        return JsonResponse(data)
    elif fmt == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=diff.csv'

        writer = csv.writer(response)
        writer.writerow(data['header'])
        for row in data['data']:
            writer.writerow(row)
        return response
    else:
        return JsonResponse({}, status=400, reason='Unrecognized "format"')


@login_required
def yang_snmp(request):
    devices = YSDeviceProfile.list(require_feature="netconf")

    return render(
        request,
        'yscoverage/yangsnmp.html',
        {'devices': devices}
    )


@login_required
def get_devices(request):
    devices = YSDeviceProfile.list(require_feature="netconf")
    return JsonResponse({'devices': devices})


@login_required
def get_yang_modules(request):
    owner = request.GET.get('owner')
    set_name = request.GET.get('setname')

    if set_name is not None:
        yang_set = YSYangSet.load(owner, set_name)
        modules = yang_set._modules
        return JsonResponse({'yangModules': modules})
    elif set_name is None:
        msg = 'Set name cannot be empty'
        return JsonResponse({}, status=500, reason=msg)


def _create_ui_list(mib_yang_path, oids_to_xpaths):
    """Convert dict to UI format with random IDs."""
    yang_paths = []
    mib_paths = []
    mib_path_to_yang_path = {}
    mib_path_options = {}

    # Create list of readable MIB paths, each list item has path and ID
    for oid, xpaths in oids_to_xpaths.items():
        mib_path = {
            # OID to identify Mapping in DB
            'oid': oid,
            # MIB path
            'value': oid,
            # Random ID to help frontend rendering
            'id': uuid.uuid4().__str__()
        }

        mib_paths.append(mib_path)

        if xpaths:
            # Possible Xpath matches.
            xp_objs = []
            for xpath in xpaths:
                xp_objs.append({
                    'label': xpath,
                    'value': xpath,
                    'model': mib_yang_path.yobj.model,
                    'id': uuid.uuid4().__str__()
                })
            mib_path_options[oid] = xp_objs
            mib_path_to_yang_path[oid] = xp_objs[0]['value']
        else:
            mib_path_to_yang_path[oid] = ''

    # Create list of YANG XPaths, each list item has YANG XPath and ID
    oids_to_xpaths_values = oids_to_xpaths.values()
    for xpath in mib_yang_path.yobj.xpaths:
        for xpaths in oids_to_xpaths_values:
            if xpath in xpaths:
                break
        else:
            yang_paths.append({
                # XPath
                'value': xpath,
                'label': xpath,
                'model': mib_yang_path.yobj.model,
                # Random ID to help frontend rendering
                'id': uuid.uuid4().__str__()
            })
    return (yang_paths, mib_paths, mib_path_to_yang_path, mib_path_options)


@login_required
def match_oids_to_xpaths(request):
    """Try to match list of OIDs to list of Xpaths."""
    user_obj = request.user
    user = user_obj.username
    yang_module = request.GET.get('yangmodule')
    yang_set = request.GET.get('setname')
    device_name = request.GET.get('device')
    force_walk = request.GET.get('forcewalk')
    community = request.GET.get('community', '')
    v3pwd = request.GET.get('v3password', '')
    map_filename = request.GET.get('mapfile', '')
    starting_oids = request.GET.get('oids', '')

    if not device_name:
        return JsonResponse(
            {},
            status=400,
            reason="Must select a device."
        )
    if not community and not v3pwd:
        return JsonResponse(
            {},
            status=400,
            reason="Please input community string or SNMPv3 password."
        )

    device_profile = YSDeviceProfile.get(device_name)
    if not hasattr(device_profile, 'netconf'):
        # Device must support NETCONF
        return JsonResponse(
            {},
            status=500,
            reason='Device is not configured for NETCONF'
        )
    if community:
        # SNMP community string used
        device_profile.base.username = community
        device_profile.base.password = ''
    elif v3pwd:
        # SNMPv3 password used
        device_profile.base.password = v3pwd
    else:
        return JsonResponse(
            {},
            status=403,
            reason='Need SNMPv3 password or community string.'
        )

    try:
        # Dynamically map OIDs to XPaths using device's values
        mib_yang_path = MIBYANGpath.get(
            yang_module,
            user,
            device_profile,
            yangset=yang_set,
            map_filename=map_filename,
            starting_oids=starting_oids
        )
        if force_walk.lower() == 'true':
            # remove all SNMP walk data to force a new SNMP walk
            mib_yang_path.force_walk(yang_module, user)

        oids_to_xpaths = mib_yang_path.get_device_oids_to_xpaths_map()

        xpaths, mib_paths, mib_path_to_xpath, mib_options = _create_ui_list(
            mib_yang_path, oids_to_xpaths
        )
        return JsonResponse({
            'yangPaths': xpaths,
            'mibPaths': mib_paths,
            'mibPathToYangPath': {
                **mib_path_to_xpath
            },
            'matchedYangPathOptions': mib_options,
            'modelsToYangPath': mib_yang_path.modules_to_matched_xpaths
        })
    except Exception as exc:
        return JsonResponse(
            {'message': str(exc)},
            status=500,
            reason=str(exc)
        )


@login_required
def save_mapping(request):
    """Save OIDs and Xpaths in XLSX spreadsheet."""
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'yangPath' not in body:
        return JsonResponse(
            {'message': 'No Xpath found.'},
            status=400,
            reason='No Xpath found.'
        )

    oid = body['oid']
    yang_path = body['yangPath']
    yang_module = body['yangModule']
    yang_paths = body['yangPaths']
    mib_paths = body['mibPaths']
    mib_to_yang_paths = body['mibToYangPaths']
    mapfile = body['mapFile']
    if 'modelsToYangPath' in body:
        model_to_xpath = body['modelsToYangPath']
    else:
        model_to_xpath = {}

    try:
        if not mapfile:
            if not yang_module:
                return JsonResponse(
                    {'message': 'Choose model (needed to "Save" mapping).'},
                    status=400,
                    reason='Choose model (needed to "Save" mapping).'
                )
            mypath = MIBYANGpath.get(
                yang_module,
                request.user.username
            )
            if not mypath:
                return JsonResponse(
                    {'message': 'Execute "Match OIDs to Xpaths" again.'},
                    status=500,
                    reason='"Match OIDs to Xpaths" must be executed again.'
                )
            mapfile = os.path.basename(
                mypath.walk_file
            ).replace('.walk', '.csv')
        map_file = os.path.join(
            get_path('mibyang_mappings_dir', user=request.user.username),
            mapfile
        )
        myw = MibYangWriter.get(
            map_file,
            request.user.username,
            mib_paths,
            yang_paths,
            model_to_xpath,
            yang_module,
        )
        myw.save_mapping_in_csv(oid, yang_path, mib_to_yang_paths)

    except Exception as e:
        log.error(str(e))
        return JsonResponse(
            {'message': str(e)},
            status=500,
            reason=str(e)
        )

    return JsonResponse({}, status=204)


@login_required
def delete_mapping(request):
    oid = request.GET.get('oid')
    yang_module = request.GET.get('yangmodule')
    mapfile = request.GET.get('mapFile')

    try:
        if not mapfile:
            if not yang_module:
                return JsonResponse(
                    {'message': 'Choose model (needed to "Delete" mapping).'},
                    status=400,
                    reason='Choose model (needed to "Delete" mapping).'
                )
            mypath = MIBYANGpath.get(
                yang_module,
                request.user.username
            )
            mapfile = os.path.basename(
                mypath.walk_file
            ).replace('.walk', '.csv')
        map_file = os.path.join(
            get_path('mibyang_mappings_dir', user=request.user.username),
            mapfile,
        )
        myw = MibYangWriter.get(
            map_file,
            request.user.username,
        )
        myw.delete_mapping_in_csv(oid)
    except Exception as e:
        log.error(e.msg)
        return JsonResponse(
            {'message': e.msg},
            status=500,
            reason=e.msg
        )

    return JsonResponse({}, status=204)


@login_required
def import_mappings(request):
    """Import spreadsheet data from UI and present back to UI."""
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    file_data = body.get('fileDataArray')  # Contents of files

    if file_data is None:
        return JsonResponse(
            {'message': 'No data in spreadsheet.'},
            status=400,
            reason='No data in spreadsheet.'
        )
    if isinstance(file_data, list) and len(file_data) == 1:
        filename = file_data[0].get('filename')
        filename = filename.replace('.xlsx', '.csv')
        file_path = os.path.join(
            get_path('mibyang_mappings_dir', user=request.user.username),
            filename
        )
    else:
        return JsonResponse(
            {'message': 'Unrecognized spreadsheet data.'},
            status=400,
            reason='Unrecognized spreadsheet data.'
        )
    data = process_import_data(file_data, file_path, request.user.username)
    # TODO: the data is all empty because show mappings handles it now.
    mib_paths, yang_paths, mib_path_to_yang_path = data

    return JsonResponse({
        'yangPaths': yang_paths,
        'mibPaths': mib_paths,
        'mibPathToYangPath': mib_path_to_yang_path
    })


@login_required
def get_oid_result(request):
    """Send single OID to device and return result."""
    oid = request.GET.get('oid', '')
    device_name = request.GET.get('device', '')
    community = request.GET.get('community', '')
    v3pwd = request.GET.get('v3password', '')

    if not device_name:
        return JsonResponse(
            {},
            status=400,
            reason="Must select a device."
        )
    if not community and not v3pwd:
        return JsonResponse(
            {},
            status=400,
            reason="Please input community string or SNMPv3 password."
        )

    device_profile = YSDeviceProfile()
    device = device_profile.get(device_name)
    device_username = device.dict()['base']['username']
    device_address = device.dict()['base']['address']

    if v3pwd:
        cmd = [
            'snmpwalk',
            '-v3',
            '-l',
            'authNoPriv',
            '-u',
            device_username,
            '-a',
            'MD5',
            '-A',
            v3pwd,
            device_address,
            oid
        ]
    else:
        cmd = [
            'snmpwalk',
            '-v2c',
            '-c',
            community,
            device_address,
            oid
        ]

    log.info(f'Running SNMP cmd: {cmd}')
    # Run the command
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    out, err = process.communicate()

    if err:
        # Unsuccessful process return
        if err:
            # TODO: UI does not handle multiple lines in return
            err = err.replace(
                'No log handling enabled - using stderr logging', ''
            ).replace('\n', ' ')
            log.error(err)
        return JsonResponse(
            {'message': err},
            status=500,
            reason=err
        )

    return JsonResponse({'result': out})


@login_required
def get_map_result(request):
    """Get OID result and Xpath result and compare."""
    model = request.GET.get('model')
    yangset = request.GET.get('yangset')
    oid = request.GET.get('oid')
    xpath = request.GET.get('xpath')
    device = request.GET.get('device')
    community = request.GET.get('community', '')
    v3pwd = request.GET.get('v3password', '')

    if not device:
        return JsonResponse(
            {'message': "Choose device."},
            status=400,
            reason="Choose device."
        )
    if not community and not v3pwd:
        return JsonResponse(
            {},
            status=400,
            reason="Please input community string or SNMPv3 password."
        )
    if not model:
        return JsonResponse(
            {'message': 'Choose model (need namespace for "Run").'},
            status=400,
            reason='Choose model (need namespace for "run").'
        )

    if not xpath:
        return JsonResponse(
            {'message': "No YANG Xpath."},
            status=400,
            reason="No YANG Xpath."
        )
    if not oid:
        return JsonResponse(
            {'message': "No OID."},
            status=400,
            reason="No OID."
        )

    try:
        dev_profile = YSDeviceProfile.get(device)
        if community:
            # SNMP community string used
            dev_profile.base.username = community
            dev_profile.base.password = ''
        elif v3pwd:
            # SNMPv3 password used
            dev_profile.base.password = v3pwd
        mypath = MIBYANGpath.get(
            model, request.user.username, dev_profile, yangset
        )
        if model != mypath.yobj.model:
            mypath.yobj.model = model
        result = mypath.run_compare(oid, xpath)
    except Exception as exc:
        return JsonResponse(
            {'message': str(exc)},
            status=500,
            reason=str(exc)
        )

    return JsonResponse(result)


@login_required
def get_mapping_filenames(request):
    """Return a list of all XLSX filenames with mappings."""
    mappings_dir = get_path('mibyang_mappings_dir', user=request.user.username)
    mapping_filenames = []

    for (dpath, dnames, fnames) in os.walk(mappings_dir):
        for fname in fnames:
            if fname.startswith('~'):
                # Excel saves copies when file is open in Excel so skip it.
                continue
            if '.csv' in fname:
                mapping_filenames.append(
                    {
                        'id': uuid.uuid4().__str__(),
                        'value': fname,
                        'label': fname
                    }
                )
        # Break after all the files in top-most directory have been scanned
        break
    return JsonResponse({
        'mappingFilenames': mapping_filenames
    })


@login_required
def import_show_mappings_file(request):
    """Show mapping data from imported or newly mapped spreadsheets."""
    filepath = request.GET.get('filepath', '')
    filepath = os.path.join(
        get_path('mibyang_mappings_dir', user=request.user.username),
        filepath
    )

    try:
        mib_paths, yang_paths, mpath_to_ypath, model_xp = show_mapping_data(
            filepath, request.user.username
        )
    except (MappingException, Exception) as exc:
        return JsonResponse(
            {'message': str(exc)},
            status=500,
            reason=str(exc)
        )

    return JsonResponse({
        'mibPaths': mib_paths,
        'yangPaths': yang_paths,
        'mibPathToYangPath': mpath_to_ypath,
        'modelsToYangPath': model_xp,
    })


@login_required
def export_mapping_file(request):
    """Export mapping data spreadsheet."""
    filepath = request.GET.get('filepath', '')
    filepath = os.path.join(
        get_path('mibyang_mappings_dir', user=request.user.username),
        filepath
    )

    if not os.path.isfile(filepath):
        return JsonResponse(
            {'message': f'{filepath} not found.'},
            status=500,
            reason=f'{filepath} not found.'
        )

    try:
        filedata = open(filepath).read()
        return JsonResponse(
            {'filedata': filedata},
            status=200,
        )
    except Exception as exc:
        return JsonResponse(
            {'message': str(exc)},
            status=500,
            reason=str(exc),
        )
