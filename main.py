import dearpygui.dearpygui as dpg
import dbms

dpg.create_context()
dpg.create_viewport(title="Toronto Crime Statistics", width=800, height=400)
dpg.setup_dearpygui()

with dpg.value_registry():
    # Login Values
    dpg.add_string_value(tag="user_value")
    dpg.add_string_value(tag="pass_value")
    # Temp Values
    dpg.add_string_value(tag="temp_value")

def dataWindow():
    with dpg.window(label="Data from query"):
        dpg.add_text("temp test text")

def login():
    dbms.create(dpg.get_value("user_value"), dpg.get_value("pass_value"))
    dpg.delete_item("pass_value")
    with dpg.window(tag="MainWindow"):
        with dpg.group(horizontal=True):
            dpg.add_text("Table to query:")
            dpg.add_input_text(source="temp_value")
        dpg.add_button(label="Get", callback=dbms.select, user_data=dpg.get_value("temp_value"))
    dpg.set_primary_window("MainWindow", True)
    dpg.delete_item("LoginWindow")

with dpg.window(tag="LoginWindow"):
    dpg.add_text("Please Login:")
    with dpg.group(horizontal=True):
        dpg.add_text("Username:")
        dpg.add_input_text(source="user_value")
    with dpg.group(horizontal=True):
        dpg.add_text("Password:")
        dpg.add_input_text(source="pass_value", password=True)
    dpg.add_button(label="Connect", callback=login)
dpg.set_primary_window("LoginWindow", True)

dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()
dbms.destroy()

