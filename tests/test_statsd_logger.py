# -*- coding: utf-8 -*-

import time
import mock
import unittest

import statsd

from .context import statsd_logger

##
## Test constants
##
statsd_logger.namespace = 'Dummy'
counter_delta = 10
increment_delta = 5
decrement_delta = 5
timer_seconds = 0.1
gauge_value = 1


class StatsdDecoratorTests(unittest.TestCase):

    class Dummy(object):
        """A dummy class to test out decorated methods"""

        @statsd_logger.counter('dummy_counter', 10)
        def counter(self):
            pass

        @statsd_logger.increment('dummy_increment')
        def increment(self):
            pass

        @statsd_logger.decrement('dummy_decrement')
        def decrement(self):
            pass

        @statsd_logger.increment('dummy_increment', delta=increment_delta)
        def increment_delta(self):
            pass

        @statsd_logger.decrement('dummy_decrement', delta=decrement_delta)
        def decrement_delta(self):
            pass

        @statsd_logger.timer('dummy_timer')
        def timer(self, seconds=timer_seconds):
            time.sleep(seconds)

        @statsd_logger.gauge('dummy_gauge')
        def gauge(self, value=gauge_value):
            return value

    def setUp(self):
        self.dummy = self.Dummy()

    def test_increment_decorator(self):
        with mock.patch('statsd.Client') as statsd_client:
            self.dummy.counter()
            statsd_client._send.assert_called_with(
                mock.ANY, {'Dummy.dummy_counter': '%i|c' % counter_delta})

    def test_increment_decorator(self):
        with mock.patch('statsd.Client') as statsd_client:
            self.dummy.increment()
            statsd_client._send.assert_called_with(
                mock.ANY, {'Dummy.dummy_increment': '1|c'})

    def test_decrement_decorator(self):
        with mock.patch('statsd.Client') as statsd_client:
            self.dummy.decrement()
            statsd_client._send_assert_called_with(
                mock.ANY, {'Dummy.dummy_decrement': '-1|c'})

    def test_increment_decorator_with_delta(self):
        with mock.patch('statsd.Client') as statsd_client:
            self.dummy.increment_delta()
            statsd_client._send_assert_called_with(
                mock.ANY, {'Dummy.dummy_increment': '%i|c' % increment_delta})

    def test_decrement_decorator_with_delta(self):
        with mock.patch('statsd.Client') as statsd_client:
            self.dummy.decrement_delta()
            statsd_client._send_assert_called_with(
                mock.ANY, {'Dummy.dummy_decrement': '%i|c' % decrement_delta})

    def test_timer(self):
        with mock.patch('statsd.Client') as statsd_client:
            self.dummy.timer()
            statsd_client._send_assert_called_with(
                mock.ANY, {'Dummy.dummy_timer': '%i|ms' % timer_seconds * 1000})
            self.dummy.timer(0.05)
            statsd_client._send_assert_called_with(
                mock.ANY, {'Dummy.dummy_timer': '%i|ms' % 50})

    def test_gauge(self):
        with mock.patch('statsd.Client') as statsd_client:
            value = self.dummy.gauge()
            statsd_client._send_assert_called_with(
                mock.ANY, {'Dummy.dummy_gauge': '%i|g' % value})
            value = self.dummy.gauge(500)
            statsd_client._send_assert_called_with(
                mock.ANY, {'Dummy.dummy_gauge': '%i|g' % 500})

    def test_disabled_logger(self):
        statsd_logger.disabled = True
        with mock.patch('statsd.Client') as statsd_client:
            self.dummy.increment()
            statsd_client._send_assert_called_with(mock.ANY, None)
            self.dummy.decrement()
            statsd_client._send_assert_called_with(mock.ANY, None)
            self.dummy.timer(0.01)
            statsd_client._send_assert_called_with(mock.ANY, None)
            self.dummy.gauge(1)
            statsd_client._send_assert_called_with(mock.ANY, None)
        statsd_logger.disabled = False


if __name__ == '__main__':
    unittest.main()
