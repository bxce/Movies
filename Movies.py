import requests
import webbrowser
import io
import sys
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


API_KEY = ""  # your OMDb API key

def search_movie():
    movie_name = entry_movie.get().strip()
    if not movie_name:
        messagebox.showwarning("Please enter a movie name.")
        return

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            # Update labels with movie information
            label_title.config(text=f"Title: {data['Title']}")
            label_year.config(text=f"Year: {data['Year']}")
            label_runtime.config(text=f"Runtime: {data['Runtime']}")
            label_id.config(text=f"IMDb ID: {data['imdbID']}")

            # Show poster
            poster_url = data.get("Poster", "")
            if poster_url and poster_url != "N/A":
                try:
                    image_bytes = requests.get(poster_url).content
                    image = Image.open(io.BytesIO(image_bytes))
                    image = image.resize((250, 370))  
                    poster_img = ImageTk.PhotoImage(image)
                    label_poster.config(image=poster_img)
                    label_poster.image = poster_img  
                except Exception:
                    label_poster.config(image="", text="Could not load poster.")
            else:
                label_poster.config(image="", text="No poster available")

            global movie_link
            movie_link = f"https://vidfast.pro/movie/{data['imdbID']}"
            button_link.config(state=NORMAL)
        else:
            messagebox.showinfo("Movie not found.")
    else:
        messagebox.showerror("Error connecting to OMDb.")

def open_link():
    if movie_link:
        webbrowser.open(movie_link)
        root.destroy()

# -------------------------------
#  MAIN GUI
# -------------------------------

root = Tk()
root.title("Movie Finder")
root.geometry("500x750")
root.config(bg="#202124")

movie_link = None

# Input field
Label(root, text="Name:", fg="white", bg="#202124", font=("Arial", 12)).pack(pady=10)
entry_movie = Entry(root, font=("Arial", 14), width=30)
entry_movie.pack(pady=5)

button_search = Button(root, text="Search", command=search_movie, font=("Arial", 12), bg="#4285F4", fg="white")
button_search.pack(pady=10)

# Enter to search
root.bind("<Return>", lambda event: search_movie())

# Frame to display results
frame_result = Frame(root, bg="#303134")
frame_result.pack(pady=15, padx=10, fill="both", expand=True)

label_title = Label(frame_result, text="", bg="#303134", fg="white", font=("Arial", 12))
label_title.pack(anchor="w", pady=2)

label_year = Label(frame_result, text="", bg="#303134", fg="white", font=("Arial", 12))
label_year.pack(anchor="w", pady=2)

label_runtime = Label(frame_result, text="", bg="#303134", fg="white", font=("Arial", 12))
label_runtime.pack(anchor="w", pady=2)

label_id = Label(frame_result, text="", bg="#303134", fg="white", font=("Arial", 12))
label_id.pack(anchor="w", pady=2)

# Poster image
label_poster = Label(frame_result, bg="#303134")
label_poster.pack(pady=10)

# Open link
button_link = Button(root, text="Open", state=DISABLED, command=open_link, font=("Arial", 12), bg="#0F9D58", fg="white")
button_link.pack(pady=15)

root.mainloop()
