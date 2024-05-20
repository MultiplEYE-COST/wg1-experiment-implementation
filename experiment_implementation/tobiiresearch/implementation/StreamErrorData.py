##
# @namespace tobii_research All functionality is in this module.

STREAM_ERROR_SOURCE_USER = "stream_error_source_user"
STREAM_ERROR_SOURCE_STREAM_PUMP = "stream_error_source_stream_pump"
STREAM_ERROR_SOURCE_SUBSCRIPTION_GAZE_DATA = "stream_error_source_subscription_gaze_data"
STREAM_ERROR_SOURCE_SUBSCRIPTION_USER_POSITION_GUIDE = "stream_error_source_subscription_user_position_guide"
STREAM_ERROR_SOURCE_SUBSCRIPTION_EXTERNAL_SIGNAL = "stream_error_source_subscription_external_signal"
STREAM_ERROR_SOURCE_SUBSCRIPTION_TIME_SYNCHRONIZATION_DATA = \
    "stream_error_source_subscription_time_synchronization_data"
STREAM_ERROR_SOURCE_SUBSCRIPTION_EYE_IMAGE = "stream_error_source_subscription_eye_image"
STREAM_ERROR_SOURCE_SUBSCRIPTION_NOTIFICATION = "stream_error_source_subscription_notification"

STREAM_ERROR_CONNECTION_LOST = "stream_error_connection_lost"
STREAM_ERROR_INSUFFICIENT_LICENSE = "stream_error_insufficient_license"
STREAM_ERROR_NOT_SUPPORTED = "stream_error_not_supported"
STREAM_ERROR_TOO_MANY_SUBSCRIBERS = "stream_error_too_many_subscribers"
STREAM_ERROR_INTERNAL_ERROR = "stream_error_internal_error"
STREAM_ERROR_USER_ERROR = "stream_error_user_error"


class StreamErrorData(object):
    '''Provides information about a stream error.
    '''

    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("You shouldn't create StreamErrorData objects yourself.")

        self._system_time_stamp = data["system_time_stamp"]
        self._error = data["error"]
        self._source = data["source"]
        self._message = data["message"]

    @property
    def system_time_stamp(self):
        '''Gets the time stamp according to the computer's internal clock.
        '''
        return self._system_time_stamp

    @property
    def source(self):
        '''Source of the error.

        @ref STREAM_ERROR_SOURCE_USER User callback failed.
        @ref STREAM_ERROR_SOURCE_STREAM_PUMP Error when pumping event.
        @ref STREAM_ERROR_SOURCE_SUBSCRIPTION_GAZE_DATA Error when subscribing to event for gaze data.
        @ref STREAM_ERROR_SOURCE_SUBSCRIPTION_USER_POSITION_GUIDE Error when subscribing to event for user position guide.
        @ref STREAM_ERROR_SOURCE_SUBSCRIPTION_EXTERNAL_SIGNAL Error when subscribing to event for external signal.
        @ref STREAM_ERROR_SOURCE_SUBSCRIPTION_TIME_SYNCHRONIZATION_DATA Error when subscribing to event for time synchronization data.
        @ref STREAM_ERROR_SOURCE_SUBSCRIPTION_EYE_IMAGE Error when subscribing to event for eye images.
        @ref STREAM_ERROR_SOURCE_SUBSCRIPTION_NOTIFICATION Error when subscribing to notification event.
        '''

        return self._source

    @property
    def error(self):
        '''The error message.

        @ref STREAM_ERROR_CONNECTION_LOST Indicates that the connection to the eye tracker was lost.
        @ref STREAM_ERROR_INSUFFICIENT_LICENSE Indicates that the license is insufficient for subscribing to the stream.
        @ref STREAM_ERROR_NOT_SUPPORTED Indicates that the stream isn't supported by the eye tracker.
        @ref STREAM_ERROR_TOO_MANY_SUBSCRIBERS Indicates that number of subscriptions to the stream has reached its limit.
        @ref STREAM_ERROR_INTERNAL_ERROR Indicates that an internal error occurred.
        @ref STREAM_ERROR_USER_ERROR Indicates that the user threw an exception in the callback.

        '''
        return self._error

    @property
    def message(self):
        return self._message
