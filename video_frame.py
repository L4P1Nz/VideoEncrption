import cv2
import numpy as np
import vector_process

def preprocess_video(frame_list, N):

    new_frame_list = []
    frame_prev = None
    for i, frame in enumerate(frame_list):
        
        if (i % N) == 0:
            frame_prev = frame
            new_frame_list.append(frame_prev)
            continue

        height, width, channels = frame.shape
        frame_pre_vector = vector_process.reshape_frame_to_vector(frame_prev)
        frame_vector = vector_process.reshape_frame_to_vector(frame)
        frame_diff = vector_process.reshape_vector_to_frame(frame_pre_vector - frame_vector , height, width)
        new_frame_list.append(frame_diff)

    return new_frame_list

def convert_frames_to_video(frame_list, output_path, fps):
    if not frame_list:
        print("Empty frame list")
        return

    height, width, channels = frame_list[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frame_list:
        out.write(frame)

    out.release()
    print(f"Video saved successfully at {output_path}")

def get_video_fps(video_path):
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Error opening video file")
        return None

    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()

    return fps

def process_video_decrypt(frame_list, N):

    new_frame_list = []
    frame_prev = None
    for i, frame in enumerate(frame_list):
        
        if (i % N) == 0:
            frame_prev = frame
            new_frame_list.append(frame_prev)
            continue

        height, width, channels = frame.shape
        frame_pre_vector = vector_process.reshape_frame_to_vector(frame_prev)
        frame_diff_vector = vector_process.reshape_frame_to_vector(frame)
        frame_original = vector_process.reshape_vector_to_frame(frame_pre_vector - frame_diff_vector , height, width)
        new_frame_list.append(frame_original)
    
    return new_frame_list

def convert_video_to_frame_list(video_path):
    # Read the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Unable to open video")
        return

    list_frame = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        list_frame.append(frame)

    cap.release()
    return list_frame

def save_frame_to_img(frame_list, path):
    for i, frame in enumerate(frame_list):
        cv2.imwrite(f".\img2\\{path}\\frame_{i}.jpg", frame)
        print(f"Store successfully frame_{i}.jpg")