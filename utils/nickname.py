import random


NAMES = [
    'BlueFox',
    'SilentMoon',
    'CloudWalker',
    'NightStar',
    'LittleRiver',
    'RedLeaf',
    'SnowOwl',
    'DarkPhoenix',
    'GoldenEagle',
    'SilverWolf'
]


def generate_nickname():
    name = random.choice(NAMES)
    suffix = random.randint(100, 999)
    return f'{name}{suffix}'
