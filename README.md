# Python Statsd Decorators

Decorators for logging to [Etsy's statsd](https://github.com/etsy/statsd) with Python.
Uses [python-statsd](https://github.com/WoLpH/python-statsd).

## Usage

### Importing

    # import the statsd logger
    from statsd_decorators import statsd_logger

    # set the application namespace
    statsd_logger.namespace = 'MyApplication'

    # if for some reason you're in debug mode or whatever and don't want
    # to send anything to statsd, you can disable the logger
    statsd_logger.disabled = True


### Counter

Increment or decrement a counter every time a function or method is called.


    @statsd_logger.counter('my_counter', 10)
    def counter_function():
        pass

    # increment a counter with a default of 1
    @statsd_logger.increment('my_counter')
    def increment_when_called():
        pass

    # decrement a counter with a default of 1
    @statsd_logger.decrement('my_counter')
    def decrement_when_called()
        pass


### Timer

Decorate a function or method to time its execution and send to statsd.

    @statsd_logger.timer('my_timer')
    def hello():
        print "Hello, world."


### Gauge

Pass the return value of your function to a gauge.

    @statsd_logger.gauge('my_gauge')
    def fib(i):
        """Slightly crazy example"""
        if i == 0:
            return 0
        if i == 1:
            return 1
        return fib(n - 1) + fib(n - 2)
