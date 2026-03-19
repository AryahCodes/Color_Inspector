import os


class Logger:
    def __init__(self, log_path):
        log_dir = os.path.dirname(log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.file = open(log_path, "a")

    def log(self, message):
        print(message)
        self.file.write(message + "\n")
        self.file.flush()

    def close(self):
        if self.file and not self.file.closed:
            self.file.close()
