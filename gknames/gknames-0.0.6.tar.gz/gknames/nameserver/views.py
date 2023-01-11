from django.shortcuts import get_object_or_404, render
from gkhtm._gkhtm import htmID
from gkutils.commonutils import coneSearchHTM, FULL, CAT_ID_RA_DEC_COLS, base26, Struct

from .models import *
from django import forms

from django_tables2 import RequestConfig
from django_tables2.utils import A  # alias for Accessor
import django_tables2 as tables2
from datetime import datetime
from django.db import IntegrityError

RADIUS = 3.0 # arcsec
MULTIPLIER = 10000000

# I can't believe that this works! The events table is not part of my long list,
# but we can add it here.
CAT_ID_RA_DEC_COLS['events'] = [['id', 'ra', 'decl'],1017]

# 2021-12-27 KWS Added years 2013 to 2015 for Pan-STARRS.
years = {2013: Y2013,
         2014: Y2014,
         2015: Y2015,
         2016: Y2016,
         2017: Y2017,
         2018: Y2018,
         2019: Y2019,
         2020: Y2020,
         2021: Y2021,
         2022: Y2022,
         2023: Y2023,
         2024: Y2024,
         2025: Y2025,
         2026: Y2026,
         2027: Y2027,
         2028: Y2028,
         2029: Y2029,
         2030: Y2030,
        }


class EventsTable(tables2.Table):
    id = tables2.Column()
    ra = tables2.Column()
    dec = tables2.Column()
    class Meta:
        model = Events
        exclude = []




class AddEventForm(forms.Form):
    internalObjectId = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'size':'20'}))
    internalName = forms.CharField(widget=forms.TextInput(attrs={'size':'20'}))
    ra = forms.FloatField(required=True)
    decl = forms.FloatField(required=True)

    flagDate = forms.DateField(required=False, widget = forms.SelectDateWidget(years=range(2016, 2030)))
    userId = forms.CharField(required=True, widget=forms.TextInput(attrs={'size':'20'}))
    survey_database = forms.CharField(required=True, widget=forms.TextInput(attrs={'size':'20'}))


def eventList(request):
    from django.db import connection
    queryset = Events.objects.all().order_by('id')

    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid(): # All validation rules pass

            ra = form.cleaned_data['ra']
            decl = form.cleaned_data['decl']
            flagDate = form.cleaned_data['flagDate']
            userId = form.cleaned_data['userId']
            internalObjectId = form.cleaned_data['internalObjectId']
            internalName = form.cleaned_data['internalName']
            survey_database = form.cleaned_data['survey_database']
            htm16id = htmID(16,ra,decl)

            if not flagDate:
                flagDate = datetime.now()

            year = flagDate.year
            print(year)

            # Is there an object within RADIUS arcsec of this object?
            message, results = coneSearchHTM(ra, decl, RADIUS, 'events', queryType = FULL, conn = connection, django = True)

            # So - if there are NO matches, insert into the relevant year based
            # on either the flag date OR choose from the current year.
            # But if there ARE matches, shove into the AKAs table with the RA and
            # dec.  We may use this later to recalculate the RA and Dec in the
            # events table.
            if len(results) > 0:
                event = Struct(**results[0][1])
                separation = results[0][0]

                try:
                    aka = Akas(ra = ra,
                               decl = decl,
                               event_id_id = event.id,
                               object_id = internalObjectId,
                               aka = internalName,
                               survey_database = survey_database,
                               user_id = userId,
                               source_ip = None,
                               htm16id = htm16id)  # Field name made lowercase.
                    aka.save()
                except IntegrityError as e:
                    #print(e[0])
                    #if e[0] == 1062: # Duplicate Key error
                    pass # Do nothing - will eventually raise some errors on the form

            else:
                y = years[year](ra = ra,
                                decl = decl,
                                object_id = internalObjectId,
                                survey_database = survey_database,
                                user_id = userId,
                                source_ip = None,
                                htm16id = htm16id)  # Field name made lowercase.
                y.save()
                print(y)

                acquiredId = y.pk
                print(acquiredId)
                suffix = base26(acquiredId - (MULTIPLIER * (year - 2000)))
                print(suffix)
                event = Events(id = acquiredId,
                               ra = ra,
                               decl = decl,
                               ra_original = ra,
                               decl_original = decl,
                               year = year,
                               base26suffix = suffix,
                               htm16id = htm16id)  # Field name made lowercase.

                           #survey_database = survey_database,
                event.save()

                # Add the aka
                aka = Akas(ra = ra,
                           decl = decl,
                           event_id_id = acquiredId,
                           object_id = internalObjectId,
                           aka = internalName,
                           survey_database = survey_database,
                           user_id = userId,
                           source_ip = None,
                           htm16id = htm16id)  # Field name made lowercase.
                aka.save()


    else:
        form = AddEventForm()

    table = EventsTable(queryset, order_by=request.GET.get('sort', '-id'))
    RequestConfig(request, paginate={"per_page": 100}).configure(table)
    return render(request, 'events.html', {'table': table, 'form' : form})

