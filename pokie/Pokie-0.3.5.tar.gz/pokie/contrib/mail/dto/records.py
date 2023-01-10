from rick_db import fieldmapper


@fieldmapper(tablename="message_template", pk="id_message_template", schema="public")
class MessageTemplateRecord:
    id = "id_message_template"
    template = "template"
    language = "language"
    created = "created"
    channel = "channel"
    label = "label"
    subject = "subject"
    body = "body"
    html = "html"
    placeholders = "placeholders"


@fieldmapper(tablename="message_queue", pk="id_message_queue", schema="public")
class MessageQueueRecord:
    id = "id_message_queue"
    created = "created"
    sent = "sent"
    channel = "channel"
    status = "status"
    msg_from = "msg_from"
    msg_to = "msg_to"
    title = "title"
    content = "content"
    html = "html"
