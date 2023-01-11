import argparse
import json

import libcoveofds.additionalfields
import libcoveofds.geojson
import libcoveofds.jsonschemavalidate
import libcoveofds.python_validate
import libcoveofds.schema


def main():
    parser = argparse.ArgumentParser(description="Lib Cove OFDS CLI")
    subparsers = parser.add_subparsers(dest="subparser_name")

    python_validate_parser = subparsers.add_parser(
        "pythonvalidate",
        aliases=["pv"],
        help="Check that data conforms to normative rules specified in OFDS",
    )
    python_validate_parser.add_argument(
        "inputfilename", help="File name of an input JSON data file"
    )

    additional_fields_parser = subparsers.add_parser(
        "additionalfields",
        aliases=["af"],
        help="Report additional fields not specified in the schema",
    )
    additional_fields_parser.add_argument(
        "inputfilename", help="File name of an input JSON data file"
    )

    json_schema_validate_parser = subparsers.add_parser(
        "jsonschemavalidate", aliases=["jsv"], help="Validate data against the schema"
    )
    json_schema_validate_parser.add_argument(
        "inputfilename", help="File name of an input JSON data file"
    )

    json_to_geojson_parser = subparsers.add_parser(
        "jsontogeojson",
        aliases=["jtogj"],
        help="Convert data from JSON format to GeoJSON format",
    )
    json_to_geojson_parser.add_argument(
        "inputfilename", help="File name of an input JSON data file"
    )
    json_to_geojson_parser.add_argument(
        "outputnodesfilename", help="Output filename to write Nodes GeoJSON data to"
    )
    json_to_geojson_parser.add_argument(
        "outputspansfilename", help="Output filename to write Spans GeoJSON data to"
    )
    json_to_geojson_parser.add_argument(
        "--outputmetafilename",
        help="Output filename to write meta JSON data to",
        required=False,
    )

    geojson_to_json_parser = subparsers.add_parser(
        "geojsontojson",
        aliases=["gjtoj"],
        help="Convert data from GeoJSON to JSON format",
    )
    geojson_to_json_parser.add_argument(
        "inputnodesfilename", help="File name of an input Nodes GeoJSON data file"
    )
    geojson_to_json_parser.add_argument(
        "inputspansfilename", help="File name of an input Spans GeoJSON data file"
    )
    geojson_to_json_parser.add_argument(
        "outputfilename", help="Output filename to write JSON data to"
    )
    geojson_to_json_parser.add_argument(
        "--outputmetafilename",
        help="Output filename to write meta JSON data to",
        required=False,
    )

    args = parser.parse_args()

    if args.subparser_name == "pythonvalidate" or args.subparser_name == "pv":

        with open(args.inputfilename) as fp:
            input_data = json.load(fp)

        schema = libcoveofds.schema.OFDSSchema()
        validator = libcoveofds.python_validate.PythonValidate(schema)

        output = validator.validate(input_data)

        print(json.dumps(output, indent=4))

    elif args.subparser_name == "additionalfields" or args.subparser_name == "af":

        with open(args.inputfilename) as fp:
            input_data = json.load(fp)

        schema = libcoveofds.schema.OFDSSchema()
        validator = libcoveofds.additionalfields.AdditionalFields(schema)

        output = validator.process(input_data)

        print(json.dumps(output, indent=4))

    elif args.subparser_name == "jsonschemavalidate" or args.subparser_name == "jsv":

        with open(args.inputfilename) as fp:
            input_data = json.load(fp)

        schema = libcoveofds.schema.OFDSSchema()
        validators = libcoveofds.jsonschemavalidate.JSONSchemaValidator(schema)

        output = validators.validate(input_data)

        output_json = [o.json() for o in output]

        print(json.dumps(output_json, indent=4))

    if args.subparser_name == "jsontogeojson" or args.subparser_name == "jtogj":

        with open(args.inputfilename) as fp:
            input_data = json.load(fp)

        converter = libcoveofds.geojson.JSONToGeoJSONConverter()
        converter.process_package(input_data)

        with open(args.outputnodesfilename, "w") as fp:
            json.dump(converter.get_nodes_geojson(), fp, indent=4)

        with open(args.outputspansfilename, "w") as fp:
            json.dump(converter.get_spans_geojson(), fp, indent=4)

        if args.outputmetafilename:
            with open(args.outputmetafilename, "w") as fp:
                json.dump(converter.get_meta_json(), fp, indent=4)

    elif args.subparser_name == "geojsontojson" or args.subparser_name == "gjtoj":

        with open(args.inputnodesfilename) as fp:
            nodes_data = json.load(fp)

        with open(args.inputspansfilename) as fp:
            spans_data = json.load(fp)

        converter = libcoveofds.geojson.GeoJSONToJSONConverter()
        converter.process_data(nodes_data, spans_data)

        with open(args.outputfilename, "w") as fp:
            json.dump(converter.get_json(), fp, indent=4)

        if args.outputmetafilename:
            with open(args.outputmetafilename, "w") as fp:
                json.dump(converter.get_meta_json(), fp, indent=4)


if __name__ == "__main__":
    main()
