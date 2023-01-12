#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
quantizeml main command-line interface.
"""

import argparse
import json
import os
import sys

from .models import (load_model, quantize, dump_config, save_weights, load_weights,
                     check_quantization)
from .models.transforms import fold_rescaling


def quantize_model(model_path, quant_config, fold=True, add_deq=True, output_name=None):
    """ CLI entry point to quantize a model using the provided configuration.

    Args:
        model_path (str): Path to the model to quantize.
        quant_config (str): Path to the quantization configuration file.
        fold (bool, optional): Whether to collapse foldable layers before quantizing.
            Defaults to True.
        add_deq (bool, optional): allows to convert output to float. Defaults to True.
        output_name (str, optional): name of the output quantized model. If none provided
            set a default name as <model>_<config>.h5. Defaults to None.
    """
    # Build name for the output model
    model_name = os.path.splitext(model_path)[0]
    config_name = os.path.splitext(os.path.basename(quant_config))[0]
    if output_name is None:
        output_name = f"{model_name}_{config_name}.h5"

    # Load the configuration file and the model
    with open(quant_config) as f:
        config = json.load(f)
    model = load_model(model_path)

    # Fold layers
    if fold:
        print(f"Collapsing foldable layers of {model_path}.")
        model = fold_rescaling(model)

    # Quantize the model and save it
    print(f"Quantizing model {model_path} with configuration file {quant_config}.")
    model_q = quantize(model, config, add_deq)
    model_q.save(output_name, include_optimizer=False)
    print(f"Saved quantized model to {output_name}.")


def dump_model_config(model_path, output_name=None):
    """ CLI entry point to dump the quantization configuration from a model.

    Args:
        model_path (str): Path to the model to extract the configuration from.
        output_name (str): Path to save the configuration.
            Defaults to <model_path>_quant_config.json.
    """
    # Build name for the output model
    if output_name is None:
        model_name = os.path.splitext(model_path)[0]
        output_name = f"{model_name}_quant_config.json"

    # Load the model and get its quantization configuration
    model = load_model(model_path)
    config = dump_config(model)
    with open(output_name, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Saved quantization configuration to {output_name}.")


def save_model_weights(model_path, weights_path):
    """ CLI entry point to save the model weights in an npz file.

    Args:
        model_path (str): Path to the model to extract the weights from.
        weights_path (str): Path to save the npz file.
            Defaults to <model_path>.npz.
    """
    # Build name for weights file
    if weights_path is None:
        model_name = os.path.splitext(model_path)[0]
        weights_path = f"{model_name}.npz"

    # Load the model and save its weights
    model = load_model(model_path)
    save_weights(model, weights_path)
    print(f"Saved model weights to {weights_path}.")


def load_model_weights(model_path, weights_path):
    """ CLI entry point to apply weights to a model from an npz file.

    Args:
        model_path (str): Path to the model on which apply the weights.
        weights_path (str): Path to load the npz file.
    """
    # Update the model weights with the npz file
    model = load_model(model_path)
    load_weights(model, weights_path)
    model.save(model_path, include_optimizer=False)
    print(f"Saved model with new weights to {model_path}.")


def check_quantized_model(model_path):
    """ CLI entry point to check model quantization.

    Args:
        model_path (str): Path to the model on which apply the weights.
    """
    model = load_model(model_path)
    messages = check_quantization(model)
    for msg in messages:
        print(msg)


def main():
    """ CLI entry point.

    Contains an argument parser with specific arguments depending on the model to be created.
    Complete arguments lists available using the -h or --help argument.

    """
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest="action")
    sp.add_parser("version", help="Display quantizeml version.")

    # Quantize arguments
    q_parser = sp.add_parser(
        "quantize", help="Quantize an input model, given a quantization configuration file.")
    q_parser.add_argument("-m", "--model", type=str, required=True, help="Model to quantize")
    q_parser.add_argument("-c", "--quantization_config", type=str,
                          required=True, help="Quantization configuration file")
    q_parser.add_argument("-f", "--fold", action="store_true",
                          help="Collapse foldable layers before quantizing")
    q_parser.add_argument("-nd", "--no_deq", action="store_false",
                          help="Do not add a dequantizer after head")
    q_parser.add_argument("-o", "--out_name", type=str,
                          help="Output quantized model name.")

    # Dump config arguments
    c_parser = sp.add_parser("config", help="Extract quantization configuration from a model.")
    c_parser.add_argument("-m", "--model", type=str, required=True,
                          help="Model to extract config from.")
    c_parser.add_argument("-o", "--output_path", type=str, help="Store quantization configuration. "
                          "Defaults to <model>_quant_config.json")

    # Save weights arguments
    w_parser = sp.add_parser("save_weights", help="Store models weights in an npz.")
    w_parser.add_argument("-m", "--model", type=str, required=True,
                          help="Model to extract weights from.")
    w_parser.add_argument("-w", "--weights_path", type=str,
                          help="Npz file that contains the saved weights.")

    # Load weights arguments
    w_parser = sp.add_parser("load_weights", help="Apply weights to a model from an npz file.")
    w_parser.add_argument("-m", "--model", type=str, required=True,
                          help="Model to apply the weights.")
    w_parser.add_argument("-w", "--weights_path", type=str, required=True,
                          help="Npz file that contains the weights to apply.")

    # Check action and arguments
    c_parser = sp.add_parser(
        "check", help="Check the quantization of a model to detect issues that can be fixed "
        "by adjusting the quantization configuration.")
    c_parser.add_argument("-m", "--model", type=str, required=True, help="Model to check")

    args = parser.parse_args()

    if args.action == "version":
        # importlib.metadata was introduced in Python 3.8 and is available to older versions as the
        # importlib-metadata project
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata
        print(metadata.version('quantizeml'))
    elif args.action == "quantize":
        quantize_model(
            model_path=args.model,
            quant_config=args.quantization_config,
            fold=args.fold,
            add_deq=args.no_deq,
            output_name=args.out_name
        )
    elif args.action == "config":
        dump_model_config(
            model_path=args.model,
            output_name=args.output_path,
        )
    elif args.action == "save_weights":
        save_model_weights(
            model_path=args.model,
            weights_path=args.weights_path,
        )
    elif args.action == "load_weights":
        load_model_weights(
            model_path=args.model,
            weights_path=args.weights_path,
        )
    elif args.action == "check":
        check_quantized_model(args.model)
