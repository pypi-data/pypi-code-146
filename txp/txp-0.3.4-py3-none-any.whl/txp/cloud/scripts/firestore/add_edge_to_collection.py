"""
    This script can be used to add task for machine in firestore.

    This is intended for manual operation of the manual_configuration_edit
    collection used for database initialization.
"""
import google.cloud.firestore as firestore

if __name__ == '__main__':
    collection_name = 'manual_configuration_edit'
    document_src = 'laboratorio_showroom_manual_script'
    subcollection_name = 'edges'
    edge_document = 'beer_demo_spot_2'

    db: firestore.Client = firestore.Client()
    document = db.document(f'{collection_name}/{document_src}/{subcollection_name}/{edge_document}')

    document.set({
        "logical_id": "TXP-ARMROBOT-002_31378a021e68517f2e9b45948521ddbd",
        "device_kind": "ArmRobot",
        "device_type": "ON_OFF_DEVICE",
        "parameters": {
            "physical_id": "TXP-ARMROBOT-002",
            "sensors": [
                {
                    "physical_id": "/dev/v4l/by-id/usb-lihappe8_Corp._USB_2.0_Camera-video-index0",
                    "camera_type": "Normal"
                },
                {
                    "physical_id": "/dev/v4l/by-id/usb-GroupGets_PureThermal__fw:v1.3.0__80180014-5119-3038-3532-373600000000-video-index0",
                    "camera_type": "Thermographic"
                }
            ],
            "virtual_device": {
                "position": [
                    47,
                    23,
                    110,
                    99,
                    86,
                    15
                ],
                "virtual_id_hash": "31378a021e68517f2e9b45948521ddbd"
            }
        },
        "perceptions": {
            "Image": {
                "format": "JPEG",
                "resolution": [
                    640,
                    480
                ],
                "mode": 7
            },
            "ThermalImage": {
                "mode": 7,
                "resolution": [
                    640,
                    480
                ],
                "format": "JPEG"
            }
        }
    })
