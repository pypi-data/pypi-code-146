from datetime import timedelta

from aleksis.core.celery import app


@app.task(run_every=timedelta(hours=1))
def send_info_mailings() -> None:
    from .models import InfoMailing  # noqa

    for mailing in InfoMailing.get_active_mailings():
        mailing.send()
