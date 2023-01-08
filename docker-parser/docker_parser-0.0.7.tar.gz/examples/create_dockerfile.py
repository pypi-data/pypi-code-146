import sys
import os

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__),
    '..'
))

import argparse

from docker_parser.classess import Docker, Stage
from docker_parser.parser import FROM, COPY

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', '-i', action='store', dest="image", help='Base image of docker container to use', default="httpd")
    parser.add_argument('--src', '-s', action='store', dest="src", help='Source of data to publish (public-html)', default=None)
    parser.add_argument('--dst', '-d', action='store', dest="dst", help='Destination of data to publish', default='/usr/local/apache2/htdocs/')
    parser.add_argument('file', help="path where to save dockerfile")
    args = parser.parse_args()


    img = FROM.Image(args.image)
    docker = Docker()
    docker.stages.append(Stage(img))
    if args.src:
        docker.stages[0].commands.append(COPY('COPY', f'{args.src} {args.dst}', None))
    docker.save(args.file)