class EyeOpennessData(object):
    '''Provides data for eye openness.

    You will get an object of this type to the callback you supply in EyeTracker.subscribe_to with
    @ref  EYETRACKER_EYE_OPENNESS_DATA 
    '''

    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("You shouldn't create EyeOpennessData objects yourself.")

        
        self.__device_time_stamp = data["device_time_stamp"]

        self.__system_time_stamp = data["system_time_stamp"]

        self.__left_eye_openness_value = data["left_eye_openness_value"]

        self.__left_eye_validity = bool(data["left_eye_validity"])

        self.__right_eye_openness_value = data["right_eye_openness_value"]

        self.__right_eye_validity = bool(data["right_eye_validity"])

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
    def  left_eye_validity(self):
        '''Gets the validity of the left eye openness in millimeters.
        '''
        return self.__left_eye_validity

    @property
    def  left_eye_openness_value(self):
        '''Gets the value of the left eye openness in millimeters.
        '''
        return self.__left_eye_openness_value

    @property
    def  right_eye_validity(self):
        '''Gets the validity of the right eye openness in millimeters.
        '''
        return self.__right_eye_validity


    @property
    def  right_eye_openness_value(self):
        '''Gets the value of the right eye openness in millimeters.
        '''
        return self.__right_eye_openness_value
