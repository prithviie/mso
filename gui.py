from tkinter import *
from PIL import ImageTk, Image
from astar import *

start_color_code = None
end_color_code = None

places = [locs_with_cors[i][0] for i in range(1, len(locs_with_cors) + 1)]


def popup1():
    messagebox.showinfo(
        "Treat your toungue", "Nothing can beat Mylari masale dosa\nYou must check out Yampa's Oreo milkshake\nHot bakes in Yamp are also good")


def popup2():
    messagebox.showinfo("Topper??", "Have startup ideas and interested in research??\nVenture into SJCE-step\nOur library has loads of books for any suject you wish\nAlso checout the reference section where you can sit and read in PEACE\nGet pdf of books you wish in digital library")


def popup3():
    messagebox.showinfo("Scenic Views", "Enjoy cricket matches in the beautiful lush green KSCA field\nA walk towards the polytechnic block can be soothing\nYou are allowed to sit in the garden area in between the green Grass")


def popup4():
    messagebox.showinfo(
        "ChitChats", "Yampa is the best place to hang out with your friends\nThe seatings in Hockey court provides a shady shelter\nAlso the Football seatings")


def set_start(event):
    global start_color_code
    loc_name = clicked1.get()

    for key in locs_with_cors:
        if locs_with_cors[key][0] == loc_name:
            start_color_code = locs_with_cors[key][1]


def set_end(event):
    global end_color_code

    loc_name = clicked2.get()

    for key in locs_with_cors:
        if locs_with_cors[key][0] == loc_name:
            end_color_code = locs_with_cors[key][1]


def main2(width, height, map_image, output_image, locs_with_cors, start_color_code, end_color_code):

    grid = preset_barriers(map_image, width, height)

    grid, start, end = update_grid_with_start_end_gui(
        map_image, grid, height, width, locs_with_cors, start_color_code, end_color_code)

    if start and end:
        print("start and end set")

        for row in grid:
            for node in row:
                node.update_neighbours(grid)
        print("neighbours updated")

        try:
            print('trying to find path')
            path_cos = algorithm(lambda: draw_grid(
                grid, width, height), grid, start, end)
            if path_cos:
                print('path found')
                generate_map_with_broad_path(
                    map_image, output_image, path_cos, (255, 0, 0, 255))
            else:
                print('path not found')

        except Exception as e:
            print(e)

        # else:
        # 	# print('Start or end not set')
        # 	pass


def findPath():
    # print(start_color_code, end_color_code)
    main2(WIDTH, HEIGHT, map_image, output_image,
          locs_with_cors, start_color_code, end_color_code)


root = Tk()

root.title("SJCE-Map")
top = Toplevel()
top.title("Services")

# top.geometry("400x400")
myImg = ImageTk.PhotoImage(Image.open(map_image))
myLabel = Label(image=myImg)
myLabel.pack()


# must watches in sjce
frame2 = LabelFrame(
    top, text="You must try these in our college..", padx=20, pady=50)
frame2.config(font=("Forte", 18))
frame2.pack(padx=20, pady=20)


Button(frame2, text="Treat your tongue", command=popup1).pack(padx=10, pady=10)
Button(frame2, text="Topper??", command=popup2).pack(padx=10, pady=10)
Button(frame2, text="Scenic Views", command=popup3).pack(padx=10, pady=10)
Button(frame2, text="ChitChats", command=popup4).pack(padx=10, pady=10)


frame = LabelFrame(top, text="Seek and ye shall find..", padx=15, pady=25)
frame.config(font=("Forte", 18))
frame.pack(padx=15, pady=15)

label1 = Label(frame, text="Where are you??", padx=10, pady=20)
label1.config(font=("Lucida Handwriting", 12))
label1.pack()


clicked1 = StringVar()
drop1 = OptionMenu(frame, clicked1, *places, command=set_start)
drop1.pack()

label2 = Label(frame, text="Where do you want to go??", padx=10, pady=20)
label2.config(font=("Lucida Handwriting", 12))
label2.pack()


clicked2 = StringVar()
drop2 = OptionMenu(frame, clicked2, *places, command=set_end)
drop2.pack()


button1 = Button(frame, text="Search", command=findPath, padx=5, pady=5)
button1.pack(padx=10, pady=10)


root.mainloop()
