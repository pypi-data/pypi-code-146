import argparse
import os

contents = """
<head>
    <meta http-equiv="refresh" content="0; URL=https://docs.seerai.space/geodesic/{version}/geodesic" />
</head>

<body>
    <p>Redirecting to current version</p>
</body>
"""


def main(args):
    """Update the version number."""
    version = args.version.replace('refs/tags/v', '')
    version = version.lstrip('v')
    os.environ['VERSION'] = version
    # create version file to set github variable
    with open("VERSION.txt", "w") as f:
        f.write(version)

    # Then create an index.html that redirects to this version to be uploaded to the docs page
    with open("index.html", "w") as f:
        f.write(contents.format(version=version))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version',
        '-v',
        required=True,
        type=str,
        help="The version to change this to. Must be semver."
    )
    args = parser.parse_args()

    main(args)
