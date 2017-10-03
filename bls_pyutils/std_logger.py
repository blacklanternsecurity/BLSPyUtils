import logging
import logging.handlers


class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        self.logger = logging.getLogger()
        if not self.logger.handlers:
            self.handler = logging.handlers.RotatingFileHandler(
                self.log_path, maxBytes=250000000, backupCount=2)
            self.handler.setFormatter(
                logging.Formatter('%(asctime)s #%(levelname)s# %(message)s', '%m/%d/%Y %I:%M:%S %p'))
            self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)
