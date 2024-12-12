import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import genscript
from genscript import getScript

def create_random_video(output_file, total_duration):
    # Get the current directory
    directory = os.getcwd()
    
    # Paths for Videos and Music
    videos_path = os.path.join(directory, "Videos")
    music_path = os.path.join(directory, "Music")
    
    # Validate directories
    if not os.path.exists(videos_path):
        raise FileNotFoundError(f"Videos folder not found in {directory}")
    if not os.path.exists(music_path):
        raise FileNotFoundError(f"Music folder not found in {directory}")
    
    # Get video files
    video_files = [os.path.join(videos_path, f) for f in os.listdir(videos_path) if f.endswith(".mp4")]
    if len(video_files) < 1:
        raise FileNotFoundError("No MP4 files found in Videos folder.")

    # If more than 14 videos, randomly select 14
    if len(video_files) > 14:
        video_files = random.sample(video_files, 14)
    
    # Get music files
    music_files = [os.path.join(music_path, f) for f in os.listdir(music_path) if f.lower().endswith(".mp3")
]
    if len(music_files) < 1:
        raise FileNotFoundError("No MP3 files found in Music folder.")
    

    
    # Load video clips and randomize order
    video_clips = [VideoFileClip(file).without_audio() for file in video_files]
    random.shuffle(video_clips)
    
    # Combine video clips to fit total duration
    combined_duration = 0
    selected_clips = []
    for clip in video_clips:
        if combined_duration + clip.duration <= total_duration:
            selected_clips.append(clip)
            combined_duration += clip.duration
        else:
            # Trim the last clip to fit
            remaining_time = total_duration - combined_duration
            if remaining_time > 0:
                selected_clips.append(clip.subclip(0, remaining_time))
            break
    
    # Concatenate the selected clips
    final_video = concatenate_videoclips(selected_clips, method="compose")
    
    # Choose a random music file
    music_file = random.choice(music_files)
    music = AudioFileClip(music_file).subclip(0, final_video.duration)
    
    # Add music as background audio
    final_video = final_video.set_audio(music)
    
    # Write the final video
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
    print(f"Video created successfully: {output_file}")

# Example Usage
if __name__ == "__main__":
    output_file = "final_video.mp4"  # Output in the current directory
    total_duration = int(input("Enter the desired total duration of the video (in seconds): "))
    
    try:
        create_random_video(output_file, total_duration)
    except Exception as e:
        print(f"Error: {e}")
