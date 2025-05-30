from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from tkinter import messagebox, ttk
from tkinter import *
import pandas as pd

# NOTE! For PhotoImage functions, change the directory to your desired folder.
# NOTE! This software application is made for school purposes only.

# Global Variables
user_input_table = pd.DataFrame(columns=['rateClassification', 'meterSize', 'cubicMeterConsumption', 'month'])
months_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
consumption_history = []

# User-Defined Functions
def calculate_maintenance_charge(meter_size):
    charge_dict = {
        "1/2\"": 1.50,
        "3/4\"": 2.00,
        "1\"": 3.00,
        "2\"": 6.00,
        "3\"": 10.00,
        "4\"": 20.00,
        "6\"": 35.00,
        "8\"": 50.00
    }
    if meter_size in charge_dict:
        return charge_dict[meter_size]
    else:
        return 0.00 

def calculate_total_basic_charge(cubic_meter_consumption):
    min_charge = 148.80

    if cubic_meter_consumption <= 10:
        total_bill = min_charge * cubic_meter_consumption
    elif 10 < cubic_meter_consumption <= 20:
        total_bill = min_charge + ((cubic_meter_consumption - 10) * 18.13)
    elif 20 < cubic_meter_consumption <= 40:
        total_bill = min_charge + (10 * 18.13) + ((cubic_meter_consumption - 20) * 34.38)
    elif 40 < cubic_meter_consumption <= 60:
        total_bill = min_charge + (10 * 18.13) + (20 * 34.38) + ((cubic_meter_consumption - 40) * 45.32)
    elif 60 < cubic_meter_consumption <= 80:
        total_bill = min_charge + (10 * 18.13) + (20 * 34.38) + (20 * 45.32) + ((cubic_meter_consumption - 60) * 52.93)
    elif 80 < cubic_meter_consumption <= 100:
        total_bill = min_charge + (10 * 18.13) + (20 * 34.38) + (20 * 45.32) + (20 * 52.93) + ((cubic_meter_consumption - 80) * 55.48)
    elif 100 < cubic_meter_consumption <= 150:
        total_bill = min_charge + (10 * 18.13) + (20 * 34.38) + (20 * 45.32) + (20 * 52.93) + (20 * 55.48) + ((cubic_meter_consumption - 100) * 57.96)
    elif 150 < cubic_meter_consumption <= 200:
        total_bill = min_charge + (10 * 18.13) + (20 * 34.38) + (20 * 45.32) + (20 * 52.93) + (20 * 55.48) + (50 * 57.96) + ((cubic_meter_consumption - 150) * 60.45)
    else:
        total_bill = min_charge + (10 * 18.13) + (20 * 34.38) + (20 * 45.32) + (20 * 52.93) + (20 * 55.48) + (50 * 57.96) + (50 * 60.45) + ((cubic_meter_consumption - 200) * 62.93)

    return total_bill

def btn_clicked():
    if b0_var.get() == "Low-Income Household":
        rate_classification = "Low-Income Household"
    else:
        rate_classification = "Common Residential"

    meter_size = b2_var.get()
    cubic_meter_consumption = int(entry0.get())
    month = b1_var.get()
    user_input_table.loc[len(user_input_table)] = [rate_classification, meter_size, cubic_meter_consumption, month]
    entry0.delete(0, END)

    if meter_size:
        add_to_consumption_history(rate_classification, meter_size, cubic_meter_consumption, month)

def calculate_button_clicked():
    perform_prediction()

def add_to_consumption_history(rate_classification, meter_size, cubic_meter_consumption, month):
    consumption_history.append({
        "Rate Class": rate_classification,
        "Meter Size": meter_size,
        "Consumption": cubic_meter_consumption,
        "Month": month
    })

def show_consumption_history():
    history_window = Toplevel(window)
    history_window.geometry("600x400")
    history_window.title("Consumption History")
    history_label = Label(
        history_window,
        text="Water Consumption History",
        font=("Poppins", 14),
        justify=LEFT,
    )
    history_label.pack(pady=10)

    tree = ttk.Treeview(history_window, show="headings")
    tree["columns"] = ("Entry No.", "Month", "Rate Class", "Meter Size", "CU.M. Used")
    tree.heading("Entry No.", text="Entry No.")
    tree.column("Entry No.", anchor="center", width=50)
    tree.heading("Month", text="Month")
    tree.column("Month", anchor="center", width=100)
    tree.heading("Rate Class", text="Rate Class")
    tree.column("Rate Class", anchor="center", width=150)
    tree.heading("Meter Size", text="Meter Size")
    tree.column("Meter Size", anchor="center", width=100)
    tree.heading("CU.M. Used", text="CU.M. Used")
    tree.column("CU.M. Used", anchor="center", width=100)

    for i, entry in enumerate(consumption_history, start=1):
        tree.insert("", i, values=(i, entry['Month'], entry['Rate Class'], entry['Meter Size'], entry['Consumption']))

    tree.pack(padx=20, pady=10, fill="both", expand=True)

    clear_button = Button(
        history_window,
        text="Clear History",
        command=clear_history
    )
    clear_button.pack(pady=5)

def clear_history():
    global consumption_history
    consumption_history = []
    messagebox.showinfo("History Cleared", "Consumption history has been cleared.")

def validate_input(value):
    if value == "":
        return True
    try:
        int(value)
        return True
    except ValueError:
        return False

def perform_prediction():
    historical_data = pd.DataFrame({
        'rateClassification': [2, 2, 2],
        'meterSize': ["1\"", "1\"", "1\""],
        'cubicMeterConsumption': [41, 31, 33],
        'month': ["September", "October", "November"]
    })

    combined_data = pd.concat([user_input_table, historical_data])
    X = pd.get_dummies(combined_data[['rateClassification', 'meterSize', 'month']], drop_first=True)
    y = combined_data['cubicMeterConsumption']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    most_recent_month = user_input_table['month'].iloc[-1]
    months_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    next_month_index = (months_order.index(most_recent_month) + 1) % 12
    next_month = months_order[next_month_index]

    new_data = pd.DataFrame({'rateClassification': [2], 'meterSize': ['1"'], f'month_{next_month}': [1]})  # Use the most recent month
    new_data_encoded = pd.get_dummies(new_data, drop_first=True)
    missing_cols = set(X_train.columns) - set(new_data_encoded.columns)
    
    for col in missing_cols:
        new_data_encoded[col] = 0

    new_data_encoded = new_data_encoded[X_train.columns]
    user_input_count = len(user_input_table)

    if user_input_count > 0:
        user_inputs = user_input_table['cubicMeterConsumption'].values
        average_user_consumption = sum(user_inputs) / user_input_count
        predicted_cubic_meter = round((average_user_consumption + model.predict(new_data_encoded)[0]) / 2)
        predicted_cubic_meter = max(predicted_cubic_meter, min(user_inputs))
    else:
        predicted_cubic_meter = round(model.predict(new_data_encoded)[0])

    estimated_total_basic_charge = calculate_total_basic_charge(predicted_cubic_meter)
    maintenance_service_charge = calculate_maintenance_charge(b2_var.get())
    environmental_charge = 0.25 * estimated_total_basic_charge
    government_tax = 0.02 * (estimated_total_basic_charge + environmental_charge + maintenance_service_charge)
    total_water_bill = estimated_total_basic_charge + environmental_charge + maintenance_service_charge + government_tax
    
    result_text = f"Predicted CU.M. Consumption for {next_month}: {predicted_cubic_meter}\n"
    result_text += f"Estimated Basic Charge for {next_month}: ₱{estimated_total_basic_charge:.2f}\n"
    result_text += f"Environmental Charge: ₱{environmental_charge:.2f}\n"
    result_text += f"Maintenance Service Charge: ₱{maintenance_service_charge:.2f}\n"
    result_text += f"Government Tax: ₱{government_tax:.2f}\n"
    result_text += f"Estimated Total Water Bill: ₱{total_water_bill:.2f}"

    result_label.config(text=result_text)

# Application Graphical User-Interface
window = Tk()
window.geometry("360x640")
window.configure(bg = "#FFFFFF")
window.title("Cubic Forecast")
window.iconbitmap("assets/logo/logo.ico")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 640,
    width = 360,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)
background_img = PhotoImage(file = f"assets/images/background.png")
background = canvas.create_image(
    148.0, 241.0,
    image=background_img)

# Buttons
rate_classification_options = ["Low-Income Household", "Common Residential"]
b0_var = StringVar()
b0_var.set(rate_classification_options[0])
b0 = OptionMenu(window, b0_var, *rate_classification_options)
b0.place(x=160, y=187, width=165, height=20)

meter_size_options = ["1/2\"", "3/4\"", "1\"", "1 1/4\"", "2\"", "3\"", "4\"", "6\"", "8\""]
b2_var = StringVar()
b2_var.set(meter_size_options[0])
b2 = OptionMenu(window, b2_var, *meter_size_options)
b2.place(x=160, y=238, width=163, height=20)

month_options = months_order
b1_var = StringVar()
b1_var.set(month_options[0])
b1 = OptionMenu(window, b1_var, *month_options)
b1.place(x=160, y=340, width=165, height=20)

cubicMeterConsumption = PhotoImage(file = f"assets/images/text_box.png")
entry0_bg = canvas.create_image(
    250.0, 299.0,
    image = cubicMeterConsumption)

entry0 = Entry(
    bd=0,
    bg="#eeeeee",
    highlightthickness=0,
    validate="key",
    validatecommand=(window.register(validate_input), '%P'),
    justify='center',
    width=10
)

entry0.place(
    x=160, y=289,
    width=165,
    height=20
)

calculate_button = PhotoImage(file = f"assets/images/calculate_button.png")
b3 = Button(
    image = calculate_button,
    borderwidth = 0,
    highlightthickness = 0,
    command = calculate_button_clicked,
    relief = "flat",
    bg = "#699FD2")

b3.place(
    x = 195, y = 390,
    width = 130,
    height = 50)

store_button = PhotoImage(file = f"assets/images/add_button.png")
b4 = Button(
    image = store_button,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat",
    bg = "#699FD2")

b4.place(
    x = 36, y = 390,
    width = 130,
    height = 50)

history_button = PhotoImage(file = f"assets/images/show_history_button.png")
b5 = Button(
    image = history_button,
    borderwidth = 0,
    highlightthickness = 0,
    command = show_consumption_history,
    relief = "flat",
    bg = "#FFFFFF")

b5.place(
    x = 70, y = 582,
    width = 223,
    height = 30)

# Predicted Results
result_label = Label(window, text="", font=("Poppins", 10), justify=LEFT, bg="#ffffff")
result_label.place(x=30, y=460, width=300, height=120)

window.resizable(False, False)
window.mainloop()
# End of Program, Thank You!