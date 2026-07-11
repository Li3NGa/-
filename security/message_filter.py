BLOCK_WORDS = [
    'spam',
    'test_block'
]


def check_message(content):
    for word in BLOCK_WORDS:
        if word in content.lower():
            return False
    return True
