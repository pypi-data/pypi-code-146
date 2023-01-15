'''
# [kollavarsham](http://kollavarsham.org/)

[![Circle CI Status](https://img.shields.io/circleci/build/github/kollavarsham/kollavarsham-js?label=CircleCI)](https://app.circleci.com/pipelines/github/kollavarsham/kollavarsham-js) [![Coverage Status](https://img.shields.io/coveralls/github/kollavarsham/kollavarsham-js?label=Coveralls)](https://coveralls.io/github/kollavarsham/kollavarsham-js?branch=main) [![GitHub Actions Status](https://github.com/kollavarsham/kollavarsham-js/actions/workflows/ci.yml/badge.svg)](https://github.com/kollavarsham/kollavarsham-js/actions/workflows/ci.yml?query=branch%3Amain) [![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fkollavarsham%2Fkollavarsham-js.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fkollavarsham%2Fkollavarsham-js?ref=badge_shield)

> Convert Gregorian date to Kollavarsham date and vice versa

## Install

### TypeScript/JavaScript/Node.js [![NPM version](https://img.shields.io/npm/v/kollavarsham)](https://www.npmjs.com/package/kollavarsham)

```sh
$ npm install kollavarsham
```

### Python [![PyPI version](https://img.shields.io/pypi/v/kollavarsham)](https://pypi.org/project/kollavarsham/)

```sh
$ pip install kollavarsham
```

### Go [![GitHub go.mod Go version](https://img.shields.io/github/go-mod/go-version/kollavarsham/kollavarsham-go)](https://github.com/kollavarsham/kollavarsham-go)

```sh
go get github.com/kollavarsham/kollavarsham-go/converter
```

### Java [![Maven version](https://img.shields.io/maven-central/v/org.kollavarsham.converter/kollavarsham-converter)](https://search.maven.org/artifact/org.kollavarsham.converter/kollavarsham-converter)

```xml
<dependency>
  <groupId>org.kollavarsham.converter</groupId>
  <artifactId>kollavarsham-converter</artifactId>
  <version>2.0.1</version>
</dependency>
```

### C#/dotnet [![NuGet version](https://img.shields.io/nuget/v/KollavarshamOrg.Converter)](https://www.nuget.org/packages/KollavarshamOrg.Converter)

```sh
$ dotnet add package KollavarshamOrg.Converter
```

## Usage

### TypeScript/JavaScript/Node.js

```js
import { Kollavarsham } from 'kollavarsham';

const options = {
  system: 'SuryaSiddhanta',
  latitude: 10,
  longitude: 76.2
};

const kollavarsham = new Kollavarsham(options);

const today = kollavarsham.fromGregorianDate(new Date());

console.log(today.year, today.mlMasaName, today.date, `(${today.mlNaksatraName})`);
```

### Python

```python
import datetime
import pytz
import kollavarsham

now = pytz.utc.localize(datetime.datetime.utcnow())
kv = kollavarsham.Kollavarsham(latitude=10, longitude=76.2, system="SuryaSiddhanta")

today = kv.from_gregorian_date(date=now)
print(today.year, today.ml_masa_name, today.date, '(' + today.naksatra.ml_malayalam + ')')
```

### Java

```java
package org.kollavarsham.tester;

import java.time.Instant;

import org.kollavarsham.converter.Kollavarsham;
import org.kollavarsham.converter.KollavarshamDate;
import org.kollavarsham.converter.Settings;
import org.kollavarsham.converter.Settings.Builder;

public class App {
    public static void main( final String[] args) {
        final Settings settings = new Builder().latitude(10).longitude(76.2).system("SuryaSiddhanta").build();
        final Kollavarsham kv = new Kollavarsham(settings);
        final KollavarshamDate today = kv.fromGregorianDate(Instant.now());
        System.out.println( today.getYear() + today.getMlMasaName() + today.getDate() + '(' + today.getMlNaksatraName() + ')' );
    }
}
```

### C#/dotnet

```csharp
using System;

namespace KollavarshamOrg.Tester
{
    class Program
    {
        static void Main(string[] args)
        {
            var settings = new Settings {
                Latitude = 10,
                Longitude = 76.2,
                System = "SuryaSiddhanta"
            };
            var kv = new Kollavarsham(settings);
            var today = kv.FromGregorianDate(DateTime.Now);
            Console.WriteLine($"{today.Year.ToString()} {today.MlMasaName} {today.Date.ToString()} ({today.MlNaksatraName})");
        }
    }
}
```

## Documentation

### TypeScript/JavaScript/Node.js

Check out the [Kollavarsham class](https://kollavarsham.org/kollavarsham-js/module-kollavarsham.Kollavarsham.html) within the API documentation as this is the entry point into the library.

## Release History

Check out the history at [GitHub Releases](https://github.com/kollavarsham/kollavarsham-js/releases)

## License

Copyright (c) 2014-2023 The Kollavarsham Team. Licensed under the [MIT license](http://kollavarsham.org/LICENSE.txt).

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fkollavarsham%2Fkollavarsham-js.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fkollavarsham%2Fkollavarsham-js?ref=badge_large)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *


class BaseDate(metaclass=jsii.JSIIAbstractClass, jsii_type="kollavarsham.BaseDate"):
    '''Serves as the base class for both the {@link JulianDate} and {@link KollavarshamDate} classes.

    **INTERNAL/PRIVATE**

    :class: BaseDate
    :constructor: true
    '''

    def __init__(
        self,
        year: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        date: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param year: -
        :param month: -
        :param date: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6e97f50903b9cd74239dde7e21d1838ea4fe810e0db021660357fb91c91a2d)
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument date", value=date, expected_type=type_hints["date"])
        jsii.create(self.__class__, self, [year, month, date])

    @jsii.member(jsii_name="getMasaName")
    @builtins.classmethod
    def get_masa_name(cls, masa_number: jsii.Number) -> "MasaName":
        '''Returns the month names object that has Saka, Saura and Kollavarsham (English & Malayalam) month names for the specified index ``masaNumber``.

        :param masa_number: -

        :for: BaseDate
        :method: getMasaName
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82e165f4943f71969fe40ed603bec10036b16723e1145116e8b7b58faa8740a)
            check_type(argname="argument masa_number", value=masa_number, expected_type=type_hints["masa_number"])
        return typing.cast("MasaName", jsii.sinvoke(cls, "getMasaName", [masa_number]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Converts the Date to a nicely formatted string with year, month and date.

        :for: BaseDate
        :method: toString
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="mlWeekdayName")
    def ml_weekday_name(self) -> builtins.str:
        '''Returns the weekday (in Malayalam) for the current instance of date.

        :property: mlWeekdayName
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "mlWeekdayName"))

    @builtins.property
    @jsii.member(jsii_name="sauraMasaName")
    def saura_masa_name(self) -> builtins.str:
        '''Returns the Saura Masa name for the current instance of date.

        :property: sauraMasaName
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "sauraMasaName"))

    @builtins.property
    @jsii.member(jsii_name="weekdayName")
    def weekday_name(self) -> builtins.str:
        '''Returns the weekday (in English) for the current instance of date.

        :property: weekdayName
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "weekdayName"))

    @builtins.property
    @jsii.member(jsii_name="ahargana")
    def ahargana(self) -> jsii.Number:
        '''The ``Ahargana`` corresponding to this instance of the date. **Set separately after an instance is created**.

        In Sanskrit ``ahoratra`` means one full day and ``gana`` means count.
        Hence, the Ahargana on any given day stands for the number of lunar days that have elapsed starting from an epoch.

        *Source*: http://cs.annauniv.edu/insight/Reading%20Materials/astro/sharptime/ahargana.htm

        :property: ahargana
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "ahargana"))

    @ahargana.setter
    def ahargana(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da1558e262c60ebc25b2aa43d27e3758a53d58bbfa8dffa7b5a84206c355c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ahargana", value)

    @builtins.property
    @jsii.member(jsii_name="date")
    def date(self) -> jsii.Number:
        '''The date corresponding to this instance of the date.

        :property: date
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "date"))

    @date.setter
    def date(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2d1073bad9be7b2e5c227742236b69c7337c2275019db987c99d586fee67ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "date", value)

    @builtins.property
    @jsii.member(jsii_name="gregorianDate")
    def gregorian_date(self) -> datetime.datetime:
        '''The gregorian date corresponding to this instance of the date.

        **Set separately after an instance is created**

        :property: gregorianDate
        :type: {Date}
        '''
        return typing.cast(datetime.datetime, jsii.get(self, "gregorianDate"))

    @gregorian_date.setter
    def gregorian_date(self, value: datetime.datetime) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e3cfb21709f1080cdfba65dcbd4e43dc3b53a0027e0bc2ac4eeb04ac875578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gregorianDate", value)

    @builtins.property
    @jsii.member(jsii_name="julianDay")
    def julian_day(self) -> jsii.Number:
        '''The ``Julian Day`` corresponding to this instance of the date.

        **Set separately after an instance is created**
        Julian day is the continuous count of days since the beginning of the Julian Period used primarily by astronomers.

        *Source*: https://en.wikipedia.org/wiki/Julian_day

        :property: julianDay
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "julianDay"))

    @julian_day.setter
    def julian_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1b43bf4035e1ce4bf13141770107284f620acca35b4991fdb3926ea6c51e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "julianDay", value)

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        '''The month corresponding to this instance of the date.

        :property: month
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0159473ee8dd6dd79117fe5a3e237c5fd01b017a594cbeedca0758dd2f27d823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value)

    @builtins.property
    @jsii.member(jsii_name="naksatra")
    def naksatra(self) -> "Naksatra":
        return typing.cast("Naksatra", jsii.get(self, "naksatra"))

    @naksatra.setter
    def naksatra(self, value: "Naksatra") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c58d6363095ff9e265447917b98240cbe37232df2e76ee450d02670090358f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "naksatra", value)

    @builtins.property
    @jsii.member(jsii_name="sauraDivasa")
    def saura_divasa(self) -> jsii.Number:
        '''The ``Saura Divasa`` (Solar Calendar Day) for this instance of the date.

        **Set separately after an instance is created**

        :property: sauraDivasa
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "sauraDivasa"))

    @saura_divasa.setter
    def saura_divasa(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0eca6e1d55e6e165eaf4c8eb4dd655f17a30784d61fc63ecd6f75f4e92a8e4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sauraDivasa", value)

    @builtins.property
    @jsii.member(jsii_name="sauraMasa")
    def saura_masa(self) -> jsii.Number:
        '''The ``Saura Masa`` (Solar Calendar Month) for this instance of the date.

        **Set separately after an instance is created**

        :property: sauraMasa
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "sauraMasa"))

    @saura_masa.setter
    def saura_masa(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0d827e8883903d5a9008fdbc504d1013e3e1686322e202303adbdf1695684b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sauraMasa", value)

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        '''The year corresponding to this instance of the date.

        :property: year
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200decd0802fd6b2af516536bc47a3f1144c7b0ae74e69d873af0eced7339337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value)


class _BaseDateProxy(BaseDate):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BaseDate).__jsii_proxy_class__ = lambda : _BaseDateProxy


class JulianDate(
    BaseDate,
    metaclass=jsii.JSIIMeta,
    jsii_type="kollavarsham.JulianDate",
):
    '''Represents a Julian date's year, month and day ``toGregorianDateFromSaka`` method of the {@link Kollavarsham} class returns an instance of this type for dates older than ``1st January 1583 AD``.

    **INTERNAL/PRIVATE**

    :class: JulianDate
    :constructor: true
    :extends: BaseDate
    '''

    def __init__(
        self,
        year: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        day: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param year: -
        :param month: -
        :param day: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12abbeffe6a3d7a3e3652115617a18f9118147b92fb3ad460595d749b089908e)
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
        jsii.create(self.__class__, self, [year, month, day])


class Kollavarsham(metaclass=jsii.JSIIMeta, jsii_type="kollavarsham.Kollavarsham"):
    '''The Kollavarsham class implements all the public APIs of the library.

    Create a new instance of this class, passing in the relevant options and call methods on the instance.

    :class: Kollavarsham
    :constructor: true

    Example::

        const Kollavarsham = require('kollavarsham');
        
        const options = {
         system: 'SuryaSiddhanta',
         latitude: 10,
         longitude: 76.2
        };
        
        const kollavarsham = new Kollavarsham(options);
        
        let todayInMalayalamEra = kollavarsham.fromGregorianDate(new Date());
        
        let today = kollavarsham.toGregorianDate(todayInMalayalamEra);  // Not implemented yet
    '''

    def __init__(
        self,
        *,
        latitude: jsii.Number,
        longitude: jsii.Number,
        system: builtins.str,
    ) -> None:
        '''
        :param latitude: 
        :param longitude: 
        :param system: 
        '''
        options = Settings(latitude=latitude, longitude=longitude, system=system)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="fromGregorianDate")
    def from_gregorian_date(self, date: datetime.datetime) -> "KollavarshamDate":
        '''Converts a Gregorian date to the equivalent Kollavarsham date, respecting the current configuration.

        :param date: The Gregorian date to be converted to Kollavarsham.

        :return: Converted date

        :for: Kollavarsham
        :method: fromGregorianDate

        Example::

            const Kollavarsham = require('Kollavarsham');
            const kollavarsham = new Kollavarsham();
            let today = kollavarsham.fromGregorianDate(new Date(1979, 4, 22));
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f913a1bc1b2f476c2f01f6019bccc4f967f77ccb830e0a3e87951c2539ec9b7)
            check_type(argname="argument date", value=date, expected_type=type_hints["date"])
        return typing.cast("KollavarshamDate", jsii.invoke(self, "fromGregorianDate", [date]))

    @jsii.member(jsii_name="toGregorianDate")
    def to_gregorian_date(self, date: "KollavarshamDate") -> datetime.datetime:
        '''Converts a Kollavarsham date (an instance of {@link kollavarshamDate}) to its equivalent Gregorian date, respecting the current configuration.

        This method Will return {@link JulianDate} object for any date before 1st January 1583 AD and
        `Date <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date>`_ objects for later dates.

        **This API has not been implemented yet**

        :param date: The Kollavarsham date to be converted to Gregorian.

        :return: Converted date

        :for: Kollavarsham
        :method: toGregorianDate
        :throws: **"When the API is implemented, will convert <date>"**
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624aa6f72bd374aac935f84402cd9996285a488a2d46785282c8adc5c3feb8bc)
            check_type(argname="argument date", value=date, expected_type=type_hints["date"])
        return typing.cast(datetime.datetime, jsii.invoke(self, "toGregorianDate", [date]))

    @jsii.member(jsii_name="toGregorianDateFromSaka")
    def to_gregorian_date_from_saka(self, saka_date: "SakaDate") -> "KollavarshamDate":
        '''Converts a Saka date (an instance of {@link sakaDate}) to its equivalent Gregorian date, respecting the current configuration.

        This method Will return {@link JulianDate} object for any date before 1st January 1583 AD and
        `Date <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date>`_ objects for later dates.

        :param saka_date: The Saka date to be converted to Gregorian.

        :return: Converted date

        :for: Kollavarsham
        :method: toGregorianDateFromSaka
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a50cb588f473c22a0d86f095b47c141f40d3741e093fa57660d94559244f108)
            check_type(argname="argument saka_date", value=saka_date, expected_type=type_hints["saka_date"])
        return typing.cast("KollavarshamDate", jsii.invoke(self, "toGregorianDateFromSaka", [saka_date]))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "Settings":
        return typing.cast("Settings", jsii.get(self, "settings"))

    @settings.setter
    def settings(self, value: "Settings") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75596cff9789fcfbfa397fae95dedd0d43300bc45cde0c431940b222df074bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "settings", value)


class KollavarshamDate(
    BaseDate,
    metaclass=jsii.JSIIMeta,
    jsii_type="kollavarsham.KollavarshamDate",
):
    '''Represents a Kollavarsham date's year, month and date.

    :class: KollavarshamDate
    :constructor: true
    :extends: BaseDate
    '''

    def __init__(
        self,
        year: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        day: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param year: -
        :param month: -
        :param day: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5254f0964e14ee3edac9844ad3e5eff2bb8e73b7b7c8975373eeeaee278df2)
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
        jsii.create(self.__class__, self, [year, month, day])

    @builtins.property
    @jsii.member(jsii_name="masaName")
    def masa_name(self) -> builtins.str:
        '''Returns the Kollavarsham month name (in English) for this instance of date.

        :property: masaName
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "masaName"))

    @builtins.property
    @jsii.member(jsii_name="mlMasaName")
    def ml_masa_name(self) -> builtins.str:
        '''Returns the Kollavarsham month name (in Malayalam) for this instance of date.

        :property: mlMasaName
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "mlMasaName"))

    @builtins.property
    @jsii.member(jsii_name="mlNaksatraName")
    def ml_naksatra_name(self) -> builtins.str:
        '''Returns the Kollavarsham Naksatra name (in Malayalam) for this instance of date.

        :property: mlNaksatraName
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "mlNaksatraName"))

    @builtins.property
    @jsii.member(jsii_name="naksatraName")
    def naksatra_name(self) -> builtins.str:
        '''Returns the Kollavarsham Naksatra name (in English) for this instance date.

        :property: naksatraName
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "naksatraName"))

    @builtins.property
    @jsii.member(jsii_name="sakaDate")
    def saka_date(self) -> "SakaDate":
        return typing.cast("SakaDate", jsii.get(self, "sakaDate"))

    @saka_date.setter
    def saka_date(self, value: "SakaDate") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d79793967dd0b6cbbebdd629d2838bc38e489e3c8e46d5e0c885289426f7b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sakaDate", value)


@jsii.data_type(
    jsii_type="kollavarsham.MasaName",
    jsii_struct_bases=[],
    name_mapping={
        "en_malayalam": "enMalayalam",
        "ml_malayalam": "mlMalayalam",
        "saka": "saka",
        "saura": "saura",
    },
)
class MasaName:
    def __init__(
        self,
        *,
        en_malayalam: builtins.str,
        ml_malayalam: builtins.str,
        saka: builtins.str,
        saura: builtins.str,
    ) -> None:
        '''
        :param en_malayalam: 
        :param ml_malayalam: 
        :param saka: 
        :param saura: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd87ecc792f84d7c42065b88c5ef770243ed1014e29e103973841aaea1d363e)
            check_type(argname="argument en_malayalam", value=en_malayalam, expected_type=type_hints["en_malayalam"])
            check_type(argname="argument ml_malayalam", value=ml_malayalam, expected_type=type_hints["ml_malayalam"])
            check_type(argname="argument saka", value=saka, expected_type=type_hints["saka"])
            check_type(argname="argument saura", value=saura, expected_type=type_hints["saura"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "en_malayalam": en_malayalam,
            "ml_malayalam": ml_malayalam,
            "saka": saka,
            "saura": saura,
        }

    @builtins.property
    def en_malayalam(self) -> builtins.str:
        result = self._values.get("en_malayalam")
        assert result is not None, "Required property 'en_malayalam' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ml_malayalam(self) -> builtins.str:
        result = self._values.get("ml_malayalam")
        assert result is not None, "Required property 'ml_malayalam' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def saka(self) -> builtins.str:
        result = self._values.get("saka")
        assert result is not None, "Required property 'saka' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def saura(self) -> builtins.str:
        result = self._values.get("saura")
        assert result is not None, "Required property 'saura' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MasaName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kollavarsham.Naksatra",
    jsii_struct_bases=[],
    name_mapping={
        "en_malayalam": "enMalayalam",
        "ml_malayalam": "mlMalayalam",
        "saka": "saka",
    },
)
class Naksatra:
    def __init__(
        self,
        *,
        en_malayalam: builtins.str,
        ml_malayalam: builtins.str,
        saka: builtins.str,
    ) -> None:
        '''
        :param en_malayalam: 
        :param ml_malayalam: 
        :param saka: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836a8c71e9c12fb33be6a8890029dedeb6197bff6d8172a87571e851136d6011)
            check_type(argname="argument en_malayalam", value=en_malayalam, expected_type=type_hints["en_malayalam"])
            check_type(argname="argument ml_malayalam", value=ml_malayalam, expected_type=type_hints["ml_malayalam"])
            check_type(argname="argument saka", value=saka, expected_type=type_hints["saka"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "en_malayalam": en_malayalam,
            "ml_malayalam": ml_malayalam,
            "saka": saka,
        }

    @builtins.property
    def en_malayalam(self) -> builtins.str:
        result = self._values.get("en_malayalam")
        assert result is not None, "Required property 'en_malayalam' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ml_malayalam(self) -> builtins.str:
        result = self._values.get("ml_malayalam")
        assert result is not None, "Required property 'ml_malayalam' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def saka(self) -> builtins.str:
        result = self._values.get("saka")
        assert result is not None, "Required property 'saka' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Naksatra(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SakaDate(BaseDate, metaclass=jsii.JSIIMeta, jsii_type="kollavarsham.SakaDate"):
    '''Represents an Saka date's year, month and paksa and tithi.

    :class: SakaDate
    :constructor: true
    :extends: BaseDate
    '''

    def __init__(
        self,
        year: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        tithi: typing.Optional[jsii.Number] = None,
        paksa: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param year: -
        :param month: -
        :param tithi: -
        :param paksa: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3ac1e3a46d48a00c23d9e0fcf39e5e3e9a7bfd805a6c1d82137fe7a2c63500)
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument tithi", value=tithi, expected_type=type_hints["tithi"])
            check_type(argname="argument paksa", value=paksa, expected_type=type_hints["paksa"])
        jsii.create(self.__class__, self, [year, month, tithi, paksa])

    @jsii.member(jsii_name="generateKollavarshamDate")
    def generate_kollavarsham_date(self) -> KollavarshamDate:
        '''Generates an instance of {@link KollavarshamDate} from this instance of SakaDate.

        :for: SakaDate
        :method: generateKollavarshamDate
        '''
        return typing.cast(KollavarshamDate, jsii.invoke(self, "generateKollavarshamDate", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Converts the Date to a nicely formatted string with year, month and date.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="masaName")
    def masa_name(self) -> builtins.str:
        '''Returns the month name for this instance of SakaDate.

        :property: masaName
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "masaName"))

    @builtins.property
    @jsii.member(jsii_name="naksatraName")
    def naksatra_name(self) -> builtins.str:
        '''Returns the Saka Naksatra name for this instance of SakaDate.

        :property: naksatraName
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "naksatraName"))

    @builtins.property
    @jsii.member(jsii_name="sakaYear")
    def saka_year(self) -> jsii.Number:
        '''Returns the Saka year on this instance of SakaDate (same as the underlyiung ``year`` property from the {@link BaseDate} class).

        :property: sakaYear
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "sakaYear"))

    @builtins.property
    @jsii.member(jsii_name="tithi")
    def tithi(self) -> jsii.Number:
        '''Returns the Tithi on this instance of SakaDate (same as the underlyiung ``date`` property from the {@link BaseDate} class).

        In Vedic timekeeping, a tithi (also spelled thithi) is a lunar day, or the time it takes for the longitudinal angle between the Moon and the Sun to increase by 12°.
        Tithis begin at varying times of day and vary in duration from approximately 19 to approximately 26 hours.

        *Source*: https://en.wikipedia.org/wiki/Tithi

        :property: tithi
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "tithi"))

    @builtins.property
    @jsii.member(jsii_name="vikramaYear")
    def vikrama_year(self) -> jsii.Number:
        '''Returns the Vikrama year corresponding to the Saka year of this instance.

        :property: vikramaYear
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "vikramaYear"))

    @builtins.property
    @jsii.member(jsii_name="adhimasa")
    def adhimasa(self) -> builtins.str:
        '''The Adhimasa (``Adhika Masa``) prefix corresponding to this instance of the date.

        **Set separately after an instance is created**

        :property: adhimasa
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "adhimasa"))

    @adhimasa.setter
    def adhimasa(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583ca71b4333d0a38d5efb4872190078e28aea65913c206a979d1399cef179ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adhimasa", value)

    @builtins.property
    @jsii.member(jsii_name="fractionalTithi")
    def fractional_tithi(self) -> jsii.Number:
        '''The fractional ``Tithi``corresponding to this instance of the date.

        **Set separately after an instance is created**

        :property: fractionalTithi
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "fractionalTithi"))

    @fractional_tithi.setter
    def fractional_tithi(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502984095c2a17e33bc58fd17ba0fc7c7d78a464cc1ca7fd35e3fc24eb6e389b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fractionalTithi", value)

    @builtins.property
    @jsii.member(jsii_name="kaliYear")
    def kali_year(self) -> jsii.Number:
        '''The Kali year corresponding to this instance of the date.

        **Set separately after an instance is created**

        :property: kaliYear
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "kaliYear"))

    @kali_year.setter
    def kali_year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839cf7c7def6891526308e4e5397dd52e0a19cf1e8c930b709e8e5d7304099f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kaliYear", value)

    @builtins.property
    @jsii.member(jsii_name="originalAhargana")
    def original_ahargana(self) -> jsii.Number:
        '''The original ahargana passed in to the celestial calculations (TODO: Not sure why we need this!?).'''
        return typing.cast(jsii.Number, jsii.get(self, "originalAhargana"))

    @original_ahargana.setter
    def original_ahargana(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca0ff9143c49a0a7466cf3bb3ae81e0b165dfd6197e90dbf6ecb8b8fd630d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originalAhargana", value)

    @builtins.property
    @jsii.member(jsii_name="paksa")
    def paksa(self) -> builtins.str:
        '''The Paksha/Paksa corresponding to this instance of the date.

        Paksha (or pakṣa: Sanskrit: पक्ष), refers to a fortnight or a lunar phase in a month of the Hindu lunar calendar.

        *Source*: https://en.wikipedia.org/wiki/Paksha

        :property: paksa
        :type: {string}
        '''
        return typing.cast(builtins.str, jsii.get(self, "paksa"))

    @paksa.setter
    def paksa(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652b126474ae0721fbcc4d0f5d3d6ec68ab3a83f2e757a56d166caa564cdefa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paksa", value)

    @builtins.property
    @jsii.member(jsii_name="sunriseHour")
    def sunrise_hour(self) -> jsii.Number:
        '''The hour part from the sunrise time for this date.

        **Set separately after an instance is created**

        :property: sunriseHour
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "sunriseHour"))

    @sunrise_hour.setter
    def sunrise_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11e3a9b66c25d72b81586619167456a4449559d2972a1fb4540f23c6a8db0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sunriseHour", value)

    @builtins.property
    @jsii.member(jsii_name="sunriseMinute")
    def sunrise_minute(self) -> jsii.Number:
        '''The minute part from the sunrise time for this date.

        **Set separately after an instance is created**

        :property: sunriseMinute
        :type: {Number}
        '''
        return typing.cast(jsii.Number, jsii.get(self, "sunriseMinute"))

    @sunrise_minute.setter
    def sunrise_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a311ead849a592248bb7c7ad3bcea95f3c8a4a9c42d8b494061868b2c4a91424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sunriseMinute", value)


@jsii.data_type(
    jsii_type="kollavarsham.Settings",
    jsii_struct_bases=[],
    name_mapping={
        "latitude": "latitude",
        "longitude": "longitude",
        "system": "system",
    },
)
class Settings:
    def __init__(
        self,
        *,
        latitude: jsii.Number,
        longitude: jsii.Number,
        system: builtins.str,
    ) -> None:
        '''
        :param latitude: 
        :param longitude: 
        :param system: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6bcd9021ac3f0d388ed596fb008a510f8dba66c8f1fc985c3091e925a7d2662)
            check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
            check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            check_type(argname="argument system", value=system, expected_type=type_hints["system"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "latitude": latitude,
            "longitude": longitude,
            "system": system,
        }

    @builtins.property
    def latitude(self) -> jsii.Number:
        result = self._values.get("latitude")
        assert result is not None, "Required property 'latitude' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def longitude(self) -> jsii.Number:
        result = self._values.get("longitude")
        assert result is not None, "Required property 'longitude' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def system(self) -> builtins.str:
        result = self._values.get("system")
        assert result is not None, "Required property 'system' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Settings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BaseDate",
    "JulianDate",
    "Kollavarsham",
    "KollavarshamDate",
    "MasaName",
    "Naksatra",
    "SakaDate",
    "Settings",
]

publication.publish()

def _typecheckingstub__0a6e97f50903b9cd74239dde7e21d1838ea4fe810e0db021660357fb91c91a2d(
    year: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    date: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82e165f4943f71969fe40ed603bec10036b16723e1145116e8b7b58faa8740a(
    masa_number: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da1558e262c60ebc25b2aa43d27e3758a53d58bbfa8dffa7b5a84206c355c3c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2d1073bad9be7b2e5c227742236b69c7337c2275019db987c99d586fee67ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e3cfb21709f1080cdfba65dcbd4e43dc3b53a0027e0bc2ac4eeb04ac875578(
    value: datetime.datetime,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1b43bf4035e1ce4bf13141770107284f620acca35b4991fdb3926ea6c51e43(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0159473ee8dd6dd79117fe5a3e237c5fd01b017a594cbeedca0758dd2f27d823(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c58d6363095ff9e265447917b98240cbe37232df2e76ee450d02670090358f(
    value: Naksatra,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0eca6e1d55e6e165eaf4c8eb4dd655f17a30784d61fc63ecd6f75f4e92a8e4a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0d827e8883903d5a9008fdbc504d1013e3e1686322e202303adbdf1695684b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200decd0802fd6b2af516536bc47a3f1144c7b0ae74e69d873af0eced7339337(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12abbeffe6a3d7a3e3652115617a18f9118147b92fb3ad460595d749b089908e(
    year: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    day: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f913a1bc1b2f476c2f01f6019bccc4f967f77ccb830e0a3e87951c2539ec9b7(
    date: datetime.datetime,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624aa6f72bd374aac935f84402cd9996285a488a2d46785282c8adc5c3feb8bc(
    date: KollavarshamDate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a50cb588f473c22a0d86f095b47c141f40d3741e093fa57660d94559244f108(
    saka_date: SakaDate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75596cff9789fcfbfa397fae95dedd0d43300bc45cde0c431940b222df074bf7(
    value: Settings,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5254f0964e14ee3edac9844ad3e5eff2bb8e73b7b7c8975373eeeaee278df2(
    year: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    day: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d79793967dd0b6cbbebdd629d2838bc38e489e3c8e46d5e0c885289426f7b2(
    value: SakaDate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd87ecc792f84d7c42065b88c5ef770243ed1014e29e103973841aaea1d363e(
    *,
    en_malayalam: builtins.str,
    ml_malayalam: builtins.str,
    saka: builtins.str,
    saura: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836a8c71e9c12fb33be6a8890029dedeb6197bff6d8172a87571e851136d6011(
    *,
    en_malayalam: builtins.str,
    ml_malayalam: builtins.str,
    saka: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3ac1e3a46d48a00c23d9e0fcf39e5e3e9a7bfd805a6c1d82137fe7a2c63500(
    year: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    tithi: typing.Optional[jsii.Number] = None,
    paksa: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583ca71b4333d0a38d5efb4872190078e28aea65913c206a979d1399cef179ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502984095c2a17e33bc58fd17ba0fc7c7d78a464cc1ca7fd35e3fc24eb6e389b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839cf7c7def6891526308e4e5397dd52e0a19cf1e8c930b709e8e5d7304099f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca0ff9143c49a0a7466cf3bb3ae81e0b165dfd6197e90dbf6ecb8b8fd630d7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652b126474ae0721fbcc4d0f5d3d6ec68ab3a83f2e757a56d166caa564cdefa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11e3a9b66c25d72b81586619167456a4449559d2972a1fb4540f23c6a8db0e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a311ead849a592248bb7c7ad3bcea95f3c8a4a9c42d8b494061868b2c4a91424(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6bcd9021ac3f0d388ed596fb008a510f8dba66c8f1fc985c3091e925a7d2662(
    *,
    latitude: jsii.Number,
    longitude: jsii.Number,
    system: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
