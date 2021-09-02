import copy
import pickle
import logging

from pathlib import Path
from functools import wraps
from hashlib import sha256

DEFAULT_CACHE = Path(".cache/")
DEFAULT_LOGGER = logging.getLogger()


NotFound = object()


def cached_method(method):
    cache = {}
    disabled_shown = False

    def calc_key(self, *args, **kwargs):
        cls_name = type(self).__name__
        meth_name = method.__name__

        args_key = str((args, sorted(kwargs.items())))
        args_key = sha256(args_key.encode()).hexdigest().upper()
        key = f"{cls_name}.{meth_name}.self_{self.cache_key}.args_{args_key}"
        return key

    @wraps(method)
    def call(self, *args, **kwargs):
        nonlocal cache, calc_key, disabled_shown
        log = getattr(self, "log", DEFAULT_LOGGER)
        self.CACHE = getattr(self, "CACHE", DEFAULT_CACHE)
        if self.CACHE:
            self.CACHE = Path(self.CACHE)

            if not self.CACHE.is_dir():
                log.debug(f"cache folder {self.CACHE} does not exist, disabling cache")
                self.CACHE = None
        else:
            if not disabled_shown:
                log.debug("cache disabled")
                disabled_shown = True
            self.CACHE = None

        key = calc_key(self, *args, **kwargs)

        ret = cache.get(key, NotFound)
        if ret is not NotFound:
            return copy.deepcopy(ret)

        if self.CACHE:
            cache_filename = self.CACHE / key
            try:
                ret = pickle.load(open(cache_filename, "rb"))
                log.info(f"load {cache_filename} succeeded")
            except Exception as err:
                log.debug(f"load {cache_filename} failed: {err}")
                pass

            if ret is not NotFound:
                cache[key] = ret
                return copy.deepcopy(ret)

            log.info(f"computing {key}")

        ret = method(self, *args, **kwargs)
        cache[key] = ret

        if self.CACHE:
            pickle.dump(ret, open(cache_filename, "wb"))
            log.info(f"save {cache_filename} succeeded")
        return copy.deepcopy(ret)

    call._calc_key = calc_key
    call._cache = cache
    return call


def cached_func(method=None, CACHE=DEFAULT_CACHE, log=DEFAULT_LOGGER):
    def deco(method):
        nonlocal CACHE, log
        method._cache = {}
        if CACHE:
            CACHE = Path(CACHE)
            if not CACHE.is_dir():
                log.warning(
                    f"cache folder {CACHE} does not exist, "
                    "disabling file cache"
                )
                CACHE = None
        else:
            log.warning("file cache disabled")
            CACHE = None

        @wraps(method)
        def call(*args, **kwargs):
            meth_name = method.__name__

            args_key = str((args, sorted(kwargs.items())))
            args_key = sha256(args_key.encode()).hexdigest().upper()
            key = f"{meth_name}.args_{args_key}"

            ret = method._cache.get(key, NotFound)
            if ret is not NotFound:
                return copy.deepcopy(ret)

            if CACHE:
                cache_filename = CACHE / key
                try:
                    ret = pickle.load(open(cache_filename, "rb"))
                    log.info(f"load {cache_filename} succeeded")
                except Exception as err:
                    log.warning(f"load {cache_filename} failed: {err}")
                    pass

                if ret is not NotFound:
                    method._cache[key] = ret
                    return copy.deepcopy(ret)

            log.info(f"computing {key}")

            ret = method(*args, **kwargs)
            method._cache[key] = ret

            if CACHE:
                pickle.dump(ret, open(cache_filename, "wb"))
                log.info(f"save {cache_filename} succeeded")
            return copy.deepcopy(ret)
        return call
    if method is None:
        return deco
    return deco(method)
