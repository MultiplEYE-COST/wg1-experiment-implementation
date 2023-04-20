class UserPosition(object):
    '''Provides properties for the user position.

    UserPosition objects are used as values for UserPositionGuide.left_eye and UserPositionGuide.right_eye.
    '''

    def __init__(self,
                 user_position,
                 user_position_validity):
        if ((not isinstance(user_position, tuple) or
             not isinstance(user_position_validity, int))):
            raise ValueError(
                "You shouldn't create UserPosition objects yourself.")

        self.__user_position = user_position
        self.__validity = bool(user_position_validity)

    @property
    def user_position(self):
        '''Gets user position as a normalized three valued tuple (x, y, z).
        '''
        return self.__user_position

    @property
    def validity(self):
        '''Gets the validity of the user position.

        True if valid. False if invalid.
        '''
        return self.__validity


class UserPositionGuide(object):
    '''Provides data for the user position guide.

    You will get an object of this type to the callback you supply in EyeTracker.subscribe_to with
    @ref EYETRACKER_USER_POSITION_GUIDE.
    '''

    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("You shouldn't create UserPositionGuide objects yourself.")

        self.__left = UserPosition(
            data["left_user_position"],
            data["left_user_position_validity"])

        self.__right = UserPosition(
            data["right_user_position"],
            data["right_user_position_validity"])

    @property
    def left_eye(self):
        '''Gets the user position for the left eye as an UserPosition object.
        '''
        return self.__left

    @property
    def right_eye(self):
        '''Gets the user position for the right eye as an UserPosition object.
        '''
        return self.__right
