import numpy as np
import keygen
import vector_process
import video_frame
from Crypto.Cipher import ChaCha20

def xor_with_key(frame_vector, key):
    block_size = len(key)
    num_blocks = len(frame_vector) // block_size

    block_xor = []
    for i in range(num_blocks):
        start_index = i * block_size
        end_index = start_index + block_size

        if end_index > len(frame_vector):
            end_index = len(frame_vector)
        
        frame_block = frame_vector[start_index:end_index]

        for j in range(len(frame_block)):
            frame_block[j] ^= key[j]

        block_xor.append(frame_block)

    return block_xor

def data_permutation(frame_list, a1, b1, Xo1, Yo1):

    height, width, channels = frame_list[0].shape
    size_frame = height*width*channels
    X,Y = keygen.henon_chaotic_map_1(a1, b1, Xo1, Yo1, size_frame)

    Keys_X = tuple(np.round(key * size_frame).astype(int) for key in X)
    Keys_Y = tuple(np.round(key * size_frame).astype(int) for key in Y)

    new_frame_list = []

    for frame in (frame_list):

        frame_vector = vector_process.reshape_frame_to_vector(frame)
        for i in range(size_frame):
            x = Keys_X[i] % size_frame
            y = Keys_Y[i] % size_frame
            frame_vector[x], frame_vector[y] = frame_vector[y], frame_vector[x]

        new_frame = vector_process.reshape_vector_to_frame(frame_vector,height,width,channels)
        new_frame_list.append(new_frame)

    return new_frame_list


def data_permutation_decrypt(frame_list, a1, b1, Xo1, Yo1):

    height, width, channels = frame_list[0].shape
    size_frame = height*width*channels
    X,Y = keygen.henon_chaotic_map_1(a1, b1, Xo1, Yo1, size_frame)
    Keys_X = tuple(np.round(key * size_frame).astype(int) for key in X)
    Keys_Y = tuple(np.round(key * size_frame).astype(int) for key in Y)

    new_frame_list = []

    for frame in (frame_list):

        frame_vector_de = vector_process.reshape_frame_to_vector(frame)

        for i in reversed(range(size_frame)):
            x = Keys_X[i] % size_frame
            y = Keys_Y[i] % size_frame
            frame_vector_de[x], frame_vector_de[y]  = frame_vector_de[y], frame_vector_de[x]

        new_frame = vector_process.reshape_vector_to_frame(frame_vector_de,height,width,channels)
        new_frame_list.append(new_frame)
    
    return new_frame_list

def stream_encrypt(frame_list, a2, b2, Xo2, Yo2):

    height, width, channels = frame_list[0].shape
    Key2 = keygen.henon_chaotic_map_2(a2, b2, Xo2, Yo2, len(frame_list))

    encrypted_frame_list = []
    for i, frame in enumerate(frame_list):
        frame_vector = vector_process.reshape_frame_to_vector(frame)

        plaintext = Key2[i]
        key_chacha20 = Key2[i][:32]
        nonce = Key2[i][32:40]
        cipher = ChaCha20.new(key=key_chacha20, nonce=nonce)
        final_key = cipher.encrypt(plaintext)

        encrypted_vector_frame = xor_with_key(frame_vector,final_key)

        new_frame = vector_process.reshape_vector_to_frame(encrypted_vector_frame,height,width,channels)
        encrypted_frame_list.append(new_frame)

    return encrypted_frame_list

def stream_decrypt(frame_list, a2, b2, Xo2, Yo2):

    height, width, channels = frame_list[0].shape
    Key2 = keygen.henon_chaotic_map_2(a2, b2, Xo2, Yo2, len(frame_list))

    decrypted_frame_list = []
    for i, frame in enumerate(frame_list):
        frame_vector = vector_process.reshape_frame_to_vector(frame)

        plaintext = Key2[i]
        key_chacha20 = Key2[i][:32]
        nonce = Key2[i][32:40]
        cipher = ChaCha20.new(key=key_chacha20, nonce=nonce)
        final_key = cipher.encrypt(plaintext)

        decrypted_vector_frame = xor_with_key(frame_vector,final_key)

        new_frame = vector_process.reshape_vector_to_frame(decrypted_vector_frame,height,width,channels)
        decrypted_frame_list.append(new_frame)
    
    return decrypted_frame_list


def encrypt(video_path_in, video_path_out, N, a1 , b1, Xo1, Yo1, a2, b2, Xo2, Yo2):
    fps_video = video_frame.get_video_fps(video_path_in)

    frame_list = video_frame.convert_video_to_frame_list(video_path_in)
    #Encrypt
    frame_list_preprocess = video_frame.preprocess_video(frame_list, N)
    frame_list_permutation = data_permutation(frame_list_preprocess, a1 , b1, Xo1, Yo1)
    frame_list_permutation_xor = stream_encrypt(frame_list_permutation, a2, b2, Xo2, Yo2)

    #Convert to video
    video_frame.convert_frames_to_video(frame_list=frame_list_permutation_xor, output_path=video_path_out, fps=fps_video)
    return frame_list_permutation_xor, fps_video

def decrypt(video_path_out, frame_list, fps_video, N, a1 , b1, Xo1, Yo1, a2, b2, Xo2, Yo2):
    frame_list_permutation_xor_de = stream_decrypt(frame_list, a2, b2, Xo2, Yo2)
    frame_list_permutation_de = data_permutation_decrypt(frame_list_permutation_xor_de, a1 , b1, Xo1, Yo1)
    frame_list_de = video_frame.process_video_decrypt(frame_list_permutation_de, N)
    video_frame.convert_frames_to_video(frame_list=frame_list_de, output_path=video_path_out, fps=fps_video)


if __name__ == "__main__":

    N = 20

    a1 = 1.4
    b1 = 0.3
    Xo1 = 0.5
    Yo1 = 0.5

    a2 = 0.4
    b2 = 0.3
    Xo2 = 1.2
    Yo2 = 0.8

    encrtypted_frame, fps = encrypt(".\\video_ori\\video.mp4", ".\\video_encrypt\\video_out.mp4", N, a1, b1, Xo1, Yo1, a2, b2, Xo2, Yo2)
    decrypt(".\\video_decrypt\\video_de_out.mp4", encrtypted_frame, fps, N, a1, b1, Xo1, Yo1, a2, b2, Xo2, Yo2)
