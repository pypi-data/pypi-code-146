"""
    This script can be used to add task for machine in firestore.

    This is intended for manual operation of the manual_configuration_edit
    collection used for database initialization.
"""
import google.cloud.firestore as firestore

if __name__ == '__main__':
    collection_name = 'manual_configuration_edit'
    document_src = 'laboratorio_showroom_manual_script'
    subcollection_name = 'machines'
    machine_document = 'beer_demo'

    db: firestore.Client = firestore.Client()

    # get collection
    document = db.document(f'{collection_name}/{document_src}/{subcollection_name}/{machine_document}')

    document.update({
        'tasks': {
            'beer_spot_1': {
                'task_id': 'beer_spot_1',
                'asset_id': 'Showroom_Fridge',
                'task_type': 'SlicPatchRecognitionTask',
                'schema': {
                    'TXP-ARMROBOT-002_31378a021e68517f2e9b45948521ddbd': {
                        'Image': {
                            'time': True
                        }
                    }
                },
                'edges': ['TXP-ARMROBOT-002_31378a021e68517f2e9b45948521ddbd'],
                'parameters': {
                    'image_shape': [640, 480, 3],
                    'number_of_segments': 40,
                    'pandas_cols': ['image', 'label'],
                    'patch_x_y_image': [128, 82],
                    'patch_x_y_thermal': [20, 8],
                    'thermal_image_shape': [120, 160, 3]
                },
                'label_def': {
                    "labels": [
                        "PresentBeer",
                        "NotPresentBeer"
                    ],
                    "label_to_int": {
                        "PresentBeer": 1,  # Classification 1 True
                        "NotPresentBeer": 0  # Classification 0 False
                    },
                    "int_to_label": {
                        '1': "PresentBeer",
                        '0': "NotPresentBeer"
                    },
                    "label_to_taxonomy": {
                        "PresentBeer": "Harmless",
                        "NotPresentBeer": "Detrimental"
                    }
                }
            },
            'beer_spot_2': {
                'task_id': 'beer_spot_2',
                'asset_id': 'Showroom_Fridge',
                'task_type': 'SlicPatchRecognitionTask',
                'schema': {
                    'TXP-ARMROBOT-002_3271389c2310a31b4f893dbf33054a61': {
                        'Image': {
                            'time': True
                        }
                    }
                },
                'edges': ['TXP-ARMROBOT-002_3271389c2310a31b4f893dbf33054a61'],
                'parameters': {
                    'image_shape': [640, 480, 3],
                    'number_of_segments': 40,
                    'pandas_cols': ['image', 'label'],
                    'patch_x_y_image': [120, 60],
                    'patch_x_y_thermal': [20, 8],
                    'thermal_image_shape': [120, 160, 3]
                },
                'label_def': {
                    "labels": [
                        "PresentBeer",
                        "NotPresentBeer"
                    ],
                    "label_to_int": {
                        "PresentBeer": 1,  # Classification 1 True
                        "NotPresentBeer": 0  # Classification 0 False
                    },
                    "int_to_label": {
                        '1': "PresentBeer",
                        '0': "NotPresentBeer"
                    },
                    "label_to_taxonomy": {
                        "PresentBeer": "Harmless",
                        "NotPresentBeer": "Detrimental"
                    }
                }
            }
        }
    })

