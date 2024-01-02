from pytube import Playlist
from pytube import YouTube

import customtkinter 
from PIL import Image, ImageTk
import requests
from io import BytesIO


# data required 
overall_t = ""
video_url = []
thumbnail_im_data = []
video_title = []

# checked_v = []
checkbox_vars = []

def button_callback1():
    global overall_t, video_url, thumbnail_im_data,video_title
    print("submitted searching for playlist")
    playlist_link = pl_link.get()
    p = Playlist(playlist_link)
    overall_t = p.title
    video_url = p.video_urls
    for x in video_url:
        yt = YouTube(x)
        image_url = yt.thumbnail_url  # Replace with the URL of your image
        response = requests.get(image_url)
        image_data = BytesIO(response.content)
        thumbnail_im_data.append(image_data)
        tt= yt.title
        tt2 = tt[:40]
        video_title.append(tt2)
        
    fetch_data()

def download_video(vl, output_path="./aa_UI"):
    try:
        yt = YouTube(vl)
        video_stream = yt.streams.get_highest_resolution()
        video_title = yt.title

        print(f"Downloading: {video_title}")
        video_stream.download(output_path)
        print("Download completed!")
    except Exception as e:
        print(f"Error: {str(e)}")

def Download_all():
    print("All video downloading start")
    global video_url
    for x in video_url:
        # print(f"downloading {x}")
        # print("started")
        download_video(x)

def Download_selected():
    print("selected video download start")
    # print(len(checkbox_vars))
    # print(checkbox_vars)
    for i in range(0,len(checkbox_vars)):
        if(checkbox_vars[i]):
            download_video(video_url[i])

def button_callback(index):
    global video_url
    print(f"Button {index + 1} clicked")
    download_video(video_url[index])

def checkbox_event(index):
    print(f"Checkbox {index} toggled")
    checkbox_vars[index]= not(checkbox_vars[index])
    # print(checkbox_vars)


app = customtkinter.CTk()
app.geometry("1080x720")

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=10, padx=20, fill="both")

# Create a label on top of the frame
label_text = "Welcome to Playlist Downloader"
label = customtkinter.CTkLabel(frame, text=label_text, font=("Comic Sans MS", 22, "bold"))
label.pack(pady=10)

# Create a text input in the next line
pl_link = customtkinter.CTkEntry(frame, width=700,height=40, placeholder_text="Enter playlist link")
pl_link.pack(pady=10)

# Create a button in the next line
submit_button = customtkinter.CTkButton(frame, text="Submit", command=button_callback1 ,width=500,height=50)
submit_button.pack(pady=10)

# Create five buttons in the next line
frame2 = customtkinter.CTkFrame(master=app)
frame2.pack(pady=10, padx=20, fill="both")
label_text2 = "Your video from the playlist is here"
label2 = customtkinter.CTkLabel(frame2, text=label_text2, font=("Comic Sans MS", 18, "bold"))
label2.pack(pady=10)

# def create_checkbox(index):
    # check_var = customtkinter.StringVar(value="off")
    # checkbox = customtkinter.CTkCheckBox(frame3, text=f"check", command=lambda: checkbox_event(index), variable=check_var, onvalue="on", offvalue="off")
    # checkbox.pack(side="left", padx=5, pady=20)
    # checkbox_vars.append(check_var)

scrollable_frame = customtkinter.CTkScrollableFrame(master=app, width=200, height=300)
scrollable_frame.pack(pady=20, padx=20, fill="both")

def fetch_data():
    def create_checkbox(index):
        check_var = customtkinter.StringVar(value="off")
        checkbox = customtkinter.CTkCheckBox(frame3, text=f"check", command=lambda: checkbox_event(index), variable=check_var, onvalue="on", offvalue="off")
        checkbox.pack(side="left", padx=5, pady=20)
        checkbox_vars.append(False)
    for i in range (0,len(thumbnail_im_data)):
        frame3 = customtkinter.CTkFrame(master=scrollable_frame)
        frame3.pack(pady=8, padx=20, fill="both")

        create_checkbox(i)
        vn = customtkinter.CTkLabel(frame3, text=f'Video {i}', font=("Arial", 18))
        vn.pack(side="left", padx=10, pady=20)
        

        # image_path = "./aa_UI/ms.jpg"
        image = Image.open(thumbnail_im_data[i])
        image = image.resize((240, 120))  # Resize the image
        photo = ImageTk.PhotoImage(image)

        # Create a label for the image
        image_label = customtkinter.CTkLabel(frame3, image=photo,text="")
        image_label.image = photo  # Save a reference to the image to prevent garbage collection
        image_label.pack(side="left", padx=10, pady=20)

        v_t = customtkinter.CTkLabel(frame3, text=f"{video_title[i]}......", font=("Arial", 18))
        v_t.pack(side="left", padx=15, pady=20)

        button_d = customtkinter.CTkButton(frame3, text=f"Button", command=lambda i=i: button_callback(i))
        button_d.pack(side="left", padx=15, pady=20)


frame3 = customtkinter.CTkFrame(master=app)
frame3.pack(pady=8, padx=20, fill="both")

button_d = customtkinter.CTkButton(frame3, text=f"Download All", command=Download_all,width=350,height=35)
button_d.pack(side="left", padx=25, pady=20)
button_d = customtkinter.CTkButton(frame3, text=f"Download selected", command=Download_selected,width=350,height=35)
button_d.pack(side="right", padx=25, pady=20)
app.mainloop()
