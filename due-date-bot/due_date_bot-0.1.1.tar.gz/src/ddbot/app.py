#!/usr/bin/env python

import argparse
import logging
import os
import sys
from datetime import datetime, timedelta

import telegram.ext
import tzlocal
from jinja2 import Template
from telegram import __version__ as TG_VER

from ddbot.lang import LOCALE, Locale
from ddbot.logic import Pregnancy

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]


if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def app(token: str, pregnancy: Pregnancy, locale: Locale) -> telegram.ext.Application:
    application = Application.builder().token(token).build()

    async def send_update(context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send the alarm message."""
        job = context.job
        message = Template(locale.message).render(p=pregnancy)
        await context.bot.send_message(job.chat_id, text=message, parse_mode="Markdown")

    def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Remove job with given name. Returns whether job was removed."""
        if not context.job_queue:
            return False
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_markdown(locale.help)

    # Define bot handlers.
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_markdown(locale.welcome)
        await help_command(update, context)

    async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        chat_id = update.effective_message.chat_id
        remove_job_if_exists(str(chat_id), context)
        await update.message.reply_markdown(locale.schedule_cleared)

    async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_message.chat_id
        remove_job_if_exists(str(chat_id), context)

        run_at = datetime.now(tz=tzlocal.get_localzone()) + timedelta(seconds=1)
        context.job_queue.run_daily(
            send_update,
            time=run_at,
            chat_id=chat_id,
            name=str(chat_id)
        )
        await update.effective_message.reply_markdown(
            Template(locale.schedule_daily).render(time=run_at)
        )

    async def weekly(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_message.chat_id
        job_removed = remove_job_if_exists(str(chat_id), context)

        first = datetime.now(tz=tzlocal.get_localzone()) + timedelta(seconds=1)
        context.job_queue.run_repeating(
            send_update,
            interval=timedelta(days=7),
            first=timedelta(seconds=1),
            chat_id=chat_id,
            name=str(chat_id)
        )
        text = "weekly activated" if not job_removed else "weekly updated"
        text += f"\nFrom Today each week at {first.hour}:{first.minute}"
        await update.effective_message.reply_markdown(Template(locale.schedule_weekly).render(time=first))

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("weekly", weekly))
    application.add_handler(CommandHandler("clear", clear))

    return application


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "date",
        help="Specify a date (see --type option) to calculate the due date. "
             "Accepts ISO format, e.g.: 2022-06-07"
    )
    parser.add_argument("-t", "--type", choices=["due, conception, menstrual"], default="due")
    parser.add_argument("-l", "--lang", choices=LOCALE.keys(), default="en")
    parser.add_argument("--token", default=None)

    args = parser.parse_args()

    token = args.token
    if not token:
        token = os.environ.get("TELEGRAM_TOKEN", None)
    if not token:
        logger.error(
            "Missing Telegram API token. Specify via the 'token' option "
            "or 'TELEGRAM_TOKEN' env var."
        )
        sys.exit(1)

    pregnancy = Pregnancy(due_date=datetime.fromisoformat(args.date))

    application = app(token, pregnancy, LOCALE.get(args.lang))
    application.run_polling()


if __name__ == "__main__":
    main()
