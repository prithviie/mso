import csv

locs_data = {}
with open('locswithpixelcor.txt', 'r') as f:
    csv_reader = csv.reader(f)

    next(csv_reader)
    count = 1
    for line in csv_reader:

        essentials = []
        if line[0][0].isupper():
            loc = line[0]
        else:
            loc = line[0].capitalize()

        color_code = (int(line[5][1:]), int(line[6]), int(line[7][:-1]))
        essentials.append(color_code)

        pixel_cors = (int(line[8]), int(line[9]))
        essentials.append(pixel_cors)

        locs_data[loc] = essentials

# printing
for i, key in enumerate(locs_data, start=1):
    print(key, "---------------", locs_data[key])


# to generate dictionary
with open('locswithcors-dic.txt', 'w+') as f:
    f.write('{')
    count = 1
    for key in locs_data:
        f.write(
            f"{count}: ['{key}', {locs_data[key][0]}, {locs_data[key][1]}],\n")
        count += 1
    f.write('}')
