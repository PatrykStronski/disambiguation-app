from config import BCOLORS

class Logger:
    def debug(self, text):
        print(BCOLORS["OKCYAN"] + text + BCOLORS["ENDC"])

    def successful(self, text):
        print(BCOLORS["OKGREEN"] + text + BCOLORS["ENDC"])

    def warning(self, text):
        print(BCOLORS["WARNING"] + text + BCOLORS["ENDC"])

    def error(self, text):
        print(BCOLORS["FAIL"] + text + BCOLORS["ENDC"])
