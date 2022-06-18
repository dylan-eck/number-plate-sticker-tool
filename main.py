import os
import pandas as pd
from PIL import (
    Image,
    ImageDraw,
    ImageFont
)
from tkinter import (
    Tk,
    Label,
    Entry,
    Frame,
    Button,
    filedialog
)

def create_sheet(stickers):
    width, height = stickers[0].size
    sticker_sheet = Image.new(mode="RGB", size=(width * 4, height * 6))

    num = 0
    for row in range(6):
        for column in range(4):
            sticker_sheet.paste(stickers[num], (column * width, row * height))
            num += 1

    return sticker_sheet

def choose_file():
    global filename
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Choose a File",
        filetypes=(
            ("comma separated values (.csv)", "*.csv"),
            (".xls", "*.xls"),
            (".xlsx", "*.xlsx")
        )
    )
    file_entry_box.insert(index=0, string=filename)

def generate_stickers():
    update_parameter_variables()
    global parameter_entry_dict
    sticker_width = parameter_entry_dict['sticker width'].value
    sticker_height = parameter_entry_dict['sticker height'].value
    dot_radius = parameter_entry_dict['dot radius'].value
    dot_spacing = parameter_entry_dict['dot spacing'].value
    font_size = parameter_entry_dict['font size'].value
    highlight_padding = parameter_entry_dict['highlight padding'].value

    global filename
    if not filename:
        choose_file()

    if not os.path.exists('out'):
        os.mkdir('out')

    sticker_info = pd.read_excel(r'./stickers.xlsx').values.tolist()

    image_buffer = []

    num = 0
    for row in sticker_info:
        plate_number = row[0]
        color = row[1]
        subgroup = row[2]

        skills = row[3:7]
        skills_str = f'{skills[0]}{skills[1]}{skills[2]}{skills[3]}'

        time = row[7]

        image = Image.new(
            mode="RGB",
            size=(sticker_width, sticker_height),
            color=color
        )
        draw = ImageDraw.Draw(image)

        if subgroup == 'polka dot':
            num_dots_horiz = int(sticker_width / dot_spacing)
            num_dots_vert = int(sticker_height / dot_spacing)

            dwidth = (num_dots_horiz - 1) * dot_spacing
            dheight = (num_dots_vert - 1) * dot_spacing

            for i in range(num_dots_horiz):
                for j in range(num_dots_vert):
                    x = (i * dot_spacing) + ((sticker_width - dwidth) / 2)
                    y = (j * dot_spacing) + ((sticker_height - dheight) / 2)

                    p1 = (x - dot_radius, y - dot_radius)
                    p2 = (x + dot_radius, y + dot_radius)

                    draw.ellipse((p1, p2), fill='white')

        draw.rectangle(
            [(0, 0), (sticker_width, sticker_height)],
            outline='white',
            width=4,
            fill=None
        )

        main_font = ImageFont.truetype("arial.ttf", font_size)
        sub_font = ImageFont.truetype("arial.ttf", int(font_size * 0.7))

        x0, y0, x1, y1 = draw.textbbox(
            (sticker_width / 2, sticker_height / 2),
            f'{plate_number}\n{skills_str}\n{time}',
            font=main_font,
            anchor='mm'
        )

        draw.rectangle(
            [
                (x0 - highlight_padding, y0 - highlight_padding),
                (x1 + highlight_padding, y1 + highlight_padding)
            ],
            outline=(110, 110, 100),
            width=4,
            fill='white'
        )
        
        draw.text(
            (sticker_width / 2, sticker_height / 2 - font_size),
            str(plate_number),
            fill="Black",
            font=main_font,
            anchor='mm'
        )

        draw.text(
            (sticker_width / 2, sticker_height / 2),
            skills_str,
            fill="Black",
            font = sub_font,
            anchor='mm'
        )

        draw.text(
            (sticker_width / 2, sticker_height / 2 + font_size),
            str(time),
            fill="Black",
            font = sub_font,
            anchor='mm'
        )

        if len(image_buffer) == 24:
            sticker_sheet = create_sheet(image_buffer)
            sticker_sheet.save("out/sticker_sheet_" + str(num) + ".pdf")
            image_buffer = []
            num += 1
        else:
            image_buffer.append(image)

def update_parameter_variables():
    global parameter_entry_dict
    for key in parameter_entry_dict:
        for widget in parameter_entry_dict[key].entry_frame.winfo_children():
            if widget.winfo_class() == 'Entry':
                parameter_entry_dict[key].value = int(widget.get())

def create_labeled_entry_box(parent, text, font):
    frame = Frame(parent)
    label = Label(frame, text=text, font=font)
    entry = Entry(frame, font=font)
    label.grid(row=0,column=0)
    entry.grid(row=0, column=1)
    return frame

class Parameter:
    def __init__(self, name, default_value, entry_frame):
        self.name = name
        self.value = None
        self.default_value = default_value
        self.entry_frame = entry_frame

if __name__ == '__main__':
    parameter_info = {
        'font size': 50,
        'highlight padding': 10,
        'sticker width': 300,
        'sticker height': 256,
        'dot radius': 15,
        'dot spacing': 50
    }

    global filename
    filename = ""

    font = ("Monaco", 12)

    ### window items ###
    root = Tk()
    root.title(string='number plate sticker tool')
    wwidth = 320
    wheight = 240 
    root.geometry(str(wwidth) + 'x' + str(wheight))
    root.resizable(False, False)

    global parameter_entry_dict
    parameter_entry_dict = {}
    for key in parameter_info:
        name = key
        default_value = parameter_info[key]
        entry_frame = create_labeled_entry_box(root, name + ':', font)
        parameter = Parameter(name, default_value, entry_frame)
        parameter_entry_dict[key] = parameter

    global file_entry_box
    file_entry_box = Entry(root, width=41, font=font)

    load_button = Button(
        root,
        text="choose file",
        width=16,
        command=choose_file,
        font=font
    )
    generate_button = Button(
        root,
        text="generate stickers",
        width=16,
        command=generate_stickers, 
        font=font
    )

    ### layout ###
    row = 0
    for parameter in parameter_entry_dict.values():
        for widget in parameter.entry_frame.winfo_children():
            if widget.winfo_class() == 'Entry':
                widget.insert(0, str(parameter.default_value))

        parameter.entry_frame.grid(row=row, column=0, columnspan=2)
        row += 1

    file_entry_box.grid(row=row, column=0, columnspan=2)
    row += 1
    load_button.grid(row=row, column=0)
    generate_button.grid(row=row, column=1)

    root.mainloop()