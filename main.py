import dearpygui.dearpygui as dpg
import dbms
import plotter
from datetime import date

dpg.create_context()
dpg.create_viewport(title="Toronto Crime Statistics", width=800, height=400)
dpg.setup_dearpygui()

def areaSearchCallback():
    lat, long = dbms.addessToLatLong(dpg.get_value("address_query_value"))
    if lat == None or long == None:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Please enter a valid address.")
        return
    status, result = dbms.crimesInArea(lat, long, dpg.get_value("hori_value"), dpg.get_value("vert_value"))
    if status == 0:
        lats = []
        longs = []
        crimes = []
        for row in result:
            lats.append(row[0])
            longs.append(row[1])
            crimes.append(row[2])
        plotter.make_map(lat, long, lats, longs, crimes)
        width, height, channels, data = dpg.load_image("output_map.jpg")
        with dpg.texture_registry():
            dpg.add_static_texture(width=width, height=height, default_value=data, tag="output_map")
        with dpg.window(label="Crimes in Area", width=width, height=height):
            dpg.add_image("output_map")
    else:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Wasn't able to complete query.")

def insertCallback():
    lat, long = dbms.addessToLatLong(dpg.get_value("address_insert_value"))
    if lat == None or long == None:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Please enter a valid address.")
        return
    
    occurDate = dpg.get_value("date_value")
    status = dbms.insert(
        dpg.get_value("ucr_value"), dpg.get_value("offense_value"),
        dpg.get_value("mci_category_value"), date(occurDate['year'], occurDate['month'], occurDate['month_day']),
        dpg.get_value("hour_value"), dpg.get_value("address_insert_value"),
        dpg.get_value("hoodcode_value"), dpg.get_value("hood_value"),
        dpg.get_value("premise_value"), dpg.get_value("location_value"),
        dpg.get_value("division_value"))
    
    if status == 0:
        with dpg.window(label="Success", width=300, height=50, no_resize=True):
            dpg.add_text("Item successfully added to DB.")
    else:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Wasn't able to complete query.")

def login():
    if dbms.create(dpg.get_value("user_value"), dpg.get_value("pass_value")) != 0:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Error logging in, please try again.")
        return
    dpg.delete_item("pass_value")
    with dpg.window(tag="MainWindow"):
        with dpg.tab_bar():
            with dpg.tab(label="Query"):
                with dpg.group(horizontal=True):
                    dpg.add_text("Address to Query:")
                    dpg.add_input_text(tag="address_query_value")
                dpg.add_text("Region to Search in:")
                dpg.add_input_float(tag="hori_value", min_value=0.1, min_clamped=True, default_value=0.1)
                dpg.add_input_float(tag="vert_value", min_value=0.1, min_clamped=True, default_value=0.1)
                dpg.add_button(label="Get", callback=areaSearchCallback)
            with dpg.tab(label="Insert"):
                with dpg.group(horizontal=True):
                    dpg.add_text("UCR:")
                    dpg.add_input_text(tag="ucr_value")
                with dpg.group(horizontal=True):
                    dpg.add_text("Offense:")
                    dpg.add_input_text(tag="offense_value")
                with dpg.group(horizontal=True):
                    dpg.add_text("MCI Category:")
                    dpg.add_input_text(tag="mci_category_value")
                with dpg.group(horizontal=True):
                    dpg.add_text("Date & Time:")
                    dpg.add_date_picker(tag="date_value")
                    dpg.add_input_int(tag="hour_value", min_value=0, max_value=23)
                with dpg.group(horizontal=True):
                    dpg.add_text("Address:")
                    dpg.add_input_text(tag="address_insert_value")
                with dpg.group(horizontal=True):
                    dpg.add_text("Neighborhood Code:")
                    dpg.add_input_text(tag="hoodcode_value")
                with dpg.group(horizontal=True):
                    dpg.add_text("Neighborhood:")
                    dpg.add_input_text(tag="hood_value")
                with dpg.group(horizontal=True):
                    dpg.add_text("Premise Type:")
                    dpg.add_input_text(tag="premise_value")
                with dpg.group(horizontal=True):
                    dpg.add_text("Location Type:")
                    dpg.add_input_text(tag="location_value")
                with dpg.group(horizontal=True):
                    dpg.add_text("Division:")
                    dpg.add_input_text(tag="division_value")
                dpg.add_button(label="Insert", callback=insertCallback)
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

