# crosstalk.py
from dialogue.jokes import JOKES
from dialogue.stories import STORIES
from dialogue.facts import FACTS
from dialogue.ambient import AMBIENT
from dialogue.council import COUNCIL
from dialogue.visitor import VISITOR, GREETINGS, PEERING_EYES
from dialogue.reactions import TAP_REACTIONS, FEED_REACTIONS, TAP_GRUNTS, FEED_GRUNTS, INTERJECTIONS
from dialogue.biome import BIOME_REACTIONS
from dialogue.poetry import POETRY
from dialogue.lyrics import LYRICS
from dialogue.requests import REQUESTS
from dialogue.riddles import RIDDLES
from dialogue.wisdom import WISDOM
from dialogue.daily import MORNING, EVENING, LATE_NIGHT, ABSENCE, STRESS, BUSY, WEATHER
from dialogue.dreams import DREAMS_NIGHTMARE, DREAMS_PEACEFUL, DREAMS_PLAYFUL, DREAMS_ABSENCE
from dialogue.huddle import HUDDLE
from dialogue.bedtime import BEDTIME_RESISTANCE, WAKING_NUDGE, WAKING_OTHERS

DIALOGUE_BANK = {
    "jokes": JOKES,
    "stories": STORIES,
    "facts": FACTS,
    "ambient": AMBIENT,
    "council": COUNCIL,
    "visitor": VISITOR,
    "greetings": GREETINGS,
    "peering_eyes": PEERING_EYES,
    "tap_reactions": TAP_REACTIONS,
    "feed_reactions": FEED_REACTIONS,
    "tap_grunts": TAP_GRUNTS,
    "feed_grunts": FEED_GRUNTS,
    "interjections": INTERJECTIONS,
    "poetry": POETRY,
    "lyrics": LYRICS,
    "requests": REQUESTS,
    "riddles": RIDDLES,
    "wisdom": WISDOM,
    "daily_morning": MORNING,
    "daily_evening": EVENING,
    "daily_night": LATE_NIGHT,
    "daily_absence": ABSENCE,
    "daily_stress": STRESS,
    "daily_busy": BUSY,
    "daily_weather": WEATHER,
    "dream_nightmare": DREAMS_NIGHTMARE,
    "dream_peaceful": DREAMS_PEACEFUL,
    "dream_playful": DREAMS_PLAYFUL,
    "dream_absence": DREAMS_ABSENCE,
    "huddle": HUDDLE,
    "bedtime_resistance": BEDTIME_RESISTANCE,
    "waking_nudge": WAKING_NUDGE,
    "waking_others": WAKING_OTHERS
}

def get_bank(bank_name):
    return DIALOGUE_BANK.get(bank_name, [])