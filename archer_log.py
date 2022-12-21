import logging
import sys

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s \t\t\t%(pathname)s %(funcName)s %(lineno)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
log.addHandler(handler)

if __name__ == '__main__':
    log.info('hello world')
