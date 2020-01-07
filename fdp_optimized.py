from numpy import uint16, ndarray, concatenate, object as obj
from compatibility import block_from_secret, roll_output_block, numpy_ufunc
from lookup_tables import PERMUTE

@numpy_ufunc(2, 1)
def filter_block (state: uint16, echo: uint16) -> uint16:
    """Create accumulator ufunc which generates a "running total"-like array"""
    return state - (state >> 4) + echo

def next_block (block: ndarray, state: uint16) -> (ndarray, uint16):
    """Encode an arbitrary-sized 1d block a single time (1 iteration)"""

    # PERMUTE
    permuted_block = PERMUTE[block] << 4

    # FILTER
    filtered_states = filter_block.accumulate(
        concatenate(([state], permuted_block)), # state is initial value
        dtype=obj # np.frompyfunc requires casting to object and back
    ).astype(uint16)[1:] # drop prev state

    # ECHO
    next_state = filtered_states[-1]
    next_block = (filtered_states >> 3) & 0x00FF
    return next_block, next_state

def encode (
        secret: bytes,
        block_size=512,
        iterations=20,
        backwards_compatible=True) -> (ndarray, uint16):
    """Perform PermuteFilterEcho hash"""
    block, state = block_from_secret(block_size, secret, backwards_compatible)

    for _ in range(iterations):
        block, state = next_block(block, state)

    block = roll_output_block(block, len(secret), backwards_compatible)
    return state, block

if __name__ == '__main__':
    state, echoes = encode(b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print('State:', state)
    print('Delay line:')
    print(echoes)
