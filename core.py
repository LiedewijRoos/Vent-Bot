import discord,datetime,asyncio
from discord.ext import commands

class Vent(discord.Client):
    def __init__(self, approval, support, name, imagelink, cooldown=False):
        super().__init__()
        self.approval_ch = approval
        self.support_ch = support
        self.server_name = name
        self.imagelink = imagelink
        self.cooldown_on = cooldown

    async def on_ready(self):
        print("^w^ Ready")
        activity = discord.Activity(name='your woes', type=discord.ActivityType.listening)
        await self.change_presence(activity=activity)
        self.talkedRec = {}
        print(self.user)

    async def on_message(self, message):
        _approval = self.get_channel(self.approval_ch)
        _support = self.get_channel(self.support_ch)
        if isinstance(message.channel, discord.DMChannel) and message.author != self.user:
            if self.cooldown_on:
                timeMessageReceived = datetime.datetime.now()
                if (message.author in self.talkedRec):
                    if ((timeMessageReceived - self.talkedRec[message.author]).seconds < 600):
                        embedCooldown = discord.Embed(title='Anonymous Vent',
                                                      description='You are on a cooldown, please message again later.',
                                                      color=0x969696)
                        await message.author.send(embed=embedCooldown)
                        return
                    elif ((timeMessageReceived - self.talkedRec[message.author]).seconds >= 600):
                        pass
                elif (message.author not in self.talkedRec):

                    self.talkedRec[message.author] = timeMessageReceived

            embed = discord.Embed(title='Anonymous Vent', description=message.content, color=0xf1bdff)
            approvalMessage = await _approval.send(embed=embed)
            await approvalMessage.add_reaction('👍')
            await approvalMessage.add_reaction('❌')
            await approvalMessage.add_reaction('🤚')
            await approvalMessage.add_reaction('👮')
            embdedReceived = discord.Embed(title='Anonymous Vent',
                                           description="Your vent has been received and the mod team is reviewing it.",
                                           color=0x969696)
            embdedReceived.set_author(name="{0} Vent".format(self.server_name), icon_url=self.imagelink)
            await message.author.send(embed=embdedReceived)
            while (True):
                reaction,rUser = await self.wait_for('reaction_add', timeout=None)
                if (rUser != self.user and reaction.message.id == approvalMessage.id):
                    if (str(reaction) == '👍'):
                        embedVent = discord.Embed(title="Anonymous Vent", description=message.content, color=0xf1bdff)
                        supportMSG = await _support.send(embed=embedVent)
                        embedAccept = discord.Embed(color=0x969696)
                        embedAccept.add_field(name="Vent posted", value=supportMSG.jump_url)
                        await _approval.send(embed=embedAccept)
                        embdedPM = discord.Embed(title="Anonymous Vent",
                                                 description="The Mod Team has posted your vent",
                                                 color=0x969696)
                        await message.author.send(embed=embdedPM)
                        break
                    elif (str(reaction) == '❌'):
                        embedDenied = discord.Embed(title="Anonymous Vent",
                                                    description="The Mod Team has decided not to post your vent.",
                                                    color=0x969696)
                        await message.author.send(embed=embedDenied)
                        break
                    elif (str(reaction) == '🤚'):
                        embedTW = discord.Embed(title='Anonymous Vent',
                                                description="**The Moderator Team has decided to include a "
                                                            "trigger warning for the following vent as the "
                                                            "following vent contains content that is likely "
                                                            "triggering to a number of people such as "
                                                            "traumatic events, EDs, self-harm and so on**",
                                                color=0xf1bdff)
                        supportMSG = await _support.send(embed=embedTW)
                        twCleanedMSG = message.clean_content[:].replace("||","")
                        embedTWVent = discord.Embed(title='_ _', description=("||" + twCleanedMSG + " ||"),
                                                    color=0xf1bdff)
                        twVentMSG = await _support.send(embed=embedTWVent)
                        embedCaution = discord.Embed(color=0x969696)
                        embedCaution.add_field(name="Vent posted with Warning", value=supportMSG.jump_url)
                        await _approval.send(embed=embedCaution)
                        embdedPM = discord.Embed(title='Anonymous Vent',
                                                 description="The Mod Team has posted your vent with a trigger warning",
                                                 color=0x969696)
                        await message.author.send(embed=embdedPM)
                        break
                    elif (str(reaction) == '👮'):
                        embedDeny = discord.Embed(title='Author Identified',
                                                  description='The author of the rejected vent is ' +
                                                              message.author.mention + "\n" + approvalMessage.jump_url,
                                                  color=0x969696)
                        await _approval.send(embed=embedDeny)
                        embedDenyPM = discord.Embed(title="Your identity has been revealed to the mod team",
                                                    description="Due to the rule breaking contents of your vent, the"
                                                                " mod team has been made aware of your identity",
                                                    color=0x969696)
                        await message.author.send(embed=embedDenyPM)
                        break
ventBot = Vent(_APPROVAL,_SUPPORT,_NAME,_LOGO)
ventBot.run(_TOKEN)