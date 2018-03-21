#!/usr/bin/python
import time
import logging


DEFAULT_THRESHOLD = 0.02

logger = logging.getLogger(__name__)

# configure logger for console output
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class _Timetracked(object):
    """Decorator class for function and method execution time tracking.
    """

    def __init__(self, function_, threshold, instance=None, owner=None):
        self.function = function_
        self.threshold = threshold
        self.instance = instance
        self.owner = owner

    def __get__(self, instance=None, owner=None):
        # the descriptor is executed when decorated function is referenced
        # as a method.
        if self.instance == instance and self.owner == owner:
            return self
        # return the special instance
        return _Timetracked(
            self.function.__get__(instance, owner),
            self.threshold, instance, owner
        )

    def __call__(self, *args, **kwargs):
        # measure the duration and compare it to the threshold value
        start_time = time.time()
        result = self.function(*args, **kwargs)
        end_time = time.time()

        duration = end_time - start_time
        if duration > self.threshold:
            if self.owner is not None:
                logger.warning(
                    '{class_name}.{function_name} {time:.3f}'.format(
                        class_name=self.owner.__name__,
                        function_name=self.function.__name__,
                        time=end_time - start_time
                    )
                )
            else:
                logger.warning(
                    '{function_name} {time:.3f}'.format(
                        function_name=self.function.__name__,
                        time=end_time - start_time
                    )
                )
        return result

    def __getattribute__(self, attr_name):
        if attr_name in (
            '__init__', '__get__', '__call__', '__getattribute__',
            'function', 'instance', 'owner', 'threshold'
        ):
            return object.__getattribute__(self, attr_name)
        # get other attributes from decorated function
        return getattr(self.function, attr_name)

    def __repr__(self):
        # __repr__ bypasses __getattributes__
        return self.func.__repr__()


def timetracked(function_=None, threshold=DEFAULT_THRESHOLD):
    """Decorator for function and method execution time tracking.

    It can be specified as @timetracked or @timetracked(threshold=value)
    before function or method definition.
    """
    if function_ is None:
        # the threshold was specified in parameter
        def wrapper(func_):
            return _Timetracked(func_, threshold)
        return wrapper
    else:
        return _Timetracked(function_, threshold)


# tests
def example():

    class Foo(object):

        @timetracked
        @classmethod
        def some_class_method(cls, a):
            time.sleep(a)

        @timetracked(threshold=0.3)
        @classmethod
        def other_class_method(cls, a):
            time.sleep(a)

        @timetracked
        @staticmethod
        def some_static_method(a):
            time.sleep(a)

        @timetracked(threshold=0.3)
        @staticmethod
        def other_static_method(a):
            time.sleep(a)

        @timetracked
        def some_function(self, a):
            time.sleep(a)

        @timetracked(threshold=0.3)
        def other_function(self, a):
            time.sleep(a)

    class Bar(Foo):

        @timetracked
        def another_function(self, a):
            time.sleep(a)

    @timetracked(threshold=0.01)
    def some_function(a):
        time.sleep(a)

    Foo.some_class_method(0.02)  # warning
    Foo.other_class_method(0.02)  # ok
    Foo.some_static_method(0.02)  # warning
    Foo.other_static_method(0.5)  # warning
    Foo().some_function(0.02)  # warning
    Foo().other_function(0.02)  # ok
    Bar.some_class_method(0.02)  # warning
    Bar.some_static_method(0.02)  # warning
    Bar().some_function(0.02)  # warning
    Bar().another_function(0.02)  # warning
    some_function(0.02)  # warning


if __name__ == '__main__':
    example()
