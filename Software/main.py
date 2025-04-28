import dearpygui.dearpygui as dpg
import dbms
import plotter
from datetime import date
import time

# Tells image display logic in areaSearchCallback to wait for mathplotlib in plotter
# to finish constructing its plot. 
wait = False

# Initializing the GUI library & creating a window.
dpg.create_context()
dpg.create_viewport(title="Toronto Crime Statistics", width=800, height=400)
dpg.setup_dearpygui()

# Callback for the 'Get' button in the query tab.
def areaSearchCallback():
    global wait
    lat, long = dbms.addressToLatLong(dpg.get_value("address_query_value"))
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
        wait = True
        while wait:
            time.sleep(0.1)
        width, height, channels, data = dpg.load_image("output_map.jpg")
        try:
            dpg.delete_item("output_map")
            dpg.delete_item("query_output")
        except:
            pass
        with dpg.texture_registry():
            dpg.add_static_texture(width=width, height=height, default_value=data, tag="output_map")
        with dpg.window(tag="query_output", label="Crimes in Area", width=width, height=height):
            dpg.add_image("output_map")
    else:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Wasn't able to complete query.")

# Callback for the 'Insert' button in the Insert tab.
def insertCallback():
    lat, long = dbms.addressToLatLong(dpg.get_value("address_insert_value")+", Toronto")
    if lat == None or long == None:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Please enter a valid address.")
        return
    occurDate = dpg.get_value("date_value")
    print(occurDate)
    status = dbms.insert(
        dpg.get_value("ucr_value"), dpg.get_value("offense_value"),
        dpg.get_value("mci_category_value"), date(occurDate['year']+1900, occurDate['month']+1, occurDate['month_day']),
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

# Callback for the 'Delete' button in the Delete tab.
def deleteSearchCallback():
    dateVal = dpg.get_value("delete_date_value")
    status, result = dbms.searchForDelete(date(dateVal['year']+1900, dateVal['month']+1, dateVal['month_day']))
    if status == 0:
        with dpg.window(tag="confirm_delete", label="Confirm Delete", width=400, height=50, no_resize=True):
            dpg.add_text("You're attempting to delete {0} crime reports.".format(result[0][0]))
            dpg.add_text("Are you sure you want to do this?")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Yes", callback=deleteCallback)
                dpg.add_button(label="No", callback=deleteCancelCallback)
    else:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Wasn't able to complete query.")

# Callback for the 'Yes' button in the delete confirmation popup.
def deleteCallback():
    dateVal = dpg.get_value("delete_date_value")
    status = dbms.delete(date(dateVal['year']+1900, dateVal['month']+1, dateVal['month_day']))
    if status == 0:
        with dpg.window(label="Success", width=300, height=50, no_resize=True):
            dpg.add_text("Items successfully removed from DB.")
    else:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Deletion failed.")
    dpg.delete_item("confirm_delete")

# Callback for the 'No' button in the delete confirmation popup.
def deleteCancelCallback():
    dpg.delete_item("confirm_delete")

# Callback for the 'Login' button on the login screen.
def login():
    # Attempting to create DB connection instance with credentials.
    if dbms.create(dpg.get_value("user_value"), dpg.get_value("pass_value")) != 0:
        with dpg.window(label="Error", width=300, height=50, no_resize=True):
            dpg.add_text("Error logging in, please try again.")
        return
    # Deleting local storage password upon successful login.
    dpg.delete_item("pass_value")
    # Constructing the main window GUI for application functions.
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
                    dpg.add_text("Date & Hour:")
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
            with dpg.tab(label="Delete"):
                with dpg.group(horizontal=True):
                    dpg.add_text("Date:")
                    dpg.add_date_picker(tag="delete_date_value")
                dpg.add_button(label="Delete", callback=deleteSearchCallback)
    # Replacing the login window with the new one.
    dpg.set_primary_window("MainWindow", True)
    dpg.delete_item("login_window")

# Creating the login window GUI upon startup.
with dpg.window(tag="login_window"):
    dpg.add_text("Please Login:")
    with dpg.group(horizontal=True):
        dpg.add_text("Username:")
        dpg.add_input_text(tag="user_value", default_value="dlayton")
    with dpg.group(horizontal=True):
        dpg.add_text("Password:")
        dpg.add_input_text(tag="pass_value", password=True)
    dpg.add_button(label="Connect", callback=login)
dpg.set_primary_window("login_window", True)

# Main render loop.
dpg.show_viewport()
while dpg.is_dearpygui_running():
    # Update matplotlib plot on main thread if an update to the plot is needed.
    if plotter.updatePlot():
        wait = False
    # Render GUI.
    dpg.render_dearpygui_frame()

# Cleaning up GUI library and DB connection.
dpg.destroy_context()
dbms.destroy()

