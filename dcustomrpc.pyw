import time
import pypresence
import ruamel.yaml
import os
import sys
import logging
import threading
import webbrowser
import requests
from io import StringIO
# Imports go here.

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    pass
# Imports tkinter if it can.

try:
    import pystray
    from PIL import Image
except ImportError:
    pass
# Tries to import PIL and pystray.

cycle = True
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
        with open(config_location, "r", encoding="utf8") as file_stream:
            loaded_file = ruamel.yaml.load(file_stream, Loader=ruamel.yaml.Loader)
    except ruamel.yaml.YAMLError:
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


def listening_sleeper(_time):
    global cycle
    ticks = _time / 0.1
    count = 0
    while cycle and count != ticks:
        try:
            time.sleep(0.1)
            count += 1
        except KeyboardInterrupt:
            cycle = False
            return
# Listens and sleeps.


log_stream = StringIO()
# The stream of the logger.


def main():
    logging.basicConfig(
        level=logging.INFO
    )

    formatting = logging.Formatter(
        "%(levelname)s:%(name)s:%(message)s"
    )

    log = logging.StreamHandler(log_stream)
    log.setLevel(logging.INFO)
    log.setFormatter(formatting)
    logger.addHandler(log)

    logger.info("Loading the config.")
    config = load_config(root + "/config.yaml")

    try:
        client_id = config.client_id
    except AttributeError:
        raise ClientIDNotProvided(
            "No client ID was provided in the config."
        )

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

    client = pypresence.Presence(
        client_id,
        pipe=0
    )

    logger.info("Connecting the client.")
    client.connect()

    try:
        games = game_cycle.get("games", [
                {
                    "state": "No cycle found.",
                    "details": "Nothing to cycle."
                }
        ])
        time_until_cycle = game_cycle.get(
            "time_until_cycle", 10)
        while cycle:
            for game in games:
                if not cycle:
                    break

                try:
                    client.update(**game)
                    logger.info("Changed the game.")
                    listening_sleeper(time_until_cycle)
                except TypeError:
                    logger.error("The game is formatted wrong.")

        client.close()
    except BaseException as e:
        try_show_error_box(e)
        logger.exception(e)
        sys.exit(1)
# The main script that is executed.


class TrayIcon(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
    # Initialises the thread.

    @staticmethod
    def exit_app():
        global cycle
        cycle = False
    # Exits the application.

    @staticmethod
    def display_logs():
        post = requests.post(
            "https://hastebin.com/documents",
            data=log_stream.getvalue()
        )
        webbrowser.open(
            "https://hastebin.com/" +
            post.json()["key"] + ".txt"
        )
    # Displays logs from the past 15 mins.

    def main_function(self):
        image = Image.open(root + "/logo.ico")

        menu = pystray.Menu(
            pystray.MenuItem(
                "Exit", self.exit_app
            ),
            pystray.MenuItem(
                "Show Logs", self.display_logs
            )
        )

        tray_icon = pystray.Icon(
            "DCustomRPC", image,
            "DCustomRPC", menu
        )

        def setup(icon):
            tray_icon.visible = True

        tray_icon.run(setup)
    # The main function.

    def run(self):
        try:
            self.main_function()
        except BaseException:
            pass
    # Tries to launch the task tray.


def flush_log_every_15_mins():
    while True:
        time.sleep(900)
        log_stream.truncate(0)
        log_stream.seek(0)
# Flushes the log every 15 mins.


if __name__ == '__main__':
    tray = TrayIcon()
    tray.start()

    threading.Thread(
        target=flush_log_every_15_mins,
        daemon=True
    ).start()

    try:
        main()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        try_show_error_box(e)
        logger.exception(e)
        sys.exit(1)
# Starts the script.
