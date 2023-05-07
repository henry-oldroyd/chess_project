# this file does 2 things:
# it decides which objects should be exported as part of the database module
# it initialise the database (creates a connection and creates all tables)

# objects to export
from .create_database import create_session, end_session, create_engines, end_engines
from .models import Minimax_Cache_Item, create_tables
from .handle_games import get_saved_game, save_game


# initialise database
engines_dict = create_engines(echo=False)

create_tables(engines_dict)

persistent_DB_engine = engines_dict["persistent_DB_engine"]
volatile_RAM_engine = engines_dict["volatile_RAM_engine"]
