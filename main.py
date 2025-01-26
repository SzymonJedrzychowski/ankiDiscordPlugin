from collection_wrapper import CollectionWrapper
from dotenv import load_dotenv
import os
import discord


def main():
    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    collection_wrapper = CollectionWrapper('data/collection.anki2')

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        to_send = None

        content = message.content

        if content.startswith('$hello'):
            to_send = collection_wrapper.generate_welcome_message()
        elif content.startswith('$decks'):
            to_send = collection_wrapper.generate_decks_message()
        elif content.startswith('$deck'):
            to_send = collection_wrapper.select_deck(content[5:])

        if to_send:
            await message.channel.send(to_send)

    client.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    main()
