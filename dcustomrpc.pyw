import asyncio
import pypresence
import yaml
import os
import logging
# Imports go here.


cycle = False
# Sets whether we are cycling games.


class ConfigNotFound(Exception):
    pass
# The config not found exception.


class NothingToDoHere(Exception):
    pass
# I have nothing to do here!


class GamesNotFound(Exception):
    pass
# The Games were not found.


class ConfigOpenError(Exception):
    pass
# The exception when the config cannot be opened.


class ClientIDNotProvided(Exception):
    pass
# The exception when a client ID is not provided.


def dict2class(_dict: dict):
    class DictBasedClass:
        pass

    for key in _dict:
        setattr(DictBasedClass, key, _dict[key])

    return DictBasedClass
# Converts a dictionary to a class.


def load_config(config_location: str):

    if not os.path.isfile(config_location):
        raise ConfigNotFound(
            "Could not find the config."
        )

    try:
        with open(config_location, "r") as file_stream:
            loaded_file = yaml.load(file_stream)
    except yaml.YAMLError:
        raise ConfigOpenError(
            "The YAML config seems to be malformed."
        )
    except IOError:
        raise ConfigOpenError(
            "Could not open the config file."
        )
    except FileNotFoundError:
        raise ConfigNotFound(
            "Could not find the config."
        )

    return dict2class(loaded_file)
# Loads the config.


logger = logging.getLogger("dcustomrpc")
# Sets the logger.


root = os.path.dirname(os.path.abspath(__file__))
# The root folder for DCustomRPC.


async def game_cycle_loop(game_cycle, client, loop):
    try:
        games = game_cycle["games"]
    except KeyError:
        raise GamesNotFound("Games not found in the config.")
    try:
        time_until_cycle = game_cycle["time_until_cycle"]
    except KeyError:
        time_until_cycle = 10
    while cycle:
        for game in games:

            def blocking_wrap():
                client.update(**game)

            await loop.run_in_executor(
                None,
                blocking_wrap
            )
            logger.info("Changed the game.")
            await asyncio.sleep(time_until_cycle)
# Runs the game cycle loop.


def main(loop):
    logging.basicConfig(level=logging.INFO)

    logger.info("Loading the config.")
    config = load_config(root + "/config.yaml")

    try:
        client_id = config.client_id
    except AttributeError:
        raise ClientIDNotProvided(
            "No client ID was provided in the config."
        )

    global cycle

    try:
        game_cycle = config.game_cycle
        logger.info("Found a list of games to cycle.")
        cycle = True
    except AttributeError:
        game_cycle = None

    if not game_cycle:
        raise NothingToDoHere("I have nothing to do here!")

    client = pypresence.Presence(
        client_id,
        pipe=0
    )

    logger.info("Connecting the client.")
    client.connect()

    if game_cycle:
        loop.create_task(
            game_cycle_loop(game_cycle, client, loop)
        )
        logger.info("Created the game cycle task.")
# The main script that is executed.


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    main(loop)
    loop.run_forever()
# Starts the script.
