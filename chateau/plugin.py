#!/usr/bin/env python3

class Plugin(object):
    def subscribe(fn, *types):
        new = set(types)
        try:
            old = getattr(fn, 'subscription')
            union = old | new
        except AttributeError:
            union = new
        setattr(fn, 'subscription', union)
