import asyncio
import pypresence
import yaml
import os
import sys
import logging
# Imports go here.

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    pass
# Imports tkinter if it can.

cycle = False
# Sets whether we are cycling games.


class ConfigNotFound(Exception):
    pass
# The config not found exception.


class ConfigOpenError(Exception):
    pass
# The exception when the config cannot be opened.


class ClientIDNotProvided(Exception):
    pass
# The exception when a client ID is not provided.


def dict2class(_dict: dict):
    class DictBasedClass:
        def __getattribute__(self, item):
            self.__getattr__(item)

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


def try_show_error_box(exception):
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "DCustomRPC", "{}".format(exception))
    except BaseException:
        pass
# Tries to show a error.


async def game_cycle_loop(game_cycle, client, loop):
    try:
        games = game_cycle.get("games", [
                {
                    "state": "No cycle found.",
                    "details": "Nothing to cycle."
                }
        ])
        try:
            time_until_cycle = game_cycle.get(
                "time_until_cycle", 10)
        except KeyError:
            time_until_cycle = 10
        while cycle:
            for game in games:

                def blocking_wrap():
                    client.update(**game)

                try:
                    await loop.run_in_executor(
                        None,
                        blocking_wrap
                    )
                    logger.info("Changed the game.")
                    await asyncio.sleep(time_until_cycle)
                except TypeError:
                    logger.error("The game is formatted wrong.")
    except BaseException as e:
        try_show_error_box(e)
        logger.exception(e)
        sys.exit(1)
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
    except AttributeError:
        game_cycle = {
            "time_until_cycle": 10,
            "games": [
                {
                    "state": "No cycle found.",
                    "details": "Nothing to cycle."
                }
            ]
        }

    cycle = True

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
    try:
        loop = asyncio.get_event_loop()
        main(loop)
        loop.run_forever()
    except SystemExit:
        pass
    except BaseException as e:
        try_show_error_box(e)
        logger.exception(e)
        sys.exit(1)
# Starts the script.
