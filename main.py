import dearpygui.dearpygui as dpg
import dbms

dpg.create_context()
dpg.create_viewport(title="Toronto Crime Statistics", width=800, height=400)
dpg.setup_dearpygui()

def tempCallback():
    dbms.select(dpg.get_value("table_value"))

def areaSearchCallback():
    status, result = dbms.crimesInArea(dpg.get_value("address_value"), dpg.get_value("hori_value"), dpg.get_value("vert_value"))
    if status == 0:
        with dpg.window(label="Crimes in Area"):
            for row in result:
                print(row)

def dataWindow():
    with dpg.window(label="Data from query"):
        dpg.add_text("temp test text")

def login():
    dbms.create(dpg.get_value("user_value"), dpg.get_value("pass_value"))
    dpg.delete_item("pass_value")
    with dpg.window(tag="MainWindow"):
        # with dpg.group(horizontal=True):
        #     dpg.add_text("Table to query:")
        #     dpg.add_input_text(tag="table_value", default_value="crimes_in_toronto")
        # dpg.add_button(label="Get", callback=tempCallback)
        with dpg.group(horizontal=True):
            dpg.add_text("Address to Query:")
            dpg.add_input_text(tag="address_value")
        dpg.add_text("Region to Search in:")
        dpg.add_input_float(tag="hori_value", min_value=0.1)
        dpg.add_input_float(tag="vert_value", min_value=0.1)
        dpg.add_button(label="Get", callback=areaSearchCallback)
    dpg.set_primary_window("MainWindow", True)
    dpg.delete_item("LoginWindow")

with dpg.window(tag="LoginWindow"):
    dpg.add_text("Please Login:")
    with dpg.group(horizontal=True):
        dpg.add_text("Username:")
        dpg.add_input_text(tag="user_value", default_value="dlayton")
    with dpg.group(horizontal=True):
        dpg.add_text("Password:")
        dpg.add_input_text(tag="pass_value", password=True)
    dpg.add_button(label="Connect", callback=login)
dpg.set_primary_window("LoginWindow", True)

dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()
dbms.destroy()

