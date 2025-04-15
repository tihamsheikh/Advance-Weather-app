# An application to send weather summary through email
# pkg smtplib, gemini, tkinter, schedule, email
# api open weather

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# use try except bfor production

# key hash- do not remove!!!!
# hTaChIdMrBfTafjf 43uh934 f
# aHdOhSfA9Y3I48(*GB(*YNR*(W
# oIgDj98D*(&HG e 89w4987
# uS2E37fEdh7A7G87 789 f4
# hajfh uawehM uisadhniw

# email pkgs
import smtplib, requests, time
import KEYS
from google import genai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# GUI pkgs
import tkinter as tk
import ttkbootstrap as ttk

state = True

# weather info acquiring (1st operation)
def weather_info(place):
    api_key = KEYS.open_weather_key

    weather_call_url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={place}"

    response = requests.get(weather_call_url).json()
    # print(response)
    print("Acquired weather information")
    return response

# weather info summarization (2nd operation)
def summarize_weather_info(place):
    api_key = KEYS.genai_key

    client = genai.Client(api_key=api_key)

    weather_information = weather_info(place)
    # print(weather_information)

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

    # print(re)
    return response.text

# email sending section (3rd operation)
def email_section(username, password, client, place):
    port = 587
    host = "smtp.gmail.com"

    server = smtplib.SMTP(host=host, port=port)

    server.starttls()
    server.login(user=username, password=password)

    content = summarize_weather_info(place).split("\n")

    # email formating (start)
    main_content = ""
    count = 0
    template_list = [
        "<html><head></head><body><h2><strong>",
        "</strong></h2><p>",
        "</p><h3><strong>",
        "</strong></h3><p>",
        "</p></body></html>"
    ]

    for info in content:
        if info == "":
            continue
        # print(template_list[count], "\n",info)
        main_content += template_list[count]    # adding html
        main_content += info                    # adding content
        count += 1
    main_content += template_list[-1]

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

    def run_task():
        username = KEYS.username        # username_var.get()
        app_password = KEYS.gmail_key   # password_var.get()
        client = client_var.get()
        place = place_var.get()
        interval = interval_var.get()

        if state:
            try :
                email_section(username, app_password, client, place)
                confirmation_var.set("Weather mail is active")
                app.after(interval * 60 * 60 * 1000, run_task)

            except Exception:
                confirmation_var.set("Error!!! Reset the app")
    run_task()

# resets the variable and task
def reset():
    global state
    state = False

    confirmation_var.set("Weather mailing is cancelled")
    username_var.set(value="")
    password_var.set(value="")
    client_var.set(value="")
    place_var.set(value="")

# GUI start
app = ttk.Window(themename="journal")
app.title("Advance weather")
app.iconbitmap(r"C:\Users\tiham\Personal Projects\Project2_AppDev\cloudy.ico")
app.geometry("450x650")
# style variable
font = "Calibri"

# after submition every entry field would go blank except buttons
# but on reset the vars would go blank and entry would go normal

username_var = tk.StringVar()
password_var = tk.StringVar()
client_var = tk.StringVar()
place_var = tk.StringVar()
interval_var = tk.IntVar()

confirmation_var = tk.StringVar(value="State")

label = ttk.Label(
    master=app,
    text="Enter your details",
    font=f"{font} 20")
label.pack(padx=2, pady=5, ipadx=2, ipady=2)


# widget for username, password, client, place
frame_username = ttk.Frame(master=app)
frame_password= ttk.Frame(master=app)
frame_client = ttk.Frame(master=app)
frame_place = ttk.Frame(master=app)
frame_interval = ttk.Frame(master=app)
frame_buttons = ttk.Frame(master=app)

# frame_username.pack(pady=4)
# frame_password.pack(pady=4)
frame_client.pack(pady=4)
frame_place.pack(pady=4)
frame_interval.pack(pady=10, ipady=10)
frame_buttons.pack(pady=10, ipady=6)

# username widget
username_label = ttk.Label(
    master=frame_username,
    text="Your Email ",
    font=font
)
username_entry = ttk.Entry(master=frame_username, font=font, textvariable=username_var)

username_label.pack(side="left", ipadx=13)
username_entry.pack(ipadx=10)

# password widget
password_label = ttk.Label(
    master=frame_password,
    text="Password",
    font=font
)
password_entry = ttk.Entry(master=frame_password, font=font, textvariable=password_var)

password_label.pack(side="left", ipadx=20)
password_entry.pack(ipadx=10)

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









