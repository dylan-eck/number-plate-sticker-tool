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

from pyparsing import col

def create_sheet(stickers):
    width, height = stickers[0].size
    sticker_sheet = Image.new(mode="RGB", size=(width * 4, height * 6))

    num = 0
    for row in range(6):
        for column in range(4):
            sticker_sheet.paste(stickers[num],(column * width, row * height))
            num += 1

    return sticker_sheet

def load_file():
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
    global parameters
    get_parameters()

    global filename
    if not filename:
        load_file()

    if not os.path.exists('out'):
        os.mkdir('out')

    sticker_info = pd.read_excel(r'./stickers.xlsx').values.tolist()

    image_buffer = []

    num = 0
    for row in sticker_info:
        plate_number = row[0]
        color = row[1]
        subgroup = row[2]

        image = Image.new(mode="RGB", size=(parameters['sticker_width'], parameters['sticker_height']), color=color)
        draw = ImageDraw.Draw(image)

        if subgroup == 'polka dot':
            num_dots_horiz = int(parameters['sticker_width'] / parameters['dot_spacing'])
            num_dots_vert = int(parameters['sticker_height'] / parameters['dot_spacing'])

            dwidth = (num_dots_horiz - 1) * parameters['dot_spacing']
            dheight = (num_dots_vert - 1) * parameters['dot_spacing']

            for i in range(num_dots_horiz):
                for j in range(num_dots_vert):
                    x = (i * parameters['dot_spacing']) + ((parameters['sticker_width'] - dwidth) / 2)
                    y = (j * parameters['dot_spacing']) + ((parameters['sticker_height'] - dheight) / 2)

                    p1 = (x - parameters['dot_radius'], y - parameters['dot_radius'])
                    p2 = (x + parameters['dot_radius'], y + parameters['dot_radius'])

                    draw.ellipse((p1, p2), fill='white')

        draw.rectangle([(0, 0), (parameters['sticker_width'], parameters['sticker_height'])], outline='white', width=4, fill=None)

        font = ImageFont.truetype("Arial.ttf", parameters['font_size'])
        x0, y0, x1, y1 = draw.textbbox((parameters['sticker_width'] / 2, parameters['sticker_height'] / 2), plate_number, font=font, anchor='mm')
        draw.rectangle([(x0 - parameters['highlight_padding'], y0 - parameters['highlight_padding']), (x1 + parameters['highlight_padding'], y1 + parameters['highlight_padding'])], outline=(110, 110, 100), width=4, fill='white')
        draw.text((parameters['sticker_width'] / 2, parameters['sticker_height'] / 2), plate_number, fill="Black", font=font, anchor='mm')

        if len(image_buffer) == 24:
            sticker_sheet = create_sheet(image_buffer)
            sticker_sheet.save("out/sticker_sheet_" + str(num) + ".pdf")
            image_buffer = []
            num += 1
        else:
            image_buffer.append(image)

def get_parameters():
    global parameters
    for key in parameters:
        for widget in parameters[key].winfo_children():
            if widget.winfo_class() == 'Entry':
                parameters[key] = int(widget.get())

def create_labeled_entry_box(parent, text, font):
    frame = Frame(parent)
    label = Label(frame, text=text, font=font)
    entry = Entry(frame, font=font)
    label.grid(row=0,column=0)
    entry.grid(row=0, column=1)
    return frame

if __name__ == '__main__':
    global parameters
    parameters = {
        'font_size': None,           # 50
        'highlight_padding': None,   # 10
        'sticker_width': None,       # 300
        'sticker_height': None,      # 256
        'dot_radius': None,          # 15
        'dot_spacing': None          # 50
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

    for key in parameters:
        parameters[key] = create_labeled_entry_box(root, key + ':', font)

    global file_entry_box
    file_entry_box = Entry(root, width=41, font=font)

    load_button = Button(root, text="load file", width=16, command=load_file, font=font)
    generate_button = Button(root, text="generate stickers", width=16, command=generate_stickers, font=font)

    ### layout ###
    row = 0
    for entry in parameters.values():
        entry.grid(row=row, column=0, columnspan=2)
        row += 1

    file_entry_box.grid(row=row, column=0, columnspan=2)
    row += 1
    load_button.grid(row=row, column=0)
    generate_button.grid(row=row, column=1)

    root.mainloop()