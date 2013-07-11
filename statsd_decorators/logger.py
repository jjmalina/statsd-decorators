# -*- coding: utf-8 -*-

import statsd as statsd_client


def statsd_enabled_only(method):
    """Call a method to log to statsd if not disabled"""
    def wrapper(self, *args, **kwargs):
        if self.disabled:
            return
        return method(self, *args, **kwargs)
    return wrapper


class StatsdLogger(object):
    def __init__(self, client):
        self.statsd = client
        self.disabled = False
        self.namespace = ''

    def bucket_key(self, name):
        return '%s%s' % (('%s.' % self.namespace) if self.namespace else '',
                         name)

    @statsd_enabled_only
    def _counter(self, path, delta):
        self.statsd.increment(path, delta=delta)

    def _counter_wrapper(self, func, name, delta):
        def inner(*args, **kwargs):
            self._counter(self.bucket_key(name), delta=delta)
            result = func(*args, **kwargs)
            return result
        return inner

    def increment(self, name, delta=1):
        """Returns a decorator for incrementing a counter"""
        def decorator(func):
            return self._counter_wrapper(func, name, delta)
        return decorator

    def decrement(self, name, delta=-1):
        """Returns a decorator for decrementing a counter"""
        def decorator(func):
            return self._counter_wrapper(func, name, delta)
        return decorator

    def counter(self, name, delta):
        """Pass an arbitrary number"""
        return self.increment(name, delta)

    def timer(self, name):
        """Returns a decorator for using a timer"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                timer = self.statsd.Timer(self.namespace)
                if not self.disabled:
                    timer.start()
                result = func(*args, **kwargs)
                if not self.disabled:
                    timer.stop(name)
                return result
            return wrapper
        return decorator

    def gauge(self, name):
        """Returns a decorator for using a gauge"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not self.disabled:
                    gauge = self.statsd.Gauge(self.namespace)
                    gauge.send(name, result)
                return result
            return wrapper
        return decorator


# The statsd logger instance to get decorators from.
statsd_logger = StatsdLogger(statsd_client)
