# Import Module
from selenium import webdriver
import time
import pyautogui
from datetime import datetime
from flask import Flask, render_template, request
import sys

# Changing default recursion limit to 6000
app = Flask(__name__)
sys.setrecursionlimit(6000)


@app.route('/', methods=['POST', 'GET'])
def form_data():
    if request.method == 'POST':
        # Get user inputs from HTML form
        form_data.fname = request.form.get('fname')
        form_data.lname = request.form.get('lname')
        form_data.email = request.form.get('email')
        form_data.webinar_url = request.form.get('webinar_url')
        form_data.time_to_join = request.form.get('time_to_join')
        form_data.custque0 = request.form.get('custque0')
        form_data.custque1 = request.form.get('custque1')

        # current system time
        current_time = datetime.now().strftime("%H:%M:%S")

        # Assigning user_url to provided url
        user_url = form_data.webinar_url

        # time when you webinar to get launched

        launch_time = form_data.time_to_join  # launch time in HH:MM:SS format only

        launch_time2 = datetime.strptime(launch_time, "%H:%M:%S")
        current_time2 = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")

        # To check remaining time to launch

        for i in range(10000):

            if current_time2 < launch_time2:
                launch_time3 = datetime.strptime(launch_time, "%H:%M:%S")
                current_time3 = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
                time_remaining = launch_time3 - current_time3
                Hr = int(time_remaining.seconds // 3600)
                Min = int(time_remaining.seconds % 3600 / 60.0)
                Sec = int(time_remaining.seconds % 60.0)
                remaining_time =print("Remaining time is:", Hr, "Hr", Min, "Min", Sec, "Sec")
                time.sleep(1)
                i += 1

                if Hr == Min == Sec == 0:
                    break
                else:
                    continue

        # launch_time = print(input("Enter launch time in HH:MM:SS format only"))
        # open Chrome
        driver = webdriver.Chrome('C:\EXTRAS\Python-Developer-Course-Codes\Auto Gform\chromedriver.exe')

        # Open URL
        driver.get(user_url)
        # driver.get('https://register.gotowebinar.com/register/2618711656922297868')

        time.sleep(1)

        # wait for one second, until page gets fully loaded
        time.sleep(1)
        driver.implicitly_wait(2)

        # Enters the given values in test fields
        fname = driver.find_element_by_id('registrant.firstName')
        fname.send_keys(form_data.fname)

        lname = driver.find_element_by_id('registrant.lastName')
        lname.send_keys(form_data.lname)

        email = driver.find_element_by_id('registrant.email')
        email.send_keys(form_data.email)

        # Extra input values in case if there are extra questions (Modify them accordingly)
        if form_data.custque0 != '':
            custQue0 = driver.find_element_by_id('customQuestion0')
            custQue0.send_keys(form_data.custque0)
        if form_data.custque1 != '':
            custQue1 = driver.find_element_by_id('customQuestion1')
            custQue1.send_keys(form_data.custque1)

        # submit the registration form
        submit = driver.find_element_by_id('registration.submit.button').click()

        driver.implicitly_wait(2)
        time.sleep(4)

        if "https://applauncher.gotowebinar.com/#join/attendee" in driver.current_url:
            driver.maximize_window()
            pyautogui.moveTo(1071, 220)
            time.sleep(5)
            cursor = pyautogui.leftClick(1071, 220)    # Accepts the request of opening GoToOpener

        if "https://register.gotowebinar.com/registrationConfirmation" in driver.current_url:
            # click on join the webinar
            join_link = driver.find_element_by_link_text('join the webinar.').click()
            driver.maximize_window()

            # switches the WebDriver focus to new tab
            driver.switch_to.window(driver.window_handles[1])
            if "https://applauncher.gotowebinar.com/#join/attendee" in driver.current_url:
                pyautogui.moveTo(1071, 220)
                time.sleep(5)
                # Accepts the request of opening GoToOpener
                cursor = pyautogui.leftClick(1071, 220)

            # Closes everything if webinar is not started
            if "https://applauncher.gotowebinar.com/#notStarted" in driver.current_url:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.implicitly_wait(1)
                driver.close()
                print("Webinar is ended.")
        return render_template("goto_gui.html", fname=form_data.fname)
    return render_template("goto_gui.html")

if __name__ == "__main__":
    app.run(debug=True)