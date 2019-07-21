from config import CODE_DICT
import api

api.update_xrate(CODE_DICT["USD"], CODE_DICT["UAH"])
api.update_xrate(CODE_DICT["EUR"], CODE_DICT["UAH"])
api.update_xrate(CODE_DICT["RUB"], CODE_DICT["UAH"])
api.update_xrate(CODE_DICT["EUR"], CODE_DICT["USD"])
api.update_xrate(CODE_DICT["BTC"], CODE_DICT["USD"])
api.update_xrate(CODE_DICT["BTC"], CODE_DICT["UAH"])