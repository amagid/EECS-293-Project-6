'''
Class to implement caching function. Exposes a 'get' method which retrieves
an object from the cache by key or creates a new object at the given key if no
such object currently exists.
'''
class Cache():
    
    def __init__(self):
        self._cache = {}

    # TA: Is there a better way I can organize this method?
    # I'd rather have fewer conditionals, but I'd also rather 
    # not sandwich the nominal case in between error cases by
    # moving the "if key is None" up into a guard clause.
    def get(self, key, constructor):

        if key in self._cache:
            return self._cache[key]
        elif constructor is not None:
            self._cache[key] = constructor(key)
            return self._cache[key]

        if key is None:
            raise ValueError("No key passed")
        else:
            raise ValueError("Key not found, and no constructor passed to create new object")
            
