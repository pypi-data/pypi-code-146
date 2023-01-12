# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/azai/vision/license for the full license information.
"""
Classes that represents the handling of Image Analysis functionalities.
"""

import asyncio
import json
import ctypes

from typing import List
from .properties import PropertyCollection
from .interop import (
    _Handle, _c_str, _call_hr_fn, _sdk_lib, _spx_handle, _max_uint32, _unpack_context, _char_pointer_to_string)
from .vision_base_client import (
    EventSignal, VisionSession, VisionServiceOptions, VisionSource)
from .enums import (
    ImageAnalysisOption, ImageAnalysisErrorReason, ImageAnalysisFeature,
    ImageAnalysisResultOption, ImageAnalysisResultReason,
    _ImageAnalysisCoreResultReason, _ImageAnalysisCoreStopReason)
from .image_analysis_data import (
    Rectangle, DetectedObject, DetectedObjects, ContentTag, ContentTags, CropSuggestion, CropSuggestions,
    ContentCaption, ContentCaptions, DetectedPerson, DetectedPeople, DetectedTextLine, DetectedText,
    DetectedTextWord)


class ImageAnalysisOptions():
    """
    Represents the configuration options that control the function of the ImageAnalyzer
    """

    __feature_to_text_dict = dict([(ImageAnalysisFeature.TAGS, 'tags'),
                                  (ImageAnalysisFeature.CAPTIONS, 'description'),
                                  (ImageAnalysisFeature.OBJECTS, 'objects'),
                                  (ImageAnalysisFeature.PEOPLE, 'people'),
                                  (ImageAnalysisFeature.TEXT, 'read'),
                                  (ImageAnalysisFeature.CROP_SUGGESTIONS, 'smartCrops')])

    def __init__(self):
        core_properties_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.ai_core_properties_handle_create, *[ctypes.byref(core_properties_handle)])
        self.__properties = PropertyCollection(core_properties_handle)

    @property
    def features(self) -> ImageAnalysisFeature:
        """
        Gets the list of one or more visual features to extract from the image.
        """
        selected_feature_names = self.properties.get_property_by_id(ImageAnalysisOption.VISUAL_FEATURES, "")
        if selected_feature_names == "":
            return None
        else:
            selected_flags = 0
            values_list = selected_feature_names.split(",")
            for key in self.__feature_to_text_dict:
                if self.__feature_to_text_dict[key] in values_list:
                    selected_flags |= key.value
            return ImageAnalysisFeature(selected_flags)

    @features.setter
    def features(self, features: ImageAnalysisFeature):
        """
        Set a list of one or more visual features to extract from the image.

        :param feature: A single value from the ImageAnalysisFeature class, or
        an OR combination of several ImageAnalysisFeature values.
        """
        selected_feature_names = ''
        for key in self.__feature_to_text_dict:
            if key in features:
                selected_feature_names += self.__feature_to_text_dict[key] + ','

        if selected_feature_names != '':
            self.properties.set_property_by_id(ImageAnalysisOption.VISUAL_FEATURES, selected_feature_names[:-1])

    @property
    def language(self) -> str:
        """
        Gets the language that Image Analysis should use in the results.
        The language is in format ISO 639-1, e.g. "en" for English or "fr" for French.
        If this value is not set, the default value is "en" for English.
        See https://aka.ms/cv-languages for a list of supported language codes and which
        visual features are supported for each language.
        """
        return self.properties.get_property_by_id(ImageAnalysisOption.LANGUAGE, "en")

    @language.setter
    def language(self, language: str):
        """
        Sets the language that Image Analysis should use in the results.
        The language is in format ISO 639-1, e.g. "en" for English or "fr" for French.
        If this value is not set, the default value is "en" for English.
        See https://aka.ms/cv-languages for a list of supported language codes and which
        visual features are supported for each language.

        :param language: The desired language.
        """
        self.properties.set_property_by_id(ImageAnalysisOption.LANGUAGE, language)

    @property
    def gender_neutral_captions(self) -> bool:
        """
        Gets the gender neutrality of the Image Analysis captions result.
        Only relevant when ImageAnalysisFeature.CAPTIONS is set in the features property.
        The default is False.
        """
        value = self.properties.get_property_by_id(ImageAnalysisOption.GENDER_NEUTRAL_CAPTIONS, "no")
        if value == "yes":
            return True
        else:
            return False

    @gender_neutral_captions.setter
    def gender_neutral_captions(self, gender_neutral_captions: bool):
        """
        Sets the gender neutrality of the Image Analysis captions result.
        Only relevant when ImageAnalysisFeature.CAPTIONS is set in the features property.

        :param gender_neutral_captions:If \"True\", captions will not have gendered terms.
        If \"True\", the words \"Man/Woman\" will be replaced by \"Person\", and \"Boy/Girl\" will be replaced by \"Child\".
        If not set, defaults to \"False\".
        """
        self.properties.set_property_by_id(ImageAnalysisOption.GENDER_NEUTRAL_CAPTIONS, "yes" if gender_neutral_captions else "no")

    @property
    def model_version(self) -> str:
        """
        Gets the model version that the Image Analysis Service should use.
        """
        return self.properties.get_property_by_id(ImageAnalysisOption.MODEL_VERSION, "latest")

    @model_version.setter
    def model_version(self, version: str):
        """
        Sets the model version that the Image Analysis Service should use.
        If this option is not set, the default is "latest".
        "latest" is the only value currently supported by the service.
        In future service updates, supported model versions will be "latest" or
        in the form "YYYY-MM-DD" or "YYYY-MM-DD-preview",
        where YYYY, MM, DD are year, month, and day respectively.

        :param version: The version of the model.
        """
        self.properties.set_property_by_id(ImageAnalysisOption.MODEL_VERSION, version)

    @property
    def cropping_aspect_ratios(self) -> List[float]:
        """
        Get the list of aspect ratios to be used for cropping.
        This list will be empty if aspect ratios have not been set before.
        An aspect ratio is calculated by dividing the target crop width by the height.
        Supported values are between 0.75 and 1.8 (inclusive).
        """
        aspect_ratios = self.properties.get_property_by_id(ImageAnalysisOption.CROPPING_ASPECT_RATIOS, "")
        if aspect_ratios == "":
            return None
        else:
            str_list = aspect_ratios.split(",")
            float_list = [float(element) for element in str_list]
            return float_list

    @cropping_aspect_ratios.setter
    def cropping_aspect_ratios(self, aspect_ratios: List[float]):
        """
        Sets the list of aspect ratios that crop suggestions should attempt to fit.
        An aspect ratio is calculated by dividing the target crop width by the height.
        Supported values are between 0.75 and 1.8 (inclusive).
        Calling this method is only relevant when ImageAnalysisFeature.CROP_SUGGESTIONS is set as
        one of the image features to analyze (see features property).
        If cropping_aspect_ratios is not set, but ImageAnalysisFeature.CROP_SUGGESTIONS is specified
        as a feature, the service will return one crop suggestion with an aspect ratio it sees fit.
        :param aspect_ratios: A list of aspect rations (a positive number).
        """
        str_list = [str(element) for element in aspect_ratios]
        joined_str_list = ",".join(str_list)
        self.properties.set_property_by_id(ImageAnalysisOption.CROPPING_ASPECT_RATIOS, joined_str_list)

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of properties used for advanced settings.
        """
        return self.__properties

    def __str__(self):
        return f"ImageAnalysisOptions({type(self).__name__})"


class ImageAnalysisResult():
    """
    Represents the outcome of an Image Analysis operation.

    When an operation was successful, this result includes analyzed data for the features specified
    when setting ImageAnalysisOptions.features.

    Result data is selectively populated based on those features and will be None if
    not requested.

    :param handle: Internal handle for image analysis result.
    """

    def __init__(self, handle: _spx_handle):
        properties_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_result_properties_handle_get, *[handle, ctypes.byref(properties_handle)])
        self.__properties = PropertyCollection(properties_handle)
        self.__handle = _Handle(handle, _sdk_lib.vision_result_handle_is_valid, _sdk_lib.vision_result_handle_release)

        # By default result metadata will be empty strings
        self.__json_result_str = self.properties.get_property_by_id(ImageAnalysisResultOption.JSON, "")

        # By default, all analysis result objects will be empty ("None"):
        self.__model_version = None
        self.__image_height = None
        self.__image_width = None
        self.__tags = None
        self.__detected_objects = None
        self.__captions = None
        self.__detected_people = None
        self.__detected_text = None
        self.__crop_suggestions = None

        if self.reason is ImageAnalysisResultReason.ANALYZED and len(self.__json_result_str) > 0:

            json_result = json.loads(self.__json_result_str)

            if 'modelVersion' in json_result:
                self.__model_version = json_result['modelVersion']

            if 'metadata' in json_result:
                self.__image_height = int(json_result['metadata']['height'])
                self.__image_width = int(json_result['metadata']['width'])

            if 'tagsResult' in json_result:
                json_tags_result = json_result['tagsResult']
                if 'values' in json_tags_result:
                    self.__tags = ContentTags()
                    tags_values = json_tags_result['values']
                    for item in tags_values:
                        tag = ContentTag()
                        tag.confidence = item['confidence']
                        tag.name = item['name']
                        self.__tags.append(tag)

            if 'objectsResult' in json_result:
                json_objects_result = json_result['objectsResult']
                if 'values' in json_objects_result:
                    self.__detected_objects = DetectedObjects()
                    objects_values = json_objects_result['values']
                    for item in objects_values:
                        bounding_box = Rectangle()
                        bounding_box.x = item['boundingBox']['x']
                        bounding_box.y = item['boundingBox']['y']
                        bounding_box.w = item['boundingBox']['w']
                        bounding_box.h = item['boundingBox']['h']
                        confidence = item['confidence']
                        name = item['name']
                        detected_object = DetectedObject(bounding_box=bounding_box, name=name, confidence=confidence)
                        self.__detected_objects.append(detected_object)

            if 'descriptionResult' in json_result:
                json_captions_result = json_result['descriptionResult']
                if 'values' in json_captions_result:
                    self.__captions = ContentCaptions()
                    captions_values = json_captions_result['values']
                    for item in captions_values:
                        caption = ContentCaption()
                        caption.confidence = item['confidence']
                        caption.content = item['text']
                        self.__captions.append(caption)

            if 'peopleResult' in json_result:
                json_people_result = json_result['peopleResult']
                if 'values' in json_people_result:
                    self.__detected_people = DetectedPeople()
                    people_values = json_people_result['values']
                    for item in people_values:
                        confidence = item['confidence']
                        bounding_box = Rectangle()
                        bounding_box.x = item['boundingBox']['x']
                        bounding_box.y = item['boundingBox']['y']
                        bounding_box.w = item['boundingBox']['w']
                        bounding_box.h = item['boundingBox']['h']
                        person = DetectedPerson(bounding_box=bounding_box, confidence=confidence)
                        self.__detected_people.append(person)

            if 'readResult' in json_result:
                json_read_result = json_result['readResult']
                json_document_page = json_read_result["pages"][0]
                read_result_lines = []
                for item in json_document_page['lines']:
                    line_content = item['content']
                    line_bounding_polygon = item['boundingBox']
                    line_offset = item['spans'][0]['offset']
                    line_length = item['spans'][0]['length']
                    words = []
                    for item in json_document_page['words']:
                        word_content = item['content']
                        word_confidence = item['confidence']
                        word_bounding_polygon = item['boundingBox']
                        word_offset = item['span']['offset']
                        word_length = item['span']['length']
                        if word_offset >= line_offset and word_offset + word_length <= line_offset + line_length:
                            word = DetectedTextWord(content=word_content, bounding_polygon=word_bounding_polygon,
                                                    confidence=word_confidence)
                            words.append(word)
                    line = DetectedTextLine(content=line_content, bounding_polygon=line_bounding_polygon, words=words)
                    read_result_lines.append(line)
                self.__detected_text = DetectedText(lines=read_result_lines)

            if 'smartCropsResult' in json_result:
                json_crop_result = json_result['smartCropsResult']
                if 'values' in json_crop_result:
                    self.__crop_suggestions = CropSuggestions()
                    crop_values = json_crop_result['values']
                    for item in crop_values:
                        aspect_ratio = item['aspectRatio']
                        bounding_box = Rectangle()
                        bounding_box.x = item['boundingBox']['x']
                        bounding_box.y = item['boundingBox']['y']
                        bounding_box.w = item['boundingBox']['w']
                        bounding_box.h = item['boundingBox']['h']
                        crop_suggestion = CropSuggestion(bounding_box=bounding_box, aspect_ratio=aspect_ratio)
                        self.__crop_suggestions.append(crop_suggestion)

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of advanced properties on the result.
        """
        return self.__properties

    @property
    def result_id(self) -> str:
        """
        The unique identifier from the Vision Service, associated with this result.
        """
        return self.properties.get_property("result.id", "")

    @property
    def image_id(self) -> str:
        """
        The identifier of the analyzed image. This could be the full-path
        image file name or the image URL, depending on how the VisionSource was created.
        """
        return self.properties.get_property("result.image.id", "")

    @property
    def json_result(self) -> str:
        """
        Gets the JSON response payload from the Vision Service that was deserialized
        to create the provided ImageAnalysisResult.
        """
        return self.__json_result_str

    @property
    def reason(self) -> ImageAnalysisResultReason:
        """
        A value indicating why this result was generated.
        """

        # Error check #1: if an "error.reason" exists -- well, it's an error
        error_reason = self.properties.get_property("error.reason", "")
        if len(error_reason) > 0:
            return ImageAnalysisResultReason.ERROR

        # Error check #2 -- if "session.stopped.reason" exists and it converts to "error," it's an error
        session_stopped_reason = self.properties.get_property("session.stopped.reason", "")
        if session_stopped_reason == str(_ImageAnalysisCoreStopReason.ERROR.value):
            return ImageAnalysisResultReason.ERROR

        # If it's not an error, the "result.reason" should indicate it's a successful analysis result
        result_reason = self.properties.get_property("result.reason", "")
        if result_reason == str(_ImageAnalysisCoreResultReason.ANALYZED.value):
            return ImageAnalysisResultReason.ANALYZED

        # If we got this far and none of the above fit? Something went wrong
        return ImageAnalysisResultReason.ERROR

    @property
    def model_version(self) -> str:
        """
        The model version used by the Image Analysis Service to create this result.
        """
        return self.__model_version

    @property
    def image_height(self) -> int:
        """
        The height, in pixels, of the analyzed image.
        """
        return self.__image_height

    @property
    def image_width(self) -> int:
        """
        The width, in pixels, of the analyzed image.
        """
        return self.__image_width

    @property
    def captions(self) -> ContentCaptions:
        """
        A list of generated phrases that describe the content of the analyzed image.

        This result will only be populated if ImageAnalysisFeature.CAPTIONS was included
        while setting ImageAnalysisOptions.features.

        At the moment only one description will be returned.
        """
        return self.__captions

    @property
    def tags(self) -> ContentTags:
        """
        A list of content tag detections from the analyzed image.

        This result will only be populated if ImageAnalysisFeature.TAGS was included
        while setting ImageAnalysisOptions.features.
        """
        return self.__tags

    @property
    def objects(self) -> DetectedObjects:
        """
        A list of detected objects from the analyzed image.

        This result will only be populated if ImageAnalysisFeature.OBJECTS was included
        while setting ImageAnalysisOptions.features.
        """
        return self.__detected_objects

    @property
    def people(self) -> DetectedPeople:
        """
        A list of detected people from an analyzed image.

        This result will only be populated if ImageAnalysisFeature.PEOPLE was included
        while setting ImageAnalysisOptions.features.
        """
        return self.__detected_people

    @property
    def text(self) -> DetectedText:
        """
        A collection of extracted textual lines and words from an analyzed image.

        This result will only be populated if ImageAnalysisFeature.TEXT was included
        while setting ImageAnalysisOptions.features.
        """
        return self.__detected_text

    @property
    def crop_suggestions(self) -> CropSuggestions:
        """
        A list of suggested image crop operations of the analyzed
        image at the desired aspect ratios (if provided)

        Also knows as SmartCrops. These cropping suggestions preserve as much content
        as possible while achieving the specified aspect ratios (if provided).

        This result will only be populated if ImageAnalysisFeature.CROP_SUGGESTIONS was included
        while setting ImageAnalysisOptions.features.

        Optionally, specify one or more desired cropping aspect ratios by setting
        ImageAnalysisOptions.cropping_aspect_ratios. If cropping_aspect_ratios is not set, the Service will
        return one crop suggestion with an aspect ratio it sees fit.
        """
        return self.__crop_suggestions

    @property
    def _handle(self):
        return self.__handle.get()

    def __str__(self):
        return f"ImageAnalysisResult({type(self).__name__})"


class ImageAnalysisEventArgs():
    """
    Represents an asynchronous Image Analysis result payload as an event argument

    :param handle: Internal handle for result.
    """

    def __init__(self, handle: _spx_handle):
        self.__handle = _Handle(handle, _sdk_lib.vision_event_args_handle_is_valid, _sdk_lib.vision_event_args_handle_release)
        result_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_event_args_result_handle_get, *[self._handle, ctypes.byref(result_handle)])
        self.__result = ImageAnalysisResult(result_handle)

    @property
    def result(self) -> ImageAnalysisResult:
        """
        The Image Analysis result associated with this event.
        """
        return self.__result

    @property
    def _handle(self):
        return self.__handle.get()

    def __str__(self):
        return f"ImageAnalysisEventArgs({type(self).__name__})"


class ImageAnalysisErrorDetails():
    """
    A representation of an error associated with an image analysis result.
    """

    @staticmethod
    def from_result(result: ImageAnalysisResult):
        """
        Creates an object that contains additional error information for a failed ImageAnalysisResult.

        ImageAnalysisErrorDetail objects can only be created from ImageAnalysisResults that stopped due to an
        error. This corresponds to a value of ImageAnalysisResultReason.ERROR for ImageAnalysisResult.reason.
        Attempting to create an ImageAnalysisErrorDetails from a result that did not stop due to an error will
        return None.

        :param result: The result object from a failed image analysis operation.
        """
        if result is None:
            raise ValueError('result cannot be None')
        elif result.reason == ImageAnalysisResultReason.ANALYZED:
            return None
        else:
            error_details = ImageAnalysisErrorDetails()
            handle = result._handle
            properties_handle = _spx_handle(0)
            _call_hr_fn(fn=_sdk_lib.vision_result_properties_handle_get, *[handle, ctypes.byref(properties_handle)])
            error_details.__properties = PropertyCollection(properties_handle)
            return error_details

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of advanced properties on the error details.
        """
        return self.__properties

    @property
    def message(self) -> str:
        """
        The detailed error message.
        """
        return self.properties.get_property("error.message", "")

    @property
    def error_code(self) -> str:
        """
        The standardized code for the error.
        """
        return int(self.properties.get_property("error.code", ""))

    @property
    def reason(self) -> ImageAnalysisErrorReason:
        """
        The category of the error.
        """
        reason = int(self.properties.get_property("error.reason", "0"))
        return ImageAnalysisErrorReason(reason)

    @property
    def _handle(self):
        return self.__handle.get()

    def __str__(self):
        return f"ImageAnalysisErrorDetails({type(self).__name__})"


class ImageAnalyzer():
    """
    An object that facilitates Image Analysis operations with the Computer Vision service

    :param service_options: The Vision Service Options used to connect to the service.
    :param vision_source: The Vision Source to use.
    :param analysis_options: The Image Analysis Options to use.
    """

    def __init__(self, service_options: VisionServiceOptions, vision_source: VisionSource,
                 analysis_options: ImageAnalysisOptions):
        session_view_handle = _spx_handle(0)
        if vision_source is not None:
            vision_source.properties.set_property("adapter.passthrough", "1")
            c_file_max_size = 20 * 1024 * 1024
            vision_source.properties.set_property("source.file.max.size", str(c_file_max_size))
            c_image_file_type = 2 << 8  # = Media::SourceType::ImageFile in source\core\types\include\enums\media.h
            vision_source.properties.set_property("source.file.type", str(c_image_file_type))

        self.__session = VisionSession(service_options, vision_source)
        c_view_kind = _c_str('image.analyzer')
        _call_hr_fn(fn=_sdk_lib.vision_session_view_handle_create, *[ctypes.byref(session_view_handle), self._session._handle,
                    c_view_kind, analysis_options.properties._handle])

        prop_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_session_view_properties_handle_get, *[session_view_handle, ctypes.byref(prop_handle)])
        self.__properties = PropertyCollection(prop_handle)
        self.__handle = _Handle(session_view_handle, _sdk_lib.vision_session_view_handle_is_valid,
                                _sdk_lib.vision_session_view_handle_release)
        self.__event_loop = None

    def __del__(self):
        if _sdk_lib.vision_session_view_handle_is_valid(self._handle) is None:
            _sdk_lib.vision_event_callback_set(self._handle, "recognized", None, None)
            _sdk_lib.vision_event_callback_set(self._handle, "error", None, None)

        def clean_signal(signal: EventSignal):
            if signal is not None:
                signal.disconnect_all()

        clean_signal(self.__analyzed_signal)

    @property
    def _handle(self) -> _spx_handle:
        return self.__handle.get()

    @property
    def _session(self) -> VisionSession:
        return self.__session

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of advanced ImageAnalyzer properties.
        """
        return self.__properties

    def analyze(self) -> ImageAnalysisResult:
        """
        Performs a single Image Analysis operation using the source provided when this ImageAnalyzer was created.
        This is a synchronous (blocking) call, that will return after the results are available from the service.

        :return: The Image Analysis results.
        """
        # TBD add options
        asyncop_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_session_view_single_shot_start, *[self._session._handle, None, None,
                    ctypes.byref(asyncop_handle)])
        result_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.async_op_wait_for_result, *[asyncop_handle, _max_uint32, ctypes.byref(result_handle)])
        _call_hr_fn(fn=_sdk_lib.async_op_handle_release, *[asyncop_handle])
        return ImageAnalysisResult(result_handle)

    async def analyze_async(self) -> ImageAnalysisResult:
        """
        Begins a single Image Analysis operation against the source provided when this ImageAnalyzer was created.

        :return: The Image Analysis results.
        """
        if self.__event_loop is None:
            self.__event_loop = asyncio.get_event_loop()
        result = await self.__event_loop.run_in_executor(None, self.analyze)
        return result

    __analyzed_signal = None

    @property
    def analyzed(self) -> EventSignal:
        """
        An event signal that is raised when a new ImageAnalysisResult is available
        (either analysis succeeded or an error occurred)
        """
        def analyzed_connection(signal: EventSignal, handle: _spx_handle):
            callback = ImageAnalyzer.__session_event_callback if signal.is_connected() else None
            _sdk_lib.vision_event_callback_set(handle, _c_str("recognized"), signal._context_ptr, callback)
            _sdk_lib.vision_event_callback_set(handle, _c_str("error"), signal._context_ptr, callback)
        if self.__analyzed_signal is None:
            self.__analyzed_signal = EventSignal(self, analyzed_connection)
        return self.__analyzed_signal

    @ctypes.CFUNCTYPE(None, _spx_handle, ctypes.POINTER(ctypes.c_char), ctypes.c_void_p, _spx_handle)
    def __session_event_callback(session_handle: _spx_handle, event_name: ctypes.POINTER(ctypes.c_char), context: ctypes.c_void_p,
                                 event_handle: _spx_handle):
        event_handle = _spx_handle(event_handle)
        event_name = _char_pointer_to_string(event_name)
        obj = _unpack_context(context)
        if event_name == 'recognized':
            if obj is not None:
                event = ImageAnalysisEventArgs(event_handle)
                obj.__analyzed_signal.signal(event)
        elif event_name == 'error':
            if obj is not None:
                event = ImageAnalysisEventArgs(event_handle)
                obj.__analyzed_signal.signal(event)
