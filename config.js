exports.config = {

    // The application ID.
    "application_id" : "404026229931638784",

    /**
     * This is the interval that the RPC scrolls through the games in seconds.
     * 
     * Default: 10 Seconds.
     */
    "change_interval" : 10,

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

exports.emoticons = [
    /** 
     * Add or remove spaces to vary the chance of getting an emoticon in the "Changed Activity" message.
     * 
     * Default: 6/34.
     */ 
    "^ω^", "~(˘▾˘~)", "(^o^)／", ">^_^<", "＼(^o^)／", "（^—^）", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
]
