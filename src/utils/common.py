import json


class EcosystemBots:
    MagicConch = "CONCH_"


def load_creds(is_debug, bot: str):
    with open('config/creds.json') as fp:
        creds = json.load(fp)
        return creds[bot + "BETA_TOKEN"] if is_debug else creds[bot + "TOKEN"]


def load_references() -> dict:
    with open('config/references.json') as fp:
        refs = json.load(fp)
    return refs


def tail(f, lines):
    tail_log = []
    at_idx = 0
    for line in f.readlines():
        if len(tail_log) == lines:
            tail_log[at_idx] = line
            at_idx = (at_idx + 1) % lines
        else:
            tail_log.append(line)
    return tail_log[at_idx:] + tail_log[:at_idx]


def tail_error(f):
    last_error = ""
    listening = False
    for line in f.readlines():
        if "Catching exception in command error" in line:
            listening = True
            last_error = ""
        if line.startswith("discord.ext.commands.errors.CommandInvokeError: Command raised an exception:"):
            last_error += line
            listening = False
        if listening:
            last_error += line
    return last_error


def chunk_by_newline(string, chunk_size=1900):
    chunks = []
    current_chunk = ""
    for line in string.split("\n"):
        # Is this line able to be in the chunk size?
        if len(current_chunk + line + "\n") < chunk_size:
            current_chunk += line + "\n"
        # Is the line itself longer than the chunk size?
        elif len(line) > chunk_size:
            if len(current_chunk) > 0:
                chunks.append(current_chunk)
                current_chunk = ""
            for subchunk in [line[i: i + chunk_size] for i in range(0, len(line), chunk_size)]:
                chunks.append(subchunk)
        # Otherwise new chunk
        else:
            chunks.append(current_chunk)
            current_chunk = line + "\n"
    chunks.append(current_chunk)
    return chunks
