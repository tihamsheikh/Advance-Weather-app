# An application to send weather summary through email
# pkg smtplib, MIMEMultipart, MIMEText, gemini, tkinter, ttkbootstrap, schedule, email, requests, BeautifulSoup
# api open weathe
# key file KEYS

import smtplib, requests
from keys import KEYS
from google import genai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup

state = True

# for news
def scraped_info(url):
    response = requests.get(url)
    html_f = response.text

    soup = BeautifulSoup(html_f, "html.parser")

    title_matches = soup.find_all('span', class_=["tilte-no-link-parent"])
    link_matches = soup.find_all('a', class_=["title-link"])

    list1, list2 = [], []
    limit = 20

    count = 0
    for match in title_matches:
        if count == limit: break
        list1.append(match.text)
        count += 1
    count = 0
    for link in link_matches:
        if count == limit: break
        list2.append(link.get('href'))
        count += 1

    content = "<br/>"
    for i in range(limit):
        content += f"""<a href="{list2[i]}" style="color: inherit; text-decoration: none;">{i + 1}.{list1[i]}</a> <br/>"""
    content += "</body></html>"
    return content

# weather info acquiring (1st operation)
def weather_info(place):
    api_key = KEYS.open_weather_key

    weather_call_url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={place}"

    try:
        response = requests.get(weather_call_url).json()
        print("Acquired weather information")
    except Exception:
        confirmation_var.set("Error!!!")

    return response

# weather info summarization (2nd operation)
def summarize_weather_info(place):
    api_key = KEYS.genai_key

    client = genai.Client(api_key=api_key)

    weather_information = weather_info(place)

    response = client.models.generate_content(
    model="gemini-2.0-flash",
            contents=f"""
            {weather_information}
            Please summarize this json weather information and temperatures should be in celsius. 
            Also along with summarization recommend me what should I do in this weather.
            Note: Only start with weather summarization and do not add anything extra like you are responding. But do add titles like "Summarization of weather"
            and "Recommended activity", please.
            """
    )

    return response.text

# email sending section (3rd operation)
def email_section(username, password, client, place):
    port = 587
    host = "smtp.gmail.com"

    server = smtplib.SMTP(host=host, port=port)

    server.starttls()
    server.login(user=username, password=password)


    content = summarize_weather_info(place) # plug
    if content == 404:
        confirmation_var.set("Error!!!")

    content = content.split("\n")

    # email formating (start)
    main_content = ""
    count = 0
    template_list = [
        "<html><head></head><body><h2><strong>",
        "</strong></h2><p>",
        "</p><h3><strong>",
        "</strong></h3><p>"
    ]

    for info in content:
        if info == "":
            continue
        main_content += template_list[count]    # adding html
        main_content += info                    # adding content
        count += 1
    main_content += "</p><br/><h3>Recent News of Bangladesh</h3><br/>"

    # place to change email type

    url = "https://www.prothomalo.com/"
    main_content += scraped_info(url)

    # email formating (end)

    message = MIMEMultipart()  # email template
    message["To"] = client
    message["From"] = username
    message["Subject"] = "Weather News!!!!"
    message.attach(MIMEText(main_content, "html"))

    server.send_message(message)
    server.quit()
    print("Successfully\nEmail sent")

# scheduled mail sending part (operation 4 )
def mailing_start():
    global state
    state = True
    client_entry.configure(state="disable")
    place_entry.configure(state="disable")

    def run_task():
        username = KEYS.username        # username_var.get()
        app_password = KEYS.gmail_key   # password_var.get()
        client = client_var.get()
        place = place_var.get()
        interval = interval_var.get()

        if state:
            try :
                email_section(username, app_password, client, place)
                confirmation_var.set("Mailing is active")
                app.after(interval * 60 * 60 * 1000, run_task)

            except Exception:
                confirmation_var.set("Error!!! Reset the app")
    run_task()

# resets the variable and task
def reset():
    global state
    state = False

    client_entry.configure(state="enable")
    place_entry.configure(state="enable")
    confirmation_var.set("Mailing is cancelled")
    client_var.set(value="")
    place_var.set(value="")


# GUI start
app = ttk.Window(themename="minty") #journal, darkly, minty, united
app.title("Cloudy")
app.geometry("450x650")
# style variable
font = "Calibri"

client_var = tk.StringVar()
place_var = tk.StringVar()
interval_var = tk.IntVar()

confirmation_var = tk.StringVar(value="State")

label = ttk.Label(
    master=app,
    text="Enter your details",
    font=f"{font} 20")
label.pack(padx=2, pady=5, ipadx=2, ipady=2)


# widget for client, place
frame_client = ttk.Frame(master=app)
frame_place = ttk.Frame(master=app)
frame_interval = ttk.Frame(master=app)
frame_buttons = ttk.Frame(master=app)

frame_client.pack(pady=4)
frame_place.pack(pady=4)
frame_interval.pack(pady=10, ipady=10)
frame_buttons.pack(pady=10, ipady=6)

# client widget
client_label = ttk.Label(
    master=frame_client,
    text="Client Email",
    font=font
)
client_entry = ttk.Entry(master=frame_client, font=font, textvariable=client_var)

client_label.pack(side="left", ipadx=2, padx=7)
client_entry.pack(ipadx=10, padx=20)

# place widget
place_label = ttk.Label(
    master=frame_place,
    text="Destination",
    font=font
)
place_entry = ttk.Entry(master=frame_place, font=font, textvariable=place_var)

place_label.pack(side="left", ipadx=2, padx=8)
place_entry.pack(ipadx=10, padx=20)

# Interval selection
interval_label = ttk.Label(master=frame_interval, text="Choose Interval", font=f"{font} 14")
interval_label.pack(pady=4, ipady=10)

interval3 = ttk.Radiobutton(master=frame_interval, text="3 hours", value=3, variable= interval_var)
interval3.pack(side="left", ipadx=10)

interval6 = ttk.Radiobutton(master=frame_interval, text="6 hours", value=6, variable= interval_var)
interval6.pack(side="left", ipadx=10)

interval12 = ttk.Radiobutton(master=frame_interval, text="12 hours", value=12, variable= interval_var)
interval12.pack(side="left", ipadx=10)

# submit and reset
submit_btn = ttk.Button(
    master=frame_buttons,
    text="Submit",
    command= mailing_start
)

reset_btn = ttk.Button(
    master=frame_buttons,
    text="Reset",
    command= reset
)

submit_btn.pack(side="left", ipadx=10,  padx=15)
reset_btn.pack(side="left", ipadx=15, padx=15)


confirm_label = ttk.Label(master=app, textvariable=confirmation_var, font=f"{font} 20")
confirm_label.pack(pady=30)


app.mainloop()










