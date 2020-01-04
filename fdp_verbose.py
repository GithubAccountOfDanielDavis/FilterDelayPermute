from numpy import uint16, roll, zeros
from lookup_tables import PERMUTE, UNPERMUTE

def encode (secret: bytes, delay_length=512, iterations=20):
    echoes = zeros(delay_length, dtype=uint16)
    if len(secret) > 0:
        echoes[-len(secret):] = list(secret) # backwards compatibility
    echoes[0] = UNPERMUTE[echoes[0]]

    state = uint16(0)
    i = 0
    for _ in range(delay_length * iterations):
        shrunken_state = state - (state >> 4)
        permuted_echo = PERMUTE[echoes[i]] << 4
        state = shrunken_state + permuted_echo
        echoes[i] = state >> 3 & 0x00FF
        i += 1
        i %= delay_length
    echoes = roll(echoes, len(secret)) # backwards compatibility
    return state, echoes
