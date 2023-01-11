"""
    This script can be used to copy a collection in firestore from one document
    to another document.

    This is intended for manual operation of the manual_configuration_edit
    collection used for database initialization.
"""
import google.cloud.firestore as firestore


if __name__ == '__main__':
    collection_name = 'manual_configuration_edit'
    document_src = 'config_form'
    subcollection_name = 'jobs'  # Parse from input
    document_dst = 'gao_manual_script'

    db: firestore.Client = firestore.Client()

    # get collection
    # collection = db.collection(f'{collection_name}/{document_src}/{subcollection_name}').get()
    #
    # for doc in collection:
    #     db.collection(f'{collection_name}/{document_dst}/{subcollection_name}').document(doc.id).set(doc.to_dict())

    document = db.document('manual_configuration_edit/gao_manual_script/machines/gao_linea_de_pintura_asset')

    document.update(
        {
            'tasks': {
                'TP_01_SD': {
                    "task_id": "TP_01_SD",
                    "asset_id": "Linea_de_Pintura_GAO",
                    "task_type": "SlicPatchRecognitionTask",
                    "schema": {
                        'TXP-ARMROBOT-001_3e5be60c7a826a1e32eb9913ed11170f': {
                            "Image": {
                                'time': True
                            }
                        }
                    },  # Not relevant for tasks already trained
                    "edges": ['TXP-ARMROBOT-001_3e5be60c7a826a1e32eb9913ed11170f'],
                    "parameters": {
                        "number_of_segments": 40,
                        "image_shape": (640, 480, 3),
                        "thermal_image_shape": (120, 160, 3),
                        "patch_x_y_image": (100, 255),
                        "patch_x_y_thermal": (20, 8),
                        "pandas_cols": ['image', 'label']
                    }
                },
                'TP_02_MD': {
                    "task_id": "TP_02_MD",
                    "asset_id": "Linea_de_Pintura_GAO",
                    "task_type": "SlicPatchRecognitionTask",
                    "schema": {
                        'TXP-ARMROBOT-001_c0fcd732d555d7eb1752f65b83b8e6d5': {
                            "Image": {
                                'time': True
                            }
                        }
                    },  # Not relevant for tasks already trained
                    "edges": ['TXP-ARMROBOT-001_c0fcd732d555d7eb1752f65b83b8e6d5'],
                    "parameters": {
                        "number_of_segments": 40,
                        "image_shape": (640, 480, 3),
                        "thermal_image_shape": (120, 160, 3),
                        "patch_x_y_image": (200, 330),
                        "patch_x_y_thermal": (20, 8),
                        "pandas_cols": ['image', 'label']
                    }
                },
                'TP_03_ID': {
                    "task_id": "TP_03_ID",
                    "asset_id": "Linea_de_Pintura_GAO",
                    "task_type": "SlicPatchRecognitionTask",
                    "schema": {
                        'TXP-ARMROBOT-001_d5bdaeb38990169d310caa3e47b7a951': {
                            "Image": {
                                'time': True
                            }
                        }
                    },  # Not relevant for tasks already trained
                    "edges": ['TXP-ARMROBOT-001_d5bdaeb38990169d310caa3e47b7a951'],
                    "parameters": {
                        "number_of_segments": 40,
                        "image_shape": (640, 480, 3),
                        "thermal_image_shape": (120, 160, 3),
                        "patch_x_y_image": (220, 255),
                        "patch_x_y_thermal": (20, 8),
                        "pandas_cols": ['image', 'label']
                    }
                },
                'SD_01_SC': {
                    "task_id": "SD_01_SC",
                    "asset_id": "Linea_de_Pintura_GAO",
                    "task_type": "SlicPatchRecognitionTask",
                    "schema": {
                        'TXP-ARMROBOT-001_e135617e7c30e4fea19c15d764050d13': {
                            "Image": {
                                'time': True
                            }
                        }
                    },  # Not relevant for tasks already trained
                    "edges": ['TXP-ARMROBOT-001_e135617e7c30e4fea19c15d764050d13'],
                    "parameters": {
                        "number_of_segments": 40,
                        "image_shape": (640, 480, 3),
                        "thermal_image_shape": (120, 160, 3),
                        "patch_x_y_image": (220, 405),
                        "patch_x_y_thermal": (20, 8),
                        "pandas_cols": ['image', 'label']
                    }
                },
                'SD_02_MC': {
                    "task_id": "SD_02_MC",
                    "asset_id": "Linea_de_Pintura_GAO",
                    "task_type": "SlicPatchRecognitionTask",
                    "schema": {
                        'TXP-ARMROBOT-001_edc659ad2449fd102d70d1317446a437': {
                            "Image": {
                                'time': True
                            }
                        }
                    },  # Not relevant for tasks already trained
                    "edges": ['TXP-ARMROBOT-001_edc659ad2449fd102d70d1317446a437'],
                    "parameters": {
                        "number_of_segments": 40,
                        "image_shape": (640, 480, 3),
                        "thermal_image_shape": (120, 160, 3),
                        "patch_x_y_image": (240, 405),
                        "patch_x_y_thermal": (20, 8),
                        "pandas_cols": ['image', 'label']
                    }
                },
                'EMP_01_SI': {
                    "task_id": "EMP_01_SI",
                    "asset_id": "Linea_de_Pintura_GAO",
                    "task_type": "SlicPatchRecognitionTask",
                    "schema": {
                        'TXP-ARMROBOT-001_0a333974dfe6f2a6c55e8846ca5d82ff': {
                            "Image": {
                                'time': True
                            }
                        }
                    },  # Not relevant for tasks already trained
                    "edges": ['TXP-ARMROBOT-001_0a333974dfe6f2a6c55e8846ca5d82ff'],
                    "parameters": {
                        "number_of_segments": 40,
                        "image_shape": (640, 480, 3),
                        "thermal_image_shape": (120, 160, 3),
                        "patch_x_y_image": (70, 130),
                        "patch_x_y_thermal": (20, 8),
                        "pandas_cols": ['image', 'label']
                    }
                },
                'EMP_02_MI': {
                    "task_id": "EMP_02_MI",
                    "asset_id": "Linea_de_Pintura_GAO",
                    "task_type": "SlicPatchRecognitionTask",
                    "schema": {
                        'TXP-ARMROBOT-001_dfd684239c39d781de18751d9c62a72a': {
                            "Image": {
                                'time': True
                            }
                        }
                    },  # Not relevant for tasks already trained
                    "edges": ['TXP-ARMROBOT-001_dfd684239c39d781de18751d9c62a72a'],
                    "parameters": {
                        "number_of_segments": 40,
                        "image_shape": (640, 480, 3),
                        "thermal_image_shape": (120, 160, 3),
                        "patch_x_y_image": (150, 155),
                        "patch_x_y_thermal": (20, 8),
                        "pandas_cols": ['image', 'label']
                    }
                }
            }
        }
    )

    db.close()

    print("Elements successfully copied.")
