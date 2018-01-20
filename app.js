const { Client } = require("discord-rpc");
const log = require("fancy-log");
const config = require("./config.json");
// Imports go here.

const rpc = new Client({ transport: "ipc" });
// Defines the RPC client.

function gameloop() {
    var x = true;
    while(x) {
        var r = Math.floor(Math.random() * config.game_list.length);
        if (config.game_list[r] != global.current_game) {
            global.current_game = config.game_list[r];
            var game = config.game_list[r];
            game.startTimestamp = Date.now();
            rpc.setActivity(game);
            log("Changed activity.");
            x = false;
        }
    }
}
// Defines the game changing loop.

rpc.on('ready', () => {
    log(`Logged into Discord with the application ID ${config.application_id}.`);
    global.current_game = {};
    gameloop();
    setInterval(gameloop, config.change_interval*1000);
});
// Defines the RPC being ready and starts the loop.

rpc.login(config.application_id).catch(log.error);
// Logs into Discord.
