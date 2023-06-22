import numpy as np

def reshape_frame_to_vector(frame):
    height, width, channels = frame.shape
    reshaped_frame = np.reshape(frame, (height * width * channels))
    return reshaped_frame

def reshape_vector_to_frame(vectorized_frame, height, width, channels):
    reshaped_frame = np.reshape(vectorized_frame, (height, width, channels))
    return reshaped_frame
