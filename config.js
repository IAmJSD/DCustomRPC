exports.config = {

    // The application ID.
    "application_id" : "404026229931638784",

    /**
     * This is the interval that the RPC scrolls through the games in seconds.
     * 
     * Default: 10 Seconds.
    */
    "change_interval" : 10,

    /**
     * The chance a status change log message will have an emoticon.
     * The maximum integer is 1; the minimum is 0.
     * 
     * For example 0.75 would be equivelant to a 75% of getting an emoji
     * To disable the emoticons, just set this to 0.
    */
    "emoticon_chance" : 1,

    // The game list: All the games that shall be scrolled through.
    "game_list" : [
        {
            "details":"Feel free to check out my GitHub!",
            "state":"https://github.com/JakeMakesStuff",
            "largeImageKey":"gh_large",
            "largeImageText":"JakeMakesStuff"
        },
        {
            "details":"Powered by DCustomRPC!",
            "state":"This custom rich presence integration is powered by DCustomRPC.",
            "largeImageKey":"discord_large",
            "largeImageText":"Search for DCustomRPC on GitHub. You'll find it."
        },
        {
            "details":"Kuvien.io",
            "state":"Kuvien.io is the best image host.",
            "largeImageKey":"kuvien_large",
            "largeImageText":"https://kuvien.io/"
        },
        {
            "details":"Welcome!",
            "state":"I am a passionate 15 year old developer.",
            "largeImageKey":"wave_large"
        }
    ]
}

// The list of emoticons used in log messages.
exports.emoticons = [
    "^ω^", "~(˘▾˘~)", "(^o^)／", ">^_^<", "＼(^o^)／", "（^—^）"
]
