from pathlib import Path


def extract_random_test_images_from_zip(local_data_dir, export_dir, num_samples: int = 3):
    import zipfile
    import random

    zip_filepath = Path(local_data_dir) / 'data' / 'valid.zip'

    with zipfile.ZipFile(zip_filepath) as zf:
        image_files = zf.namelist()
        image_files.remove('_annotations.coco.json')
        selected_image_files = random.sample(image_files, num_samples)
        for image_file in selected_image_files:
            zf.extract(image_file, path=export_dir)
    
    return export_dir