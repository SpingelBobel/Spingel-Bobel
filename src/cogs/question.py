import re
import io
import random
import logging
import discord

from discord.ext import commands
from PIL import Image, ImageDraw, ImageSequence, ImageFont


class Question(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Loaded Question Cog")
        self.responses = [
            'Yes',
            'Yes',
            'Yes',
            'Certainly',
            'No',
            'No',
            'No',
            'Absolutely not',
            'Maybe some day',
            'Maybe some day',
        ]
        self.paired_responses = [
            'Both',
            'Neither',
            'The first one',
            'The last one',
        ]
        self.easter_eggs = [
            'Wow really? You asked that?',
            '...',
            'I think you already know',
            'I can\'t be bothered',
        ]
        self.bb_easter_eggs = [
            'If doveman says so',
            'Go ask dove, I have no clue',
        ]

        with open("config/questions.txt", "r") as fp:
            self.bot.total_questions = int(fp.readline())

    def update_questions(self):
        self.bot.total_questions += 1
        with open("config/questions.txt", "w") as fp:
            fp.write(str(self.bot.total_questions))

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message) and (message.content.startswith(f'<@{self.bot.user.id}>') or message.content.startswith(f'<@!{self.bot.user.id}>')):
            question = message.content[len(f'<@{self.bot.user.id}>') if message.content.startswith(f'<@{self.bot.user.id}>') else len(f'<@!{self.bot.user.id}>'):]
            question = '' if not question else question.strip().lstrip().replace("\n", ". ")
            question = Question.clean_content(message, question)

            if len(question) >= 75:
                await message.channel.send('That question is too long for me, please keep it under 75 characters.')
                return
            if len(question) <= 1:
                return

            self.logger.info(f"{message.author.id} asked the conch {question}")
            self.update_questions()

            async with message.channel.typing():
                # Get the response
                if ' or ' in question:
                    # This user asked something or something
                    resp = random.choice(self.paired_responses)
                else:
                    # This user asked a regular question
                    if random.randint(0, 100) < 10:  # Easter egg
                        if message.guild.id == 384811165949231104:
                            resp = random.choice(self.easter_eggs + self.bb_easter_eggs)
                        else:
                            resp = random.choice(self.easter_eggs)
                    else:  # Normal
                        resp = random.choice(self.responses)

                self.logger.info(f"constructing image for {message.author.id}")
                image_name = 'img/conch_small.gif'
                before = 29
                after = 51

                im = Image.open(image_name)
                cur = 0
                frames = []
                frame_font = ImageFont.truetype("fonts/impact.ttf", 15)
                frame_font_bot = ImageFont.truetype("fonts/impact.ttf", 27)

                for frame in ImageSequence.Iterator(im):
                    frame = frame.convert('RGB')
                    cur += 1
                    frame_draw = ImageDraw.Draw(frame)

                    if cur < before:
                        Question.draw_text(question, "top", frame, frame_font, frame_draw)
                    elif cur > after:
                        Question.draw_text(resp, "bottom", frame, frame_font_bot, frame_draw)

                    b = io.BytesIO()
                    frame.save(b, format='JPEG')
                    frame = Image.open(b)
                    frames.append(frame)
                self.logger.info(f'done image construction for {message.author.id}, uploading...')
                b = io.BytesIO()
                frames[0].save(b, save_all=True, append_images=frames[1:], format='GIF')
                b.seek(0)

                # check if the message was deleted while we were processing, perhaps it was automodded out
                try:
                    _ = await self.bot.fetch_message(message.id)
                    await message.channel.send(file=discord.File(b, "conch.gif"))
                except:
                    # The message was deleted, do not send the content
                    self.logger.info(f'upload canceled due to original message being deleted.')
                    return

    @staticmethod
    def draw_text_with_outline(content, x, y, draw, font):
        draw.text((x-2, y-2), content, (0, 0, 0), font=font)
        draw.text((x+2, y-2), content, (0, 0, 0), font=font)
        draw.text((x+2, y+2), content, (0, 0, 0), font=font)
        draw.text((x-2, y+2), content, (0, 0, 0), font=font)
        draw.text((x, y), content, (255, 255, 255), font=font)

    @staticmethod
    def draw_text(text, pos, img, font, draw):
        text = text.upper()
        w, h = draw.textsize(text, font)  # measure the size the text will take

        line_count = 1
        if w > img.width:
            line_count = int(round((w / img.width) + 1))

        lines = []
        if line_count > 1:
            last_cut = 0
            is_last = False
            for i in range(0,line_count):
                if last_cut == 0:
                    cut = int((len(text) / line_count) * i)
                else:
                    cut = last_cut

                if i < line_count-1:
                    next_cut = int((len(text) / line_count) * (i+1))
                else:
                    next_cut = len(text)
                    is_last = True

                # make sure we don't cut words in half
                if next_cut == len(text) or text[next_cut] == " ":
                    pass
                else:
                    while text[next_cut] != " ":
                        next_cut += 1
                line = text[cut:next_cut].strip()

                # is line still fitting ?
                w, h = draw.textsize(line, font)
                if not is_last and w > img.width:
                    next_cut -= 1
                    while text[next_cut] != " ":
                        next_cut -= 1
                last_cut = next_cut
                lines.append(text[cut:next_cut].strip())
        else:
            lines.append(text)

        last_y = -h
        if pos == "bottom":
            last_y = img.height - h * (line_count+1) - 10

        for i in range(0, line_count):
            w, h = draw.textsize(lines[i], font)
            x = img.width/2 - w/2
            y = last_y + h
            Question.draw_text_with_outline(lines[i], x, y, draw, font)
            last_y = y

    @staticmethod
    def clean_content(message, content):
        # Taken from discord message.clean_content
        transformations = {re.escape('<#%s>' % channel.id): '#' + channel.name for channel in message.channel_mentions}
        mention_transforms = {re.escape('<@%s>' % member.id): '@' + member.display_name for member in message.mentions}
        second_mention_transforms = {re.escape('<@!%s>' % member.id): '@' + member.display_name for member in message.mentions}
        role_transforms = {re.escape('<@&%s>' % role.id): '@' + role.name for role in message.role_mentions}

        transformations.update(mention_transforms)
        transformations.update(second_mention_transforms)
        transformations.update(role_transforms)

        def repl(obj):
            return transformations.get(re.escape(obj.group(0)), '')

        pattern = re.compile('|'.join(transformations.keys()))
        result = pattern.sub(repl, content)

        transformations = {'@everyone': '@\u200beveryone', '@here': '@\u200bhere'}

        def repl2(obj):
            return transformations.get(obj.group(0), '')

        pattern = re.compile('|'.join(transformations.keys()))
        return pattern.sub(repl2, result)


def setup(bot):
    bot.add_cog(Question(bot))
