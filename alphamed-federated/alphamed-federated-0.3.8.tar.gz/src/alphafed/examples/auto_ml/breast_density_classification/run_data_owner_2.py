import argparse
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)


if True:
    import alphafed  # noqa: F401, setup latest alphafed running context
    from alphafed import logger
    from alphafed.auto_ml import from_pretrained
    from alphafed.examples.auto_ml.breast_density_classification import (
        DATA_OWNER_2_ID, DEV_TASK_ID)


parser = argparse.ArgumentParser(description='Run aggregator demo.')
parser.add_argument('-r', '--recover',
                    type=bool,
                    default=False,
                    help='recover mode: true | false')
args = parser.parse_args()


if __name__ == '__main__':
    resource_dir = os.path.join(CURRENT_DIR, 'res_fed_avg')
    auto_model = from_pretrained(name='breast_density_classification_fed_avg',
                                 resource_dir=resource_dir,
                                 download=True)
    logger.debug(f'{type(auto_model)=}')
    logger.debug(f'{args.recover=}')
    auto_model.fine_tune(id=DATA_OWNER_2_ID,
                         task_id=DEV_TASK_ID,
                         dataset_dir=os.path.join(CURRENT_DIR, 'data'),
                         recover=args.recover)
