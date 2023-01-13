# Import packages
import os
import argparse

from gvxrPython3 import gvxr # Simulate X-ray images
from gvxrPython3 import json2gvxr # Process the JSON file


json_fname = None;
img_fname = None;


try:
    parser = argparse.ArgumentParser(description='Process a JSON file with gVXR to comute a simulated X-ray projection.')

    parser.add_argument('--json', type=str,
                        help='Filename of the JSON file to process')
    parser.add_argument('--proj', type=str,
                        help='Filename of the output X-ray image')
    args = parser.parse_args()

    json_fname = args.json
    img_fname = args.proj

    json2gvxr.initGVXR(json_fname);
    json2gvxr.initSourceGeometry();
    json2gvxr.initSpectrum();
    json2gvxr.initDetector();
    json2gvxr.initSamples();

    gvxr.computeXRayImage();
    gvxr.saveLastXRayImage(img_fname)

except Exception as inst:
    print(inst)
