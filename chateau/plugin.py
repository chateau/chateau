#!/usr/bin/env python3

class Plugin(object):
    """A plugin. This is meant to be subclassed."""
    
    def __init__(self, bot):
        self.apply_method_subscriptions()
    
    def apply_method_subscriptions(self):
        """Apply subscriptions "reserved" using :py:func:`.subscribe`. Called automatically by :py:func:`__init__`."""
    
    @classmethod
    def subscribe(fn, *types):
        """Flags an unbound instance method for subscription to certain event types by :py:func:`.apply_method_subscriptions`. Intended for use as a decorator.
        
        Example::
           class SomePlugin(Plugin):
               @subscribe('NICK')
               def on_nick_change:
                   pass
        
        """
        new = set(types) # The new event types to subscribe to
        try:
            old = getattr(fn, 'subscribed_to') # Get any event types to which the function is already subscribed
            union = old | new # Merge the two sets. Equivalent to old.union(new).
        except AttributeError:
            union = new # If there is no existing subscription, just save the new ones.
        setattr(fn, 'subscribed_to', union) # Save the types the function is subscribed to
        return fn # Same object