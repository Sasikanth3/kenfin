import datetime
import schedule
import time

from connector.auth_stack import AuthSingletonStack
from inference.symbol_factory import SymbolFactory


def get_tradables():
    return [{"symbol_name": "ICICI", "interval": "minute", "model_path": "../resources/pkls/icici.pkl","instrument_type":"FUT"}]

#todo :need lot more readable names
if __name__ == "__main__":
    # todo : need to be handled by a pipeline object for futher testability
    #todo :fix the 9:30 bug , if it starts later it has to be set to current time
    symbol_factory = SymbolFactory(get_tradables(), AuthSingletonStack())
    i = 0
    for symbol in symbol_factory.symbols:
        schedule.every(1).minutes.do(symbol.symbol_action)
        # schedule to morning 9:30 and separate each symbol by a lapse of a second
        schedule.jobs[-1].next_run = datetime.datetime.now().replace(hour=9, minute=30, second=i)
        i += 15

    # look for any new tasks if they are there
    while 1:
        schedule.run_pending()
        # for now 15 seconds is good but ideally this should be decided by the number of lapses in time gap
        time.sleep(15)
