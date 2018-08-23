class BaseError(Exception):

    def __init__(self, err_msg, err_type='Error'):
        message = '{}: {}'.format(err_type, err_msg)
        super().__init__(message)


class ParamError(BaseError):

    def __init__(self, err_msg):
        super().__init__(err_msg, self.__class__.__name__)