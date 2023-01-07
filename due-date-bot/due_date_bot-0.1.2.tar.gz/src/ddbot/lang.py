from collections import defaultdict
from typing import Dict


class Locale:
    welcome: str
    help: str
    schedule_daily: str
    schedule_weekly: str
    message: str
    schedule_cleared: str


class English(Locale):

    welcome = "Hello there!"
    help = """
Receive daily reminders about your little one.
To set up the reminders, use the */daily* or */weekly* commands.
Use */clear* to stop receiving any messages.
"""
    schedule_daily = "Schedule activated, daily at: {{ time.strftime('%H:%M') }}."
    schedule_weekly = "Schedule activated, weekly from Today at {{ time.strftime('%H:%M') }}."
    schedule_cleared = "Schedule cleared."
    message = """
*{{ p.week }}+{{ p.day }}* | {{ p.elapsed_mm_dd[0] }} months {{ p.elapsed_mm_dd[1] }} days | {{ p.elapsed.days }} days total

I measure *{{ p.size }} cm*
and weigh *{{ p.grams }}g*
 
Still {{ p.remaining.month }} months. and {{ p.remaining.day }} days to go! 👨‍👩‍👶‍🍼
"""


class Czech(English):
    welcome = "Nazdárek!"
    help = """
K nastavení notifikací použij příkazy */daily* a */weekly*.
Pro vypnutí příkaz */clear*.
"""
    schedule_daily = "Notifikace zapnuty, každý den v {{ time.strftime('%H:%M') }}."
    schedule_weekly = "Notifikace zapnuty, 1x týdně ode dneška v {{ time.strftime('%H:%M') }}."
    schedule_cleared = "Vypnuto."
    message = """
*{{ p.week }}+{{ p.day }}* | {{ p.elapsed_mm_dd[0] }} měs. {{ p.elapsed_mm_dd[1] }} dní | {{ p.elapsed.days }} dní

Měřím *{{ p.size }} cm*
a vážím *{{ p.grams }}g*
 
Ještě {{ p.remaining_mm_dd[0] }} měs. a {{ p.remaining_mm_dd[1] }} dní! 👨‍👩‍👶‍🍼
"""


LOCALE: Dict[str, Locale] = defaultdict(English)
LOCALE["en"] = English()
LOCALE["cz"] = Czech()
