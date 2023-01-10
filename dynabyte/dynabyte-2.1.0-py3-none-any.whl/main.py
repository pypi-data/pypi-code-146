#
# Copyright (C) 2023 LLCZ00
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.  
#

"""
dynabyte.main

- Argparse and CLI functions
"""
import sys
import argparse
import dynabyte.core as core
import dynabyte.utils as utils
from dynabyte import version

_NAME = "dynabyte"
_DESCRIPTION = f"""{_NAME} {__version__}, by LLCZ00
CLI tool and Python module designed to streamline the process of de-obfuscating data.
"""

class DynabyteParser(argparse.ArgumentParser):
    """Override argparse class for better error handler"""
    def error(self, message="Unknown error", help=False):
        if help:
            self.print_help()
        else:
            print(f"Error. {message}")
            print(f"Try './{self.prog} --help' for more information.")
        sys.exit(1)
        
class OperationValidator(argparse.Action):
    """argparse Action to parse and validate given operations/values"""
    def __call__(self, parser, namespace, op_list, option_string=None):
        operator_symbols = {
            "xor" : '^',
            "add" : '+',
            "sub" : '-',
            "rol" : 'utils.RotateLeft',
            "ror" : 'utils.RotateRight'
        }
        valididated_ops = []
        operation = None
        for index, op_val in enumerate(op_list):
            if index % 2 == 0: # Validate Op name
                op_val = op_val.lower()
                if op_val not in operator_symbols.keys():
                    parser.error(f"Invalid operation '{op_val}'")
                operation = op_val
            else: # Validate Op value
                try:
                    val = int(op_val, base=16)
                except ValueError:
                    parser.error(f"Invalid value '{op_val}'")          
                if operation is None:
                    parser.error(f"Operations error '{' '.join(op_list)}'")
                valididated_ops.append((operator_symbols[operation], val))                   
        setattr(namespace, self.dest, valididated_ops)

class HexKeyConverter(argparse.Action):
    """argparse Action to parse given hex into bytearray format"""
    def __call__(self, parser, namespace, hex_key, option_string=None):
        hex_array = bytearray([])
        for val in hex_key.split(','):
            try:
                hex_array.append(int(val, base=16))
            except ValueError:
                parser.error(f"Invalid value '{val}'")                 
        setattr(namespace, self.dest, hex_array)

class KeyConverter(argparse.Action):
    """argparse Action to parse given key string into bytearray format"""
    def __call__(self, parser, namespace, key, option_string=None):
        try:
            key = bytearray([ord(c) for c in key])
        except:
            parser.error(f"String conversion error '{key}'")               
        setattr(namespace, self.dest, key)


def parse_arguments():
    parser = DynabyteParser(
    prog=_NAME,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=_DESCRIPTION,
    epilog=f"Examples:\n\t{_NAME} --string plaintext xor 56 sub 12\n\t{_NAME} -f sus.bin -o sus.exe --xor 'password' add 0x12\n\t{_NAME} --hex 0x1b,0x52,0xa,0x18,0x44,0x16,0x19,0x57 --xor k3y"
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'Dynabyte {__version__}',
        help='Show version number and exit'
    ) 
    parser.add_argument(
        '-s', '--string', 
        metavar='INPUT',
        dest='array',
        action=KeyConverter,
        help='Input string to perform operations on.'
    )
    parser.add_argument(
        '-x', '--hex-in', 
        metavar='INPUT',
        dest='array',
        action=HexKeyConverter,
        help='Input hex (comma seperated) to perform operations on.'
    )
    parser.add_argument(
        '-f', '--file', 
        metavar='INPUT',
        dest='filepath',
        type=str,
        help='Input file to perform operation on.'
    )
    parser.add_argument(
        '-o', '--output', 
        metavar='OUTPUT',
        dest='output',
        type=str,
        help='Output file.'
    )
    parser.add_argument(
        '--xor',
        metavar='KEY',
        dest='xor_key',
        action=KeyConverter,
        help='Quick XOR; XOR input against given key (string).'
    )
    parser.add_argument(
        '--xor-hex',
        metavar='KEY',
        dest='xor_key',
        action=HexKeyConverter,
        help='Quick XOR; XOR input against given key (comma seperated hex).'
    )
    parser.add_argument(
        '--order',
        choices=['xor', 'ops'],
        dest='order',
        default='xor',
        help='Declare if Quick XOR or additional ops are executed first, if both options are being used. (Default: xor)'
    )     
    parser.add_argument(
        '--delim',
        metavar='SEP',
        dest='delim',
        default=',',
        type=str,
        help="Set output hex delimiter. (Default: ',')"
    )
    parser.add_argument(
        '--style',
        choices=['c', 'list', 'int'],
        dest='style',
        default=None,
        type=str,
        help="Set style to print output bytes. (Default: Comma deliminated hex)"
    )
    parser.add_argument(
        'ops',
        nargs='*',
        action=OperationValidator,
        help="Additional operations to be performed on each input byte, executed from left to right (xor, add, sub, rol, ror). All values interpreted as hex."
    )
    
    args = parser.parse_args()

    if not args.array and not args.filepath:
        parser.error(help=True)
        
    if not args.xor_key and not args.ops:
        parser.error("No operation options given.")
        
    if args.array and args.filepath:
        parser.error("More than one input method chosen.")
        
    return args
        
def main():
    args = parse_arguments()
    
    """
    Create dynabyte instance from either filepath or array/string
    """

    file = False
    if args.array:
        db_obj = core.Array(args.array)
    elif args.filepath and not args.array:
        db_obj = core.File(args.filepath, file=True)
        file = True
    
    """
    Dynamically generate a callback function based on given options
    """
    lambda_base = f"lambda byte, offset: "
    lambda_addon = "byte"
    
    if args.order == "xor":
        order = ["xor", "ops"]
    else:
        order = ["ops", "xor"]

    for operation in order:
        if operation.lower() == "xor" and args.xor_key:           
            lambda_addon = f"({lambda_addon} ^ key[offset % {len(args.xor_key)}])"             
        elif operation.lower() == "ops" and args.ops:
            for op_val in args.ops:
                if op_val[0] == 'utils.RotateLeft' or op_val[0] == 'utils.RotateRight':
                    lambda_addon = f"({op_val[0]}({lambda_addon}, {op_val[1]}))"
                else:
                    lambda_addon = f"({lambda_addon} {op_val[0]} {op_val[1]})"                
        else:
            pass

    callback_string = lambda_base+lambda_addon[1:-1] # Remove outer paranthesis
    callback = eval(f"{callback_string}", {'key':args.xor_key, 'utils':utils}) # I know  
    
    """
    Run and output
    """
    db_obj.run(callback, output=args.output)    
    
    print(f"Callback function:\n{callback_string}\n")
    if file:
        if args.output:
            print(f"Modified bytes written to {args.output}")
        else:    
            print(f"Modified bytes written to {args.filepath}")
    else:
        print("Output bytes:")
        db_obj.print(style=args.style, delim=args.delim)
        print("\nOutput string:")
        db_obj.print("string")
        


if __name__ == "__main__":
    sys.exit(main())
