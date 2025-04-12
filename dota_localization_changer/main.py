# -----------
# - r41ngee -
# -----------

import logging
from misc import *

logging.basicConfig(
    # level=config_logger_level_dict[config["logger_lvl"]],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='.log',
    filemode='w'
)

if __name__=="__main__":
    # main()
    input("Нажмите ENTER чтобы выйти")
    endlog(0)
