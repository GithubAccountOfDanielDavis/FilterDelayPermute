from numpy import uint16, zeros, roll, frompyfunc, concatenate, object as obj
from lookup_tables import PERMUTE, UNPERMUTE

def encode (secret: bytes, delay_length=512, iterations=20, bw_compatible=True):
    if not (delay_length > len(secret) + 1):
        raise ValueError('delay length cannot be shorted than secret length')

    # Set up initial state and echoes block
    echoes = zeros(delay_length, dtype=uint16)
    if len(secret) > 0:
        echoes[-len(secret):] = list(secret)
    if bw_compatible:
        echoes[0] = UNPERMUTE[echoes[0]]
    state = 0

    # Create accumulator ufunc which generates a "running total"-like array
    integrate = frompyfunc(
        lambda s, e: (s - (s >> 4) + e), # "shrink" state and "integrate"
        2, 1) # 2 inputs, 1 output

    # encode the block {iterations} times
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

    if bw_compatible:
        echoes = roll(echoes, len(secret))
    return state, echoes

if __name__ == '__main__':
    state, echoes = encode(b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print('State:', state)
    print('Delay line:')
    print(echoes)
