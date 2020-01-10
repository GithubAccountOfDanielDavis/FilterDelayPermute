import numpy as np
import lookup_tables as lt

frame_type = np.dtype([
    ('old_echo', np.uint16),
    ('input_state', np.uint16),
    ('output_state', np.uint16)
])


def prev_frames(prev_states, next_states, old_echoes=lt.ALL_UINT8):
    shrunken_states = prev_states - (prev_states >> 4)
    permuted_echoes = lt.PERMUTE[old_echoes] << 4
    filtered_states = np.add.outer(permuted_echoes, shrunken_states)
    valid_mask = np.isin(filtered_states, next_states)

    frames = np.empty(filtered_states.shape, dtype=frame_type)
    echo_indices, state_indices = np.indices(filtered_states.shape)
    frames['old_echo'] = old_echoes[echo_indices]
    frames['input_state'] = prev_states[state_indices]
    frames['output_state'] = filtered_states
    return frames.flatten()[valid_mask.flatten()]


def decode(block, final_state):
    SECRET_LENGTH = 40  # Assume for now
    block = np.roll(block, -SECRET_LENGTH)

    frames = []
    next_state_cands = np.array([final_state], dtype=np.uint16)
    for i in range(len(block) - 1, 0, -1):
        prev_state_cands = lt.UNECHO[block[i - 1]]
        frames.append(prev_frames(prev_state_cands, next_state_cands))
        next_state_cands = frames[-1]['input_state']
    prev_state_cands = lt.UNECHO[frames[0]['old_echo']].flatten()
    frames.append(prev_frames(prev_state_cands, next_state_cands))
    return frames
