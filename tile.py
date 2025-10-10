from PIL import Image
import os

def gif_to_frames(gif_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    gif = Image.open(gif_path)

    frame_index = 0
    try:
        while True:
            gif.seek(frame_index)
            frame = gif.convert("RGBA")
            frame.save(os.path.join(output_folder, f"frame_{frame_index}.png"))
            frame_index += 1
    except EOFError:
        pass

    print(f"{frame_index} frames extraites dans '{output_folder}'")

# Exemple :
gif_to_frames("walk_north.gif", "frames/north")
