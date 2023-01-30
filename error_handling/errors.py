from discord.ext.commands.errors import CheckFailure

class AlreadyConnected(CheckFailure):
    pass

class NoVoiceChannel(CheckFailure):
    pass

class QueueEmpty(CheckFailure):
    pass