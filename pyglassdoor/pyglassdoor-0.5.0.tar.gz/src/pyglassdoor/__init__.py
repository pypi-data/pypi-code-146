"""

A simple API for glassdoor.com

All methods require at least the `company_id`, which is the unique
identifier for each company on glassdoor.com. The most straight-forward way
to find this number is the company url on glassdoor.com.

For example, the ``company_id`` for **Apple** is **1138** which we can find in the
urls of the company on glassdoor.com.
Here are the *overview*, *reviews*, *salaries* , and *interviews* pages for apple:

    - https://www.glassdoor.com/Overview/Working-at-Apple-EI_IE1138.11,16.htm
    - https://www.glassdoor.com/Reviews/Apple-Reviews-E1138.htm
    - https://www.glassdoor.com/Salary/Apple-Salaries-E1138.htm
    - https://www.glassdoor.com/Salary/Apple-Salaries-E1138.htm
"""

__version__ = '0.5.0'

__all__ = ['get_session_info', 'get_reviews', 'get_interviews', 'get_salaries']

from .session import get_session_info
from .reviews import get_reviews
from .interviews import get_interviews
from .salaries import get_salaries
