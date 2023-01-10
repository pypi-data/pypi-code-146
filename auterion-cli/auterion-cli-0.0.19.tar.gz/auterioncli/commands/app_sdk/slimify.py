import argparse
import pathlib
import sys
import subprocess
import json
import tarfile
import os
import hashlib
import tempfile
import shutil


def run_docker_command(command, json_out=True):
    ret = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ret.returncode != 0:
        print(ret.stderr.decode(), file=sys.stderr)
        raise RuntimeError(f'Command {str(command)} failed with exit code {ret.returncode}.')

    return json.loads(ret.stdout.decode()) if json_out else ret.stdout.decode()


def delete_from_tar_file(file, files_to_delete):
    temp_dir = tempfile.mkdtemp()
    with tarfile.open(file, 'r') as f:
        f.extractall(temp_dir)

    for delete_file in files_to_delete:
        os.remove(os.path.join(temp_dir, delete_file))

    with tarfile.open(file, 'w') as f:
        for file_to_add in pathlib.Path(temp_dir).rglob('*'):
            f.add(file_to_add, file_to_add.relative_to(temp_dir))
    shutil.rmtree(temp_dir)


def error(msg, code=1):
    print(msg, file=sys.stderr)
    exit(code)


def get_file_size_mb(path):
    file_stats = os.stat(path)
    return file_stats.st_size / (1024*1024)


def get_base_image_layers(base_image, cache_dir):
    cache_key = 'slimify_' + hashlib.sha1(base_image.encode()).hexdigest() + '.json'
    if cache_dir is not None:
        cache_file = os.path.join(cache_dir, cache_key)
        if os.path.exists(os.path.join(cache_dir, cache_key)):
            print(f'.. Found cached base layer information for {base_image}')
            with open(cache_file, 'r') as f:
                return json.load(f)

    print(f'> Fetching manifest for {base_image}')
    ret = {}
    try:
        ret = run_docker_command(['docker', 'manifest', 'inspect', base_image])
    except:
        error(f'Could not fetch manifest for image {base_image}. Aborting...')

    manifests = ret['manifests']
    arm64_digest = next(d['digest'] for d in manifests if 'arm64' in d['platform']['architecture'])
    print(f'.. arm64 image digest for {base_image} is {arm64_digest}')
    print(f'> Pulling arm64 image for {base_image}')
    pull_name = base_image.split(':')[0] + '@' + arm64_digest
    try:
        run_docker_command(['docker', 'pull', pull_name], json_out=False)
    except:
        error(f'Failed to pull {pull_name}. Aborting...')

    print(f'.. Pulled {pull_name}')
    print('> Inspecting image')
    try:
        ret = run_docker_command(['docker', 'inspect', pull_name])
    except:
        error(f'Failed to inspect image {pull_name}. Aborting..')

    layers = ret[0]['RootFS']['Layers']
    print(f'.. Base image has {len(layers)} layers')

    if cache_dir is not None:
        cache_file = os.path.join(cache_dir, cache_key)
        with open(cache_file, 'w') as f:
            json.dump(layers, f)

    return layers


def slimify(save_image_path, base_image, cache_dir=None):
    base_layers = get_base_image_layers(base_image, cache_dir)
    with tarfile.open(save_image_path) as f:
        manifest_file = f.extractfile(f.getmember('manifest.json'))
        manifest = json.load(manifest_file)
        layer_entry_map = {}
        for image_information in manifest:
            image_layer_entries = image_information['Layers']
            config_name = image_information['Config']
            config_file = f.extractfile(f.getmember(config_name))
            config = json.load(config_file)
            assert(config['architecture'] == 'arm64')
            image_layers = config['rootfs']['diff_ids']
            image_layer_entry_map = {digest: (file, file in f.getnames()) for digest, file in
                                     zip(image_layers, image_layer_entries)}
            layer_entry_map.update(image_layer_entry_map)

    removable_layers = set(layer_entry_map.keys()).intersection(set(base_layers))
    print(f'> Will remove {len(removable_layers)} from app image')
    for l in removable_layers:
        entry, exists = layer_entry_map[l]
        print(f'{l}: entry {entry} ' + ('' if exists else '(already deleted)'))
    files_to_remove = [layer_entry_map[l][0] for l in removable_layers if layer_entry_map[l][1]]

    file_size_pre = get_file_size_mb(save_image_path)
    delete_from_tar_file(save_image_path, files_to_remove)
    file_size_post = get_file_size_mb(save_image_path)
    print(f'.. All done. {file_size_pre:.2f} MB -> {file_size_post:.2f} '
          f'MB ({(file_size_post / file_size_pre * 100):.3f} %)')


def main():
    parser = argparse.ArgumentParser('Remove common common layers from a docker save')
    parser.add_argument('save_image', help='The saved docker artifact tar file')
    parser.add_argument('--base', '-b', help='The common base to remove layers from', required=True)
    args = parser.parse_args()
    slimify(args.save_image, args.base)


if __name__ == '__main__':
    main()

