#! /usr/bin/env python
#
# Copyright (c) 2022 Alberto Mardegan <mardy@users.sourceforge.net>
#
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.


import os.path
import re
import textwrap


class Generator(object):
    def add_options(parser):
        pass

    def __init__(self, config):
        self.config = config

    def open_output(self, suffix):
        filename = self.config.name + suffix
        out_dir = self.config.directory
        filepath = os.path.join(out_dir, filename) if out_dir else filename
        return open(filepath, 'w')

    def generate(self, parser):
        pass


class BaseCppGenerator(Generator):
    @property
    def prefix(self):
        # TODO: make the prefix configurable
        return self.config.name

    def write_header(self, file):
        file.write(textwrap.dedent("""\
        /*
         * This file has been generated with
         *
         *  {cmdline}
         *
         */
        """.format(cmdline=self.config.cmdline_args)))

    def write_extern_c_begin(self, file):
        file.write(textwrap.dedent("""\
        #ifdef __cplusplus
        extern "C" {
        #endif
        """))

    def write_extern_c_end(self, file):
        file.write(textwrap.dedent("""\
        #ifdef __cplusplus
        }
        #endif
        """))

    def write_drawing_function_decls(self, f, functions):
        self.write_extern_c_begin(f)
        for func in functions:
            f.write(f'void {func}();\n')
        self.write_extern_c_end(f)

    def write_drawing_functions(self, f):
        functions = []
        for o in self.data.objects:
            fn = self.write_drawing_function(f, o)
            functions.append(fn)
        fn = self.write_draw_all(f, functions)
        functions.append(fn)
        return functions

    def write_draw_all(self, f, functions):
        func_name = self.prefix + '_draw_all'
        f.write(textwrap.dedent(f"""\

        void {func_name}()
        {{
        """))
        for func in functions:
            f.write(f'    {func}();\n')
        f.write("}\n")
        return func_name

    def write_setup_functions(self, f):
        functions = []
        for o in self.data.objects:
            fn = self.write_setup_function(f, o)
            if fn:
                functions.append(fn)
        fn = self.write_setup_all(f, functions)
        functions.append(fn)
        return functions

    def write_setup_all(self, f, functions):
        func_name = self.prefix + '_setup_all'
        f.write(textwrap.dedent(f"""\

        void {func_name}()
        {{
        """))
        for func in functions:
            f.write(f'    {func}();\n')
        f.write("}\n")
        return func_name

    def escape(self, text):
        return re.sub(r'[.]', '_', text)

    def write_data(self, f, data):
        text = ', '.join(data) + ','
        lines = textwrap.wrap(text, width=79, initial_indent='    ',
                              subsequent_indent='    ')
        for line in lines:
            f.write(line + '\n')
