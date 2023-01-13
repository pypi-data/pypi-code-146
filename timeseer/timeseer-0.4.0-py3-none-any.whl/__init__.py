"""Timeseer Client provides convenient remote access to Timeseer.

The `Client` class creates a connection to Timeseer.

```
client = Client(api_key=(key_name, secret), host="timeseer.example.org")
```

`Client` supports basic time series operations:

```
client.list_sources()  # list all connected time series sources
client.search(...)  # search for time series
client.get_metadata(...)  # return metadata for a time series
client.get_data(...)  # return data for a time series
```

All concepts within Timeseer are represented as Resources.
The `Resources` class should be used to configure them.

```
resources = Resources(client)
resources.list(...)
resources.create(...)
resources.read(...)
resources.delete(...)
```

Several resources can be interacted with. They have their own class:

- `DataServices`
- `DataSets`
- `Flows`

For example:

```
Flows(client).evaluate(...)
```

This package also contains several convenience functions to:

- Profile a data frame in Timeseer.
- Filter data based on event frames.

"""

from kukur import (
    DataType,
    Dictionary,
    InterpolationType,
    Metadata,
    SeriesSearch,
)

from timeseer import SeriesSelector
from timeseer_client.internal import (
    AugmentationStrategy,
    ProcessType,
    Statistic,
    TimeseerClientException,
    UnknownAugmentationStrategyException,
)
from timeseer_client.internal.client import Client
from timeseer_client.internal.data_services import DataServices
from timeseer_client.internal.data_sets import DataSets
from timeseer_client.internal.filters import filter_event_frames, filter_series
from timeseer_client.metadata.fields import register_custom_fields
from timeseer_client.internal.flows import Flows
from timeseer_client.internal.profile import profile
from timeseer_client.internal.resources import Resources


register_custom_fields(Metadata)


__all__ = [
    "AugmentationStrategy",
    "Client",
    "DataServices",
    "DataSets",
    "DataType",
    "Dictionary",
    "Flows",
    "InterpolationType",
    "Metadata",
    "ProcessType",
    "Resources",
    "SeriesSearch",
    "SeriesSelector",
    "Statistic",
    "TimeseerClientException",
    "UnknownAugmentationStrategyException",
    "filter_event_frames",
    "filter_series",
    "profile",
]
