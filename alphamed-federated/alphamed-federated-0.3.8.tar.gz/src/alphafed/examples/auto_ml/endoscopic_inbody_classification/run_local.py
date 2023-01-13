import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir, os.pardir, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)


if True:
    import alphafed  # noqa: F401, setup latest alphafed running context
    from alphafed.auto_ml import from_pretrained
    from alphafed.examples.auto_ml.endoscopic_inbody_classification import (
        AGGREGATOR_ID, DEV_TASK_ID)


if __name__ == '__main__':
    resource_dir = os.path.join(CURRENT_DIR, 'res_local')
    auto_model = from_pretrained(name='endoscopic_inbody_classification',
                                 resource_dir=resource_dir,
                                 download=True)
    auto_model.fine_tune(id=AGGREGATOR_ID,
                         task_id=DEV_TASK_ID,
                         dataset_dir=os.path.join(CURRENT_DIR, 'data'),
                         is_debug_script=True)
    image = os.path.join(CURRENT_DIR, 'data', '53125.jpg')
    predict = auto_model(image)
    print(f'{predict=}')
