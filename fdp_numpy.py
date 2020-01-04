from numpy import uint16, zeros, roll
from lookup_tables import PERMUTE, UNPERMUTE

def encode (secret: bytes, delay_length=512, iterations=20):
    echoes = zeros(delay_length, dtype=uint16)
    if len(secret) > 0:
        echoes[-len(secret):] = list(secret) # backwards compatibility
    echoes[0] = UNPERMUTE[echoes[0]]

    state = 0
    for _ in range(iterations):
        # Imperative is easier to read than one-liner below
        echoes = PERMUTE[echoes] << 4
        for i, echo in enumerate(echoes):
            state -= (state >> 4)
            state += echo
            echoes[i] = state
        echoes >>= 3
        echoes &= 0x00FF

    echoes = roll(echoes, len(secret)) # backwards compatibility
    return state, echoes
