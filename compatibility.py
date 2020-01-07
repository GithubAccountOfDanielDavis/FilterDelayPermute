from numpy import zeros, uint16, roll, ndarray, frompyfunc
from lookup_tables import UNPERMUTE

def block_from_secret (
        size: int,
        secret: bytes,
        backwards_compatible=True) -> (ndarray, uint16):
    """Create appropriate initial block out of secret"""
    if size <= len(secret):
        raise ValueError('Block size must be longer than secret length')
    block = zeros(size, dtype=uint16)
    if len(secret) > 0:
        block[:len(secret)] = list(secret)
    if backwards_compatible:
        block = roll(block, -len(secret))
        block[0] = UNPERMUTE[block[0]]
    state = uint16(0)
    return block, state

def roll_output_block (
        block: ndarray,
        secret_size: int,
        backwards_compatible=True) -> ndarray:
    """numpy.roll alias if backwards_compatible, otherwise return unchanged"""
    return roll(block, secret_size) if backwards_compatible else block

def numpy_ufunc (inputs: int, outputs: int):
    """Decorator for creating a numpy ufunc from a python function"""
    return lambda function: frompyfunc(function, inputs, outputs)
