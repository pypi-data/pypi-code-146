#! /usr/bin/env python
#
# Copyright (c) 2022 Alberto Mardegan <mardy@users.sourceforge.net>
#
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.


import logging
import textwrap
from .generator import BaseCppGenerator
from PIL import Image


log = logging.getLogger('opengl')


def color_to_params(color, alpha=1.0):
    values = [str(x) for x in color]
    if len(values) == 3:
        values.append(str(alpha))
    return ', '.join(values)


def color_to_rgba4444(color):
    c = [int(x) >> 4 for x in color]
    return hex(c[0] << 12 | c[1] << 8 | c[2] << 4 | c[3])


def color_to_rgba8888(color):
    c = [int(x) for x in color]
    return hex(c[0] << 24 | c[1] << 16 | c[2] << 8 | c[3])


class ColorFormat(object):
    def __init__(self, name, bpp, alpha_bits):
        self.name = name
        self.bpp = bpp
        self.alpha_bits = alpha_bits


# If requested, add support for indexed formats
COLOR_FORMATS = dict(
    RGBA4444=ColorFormat('GL_UNSIGNED_SHORT_4_4_4_4', bpp=16, alpha_bits=4),
    RGBA8888=ColorFormat('GL_UNSIGNED_INT_8_8_8_8', bpp=32, alpha_bits=8),
)


class TextureData(object):
    def __init__(self, name, color_format, size,
                 parsed_texture, texture_name):
        self.name = name
        self.color_format = color_format
        self.size = size
        self.parsed_texture = parsed_texture
        self.texture_name = texture_name


class OpenGLImGenerator(BaseCppGenerator):
    """ OpenGL immediate mode """
    name = 'opengl_im'

    def add_options(parser):
        cname = OpenGLImGenerator.name
        group = parser.add_argument_group(
                "OpenGL", f"Options for the {cname} generator")
        group.add_argument(
            '--mipmap', action='store_true',
            help="Generate all mipmaps for the textures used")

    def generate(self, parser):
        log.debug("OpenGL generator invoked")
        self.data = parser
        with self.open_output('.c') as f:
            self.write_header(f)
            f.write("\n#include <GL/gl.h>\n")
            functions = self.write_setup_functions(f)
            functions += self.write_drawing_functions(f)

        with self.open_output('.h') as f:
            self.write_header(f)
            self.write_drawing_function_decls(f, functions)

    def write_setup_function(self, f, obj):
        log.debug(f"Writing setup function for object {obj.name}")
        return self.write_texture_creations(f, obj)

    def write_drawing_function(self, f, obj):
        log.debug(f"Writing function for object {obj.name}")
        self.current_object = obj
        func_name = self.prefix + '_draw_' + self.escape(obj.name)
        f.write(textwrap.dedent(f"""\

        void {func_name}()
        {{
        """))
        for mat_name, mat_faces in obj.face_materials.items():
            faces = [obj.faces[i] for i in mat_faces]
            material = self.data.materials[mat_name] if mat_name else None
            self.write_faces(f, faces, material)
        f.write("}\n")
        return func_name

    def write_faces(self, f, faces, material):
        data = self.data
        for face in faces:
            self.write_bind_texture(f, material)
            if len(face) == 4:
                f.write("    glBegin(GL_QUADS);\n")
            else:
                f.write("    glBegin(GL_TRIANGLES);\n")
            if material:
                self.write_material(f, material)
            for v_data in face:
                if v_data[1] and material and material.texture_idx is not None:
                    t = data.texcoords[v_data[1] - 1]
                    f.write("    glTexCoord2f({}, {});\n".format(
                                t[0],
                                (1.0 - t[1])))
                n = data.normals[v_data[2] - 1]
                f.write("    glNormal3f({}, {}, {});\n".format(*n))
                v = data.vertexes[v_data[0] - 1]
                f.write("    glVertex3f({}, {}, {});\n".format(*v))
            f.write("    glEnd();\n")

    def write_texels(self, f, image, cformat, material):
        if material.dissolve_tex:
            alpha_size = material.dissolve_tex.image.size
            if image.size != alpha_size:
                log.error(f"Texture size ({image.size}) mismatch with "
                          f"alpha ({alpha_size})!")

        def get_alpha(x, y):
            if material.dissolve_tex:
                p = material.dissolve_tex.image.getpixel((x, y))
                return p[3]
            return 255
        texture_name = self.prefix + '_textdata_' + material.name
        data_type = 'GLuint' if cformat.bpp == 32 else 'GLushort'
        f.write(f'static const {data_type} {texture_name}[] = {{\n')
        for y in range(image.height):
            f.write(f'    // row {y}:\n')
            data = []
            for x in range(image.width):
                alpha = get_alpha(x, y)
                p = image.getpixel((x, y))[0:3] + (alpha,)
                if cformat.bpp == 32:
                    c = color_to_rgba8888(p)
                elif cformat.bpp == 16:
                    c = color_to_rgba4444(p)
                else:
                    log.error(f"Unsupported bpp: {cformat.bpp}")
                data.append(str(c))
            self.write_data(f, data)
        f.write('};\n\n')
        return texture_name

    def write_texture_creation(self, f, material):
        texture = None
        for t in (material.ambient_tex, material.diffuse_tex,
                  material.specular_tex, material.emission_tex):
            if t:
                texture = t
                break
        if not texture:
            return None

        # TODO: add a command-line option to decide if non-power-of-2 textures
        # should be accepted
        size_x = texture.image.width
        size_y = texture.image.height

        # Remove transparency
        image = Image.new('RGB', texture.image.size)
        image.paste(texture.image)

        # For now, always use 32bpp RGBA
        # TODO: pick the best color format for the image.
        cf = 'RGBA8888'
        cformat = COLOR_FORMATS[cf]

        # Pass the material for alpha information
        texture_name = self.write_texels(f, image, cformat, material)

        return TextureData(material.name, cformat, (size_x, size_y),
                           texture, texture_name)

    def write_texture_creations(self, f, obj):
        textures = []
        for material in self.data.materials.values():
            tex_data = self.write_texture_creation(f, material)
            if tex_data:
                material.texture_idx = len(textures)
                material.tex_data = tex_data
                textures.append(tex_data)
            else:
                material.texture_idx = None
        if not textures:
            return None

        obj_name = self.escape(obj.name)
        func_name = self.prefix + '_create_textures_' + obj_name
        num_textures = len(textures)
        tex_array_name = self.prefix + '_' + obj_name + '_texture_names'
        f.write(textwrap.dedent(f'''
        static int {tex_array_name}[{num_textures}];

        void {func_name}()
        {{
            glGenTextures({num_textures}, {tex_array_name});
        '''))
        for i, t in enumerate(textures):
            # TODO: add option for using mipmaps
            f.write(textwrap.indent(textwrap.dedent(f'''
            glBindTexture(GL_TEXTURE_2D, {tex_array_name}[{i}]);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                         {t.size[0]}, {t.size[1]}, 0,
                         GL_RGBA, {t.color_format.name},
                         {t.texture_name});
            '''), '    '))
            if self.config.args.mipmap:
                f.write('    glGenerateMipmap(GL_TEXTURE_2D);\n')
            else:
                f.write('    glTexParameteri(GL_TEXTURE_2D,'
                        ' GL_TEXTURE_MIN_FILTER, GL_LINEAR);\n')
            if t.parsed_texture and not t.parsed_texture.clamp:
                f.write('    glTexParameteri(GL_TEXTURE_2D,'
                        ' GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);\n')
                f.write('    glTexParameteri(GL_TEXTURE_2D,'
                        ' GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);\n')

        f.write('}\n\n')
        return func_name

    def write_material(self, f, material):
        black = (0.0, 0.0, 0.0)
        f.write(f"    // Material: {material.name}\n")

        def print_material(mat, color):
            c = color_to_params(color, material.dissolve_factor)
            f.write(textwrap.indent(textwrap.dedent(f"""\
            {{
                const GLfloat color[4] = {{ {c} }};
                glMaterialfv(GL_FRONT_AND_BACK, {mat}, color);
            }}
            """), '    '))
        print_material('GL_DIFFUSE',
                       material.diffuse if material.diffuse_on else black)
        print_material('GL_AMBIENT',
                       material.ambient if material.ambient_on else black)
        if material.highlight_on:
            print_material('GL_SPECULAR', material.specular)
        if material.emission_on:
            color = material.emission if material.emission != black \
                    else material.diffuse
        else:
            color = black
        print_material('GL_EMISSION', color)

    def write_bind_texture(self, f, material):
        obj = self.current_object
        obj_name = self.escape(obj.name)
        tex_array_name = self.prefix + '_' + obj_name + '_texture_names'
        if material.texture_idx is not None:
            ti = material.texture_idx
            f.write("    glBindTexture(GL_TEXTURE_2D, "
                    f"{tex_array_name}[{ti}]);\n")
        else:
            f.write("    glBindTexture(GL_TEXTURE_2D, 0);\n")
