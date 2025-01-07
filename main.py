import PySimpleGUI as sg
import os

exit_button = [sg.Button('Exit', size=(15, 1), key='Exit_Program')]
config_folder = f"{os.getenv('LOCALAPPDATA')}/FortniteGame/Saved/Config/WindowsClient/"
sg.LOOK_AND_FEEL_TABLE['FortniteBlue'] = {
    'BACKGROUND': '#87CEEB',
    'TEXT': '#FFFFFF',
    'INPUT': '#F0F8FF',
    'TEXT_INPUT': '#000000',
    'SCROLL': '#87CEEB',
    'BUTTON': ('#FFFFFF', '#4682B4'),
    'PROGRESS': ('#87CEEB', '#4682B4'),
    'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
}
sg.theme('FortniteBlue')
layout = [
    [sg.Text('FNSS', font="_ 15", justification='c', expand_x=True)],
    [sg.Text("Save and load wanted settings.\nYou'll be able to adjust them in-game if needed.",
             justification='c', expand_x=True, pad=((0, 0), (0, 0)))],
    [sg.Button('Load Settings', size=(15, 1), key="Load", pad=((0, 0), (10, 0)))],
    [sg.Button('Save Settings', size=(15, 1), key="Save", pad=((0, 0), (10, 0)))],
    [sg.Button('Exit', size=(7, 1), key='Exit_Program', pad=((0, 0), (10, 0)))],
]
sg.set_global_icon('fortnite_icon.ico')
window = sg.Window('FN Settings Switcher', layout, size=(375, 215), resizable=False, finalize=True,
                   element_justification='c')
def main_app():
    while True:
        event, values = window.read()
        if event in ['Load']:
            load_settings()
        elif event in ['Save']:
            save_settings()
        elif event in [sg.WIN_CLOSED, 'Exit_Program']:
            break


def load_settings():
    file_path = sg.popup_get_file("Select a .fnss file to load", file_types=(('FNSS Files', '*.fnss'),))
    if file_path:
        with open(file_path, "r") as input_file:
            file_text = input_file.read()

        sections = file_text.split('-----------------FNSSSPLITERR-----------------')
        for section in sections:
            if not section.strip():
                continue
            lines = section.splitlines()
            if len(lines) < 1:
                continue
            file_name = lines[0].replace('; ', '').strip()
            file_content = "\n".join(lines[1:])
            file_path_to_save = os.path.join(config_folder, file_name)
            with open(file_path_to_save, "w") as output_file:
                output_file.write(file_content)
        sg.popup(f"Loaded settings from: {file_path}", title="Load Successful")


def save_settings():
    file_path = sg.popup_get_file("Select a location to save your .fnss file", save_as=True,
                                  file_types=(('FNSS Files', '*.fnss'),))
    if file_path:
        if not file_path.endswith('.fnss'):
            file_path += '.fnss'
        file_text = ''
        for x in os.listdir(config_folder):
            with open(config_folder+x, "r") as file:
                line = file.readline()
                file_text = file_text + f"-----------------FNSSSPLITERR-----------------; {x}\n"
                while line:
                    file_text = file_text+line
                    line = file.readline()
        with open(file_path, "w") as file:
            file.write(file_text)
        sg.popup(f"Settings saved to: {file_path}", title="Save Successful")

if __name__ == "__main__":
    main_app()
    window.close()
