from functools import wraps
import inspect

# ref:https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p11_write_decorators_that_add_arguments_to_functions.html
class optional_inplace:
    def __init__(self, default: bool=True):
        self.default = default

    def __call__(self, func):

        if 'inplace' in inspect.getfullargspec(func).args:
            raise TypeError('inplace argument already defined')

        @wraps(func)
        def wrapper(obj, *args, inplace: bool = self.default, **kwargs):
            if not inplace:
                obj = obj.copy()
            return func(obj, *args, **kwargs)

        sig = inspect.signature(func)
        parms = list(sig.parameters.values())
        parms.append(
            inspect.Parameter('inplace',
                            inspect.Parameter.KEYWORD_ONLY,
                            default=True))
        wrapper.__signature__ = sig.replace(parameters=parms)
        return wrapper