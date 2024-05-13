import random
import discord
from discord.ext import commands
import logging
from argparse import ArgumentParser
import json


class Logger:

    def __init__(self, config:dict):

        print ("logger name ",__name__)
        self.__level___ = config["log_level"] 

        formatter = logging.Formatter(config["log_format"])

        handler = logging.StreamHandler()
        handler.setLevel(self.__level___)
        handler.setFormatter(formatter)

        f_handler = logging.FileHandler(config["log_file"])
        f_handler.setLevel(self.__level___)
        f_handler.setFormatter(formatter)

        self.log = logging.getLogger(__name__)
        self.log.setLevel(self.__level___)
        self.log.addHandler(handler)
        self.log.addHandler(f_handler)

    def infolog(self, msg: str):
        self.log.info(msg)

    def errorlog(self, msg: str):
        self.log.error(msg)

    def debuglog(self, msg: str):
        self.log.debug(msg)


class Parse:
    @staticmethod
    def parse_args():
        parser = ArgumentParser()
        parser.add_argument(
            "-c", "--config", help="Config file", required=True, dest="config"
        )
        return parser.parse_args()

class Json:
    @staticmethod
    def read_json_file(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{file_path}'.")
            return {}

class MyClient(commands.Bot):
    def __init__(self, config, *args, **kwargs):
        self.prefix = config.get("prefix")
        self.reaction = {}
        log_config = config.get("log_config", {})
        self.log = Logger(log_config)
        
        super().__init__(command_prefix=self.prefix, *args, **kwargs)
        
    async def on_ready(self):
        self.log.infolog("Bot running")
        print(f'\n\n--------[ LOGGED AS {self.user} ]--------\n')

    async def on_message(self, message):
        print(f'[ @{message.author}:{message.channel.name} ] {message.content}')
        if not message.author.bot:
            await self.process_prefix(message)

    async def process_prefix(self, message):
        if message.content.startswith(self.prefix):
            await self.process_commands(message)
        else:
            await self.process_message(message)

    async def process_commands(self, message):
        if message.content[1:].startswith('help'):
            self.log.infolog("[Command] Help")

            await message.channel.send("""```
** ------------------------ How to use it ------------------------ **

   !help                        aide du bot
                                       
   !add MESSAGE REPONSE         ajouter une reaction
   !rm REPONSE                  supprimer une reaction
   !ll                          liste des reactions

** --------------------------------------------------------------- **
```""")
            
        elif message.content[1:].startswith('add'):
            self.log.infolog("[Command] Add")
            args = message.content.split()[1:]
            if len(args) == 2 :
                trigger = args[0]
                response = args[1]
                self.reaction[trigger] = response
                await message.channel.send(f"`[ Reaction add ] '{trigger}' --> '{response}'`")

            else:
                await message.channel.send("`[!] mauvais usage [!]`")
        
        elif message.content[1:].startswith('rm'):
            self.log.infolog("[Command] Rm")
            args = message.content.split()[1:]
            if len(args) == 1:
                trigger = args[0]
                if self.reaction.get(trigger):
                    self.reaction.pop(trigger)
                    await message.channel.send(f"`[ Reaction removed ] --> '{trigger}'`")

                else:
                    self.log.errorlog("[Non reconnus] Rm")
                    await message.channel.send("`[!] Reaction non reconnus [!]`")
            else:
                self.log.errorlog("[Mauvais usage] Rm")
                await message.channel.send("`[!] mauvais usage [!]`")


        elif message.content[1:].startswith('ll'):
            self.log.errorlog("[Command] Ll")
            await message.channel.send("`[ List of reactions ]`")
            for trigger in self.reaction:
                await message.channel.send(f"`{trigger} --> {self.reaction[trigger]}`")


    async def on_member_join(self, member):
        self.log.infolog("[Notification] Nouveaux sur le serveur")
        default_channel = member.guild.system_channel
        if default_channel:
            await default_channel.send(f"🌸ꗥ～ꗥ🌸🌸 𝐵𝒾𝑒𝓃𝓋𝑒𝓃𝓊𝑒 {member.mention} 🌸🌸ꗥ～ꗥ🌸")

    async def on_member_remove(self, member):
        self.log.infolog("[Notification] Adios sur le serveur")
        default_channel = member.guild.system_channel
        if default_channel:
            await default_channel.send(f"🌸ꗥ～ꗥ🌸🌸 𝐵𝓎𝑒 𝒷𝓎𝑒 𝒮𝒶𝓎𝑒 𝒻𝑜𝓇𝑒𝓋𝑒𝓇 {member.mention} 🌸🌸ꗥ～ꗥ🌸")

    async def process_message(self, message):
        for trigger in self.reaction:
            if message.content.startswith(trigger):
                self.log.infolog(f"[Bot send message] {self.reaction[trigger]}")
                await message.channel.send(self.reaction[trigger])

    def run_bot(self, token):
        self.run(token)



if __name__ == "__main__":

    argument = Parse.parse_args()
    config = Json.read_json_file(argument.config)

    TOKEN = config.get("token")

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(config=config, intents=intents)
    client.run(TOKEN)


