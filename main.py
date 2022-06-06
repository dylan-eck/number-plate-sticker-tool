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
    StringVar,
    Button,
    filedialog
)

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

def init_parameters():
    for key in parameters:
        parameters[key] = StringVar()

def get_parameters():
    global parameters
    parameters['font_size'] = int(font_size_entry.get())
    parameters['highlight_padding'] = int(highlight_padding_entry.get())
    parameters['sticker_width'] = int(sticker_width_entry.get())
    parameters['sticker_height'] = int(sticker_height_entry.get())
    parameters['dot_radius'] = int(dot_radius_entry.get())
    parameters['dot_spacing'] = int(dot_spacing_entry.get())

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

    global window_width
    wwidth = 320
    global wheihgt
    wheight = 240 
    root.geometry(str(wwidth) + 'x' + str(wheight))
    root.resizable(False, False)

    init_parameters()

    font_size_label = Label(root, text="font size:", font=font)
    global font_size_entry
    font_size_entry = Entry(root, textvariable=parameters['font_size'], font=font)

    highlight_padding_label = Label(root, text="text highlight padding:", font=font)
    global highlight_padding_entry
    highlight_padding_entry = Entry(root, textvariable=parameters['highlight_padding'], font=font)

    sticker_width_label = Label(root, text="sticker width (px):", font=font)
    global sticker_width_entry
    sticker_width_entry = Entry(root, textvariable=parameters['sticker_width'], font=font)

    sticker_height_label = Label(root, text="sticker height (px):", font=font)
    global sticker_height_entry
    sticker_height_entry = Entry(root, textvariable=parameters['sticker_height'], font=font)

    dot_radius_label = Label(root, text="dot radius (px):", font=font)
    global dot_radius_entry
    dot_radius_entry = Entry(root, textvariable=parameters['dot_radius'], font=font)

    dot_spacing_label = Label(root, text="dot spacing (px):", font=font)
    global dot_spacing_entry
    dot_spacing_entry = Entry(root, textvariable=parameters['dot_spacing'], font=font)
    
    global file_entry_box
    file_entry_box = Entry(root, width=41, font=font)

    load_button = Button(root, text="load file", width=16, command=load_file, font=font)
    generate_button = Button(root, text="generate stickers", width=16, command=generate_stickers, font=font)

    ### layout ###
    font_size_label.grid(row=0, column=0)
    font_size_entry.grid(row=0, column=1)
    highlight_padding_label.grid(row=1, column=0)
    highlight_padding_entry.grid(row=1, column=1)

    sticker_width_label.grid(row=2, column=0)
    sticker_width_entry.grid(row=2, column=1)
    sticker_height_label.grid(row=3, column=0)
    sticker_height_entry.grid(row=3, column=1)
    dot_radius_label.grid(row=4, column=0)
    dot_radius_entry.grid(row=4, column=1)
    dot_spacing_label.grid(row=5, column=0)
    dot_spacing_entry.grid(row=5, column=1)

    file_entry_box.grid(row=6, column=0, columnspan=2)
    load_button.grid(row=7, column=0)
    generate_button.grid(row=7, column=1)
    
    root.mainloop()