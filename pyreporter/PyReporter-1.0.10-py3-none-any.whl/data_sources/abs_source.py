import pandas as pd
from .df_processor import DFProcessor
from ..view import ProgressSubject
from ..events import OutEvent
from typing import Optional, Union, Dict


DEFAULT_POST_PROCESSOR_KEY = "default"


# AbsSource: An abstract Source
class AbsSource():
    """
    An Abstract Class for reading in data

    Can be sub-classed to create your own method of reading in data from some source

    Attributes
    -----------
    post_processor: Optional[Union[Dict[:class:`str`, :class:`~Reporter.data_sources.df_processor.DFProcessor`], :class:`~Reporter.data_sources.df_processor.DFProcessor`]]
        The processors that are used to manipulate the structure of the target table

        **Default**: ``None``

    progress_checker: :class:`~Reporter.view.progress.ProgressSubject`
        The logger used to report on the progress of loading the target table
    """
    def __init__(self, post_processor: Optional[Union[Dict[str, DFProcessor], DFProcessor]] = None, progress_checker: Optional[ProgressSubject] = None):
        # store the processors used to transform the source into a dataframe
        if (post_processor is None or isinstance(post_processor, dict)):
            self.post_processor = post_processor
        else:
            self.post_processor = {DEFAULT_POST_PROCESSOR_KEY: post_processor}

        self.progress_checker = progress_checker
        self.name = None


    def __getitem__(self, key: str):
        return self.post_processor[key]


    def __setitem__(self, key: str, value: DFProcessor):
        assert isinstance(isinstance(value, DFProcessor))
        self.post_processor[key] = value


    # notify(out_event): Prints update on the progress for the Source
    def notify(self, out_event: OutEvent):
        """
        Prints update on the progress for the Source

        Parameters
        ----------
        out_event: :class:`~Reporter.events.out_event.OutEvent`
            The event for printing output
        """
        if (self.progress_checker is not None):
            self.progress_checker.notify(out_event)


    # import_data(): imports the data to become a Pandas Dataframe
    async def import_data(self) -> pd.DataFrame:
        """
        The method used to import the required data

        Returns
        -------
        `DataFrame`_
            The resultant imported data
        """
        pass


    # process(df): Prepares the data for use in the calculations
    async def prepare(self, post_processor_name: str = DEFAULT_POST_PROCESSOR_KEY) -> pd.DataFrame:
        """
        Imports and prepares the needed data for further calculations

        Parameters
        ----------
        post_processor_name : :class:`str`
            The name of the :class:`~Reporter.data_sources.df_processor.DFProcessor` used for
            editting the imported data

            **Default**: ``default``

        Returns
        -------
        `DataFrame`_
            The resultant table after importing and applying any necessary :class:`~Reporter.data_sources.df_processor.DFProcessor`
        """
        df = await self.import_data()

        if (self.post_processor is not None):
            result = None

            try:
                result = self.post_processor[post_processor_name].process(df)
            except KeyError as e:
                if (isinstance(self.post_processor, dict)):
                    key = list(self.post_processor.keys())[0]
                    result = self.post_processor[key].process(df)

                    return result
                else:
                    raise e
            else:
                return result
        else:
            return df
