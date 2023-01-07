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


log = logging.getLogger('nds')


def color_to_rgb15(color):
    triplet = ', '.join([str(int(x * 31.5)) for x in color])
    return f'RGB15({triplet})'


class ColorFormat(object):
    def __init__(self, name, is_direct=False, alpha_bits=0, palette_size=0):
        self.name = name
        self.is_direct = is_direct
        self.alpha_bits = alpha_bits
        self.palette_size = palette_size
        self.bpp = 16 if is_direct else \
            8 if (alpha_bits > 0 or palette_size > 16) else \
            4 if palette_size > 4 else 2


COLOR_FORMATS = dict(
    RGB32_A3=ColorFormat('GL_RGB32_A3', palette_size=32, alpha_bits=3),
    RGB4=ColorFormat('GL_RGB4', palette_size=4),
    RGB16=ColorFormat('GL_RGB16', palette_size=16),
    RGB256=ColorFormat('GL_RGB256', palette_size=256),
    RGB8_A5=ColorFormat('GL_RGB8_A5', palette_size=8, alpha_bits=5),
    RGBA=ColorFormat('GL_RGBA', is_direct=True, alpha_bits=1),
    RGB=ColorFormat('GL_RGB', is_direct=True, alpha_bits=0),
    # TODO: support compressed textures
)

TEXTURE_SIZES = (8, 16, 32, 64, 128, 256, 512, 1024)


class TextureData(object):
    def __init__(self, name, color_format, size,
                 parsed_texture, texture_name, palette_name):
        self.name = name
        self.color_format = color_format
        self.size = size
        self.parsed_texture = parsed_texture
        self.texture_name = texture_name
        self.palette_name = palette_name


class NdsGlGenerator(BaseCppGenerator):
    name = 'nds_gl'

    def generate(self, parser):
        log.debug("NDS generator invoked")
        self.data = parser
        with self.open_output('.c') as f:
            self.write_header(f)
            f.write("\n#include <nds.h>\n")
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
            if len(face) == 4:
                f.write("    glBegin(GL_QUADS);\n")
            else:
                f.write("    glBegin(GL_TRIANGLES);\n")
            if material:
                self.write_material(f, material)
            for v_data in face:
                if v_data[1] and material and material.texture_idx is not None:
                    tex_size = material.tex_data.size
                    t = data.texcoords[v_data[1] - 1]
                    f.write("    glTexCoord2t16(floattot16({}), "
                            "floattot16({}));\n".format(
                                t[0] * tex_size[0],
                                (1.0 - t[1]) * tex_size[1]))
                n = data.normals[v_data[2] - 1]
                f.write("    glNormal3f({}, {}, {});\n".format(*n))
                v = data.vertexes[v_data[0] - 1]
                f.write("    glVertex3f({}, {}, {});\n".format(*v))
            f.write("    glEnd();\n")

    def write_palette(self, f, palette, name):
        # TODO: check if palettes can be merged
        palette_name = self.prefix + '_palette_' + name
        f.write(f'static const uint16 {palette_name}[] = {{\n')
        log.debug(f"Palette length {len(palette)}, is {palette}")
        for i in range(int(len(palette) / 3)):
            c = (palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2])
            color = color_to_rgb15([x / 255.0 for x in c])
            f.write(f'    {color},\n')
        f.write('};\n\n')
        return palette_name

    def write_texels(self, f, image, cformat, material):
        if material.dissolve_tex:
            alpha_size = material.dissolve_tex.image.size
            if image.size != alpha_size:
                log.error(f"Texture size ({image.size}) mismatch with "
                          f"alpha ({alpha_size})!")

        def get_alpha(x, y):
            if material.dissolve_tex:
                p = material.dissolve_tex.image.getpixel((x, y))
                return p[3] / 255.0
            return material.dissolve_factor
        texture_name = self.prefix + '_textdata_' + material.name
        data_type = 'uint16' if cformat.is_direct else 'uint8'
        a_shift = 8 - cformat.alpha_bits
        a_mult = (1 << cformat.alpha_bits) - 0.5
        f.write(f'static const {data_type} {texture_name}[] = {{\n')
        for y in range(image.height):
            f.write(f'    // row {y}:\n')
            data = []
            written_bits = 0
            pixel = ''
            for x in range(image.width):
                p = image.getpixel((x, y))
                if cformat.is_direct:
                    c = color_to_rgb15([x / 255.0 for x in p[0:3]])
                    data.append(str(c))
                elif cformat.bpp == 8:
                    if cformat.alpha_bits > 0:
                        alpha = get_alpha(x, y)
                        a = int(alpha * a_mult)
                        data.append(f'{p}|{a}<<{a_shift}')
                    else:
                        data.append(str(p))
                else:
                    pixel += f'{p}<<{written_bits}'
                    written_bits += cformat.bpp
                    if written_bits == 8:
                        data.append(pixel)
                        pixel = ''
                        written_bits = 0
                    else:
                        pixel += '|'
            self.write_data(f, data)
        f.write('};\n\n')
        return texture_name

    def write_texture_creation(self, f, material):
        # The NDS handles transparency by either setting it as a poligon
        # attribute (http://problemkaputt.de/gbatek.htm#ds3dpolygonattributes)
        # or by creating a texture with alpha. We opt for the latter option, in
        # order to give the developer the possibility of playing with polygon
        # attributes for the whole object (imagine a cube with some transparent
        # faces that needs to gradually appear on screen).
        needs_alpha = True if material.dissolve_tex or \
            (material.dissolve_factor > 0 and material.dissolve_factor < 1) \
            else False

        texture = None
        for t in (material.ambient_tex, material.diffuse_tex,
                  material.specular_tex, material.emission_tex):
            if t:
                texture = t
                break

        if not texture:
            if needs_alpha:
                # Create a flat colour texture
                black = (0.0, 0.0, 0.0)
                c = material.ambient if material.ambient != black else \
                    material.diffuse if material.diffuse != black else \
                    material.emission
                flat_color = tuple([int(x * 255) for x in c])
                image = Image.new('RGB', (8, 8), color=flat_color)
                size_x = size_y = 8
            else:
                return None
        else:
            def compute_size(image_size):
                valid_sizes = [x for x in TEXTURE_SIZES if x >= image_size]
                return valid_sizes[0] if valid_sizes else TEXTURE_SIZES[-1]
            size_x = compute_size(texture.image.width)
            size_y = compute_size(texture.image.height)
            if size_x != texture.image.width or \
                    size_y != texture.image.height:
                # TODO: scale image and update UV coordinates
                log.error(f'Invalid texture size {texture.image.size}')
            # Remove transparency
            image = Image.new('RGB', texture.image.size)
            image.paste(texture.image)

        colors = image.getcolors(maxcolors=256)
        num_colors = len(colors) if colors else 257
        log.debug(f"Texture has {num_colors} colors")
        # Pick an appropriate color format
        cf = 'RGBA'
        if needs_alpha:
            cf = 'RGB32_A3' if num_colors > 8 else 'RGB8_A5'
        elif num_colors > 256:
            cf = 'RGB'
        elif num_colors > 16:
            cf = 'RGB256'
        elif num_colors > 4:
            cf = 'RGB16'
        else:
            cf = 'RGB4'
        cformat = COLOR_FORMATS[cf]
        # Convert the image
        palette_name = None
        if not cformat.is_direct:
            # Reduce the color depth, since we support only RGB555
            for y in range(image.height):
                for x in range(image.width):
                    pos = (x, y)
                    p = image.getpixel(pos)
                    p = tuple([int(int(x / 8) * 255 / 31) for x in p])
                    image.putpixel(pos, p)
            image = image.quantize(colors=cformat.palette_size)
            palette = image.getpalette()[:3*cformat.palette_size]
            palette_name = self.write_palette(f, palette, material.name)

        # Pass the material for alpha information
        texture_name = self.write_texels(f, image, cformat, material)

        return TextureData(material.name, cformat, (size_x, size_y),
                           texture, texture_name, palette_name)

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
            params = ['TEXGEN_TEXCOORD']
            if t.parsed_texture and not t.parsed_texture.clamp:
                params += ['GL_TEXTURE_WRAP_S', 'GL_TEXTURE_WRAP_T']
            params_text = '|'.join(params)
            f.write(textwrap.indent(textwrap.dedent(f'''
            glBindTexture(0, {tex_array_name}[{i}]);
            glTexImage2D(0, 0, {t.color_format.name},
                         TEXTURE_SIZE_{t.size[0]}, TEXTURE_SIZE_{t.size[1]},
                         0, {params_text}, {t.texture_name});
            '''), '    '))
            if t.palette_name:
                palette_size = t.color_format.palette_size
                f.write(f'    glColorTableEXT(0, 0, {palette_size}, '
                        f'0, 0, {t.palette_name});\n')
        f.write('}\n\n')
        return func_name

    def write_material(self, f, material):
        black = (0.0, 0.0, 0.0)
        f.write(f"    // Material: {material.name}\n")

        def print_material(mat, color, extra=''):
            c = color_to_rgb15(color)
            f.write(f"    glMaterialf({mat}, {c}{extra});\n")
        print_material('GL_DIFFUSE',
                       material.diffuse if material.diffuse_on else black)
        print_material('GL_AMBIENT',
                       material.ambient if material.ambient_on else black)
        if material.highlight_on:
            print_material('GL_SPECULAR', material.specular, ' | BIT(15)')
        else:
            print_material('GL_SPECULAR', black)
        if material.emission_on:
            color = material.emission if material.emission != black \
                    else material.diffuse
        else:
            color = black
        print_material('GL_EMISSION', color)

        # We don't use glPolyFmt(POLY_ALPHA(d), ...) for the transparency, as
        # it requires us to know the scene settings (such as which lights
        # should be enabled. It seems to be a method better suited for the game
        # developer to set the opacity on whole objects. We will use a texture
        # instead.
        obj = self.current_object
        obj_name = self.escape(obj.name)
        tex_array_name = self.prefix + '_' + obj_name + '_texture_names'
        if material.texture_idx is not None:
            ti = material.texture_idx
            f.write(f"    glBindTexture(0, {tex_array_name}[{ti}]);\n")
        else:
            f.write("    glBindTexture(0, 0);\n")
