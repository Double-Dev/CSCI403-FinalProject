import dearpygui.dearpygui as dpg
import dbms

dpg.create_context()
dpg.create_viewport(title="Toronto Crime Statistics", width=800, height=400)
dpg.setup_dearpygui()

with dpg.value_registry():
    dpg.add_string_value(tag="user_value")
    dpg.add_string_value(tag="pass_value")

def dataWindow():
    with dpg.window(label="Data from query"):
        dpg.add_text("temp test text")

def login():
    dbms.create(dpg.get_value("user_value"), dpg.get_value("pass_value"))
    with dpg.window(tag="MainWindow"):
        dpg.add_text("Hello, Dear PyGui")
        # dpg.add_button(label="Test", callback=dataWindow)
        # dpg.add_button(label="Test", callback=dbms.insert)
        dpg.add_button(label="Connect", callback=dbms.create)
        table = dpg.add_input_text(label="Table to query:")
        dpg.add_button(label="Get", callback=dbms.select, user_data=table)
    dpg.set_primary_window("MainWindow", True)
    dpg.configure_item("LoginWindow", show=False)

with dpg.window(tag="LoginWindow"):
    dpg.add_text("Please Login:")
    dpg.add_text("Username:")
    dpg.add_same_line()
    dpg.add_input_text(source="user_value")
    dpg.add_text("Password:")
    dpg.add_same_line()
    dpg.add_input_text(source="pass_value", password=True)
    dpg.add_button(label="Connect", callback=login)
dpg.set_primary_window("LoginWindow", True)

dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()
dbms.destroy()

