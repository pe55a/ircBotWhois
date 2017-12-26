# ircBotWhois

- bot will connect to each server specified from config file
- bot will use same nickname in each server connection
- bot will reply to servers PING to avoid to lose the connections
- bot will reply to private msg with "Hello " + username
- irc user will send a private msg to bot to perform a whois in each server the bot is connected to


### BOT side
    - add/remove servers in the config file
    - modify the nickname of the bot in the config file
    - start the program


### irc user side
    - connect to one of the servers specified in the bot config
    - /ping botnick  (to check that bot is running)
    - /msg botnick <message> (to open a private window chat and verify that bot reply correctly)
    - /msg botnick whois <NickToFind>

### Bugs / issues
    - no sanity checks are present on input parameters
    - sometimes the bot doesn't answer due to the bad thread implementation (fixes to be done)
    - sometimes the bot doesn't answer due to socket busy with other's thread tasks(fixes to be done)
    - bot replies with End of /WHOIS list instead of Nosuchnick )probably still due to threads/socket issues above
  
### example

<ircUser111> whois poposjasjs

<botbottest1> [:orwell.freenode.net]: :Nosuchnick/channel

<botbottest1> [:irc.mzima.net]: :Nosuchnick/channel


