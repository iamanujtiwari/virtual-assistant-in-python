import requests
from bs4 import BeautifulSoup
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import webbrowser
import random
import subprocess
import tkinter as tk
from PIL import Image, ImageTk
import threading

# Initialize the TTS (Text-to-Speech) engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set the speech rate (words per minute)
engine.setProperty('volume', 1)  # Set the volume level (0.0 to 1.0)

# Function to speak text
def speak(text):
    """Convert text to speech and speak it out loud."""
    engine.say(text)
    engine.runAndWait()

def greetme():
    """Greet the user based on the current time of day."""
    hour = int(datetime.datetime.now().hour)  # Get the current hour
    
    if hour < 12:
        speak("Hello,  sir. Good morning. How can I help you today?")
    elif hour < 18:
        speak("Hello,  sir. Good afternoon. How can I help you today?")
    else:
        speak("Hello,  sir. Good evening. How can I help you today?")

def googlesearch(query):
    """Perform a Google search and provide a summary from Wikipedia."""
    query = query.replace("google search", "").replace("google", "").strip()  # Clean up the query
    speak("This is what I found on Google.")
    try:
        pywhatkit.search(query)  # Perform a Google search using pywhatkit
        result = wikipedia.summary(query, sentences=1)  # Get a summary from Wikipedia
        speak(result)  # Speak the result
    except Exception as e:
        speak("No result available.")
        print(f"Error during Google search: {e}")

def searchyoutube(query):
    """Search for a video on YouTube and play it."""
    query = query.replace("youtube", "").strip()  # Clean up the query
    speak("This is what I found on YouTube.")
    web = "https://www.youtube.com/results?search_query=" + query  # Create YouTube search URL
    webbrowser.open(web)  # Open the search results in the web browser
    pywhatkit.playonyt(query)  # Play the first video on YouTube using pywhatkit
    speak("Done, sir.")

def searchwikipedia(query):
    """Search for information on Wikipedia and provide a summary."""
    query = query.replace("search wikipedia", "").replace("wikipedia", "").strip()  # Clean up the query
    try:
        result = wikipedia.summary(query, sentences=2)  # Get a summary from Wikipedia
        speak("According to Wikipedia.")
        print(result)  # Print the result to the console
        speak(result)  # Speak the result
    except Exception as e:
        speak("No result available.")
        print(f"Error during Wikipedia search: {e}")

def get_weather():
    """Fetch and speak the current weather."""
    city = "jaipur"
    url = f"https://www.google.com/search?q=weather+{city}"
    html = requests.get(url).content

    # Getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    try:
        global temp
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

        # Formatting data
        data = str.split('\n')
        global time
        time = data[0]
        sky = data[1]

        # Getting additional data
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        strd = listdiv[5].text
        pos = strd.find('Wind')
        other_data = strd[pos:]

        # Printing all data
        weather_info = (
            f"Temperature is {temp}. "
            f"Time: {time}. "
            f"Sky Description: {sky}. "
            f"{other_data}"
        )
        print(weather_info)
        speak(weather_info)
    except Exception as e:
        speak("Unable to fetch weather information.")
        print(f"Error during weather fetching: {e}")

def tell_time():
    """Provide the current time."""
    
    current_time = time
    speak(f"The current time is {current_time}.")  # Speak the current time

def tell_joke():
    """Tell a random joke."""
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "What do you call cheese that isn't yours? Nacho cheese!"
    ]
    joke = random.choice(jokes)  # Choose a random joke from the list
    speak(joke)  # Speak the joke

def sleep():
    """Handle the sleep command and exit the program."""
    speak("Goodnight! I am going to sleep now. Wake me up when you need me.")
    exit()  # Exit the program

def run_batch_file():
    """Run a batch file."""
    batch_file_path = r"C:\Users\ANUJ\Desktop\virtual assistant in python\python.bat"  # Specify the path to your batch file
    try:
        subprocess.run(batch_file_path, check=True)  # Execute the batch file
        speak("Batch file executed successfully.")
    except subprocess.CalledProcessError as e:
        speak("Failed to execute batch file.")
        print(f"Batch file execution error: {e}")

# Initialize gif_frames variable
gif_frames = []

def update_gif(frame=0):
    """Function to update the GIF (for animation)."""
    label.config(image=gif_frames[frame])
    frame = (frame + 1) % len(gif_frames)
    label.after(100, update_gif, frame)

def start_gui():
    """Function to initialize the GUI."""
    # Create the main window
    root = tk.Tk()
    root.title("Jarvis Assistant")

    # Set the window size to 600x700
    root.geometry("600x700")

    # Load a GIF (Replace 'your_gif.gif' with the actual path to your GIF file)
    gif_path = "jarvis.gif"
    gif = Image.open(gif_path)

    # Convert GIF into a format suitable for Tkinter
    global gif_frames
    gif_frames = []
    while True:
        gif_frames.append(ImageTk.PhotoImage(gif))
        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break

    # Create a label widget to display the GIF
    global label
    label = tk.Label(root)
    label.pack()

    # Start the GIF animation
    update_gif()

    # Run the GUI loop
    root.mainloop()

def main():
    """Main function to handle voice commands."""
    run_batch_file()  # Run the batch file first
    
    speak("Initializing Charlie")  # Announce that the assistant is initializing

    # Start GUI in a separate thread so it runs alongside the voice assistant
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.daemon = True
    gui_thread.start()

    r = sr.Recognizer()  # Initialize the speech recognizer

    while True:
        print("Listening for wake word 'wake up'...")  # Inform the user that the assistant is listening
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                print("Listening...")
                audio = r.listen(source, timeout=20, phrase_time_limit=5)  # Listen for audio input

            try:
                command = r.recognize_google(audio)  # Recognize speech using Google Speech Recognition
                print(f"You said: {command}")
                query = command.lower()  # Convert the command to lowercase
                
                if "wake up" in query:
                    greetme()  # Greet the user if the wake word is detected
                    # After greeting, listen for further commands
                    while True:
                        print("Listening for commands...")
                        try:
                            with sr.Microphone() as source:
                                r.adjust_for_ambient_noise(source)
                                audio = r.listen(source, timeout=20, phrase_time_limit=5)
                            
                            command = r.recognize_google(audio)
                            print(f"You said: {command}")
                            query = command.lower()
                            
                            if "search" in query:
                                googlesearch(query)
                            elif "youtube" in query:
                                searchyoutube(query)
                            elif "wikipedia" in query:
                                searchwikipedia(query)
                            elif "weather" in query:
                                get_weather()
                            elif "time" in query:
                                tell_time()
                            elif "joke" in query:
                                tell_joke()
                            elif "sleep" in query:
                                sleep()  # Call the sleep function and exit
                            elif "wake up" in query:
                                greetme()  # Optionally greet again if the wake word is detected
                            else:
                                speak("Sorry, I did not understand that.")
                        
                        except sr.UnknownValueError:
                            speak("Sorry, I did not understand that.")
                        
                        except sr.RequestError as e:
                            speak(f"Request error from Google Speech Recognition service: {e}")

                        except Exception as e:
                            speak(f"Error: {e}")
                            print(f"Error: {e}")

            except sr.UnknownValueError:
                speak("Sorry, I did not understand that.")
            
        except sr.RequestError as e:
            speak(f"Request error from Google Speech Recognition service: {e}")

        except Exception as e:
            speak(f"Error: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()  # Run the main function when the script is executed
