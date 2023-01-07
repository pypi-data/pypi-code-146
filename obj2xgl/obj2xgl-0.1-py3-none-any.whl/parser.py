#! /usr/bin/env python
#
# Copyright (c) 2022 Alberto Mardegan <mardy@users.sourceforge.net>
#
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.


import logging
import os.path


log = logging.getLogger("parser")


class ParserException(Exception):
    pass


class Object(object):
    def __init__(self, name):
        self.name = name
        self.faces = []
        # This maps material names with a list of face indexes which use this
        # material. A special key "" is used to group faces with no material.
        self.face_materials = {}
        self.smooth_shading = False

    def __bool__(self):
        return len(self.faces) > 0


class Texture(object):
    def __init__(self, config, line=None):
        self.config = config
        self.blendu = True
        self.blendv = True
        self.cc = False
        self.clamp = False
        self.texres = None
        self.bm = 1.0
        self.boost = 0.0
        self.offset = (0.0, 0.0, 0.0)
        self.scale = (1.0, 1.0, 1.0)
        self.turbolence = (0.0, 0.0, 0.0)
        if line:
            self.parse_texture(line)

    # This function takes the original line as input, as filenames might
    # contain spaces and tabs
    def parse_texture(self, line):
        while line.startswith('-'):
            (opt, line) = line.split(maxsplit=1)
            opt = opt[1:]  # Remove the initial '-'
            if opt in ('blendu', 'blendv', 'cc', 'clamp', 'texres',
                       'bm', 'boost'):
                (value_text, line) = line.split(maxsplit=1)
                if value_text == 'off':
                    value = False
                elif value_text == 'on':
                    value = True
                elif value_text.isdigit():
                    value = int(value_text)
                else:
                    value = float(value_text)
                setattr(self, opt, value)
            elif opt in ('o', 's', 't'):
                (u, v, w, line) = line.split(maxsplit=4)
                opt_names = dict(o='offset', s='scale', t='turbolence')
                value = tuple([float(x) for x in (u, v, w)])
                setattr(self, opt_names[opt], value)
            else:
                log.warning(f'Unsupported texture option {opt}')
        self.filename = line.strip()
        filepath = os.path.join(self.config.input_directory, self.filename) \
            if self.config.input_directory else self.filename

        from PIL import Image
        self.image = Image.open(filepath)


class Material(object):
    def __init__(self, name):
        self.name = name
        self.ambient = (0.0, 0.0, 0.0)
        self.diffuse = (0.0, 0.0, 0.0)
        self.specular = (0.0, 0.0, 0.0)
        self.emission = (0.0, 0.0, 0.0)
        self.transmission = (0.0, 0.0, 0.0)
        self.dissolve_factor = 1.0
        self.specular_exp = 0.0
        self.sharpness = 60
        self.optical_density = 1.0
        self.diffuse_on = False
        self.ambient_on = False
        self.emission_on = False
        self.highlight_on = False
        self.reflection_on = False
        self.ray_trace_on = False
        self.glass_on = False
        self.fresnel_on = False
        self.refraction_on = False
        self.shadows_on = False
        self.ambient_tex = None
        self.diffuse_tex = None
        self.specular_tex = None
        self.emission_tex = None
        self.dissolve_tex = None

    def set_illumination_mode(self, mode):
        modes = {}
        modes[0] = ['emission_on']
        modes[1] = ['diffuse_on', 'ambient_on']
        modes[2] = modes[1] + ['highlight_on']
        modes[3] = modes[2] + ['reflection_on', 'ray_trace_on']
        modes[4] = modes[3] + ['glass_on']
        modes[5] = modes[3] + ['fresnel_on']
        modes[6] = modes[3] + ['refraction_on']
        modes[7] = modes[6] + ['fresnel_on']
        modes[8] = list(filter(lambda x: x != 'ray_trace_on', modes[3]))
        modes[9] = list(filter(lambda x: x != 'ray_trace_on', modes[4]))
        modes[10] = ['shadows_on']
        for attr in modes[mode]:
            setattr(self, attr, True)


class Parser(object):
    def __init__(self, config):
        self.config = config
        self.reset()

    def reset(self):
        infinity = float('inf')
        infinity_m = float('-inf')
        self.max_x = infinity_m
        self.max_y = infinity_m
        self.max_z = infinity_m
        self.min_x = infinity
        self.min_y = infinity
        self.min_z = infinity
        self.objects = []
        self.vertexes = []
        self.normals = []
        self.texcoords = []
        self.materials = {}

    def load(self, lines):
        self.reset()
        current_obj = Object(self.config.name)
        current_material = ""
        for line in lines:
            if line.startswith('#'):
                continue
            parts = line.split()
            if not parts:
                continue
            op, args = parts[0], parts[1:]
            if op == 'v':
                if len(args) < 3 or len(args) > 4:
                    raise ParserException(f"Invalid vertex line: {line}")
                if len(args) < 4:
                    args.append(1.0)
                (x, y, z, w) = [float(x) for x in args]
                self.max_x = max(self.max_x, x)
                self.max_y = max(self.max_y, y)
                self.max_z = max(self.max_z, z)
                self.min_x = min(self.min_x, x)
                self.min_y = min(self.min_y, y)
                self.min_z = min(self.min_z, z)
                self.vertexes.append((x, y, z, w))
            elif op == 'vn':
                if len(args) != 3:
                    raise ParserException(f"Invalid normal line: {line}")
                normal = tuple([float(x) for x in args])
                self.normals.append(normal)
            elif op == 'vt':
                if len(args) != 2:
                    raise ParserException(f"Invalid UV line: {line}")
                uv = tuple([float(x) for x in args])
                self.texcoords.append(uv)
            elif op == 'f':
                if len(args) < 3 or len(args) > 4:
                    raise ParserException(f"Invalid face line: {line}")
                vertexes = [
                        tuple([int(x) if x else None for x in v.split('/')])
                        for v in args]
                o = current_obj
                face_materials = o.face_materials.get(current_material, [])
                if not face_materials:
                    o.face_materials[current_material] = face_materials
                face_materials.append(len(o.faces))
                o.faces.append(vertexes)
            elif op == 'o':
                if current_obj:
                    self.objects.append(current_obj)
                current_obj = Object(args[0])
                log.debug(f'parsing object {args[0]}')
            elif op == 's':
                current_obj.smooth_shading = \
                        False if args[0] in ('0', 'off') else True
            elif op == 'mtllib':
                filepath = os.path.join(self.config.input_directory, args[0])
                with open(filepath, "r") as f:
                    self.load_mtllib(f)
            elif op == 'usemtl':
                current_material = args[0]
            else:
                log.debug(f'read line: {parts}')

        if current_obj:
            self.objects.append(current_obj)

        log.info('Parsed {} vertexes, {} normals'.format(
            len(self.vertexes), len(self.normals)))
        log.info('Geometry range: {} - {} | {} - {} | {} - {}'.format(
            self.min_x, self.max_x,
            self.min_y, self.max_y,
            self.min_z, self.max_z))
        log.info('Parsed objects:')
        for obj in self.objects:
            log.info('- {}: {} faces'.format(obj.name, len(obj.faces)))
            for mat, faces in obj.face_materials.items():
                log.info('  - Material {} on {} faces'.format(mat, len(faces)))

    def load_mtllib(self, lines):
        current_mat = None

        def parse_color(args):
            if len(args) == 1:
                return (float(args[0]),) * 3
            return tuple([float(x) for x in args])

        for line in lines:
            if line.startswith('#'):
                continue
            parts = line.split()
            if not parts:
                continue
            op, args = parts[0], parts[1:]
            if op == 'newmtl':
                name = args[0]
                current_mat = self.materials[name] = Material(name)
            elif op == 'Ka':
                current_mat.ambient = parse_color(args)
            elif op == 'Kd':
                current_mat.diffuse = parse_color(args)
            elif op == 'Ks':
                current_mat.specular = parse_color(args)
            elif op == 'Ke':
                current_mat.emission = parse_color(args)
            elif op == 'Tf':
                current_mat.transmission = parse_color(args)
            elif op == 'Ns':
                current_mat.specular_exp = float(args[0])
            elif op == 'd':
                current_mat.dissolve_factor = float(args[0])
            elif op == 'Tr':
                current_mat.dissolve_factor = 1.0 - float(args[0])
            elif op == 'Ni':
                current_mat.optical_density = float(args[0])
            elif op == 'illum':
                current_mat.set_illumination_mode(int(args[0]))
            elif op == 'map_Ka':
                current_mat.ambient_tex = Texture(self.config, line[7:])
            elif op == 'map_Kd':
                current_mat.diffuse_tex = Texture(self.config, line[7:])
            elif op == 'map_Ks':
                current_mat.specular_tex = Texture(self.config, line[7:])
            elif op == 'map_Ke':
                current_mat.emission_tex = Texture(self.config, line[7:])
            elif op == 'map_d':
                current_mat.dissolve_tex = Texture(self.config, line[6:])
            else:
                log.debug(f'read line: {parts}')
