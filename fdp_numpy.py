from numpy import uint16, zeros, roll, frompyfunc, concatenate, object as obj
from lookup_tables import PERMUTE, UNPERMUTE

def encode (secret: bytes, delay_length=512, iterations=20):
    assert delay_length > len(secret) + 1

    # Set up initial state and echoes block
    echoes = zeros(delay_length, dtype=uint16)
    if len(secret) > 0:
        echoes[-len(secret):] = list(secret)
    echoes[0] = UNPERMUTE[echoes[0]] # backwards compatibility

    # Create accumulator ufunc which generates a "running total"-like array
    integrate = frompyfunc(
        lambda s, e: (s - (s >> 4) + e), # "shrink" state and "integrate"
        2, 1) # 2 inputs, 1 output

    state = 0
    for _ in range(iterations):

        # "permute" entire block of echoes at once
        permuted_echoes = PERMUTE[echoes] << 4

        # keep intermediate states because they all need echoed for next block
        interim_states = integrate.accumulate(
            concatenate(([state], permuted_echoes)), # state is accumulator's initial value
            dtype=obj).astype(uint16) # casting to obj and back is a workaround for frompyfunc behavior

        # get next block's state and drop previous state from end
        state, interim_states = interim_states[-1],  interim_states[1:]

        # "echo" entire block of states at once
        echoes = (interim_states >> 3) & 0xF00FF

    echoes = roll(echoes, len(secret)) # backwards compatibility
    return state, echoes
