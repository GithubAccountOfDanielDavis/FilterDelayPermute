from numpy import uint16, array, arange, fromiter, bitwise_or, add, isin, all, roll
from lookup_tables import GIVEN_ECHOES, GIVEN_STATE, PERMUTE, SHRINK

ALL_UINT8 = arange(0x0100, dtype=uint16)
LOST_ECHO_BITS = (ALL_UINT8 & 0x0007) | ((ALL_UINT8 & 0x00F8) << 8)

def thingy (input_states, output_states):
    #old_echo_cands = ALL_UINT8
    #input_permuted_echoes = PERMUTE[old_echo_cands]

    input_shrunken_states = SHRINK[input_states]
    input_interim_states = add.outer(PERMUTE, input_shrunken_states)
    input_results_mask = [all(row) for row in in1d(input_results, output_results)]
    return intersect1d(output_states_from_input_cands, possible_output_states)

def decode (echoes, ending_state):
    SECRET_LENGTH = 40 # Assume for now
    echoes = roll(echoes, -SECRET_LENGTH)

    # Get input and output states for all but the first echo
    state_cands = bitwise_or.outer(echoes << 3, LOST_ECHO_BITS) # 256 cands sublist for each echo
    input_state_cands = state_cands[:-1] # Ignore last sample because we already know the input for the next block
    output_state_cands = state_cands[1:] # Ignore first sample because we cna't get the inputs for it yet

    old_echo_cands = array([ALL_UINT8 for echo in echoes[1:]], dtype=uint16)
    permuted_echo_cands = PERMUTE[old_echo_cands]

    input_shrunken_states = SHRINK[input_state_cands]
    input_result_states = array([
        add.outer(echo, state)
        for state, echo in zip(input_shrunken_states, permuted_echo_cands)
    ], dtype=uint16)

    input_result_mask = array([
        isin(i, o) for i, o in zip(input_result_states, output_state_cands)
    ])

    # First axis is a slot for each echo
    # Second axis is old echo candidates
    # Third axis is states per old echo

    echo_mask = array([
        [all(echo_cand) for echo_cand in echo_slot]
        for echo_slot in input_result_mask
    ], dtype=uint16)

    old_echo_cands = old_echo_cands[echo_mask]
    
    print(old_echo_cands)
    print(old_echo_cands.shape)
    print(old_echo_cands.size)

decode(GIVEN_ECHOES, GIVEN_STATE)
