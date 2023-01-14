import json
import os
import traceback
from datetime import datetime
from PIL import Image

def load_portrait_hub(json_dir, hub_name):
    hub = {}
    hub_path = os.path.join(json_dir, hub_name)
    if not os.path.exists(hub_path):
        print(f'"{hub_path}": Error. "portrait_hub.json" was not found in this path.')
        os.system('pause')
        exit()
        
    with open(hub_path, 'r', encoding='UTF-8') as hub_data:
        json_hub = json.load(hub_data)
        hub_sprite_list = json_hub['_sprites']
        hub_atlas_list = json_hub['_atlases']

        hub['char_count'] = len(hub_sprite_list)
        hub['sprite_size'] = json_hub['_spriteSize']
        hub['atlases'] = []

        loaded_char_count = 0
        loaded_atlas_count = 0
        for hub_atlas in hub_atlas_list:
            atlas_json_name = hub_atlas.split('/')[-1]
            atlas_json_path = os.path.join(json_dir, f'{atlas_json_name}.json')

            try:
                with open(atlas_json_path, 'r', encoding='UTF-8') as atlas_data:
                    json_atlas = json.load(atlas_data)
                    sprite_list = json_atlas['_sprites']
                    hub['atlases'].append({
                        'atlas_name': json_atlas['_sign']['m_atlases'][0]['name'],
                        'alpha_name': json_atlas['_sign']['m_alphas'][0]['name'],
                        'sprites': sprite_list,
                    })
                    loaded_char_count += len(sprite_list)
                    loaded_atlas_count += 1
            except FileNotFoundError:
                pass
        print(f'Loaded [{loaded_char_count}/{hub["char_count"]}] chars data, from [{loaded_atlas_count}/{len(hub_atlas_list)}] atlas(-es).')

        return hub, loaded_char_count


def crop(tex_dir, out_dir, hub):
    sprite_size = (hub['sprite_size']['width'], hub['sprite_size']['height'])
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    proc_count = 0
    for atlas in hub['atlases']:
        atlas_path = os.path.join(tex_dir, f'{atlas["atlas_name"]}.png')
        alpha_path = os.path.join(tex_dir, f'{atlas["alpha_name"]}.png')

        with Image.open(atlas_path) as atlas_tex:
            with Image.open(alpha_path) as atlas_alpha:
                atlas_alpha = atlas_alpha.convert(mode='L')
                if atlas_alpha.size != atlas_tex.size:
                    atlas_alpha = atlas_alpha.resize(size=atlas_tex.size, resample=Image.BICUBIC)
                atlas_tex.putalpha(atlas_alpha)

                for sprite in atlas['sprites']:
                    char_name = sprite['name']
                    rect = sprite['rect']
                    rotate = sprite['rotate']

                    # Uses flipped Y coord
                    portrait = atlas_tex.crop(box=(rect['x'],  # x
                                                   atlas_tex.height - (rect['y'] + rect['h']),  # y
                                                   rect['x'] + rect['w'],  # width
                                                   atlas_tex.height - rect['y']))  # height
                    if rotate:
                        portrait = portrait.transpose(method=Image.ROTATE_270)
                    if rect['w'] not in sprite_size or rect['h'] not in sprite_size:  # size fix (just in case)
                        temp = Image.new(mode='RGBA', size=sprite_size, color=(1, 1, 1, 0))
                        temp.alpha_composite(im=portrait, dest=(max(sprite_size[0] - portrait.width, 0),
                                                                max(sprite_size[1] - portrait.height, 0)))
                        portrait = temp

                    output_path = os.path.join(out_dir, f'{char_name}.png')

                    portrait.save(output_path, format='PNG', compress_level=7)
                    proc_count += 1
        print(f'Processed "{atlas["atlas_name"]}" atlas.')

    return proc_count


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    date = datetime.date(datetime.now()).isoformat()
    portrait_hub_name = 'portrait_hub.json'

    input_json_path = os.path.join(current_dir, 'MonoBehaviour')
    input_tex_path = os.path.join(current_dir, 'Texture2D')
    output_dir = os.path.join(current_dir, '_output', date)

    try:
        portrait_hub, loaded_portrait_count = load_portrait_hub(input_json_path, portrait_hub_name)
        processed_count = crop(input_tex_path, output_dir, portrait_hub)
        print(f'Processed [{processed_count}/{loaded_portrait_count}] portraits.')
    except Exception as e:
        print(traceback.format_exc())
        
    os.system('pause')
