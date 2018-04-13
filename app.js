/**
 * DCustomRPC
 * 
 * Created by JakeMakesStuff and contributors (https://github.com/JakeMakesStuff/DCustomRPC/contributors).
 */

// Imports go here.
const { info, warn, error } = require("fancy-log");
const { config, emoticons } = require("./config");
const { version } = require("./package.json");
const { Client } = require("discord-rpc");
const { join } = require("path");

// Invokes an instance of the RPC client.
const rpc = new Client({ transport: "ipc" });

// Sets a variable with the current game.
let current_game = {};

// Startup message.
info(`Starting DCustomRPC, Version: ${version}. ~(˘▾˘~)`);

/**
 * Please don't change the handling of the following "if" statements, the use of RangeError is correct.
 * 
 * Read https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RangeError for more info.
 */

// Throws a RangeError if the change interval is 0.
if (Number(config.change_interval) === 0) {
    error(new RangeError(`The change interval can not be 0. The option can be found in ${join(__dirname, "./config.js") + ":11"} (Line 11). (╯°□°）╯︵ ┻━┻`));
    process.exit(-1);
}

// Throws a RangeError if the change interval is 0.
if (Number(config.emoticon_chance) > 1 || Number(config.emoticon_chance) < 0) {
    error(new RangeError(`The emoticon chance integer must be a number between 0 and 1, for example: 0.75 for a 75% chance of emoticons in an activity change message.\nThe option can be found in ${join(__dirname, "./config.js") + ":20"} (Line 20). (╯°□°）╯︵ ┻━┻`));
    process.exit(-1);
}

// RPC ready event executes loop function.
rpc.once("ready", () => {
    info(`Logged into Discord with the application ID ${config.application_id}. (^o^)／`);
    current_game = {};
    gameloop();
    setInterval(gameloop, config.change_interval * 1000);
});

// Logs into Discord if it is not a test.
if (process.argv[2] != "test") {
    rpc.login(config.application_id).catch(err => {
        error(`Error logging into RPC client! (╯°□°）╯︵ ┻━┻\n${err}`);
    });
} else {
    info("At least before logging into Discord, all seems well! >^_^<");
}

/* Reusable functions */

// Defines the game changing loop.
async function gameloop() {
    let loop = true;
    while(loop) {
        let random = Math.floor(Math.random() * config.game_list.length);
        if ((config.game_list[random] !== current_game) || (config.game_list.length === 1)) {
            current_game = config.game_list[random];
            rpc.setActivity(config.game_list[random]);
            info(emoticonify("Changed activity."));
            loop = false;
        }
    }
}

// Adds emoticons to log messages.
function emoticonify(string) {
    if (Math.random() <= config.emoticon_chance) {
        let randEmote = emoticons[Math.floor(Math.random() * emoticons.length)];
        return `${string} ${randEmote}`;
    } else return string;
}
