import discord
import logging
import re
import servos

logging.basicConfig(level=logging.INFO)

client = discord.Client()

COMMAND_PATTERN = r"^s(\d) ((\+|-)\d{1,4})( (\d*))?$"

@client.event
async def on_message(message):
    if not message.guild:
        logging.info("Ignoring DM from {}. o_0".format(message.author))
        return

    for match in re.findall(COMMAND_PATTERN, message.content, re.M):
        print(match)
        servo = int(match[0]) #int, 1 to 6
        displacement = int(match[1])
        if match[4]:
            time = int(match[4])
        else:
            time = int(abs(displacement) * 1.5) + 100
            

        logging.info(
            "command received by {}: move servo {} by {} units in {} ms".format(
                message.author,
                servo,
                displacement,
                time
            )
        )

        assert 0 <= servo <= 5
        assert -2500 <= displacement <= 2500
        assert 1 <= time <= 9999

        if servo == 4: # servo 4 is flipped, so invert displacement to make up for it
            displacement *= -1

        servos.displace(servo, displacement, time)

    if message.content == "arm info":
        await message.channel.send("idk just ask vivian")
    if message.content == "arm erect":
        servos.erect()
    if message.content == "arm dance":
        servos.dance()

@client.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)
    logging.info('--------')
    servos.erect()

with open("token", "r", encoding="utf-8") as file:
    TOKEN = file.read().strip()
client.run(TOKEN)
