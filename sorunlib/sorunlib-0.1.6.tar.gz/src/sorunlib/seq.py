import sorunlib as run
from sorunlib._internal import check_response


OP_TIMEOUT = 60


def scan(description, stop_time, width):
    """Run a constant elevation scan, collecting detector data.

    Args:
        description (str): Description of the field/object being scanned.
        stop_time (str): Time in ISO format to scan until, i.e.
            "2022-06-21T15:58:00"
        width (float): Scan width in azimuth. The scan will start at the
            current position and move in the positive azimuth direction.

    """
    # Enable SMuRF streams
    run.smurf.stream('on')

    # Grab current telescope position
    resp = run.CLIENTS['acu'].monitor.status()
    az = resp.session['data']['Corrected Azimuth']
    el = resp.session['data']['Corrected Elevation']

    # Start telescope motion
    resp = run.CLIENTS['acu'].generate_scan.start(az_endpoint1=az,
                                                  az_endpoint2=az + width,
                                                  az_speed=2,
                                                  acc=2.0,
                                                  el_endpoint1=el,
                                                  el_endpoint2=el,
                                                  el_speed=0)

    # Wait until stop time
    run.commands.wait(stop_time)

    # Stop motion
    run.CLIENTS['acu'].generate_scan.stop()
    resp = run.CLIENTS['acu'].generate_scan.wait(timeout=OP_TIMEOUT)
    check_response(resp)

    # Stop SMuRF streams
    run.smurf.stream('off')
