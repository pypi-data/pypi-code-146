from ftrack_ams.functions import get_ftrack_session


session = get_ftrack_session()
print(session.types.keys())

session.commit()
