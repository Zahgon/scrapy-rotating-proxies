# -*- coding: utf-8 -*-
from __future__ import division
import time
import random
import logging
import math

import attr

from .utils import extract_proxy_hostport

logger = logging.getLogger(__name__)


class Proxies(object):
    """
    Expiring proxies container.

    A proxy can be in 3 states:

    * good;
    * dead;
    * unchecked.

    Initially, all proxies are in 'unchecked' state.
    When a request using a proxy is successful, this proxy moves to 'good'
    state. When a request using a proxy fails, proxy moves to 'dead' state.

    For crawling only 'good' and 'unchecked' proxies are used.

    'Dead' proxies move to 'unchecked' after a timeout (they are called
    'reanimated'). This timeout increases exponentially after each
    unsuccessful attempt to use a proxy.
    """
    def __init__(self, proxy_list, backoff=None):
        self.proxies = {url: ProxyState() for url in proxy_list}
        self.proxies_by_hostport = {
            extract_proxy_hostport(proxy): proxy
            for proxy in self.proxies
        }
        self.unchecked = set(self.proxies.keys())
        self.good = set()
        self.dead = set()
        self.used = set()

        if backoff is None:
            backoff = exp_backoff_full_jitter
        self.backoff = backoff

    def get_random(self):
        """ Return a random available proxy (either good or unchecked) """
        pass

    def get_proxy(self, proxy_address):
        """
        Return complete proxy name associated with a hostport of a given
        ``proxy_address``. If ``proxy_address`` is unkonwn or empty,
        return None.
        """
        pass

    def mark_dead(self, proxy, _time=None):
        """ Mark a proxy as dead """
        pass

    def mark_good(self, proxy):
        """ Mark a proxy as good """
        pass

    def reanimate(self, _time=None):
        """ Move dead proxies to unchecked if a backoff timeout passes """
        pass

    def reset(self):
        """ Mark all dead proxies as unchecked """
        pass

    def _clean_proxy(self, proxy):
        """ Clean proxy so that it can be safely used in logs """
        pass

    @property
    def mean_backoff_time(self):
        pass

    @property
    def reanimated(self):
        pass

    def __str__(self):
        n_reanimated = len(self.reanimated)
        return "Proxies(good: {}, dead: {}, unchecked: {}, reanimated: {}, " \
               "mean backoff time: {}s)".format(
            len(self.good), len(self.dead),
            len(self.unchecked) - n_reanimated, n_reanimated,
            int(self.mean_backoff_time),
        )


@attr.s
class ProxyState(object):
    failed_attempts = attr.ib(default=0)
    next_check = attr.ib(default=None)
    backoff_time = attr.ib(default=None)  # for debugging


def exp_backoff(attempt, cap=3600, base=300):
    """ Exponential backoff time """
    # this is a numerically stable version of
    # min(cap, base * 2 ** attempt)
    max_attempts = math.log(cap / base, 2)
    if attempt <= max_attempts:
        return base * 2 ** attempt
    return cap


def exp_backoff_full_jitter(*args, **kwargs):
    """ Exponential backoff time with Full Jitter """
    return random.uniform(0, exp_backoff(*args, **kwargs))
