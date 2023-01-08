from deepernetwork import DeeperNetwork


deeper = DeeperNetwork(
    username="admin", password="", hostIp="http://34.34.34.34", proxy=""
)

newsUpdates = deeper.dashboard.inform

aktMode = deeper.dashboard.dpnMode
if aktMode != "full":

    response = deeper.mode.set_dpnMode(
        {
            "dpnMode": "full",
            "tunnelCode": "EUE",
        }
    )

    if response is True:
        print("active dpn mode: full")
