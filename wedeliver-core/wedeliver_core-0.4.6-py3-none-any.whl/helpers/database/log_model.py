from sqlalchemy import event, inspect
from sqlalchemy.orm import object_mapper, ColumnProperty

from wedeliver_core import WeDeliverCore, Auth
from wedeliver_core.helpers.kafka_producers.log_model_changes import log_model_changes


def init_log_model():
    app = WeDeliverCore.get_app()
    db = app.extensions['sqlalchemy'].db

    class LogModel(db.Model):
        __abstract__ = True
        __log_column_changes__ = []

    def get_old_value(attribute_state):
        history = attribute_state.history
        return history.deleted[0] if history.deleted else None

    def trigger_attribute_change_events(object_, is_deleted=False, is_added=False):
        column_changes = None
        for mapper_property in object_mapper(object_).iterate_properties:
            if isinstance(mapper_property, ColumnProperty):
                key = mapper_property.key
                watched_columns = dict()
                for wc in object_.__log_column_changes__:
                    column, alias = wc.split(' as ') if ' as ' in wc else [wc, wc]
                    watched_columns[column] = alias

                if key not in watched_columns.keys():
                    continue

                attribute_state = inspect(object_).attrs.get(key)
                history = attribute_state.history

                if history.has_changes():
                    value = attribute_state.value
                    # old_value is None for new objects and old value for dirty objects
                    old_value = get_old_value(attribute_state)
                    if not column_changes:
                        column_changes = []
                    column_changes.append(dict(
                        column=watched_columns[key],
                        from_value=old_value,
                        to_value=value
                    ))
        if is_added or is_deleted or column_changes:
            action_type = 'updated'
            if is_deleted:
                action_type = 'deleted'
            elif is_added:
                action_type = 'added'
            changes = dict(
                created_by=Auth.get_user_str(),
                service_name=app.config.get("SERVICE_NAME"),
                model_name=object_.__tablename__,
                model_instance_id=object_.id,
                column_changes=column_changes,
                action_type=action_type
            )
            log_changes(changes)

    def log_changes(changes):
        log_model_changes(changes)

    def on_after_flush(session, flush_context):
        try:
            deleted_objects = session.deleted
            changed_objects = session.dirty
            new_objects = session.new
            for o in changed_objects:
                if session.is_modified(o, include_collections=True) and hasattr(o,
                                                                                '__log_column_changes__') and o.__log_column_changes__:
                    trigger_attribute_change_events(o)
            for o in deleted_objects:
                if hasattr(o, '__log_column_changes__') and o.__log_column_changes__:
                    trigger_attribute_change_events(o, is_deleted=True)
            for o in new_objects:
                if hasattr(o, '__log_column_changes__') and o.__log_column_changes__:
                    trigger_attribute_change_events(o, is_added=True)
        except Exception as e:
            app.logger.error("error while logging changes: ", str(e))

    event.listen(db.session, "after_flush", on_after_flush)

    return LogModel
