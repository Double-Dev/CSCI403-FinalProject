import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Toronto Crime Statistics", width=800, height=400)
dpg.setup_dearpygui()

with dpg.window(label="Example Window"):
    dpg.add_text("Hello, Dear PyGui")

dpg.show_viewport()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()

