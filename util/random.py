import random, string


def key(result_len):
    return ''.join(random.choice(string.ascii_letters+string.digits) for i in range(result_len))
