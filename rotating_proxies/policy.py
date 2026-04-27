# -*- coding: utf-8 -*-
from scrapy.exceptions import IgnoreRequest


class BanDetectionPolicy(object):
    """ Default ban detection rules. """
    NOT_BAN_STATUSES = {200, 301, 302}
    NOT_BAN_EXCEPTIONS = (IgnoreRequest,)

    def response_is_ban(self, request, response):
        pass

    def exception_is_ban(self, request, exception):
        pass
