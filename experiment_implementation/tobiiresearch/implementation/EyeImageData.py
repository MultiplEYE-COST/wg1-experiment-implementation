##
# Indicates that the eye tracker could not identify the eyes, and the image is the full image.
#
# Value for EyeImageData.image_type
EYE_IMAGE_TYPE_FULL = "eye_image_type_full"

##
# Indicates that the image is cropped and shows the eyes.
#
# Value for EyeImageData.image_type
EYE_IMAGE_TYPE_CROPPED = "eye_image_type_cropped"

##
# Indicates that the image is part of a group of regions of interest.
#
# Value for EyeImageData.image_type
EYE_IMAGE_TYPE_MULTI_ROI = "eye_image_type_multi_roi"


##
# Indicates an unknown image type.
#
# Value for EyeImageData.image_type
EYE_IMAGE_TYPE_UNKNOWN = "eye_image_type_unknown"


class EyeImageData(object):
    '''Provides data for the eye image callback.

    You will get an object of this type to the callback you supply in EyeTracker.subscribe_to with
    @ref EYETRACKER_EYE_IMAGES.
    '''

    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("You shouldn't create EyeImageData objects yourself.")

        self.__device_time_stamp = data["device_time_stamp"]
        self.__system_time_stamp = data["system_time_stamp"]
        self.__camera_id = data["camera_id"]
        self.__top = data["top"]
        self.__left = data["left"]
        self.__region_id = data["region_id"]
        self.__image_type = data["image_type"]
        self.__image_data = data["image_data"]

    @property
    def device_time_stamp(self):
        '''Gets the time stamp according to the eye tracker's internal clock.
        '''
        return self.__device_time_stamp

    @property
    def system_time_stamp(self):
        '''Gets the time stamp according to the computer's internal clock.
        '''
        return self.__system_time_stamp

    @property
    def camera_id(self):
        '''Gets which camera generated the image.
        '''
        return self.__camera_id

    @property
    def top(self):
        '''Gets the top position in pixels for the eye image.
        '''
        return self.__top

    @property
    def left(self):
        '''Gets the left position in pixels for the eye image.
        '''
        return self.__left

    @property
    def region_id(self):
        '''Gets the region id for the eye image.
        '''
        return self.__region_id

    @property
    def image_type(self):
        '''Gets the type of eye image as a string.

        Valid values are @ref EYE_IMAGE_TYPE_FULL , @ref EYE_IMAGE_TYPE_CROPPED and @ref EYE_IMAGE_TYPE_MULTI_ROI.
        '''
        return self.__image_type

    @property
    def image_data(self):
        '''Gets the image data sent by the eye tracker in GIF format.
        '''
        return self.__image_data
