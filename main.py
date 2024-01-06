import discord
from discord.ext import tasks
import datetime as dt
import responses

DISCORD_TOKEN = ""#your bot token

# Define required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create client object
client = discord.Client(intents=intents)
POLL_OPTION_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

SENT_MESSAGE_IDS = []


@client.event
async def on_ready():
    print(f'{client.user} is now running!')


@client.event
async def on_message(message):
    global POLL_OPTION_EMOJIS

    # Handle responses
    try:
        response = responses.get_response(message.content)
        await message.channel.send(response)
    except Exception as e:
        print(e)

    # Handle poll creation
    if message.content.startswith("!create_poll"):
        params = message.content.split(";")
        name = params[0].replace("!create_poll", "").strip()
        question = params[1].strip()
        options = [x.strip() for x in params[2].strip().split(",")]
        orig_options = options
        options_count = len(options)
        countdown = params[3]

        try:
            countdown = int(countdown)
        except Exception as e:
            pass

        error = validate_params(name, question, options, countdown)

        if error is not None:
            embed = discord.Embed(title="Error", description=error, color=discord.Color.red())
            sent = await message.channel.send(embed=embed)
            return

        for i in range(len(options)):
            options[i] = f"{POLL_OPTION_EMOJIS[i]} {options[i]}"
        options = '\n'.join(options)

        embed = discord.Embed(title=f"POLL: {name}", description=f"**{question}\n{options}**", color=0x12ff51)
        sent = await message.channel.send(embed=embed)

        POLL_OPTION_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        for i in range(options_count):
            await sent.add_reaction(POLL_OPTION_EMOJIS[i])

        SENT_MESSAGE_IDS.append(sent.id)
        end_time = dt.datetime.utcnow() + dt.timedelta(seconds=int(countdown) * 60)

        @tasks.loop(seconds=1)
        async def update_countdown():
            remaining_time = (end_time - dt.datetime.utcnow()).total_seconds()

            if remaining_time > 0:
                minutes, seconds = divmod(int(remaining_time), 60)

                # Edit the message
                description = f"**{question}**\n{options}\n\n*Poll ends in {minutes:02d}:{seconds:02d}*"
                embed = discord.Embed(title=f"POLL: {name}", description=description, color=0x12ff51)
                await sent.edit(embed=embed)

            else:
                sent_message = await message.channel.fetch_message(sent.id)

                poll_results_count = {}
                total_reactions = 0

                # If countdown expired
                for reaction in sent_message.reactions:
                    for ind, emoji in enumerate(POLL_OPTION_EMOJIS):
                        if reaction.emoji == emoji:
                            poll_results_count[ind + 1] = reaction.count - 1
                            if reaction.count > 1:
                                total_reactions += 1

                poll_results_message = ""
                for ind, count in enumerate(poll_results_count):
                    perc = round(poll_results_count[ind + 1] / total_reactions * 100)
                    poll_results_message += f"{orig_options[ind]} ~ {perc}% ({poll_results_count[ind + 1]} votes)\n"

                # Send the results message
                embed = discord.Embed(title=f"POLL RESULTS: {name}", description=poll_results_message,
                                      color=0x13a6f0)
                await message.channel.send(embed=embed)

                await sent_message.delete()
                update_countdown.cancel()

        update_countdown.start()


@client.event
async def on_raw_reaction_add(payload):
    global SENT_MESSAGE_IDS
    # Get the message object
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # Get the member object
    guild = message.guild
    member = await guild.fetch_member(payload.user_id)

    if payload.member.bot:
        return

    sent_by_bot = False
    for i in SENT_MESSAGE_IDS:
        if i == message.id:
            sent_by_bot = True
            break
    if not sent_by_bot:
        return

    if payload.emoji.name not in POLL_OPTION_EMOJIS:
        # Remove reaction
        await message.remove_reaction(payload.emoji.name, member)
        return

    user_reaction_count = 0
    for r in message.reactions:
        async for u in r.users():
            if u.id == payload.user_id:
                user_reaction_count += 1
                if user_reaction_count > 1:
                    await message.remove_reaction(payload.emoji.name, member)
                    break


def validate_params(name, question, options, countdown):
    if name == "":
        return "Poll name shouldn't be empty"
    if len(name) >= 20:
        return "Name shouldn't be more than 15 characters"
    if question == "":
        return "Question shouldn't be empty"
    if len(options) <= 1:
        return "There must be a minimum of 2 options"
    if len(options) > 5:
        return "Maximum options allowed are 5"
    if not isinstance(countdown, int):
        return "Countdown value must be integer"

    return None


if __name__ == "__main__":
    # Start the bot
    client.run(DISCORD_TOKEN)
