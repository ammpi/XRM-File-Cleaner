import logging
from os.path import abspath, join, dirname


_logger_form = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s',
                                  datefmt='%d/%m/%Y %H:%M:%S')

_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_logger_form)
_stream_handler.setLevel(logging.WARNING)

_log_path = join(abspath(dirname(__file__)), "xrmfilecleaner.log")
_file_handler = logging.FileHandler(_log_path)
_file_handler.setFormatter(_logger_form)
_file_handler.setLevel(logging.DEBUG)


log = logging.getLogger("xrmfilecleaner")
log.setLevel(logging.DEBUG)
log.addHandler(_stream_handler)
log.addHandler(_file_handler)
