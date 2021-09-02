import os
import sys

import logging
import justlogs

from divprop.ciphers import ciphers

justlogs.setup(level="DEBUG")

log = logging.getLogger(__name__)

name = sys.argv[1].lower()
cipher = ciphers[name]()

path = f"data/{name}"
try:
    os.mkdir(path)
except FileExistsError:
    pass

justlogs.addFileHandler(f"{path}/divcore")
log.info(
    f"cipher {name} {cipher}"
)
log.info(f"path {path}")

snd = cipher.make_sandwich()
snd.compute_divcore(chunk=128, filename=f"{path}/divcore")
