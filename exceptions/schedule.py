

class BaseScheduleException(BaseException):
    pass


class ScheduleResponseFormatException(BaseScheduleException):
    pass


class ScheduleNoEntriesFoundException(BaseScheduleException):
    pass


class ScheduleUnknownErrorException(BaseScheduleException):
    pass

class ScheduleMultipleChoicesException(BaseScheduleException):
    pass


