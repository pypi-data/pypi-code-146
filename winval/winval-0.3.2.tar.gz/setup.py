# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['winval', 'winval.antlr']

package_data = \
{'': ['*'], 'winval': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['antlr4-python3-runtime==4.10',
 'google-cloud-storage>=2.5.0,<3.0.0',
 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'winval',
    'version': '0.3.2',
    'description': 'WDL workflow inputs validation',
    'long_description': '# winval\n### Workflow inputs validation python library\n\n* Currently, supports WDL workflows.\n* Constraints on inputs can be written as specially tagged (#@wv) comments in the WDL inputs section.\n* The syntax of constraints is a python-similar DSL, with ANTLR defined grammar.\n* The WDL + inputs.json can be validated using a script/function before submitting a workflow.\n\n## Usage:\n\n### validate_wdl_constraints\nFrom unix command-line:\n~~~\npython winval/validate_wdl_constraints.py --wdl <wdl_file> --json <json_file>\n~~~\n\nFrom python\n~~~\nfrom winval.validate_wdl_constraints import run_winval\nis_validated = run_winval(wdl_file, json_file)\n~~~\n\n### cloud_files_validater\n#### Make sure google-storage permissions are equivalent to the batch workers permissions \nFrom unix command-line:\n~~~\npython winval/cloud_files_validator.py --wdl <wdl_file> --json <json_file>\n~~~\n\nFrom python\n~~~\nfrom winval.cloud_files_validator import CloudFilesValidator\nis_validated = CloudFilesValidator(args.wdl, args.json).validate()\n~~~\n\n## WDL constraints example\n~~~\nworkflow MyWorkflow {\n\n  input {\n    File file\n    Int c\n    File* opt_file_1\n    File* opt_file_2\n    Array[File] files\n    Array[File] index_files\n    MyStruct struct_instance\n\n    #@wv defined(opt_file_1) <-> defined(opt_file_2)\n    #@wv defined(opt_file_1) -> c > 1\n    #@wv len(files) == len(index_files)\n    #@wv len(files) >= 0\n    #@wv len(index_files) >= 0\n    #@wv c <= 1 and c >= 0\n    #@wv suffix(file) == ".fasta"\n    #@wv suffix(files) <= {".bam", ".cram"} \n    #@wv prefix(index_files) == files\n    #@wv len(struct_instance[\'field_a\']) > 0\n  }\n  ...\n}\n  \n  struct MyStruct{\n     String field_a,\n     String field_b\n  }\n~~~\n\n## Generate parsers from grammar:\n~~~\ncd <project_root>/winval\nantlr4 -Dlanguage=Python3 winval.g4 -visitor -o antlr\n~~~\n\n## Available atomic expressions:\n* int: 5\n* float: 5.6\n* bool: True, False\n* str: "some string", \'some_string\'\n* workflow_variable: my_var\n* evaluates to value given by json conf, or None if not defined in json\n* empty_set: {} \n\n## Available python operators\n* `+`,`-`,`*`,`**`,`/`,`&`,`|`,`%`\n* `and`, `or`, `in`\n* `<`, `<=`, `==`, `>=`, `>`, `!=`\n* Notice the following useful operators work for sets:\n  * `-`: set subtraction\n  * `&`: set intersection\n  * `|` : is set union \n  * `<=`:  subset \n\n## Available python functions\n* `len()`, `not()`\n* `basename()`, `splitext()` (from os.path)\n\n## Available convenience functions and operators:\n* `x <-> y`: if-and-only-if logical operator (if x is true if and only if y is true)\n* `x -> y`: implies logical operator (if x is true then y should be true)\n* `defined(x)`: if x a defined variable\n* `prefix(x)`: return path prefix of String/File or list of prefixes for \n* `suffix(x)`: return path suffix of String/File or set of suffixes for Array[String]/Array[File]\n',
    'author': 'doron',
    'author_email': 'doron.shemtov@ultimagen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
