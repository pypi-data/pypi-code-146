import PIL.Image as PIL

_tiletag = "___tile-"

def partition(annotations: list, size: int, margin: float, input_path: str, output_path: str) -> list:
    """
    Uses `annotations` to divide the images referenced by the filename field into tiles that are roughly the square of `size`, having `margin` as a tolerance to defining the slicing lines. Bounding boxes for the annotations will be corrected. For bounding boxes that get sliced, ends will remain that are >=50%, and otherwise they will be discarded. 
        `annotations`: A list of dicts defining the objects in the images. Can be created by the reader function(s).
        `size`: The approximate target size for the tiles as the square root of the number of pixels, so for example 1024 for images roughly a square of 1024 by 1024. It will allow slightly larger tiles, but will attempt to avoid making smaller tiles.
        `margin`: The number of pixels as a fraction of `size` that the slice line may move to become less destructive.
        `input_path`: The path to the location of the input images.
        `output_path`: The path to the destination of the output images (tiles). 
    Returns: The annotations with corrected bounding boxes for the tiles.
    """
    import os
    result = []
    line_margin = int(size * margin)
    filenames = []
    for obj in annotations:
        filename = obj["filename"]
        if not filename in filenames:
            filenames.append(filename)
    for filename in filenames:
        objects = [x for x in annotations if x["filename"] == filename]
        width, height = objects[0]["width"], objects[0]["height"]
        image = PIL.open(os.path.join(input_path, filename))
        filename, fileext = os.path.splitext(filename)
        vertical_num = int(width / size)
        vertical_size = int(width / vertical_num)
        num_vertical_lines = vertical_num -1
        vertical_lines = []
        for i in range(1, num_vertical_lines +1):
            line = i * vertical_size
            line = _get_slice_line(line, line_margin, objects, "xmin", "xmax")
            vertical_lines.append(line)
        vertical_lines.append(width)
        horizontal_num = int(height / size)
        horizontal_size = int(height / horizontal_num)
        num_horizontal_lines = horizontal_num -1
        horizontal_lines = []
        for i in range(1, num_horizontal_lines +1):
            line = i * horizontal_size
            line = _get_slice_line(line, line_margin, objects, "ymin", "ymax")
            horizontal_lines.append(line)
        horizontal_lines.append(height)  
        prev_v = 0
        prev_h = 0
        row = 0
        for h in horizontal_lines:
            number = 0
            row = row + 1
            for v in vertical_lines:
                number = number +1
                new_filename = filename + _tiletag + _get_row_letter(row) + str(number) + fileext
                for obj in [x for x in objects if (x["xmin"] < v and x["xmin"] > prev_v and x["ymin"] < h and x["ymin"] > prev_h) or (x["xmax"] < v and x["xmax"] > prev_v and x["ymax"] < h and x["ymax"] > prev_h)]:
                    # Fixing sliced bounding boxes.
                    if obj["xmin"] < prev_v and obj["xmax"] > prev_v:
                        if obj["xmax"] - prev_v > int((obj["xmax"] - obj["xmin"])/2):
                            obj["xmin"] = prev_v
                        else:
                            continue
                    if obj["xmin"] < v and obj["xmax"] > v:
                        if v - obj["xmin"] > int((obj["xmax"] - obj["xmin"])/2):
                            obj["xmax"] = v
                        else:
                            continue
                    if obj["ymin"] < prev_h and obj["ymax"] > prev_h:
                        if obj["ymax"] - prev_h > int((obj["ymax"] - obj["ymin"])/2):
                            obj["ymin"] = prev_h
                        else:
                            continue
                    if obj["ymin"] < h and obj["ymax"] > h:
                        if h - obj["ymin"] > int((obj["ymax"] - obj["ymin"])/2):
                            obj["ymax"] = h
                        else:
                            continue
                    # Adjust bounding boxes.
                    obj["filename"] = new_filename
                    obj["width"] = v - prev_v
                    obj["height"] = h - prev_h
                    obj_w = obj["xmax"] - obj["xmin"]
                    obj_h = obj["ymax"] - obj["ymin"]
                    obj["xmin"] = obj["xmin"] - prev_v
                    obj["ymin"] = obj["ymin"] - prev_h
                    obj["xmax"] = obj["xmin"] + obj_w
                    obj["ymax"] = obj["ymin"] + obj_h
                    result.append(obj)
                tile = image.crop((prev_v, prev_h, v, h))
                tile.save(os.path.join(output_path, new_filename))
                prev_v = v
            prev_h = h
            prev_v = 0
    return result

def _get_slice_line(mid, margin, objects, min_index, max_index):
    if margin == 0:
        return mid
    results = dict()
    for d in range(margin):
        for delta in {d, d*-1}:
            line = mid + delta
            count = sum([1 for obj in objects if (obj[min_index] < line and obj[max_index] >= line)])
            if count == 0: # Return if a 'perfect' line is found.
                return line
            results[line] = count
    return min(zip(results.values(), results.keys()))[1] # Return the line with the least sliced objects.

def _get_row_letter(row): 
    return str(chr(ord('`')+row))

def split(annotations: list, size: int, input_path: str, output_path: str) -> list:
    """
    Uses `annotations` to divide the images referenced by the filename field into tiles that are roughly the square of `size`. Bounding boxes for the annotations will be corrected. For bounding boxes that get sliced, ends will remain that are >=50%, and otherwise they will be discarded. 
        `annotations`: A list of dicts defining the objects in the images. Can be created by the reader function(s).
        `size`: The approximate target size for the tiles as the square root of the number of pixels, so for example 1024 for images roughly a square of 1024 by 1024. It will allow slightly larger tiles, but will attempt to avoid making smaller tiles.
        `input_path`: The path to the location of the input images.
        `output_path`: The path to the destination of the output images (tiles). 
    Returns: The annotations with corrected bounding boxes for the tiles.
    """
    return partition(annotations, size, 0, input_path, output_path)

def collect(path: str, image_path: str) -> tuple:
    """
    Collects a list of PIL.Image (tiles) from `path`, for a the given original image at `image_path`.
        `path`: The path where the tiles are to be found.
        `image_path`: The path to the original image the tiles where made from.
    Returns: a list of PIL.Image containing the tiles, the number of rows, the number of columns, the widths of the columns, the heights of the columns.
    """
    import glob
    import os
    columns = 0
    image_name, ext = os.path.splitext(os.path.basename(image_path))
    files = glob.glob(os.path.join(path, image_name + _tiletag + "*"))
    for f in files:
        if f[f.find(_tiletag)+len(_tiletag):][0] == "a":
            columns += 1
        else:
            continue
    rows = int(len(files) / columns)
    ratios_w, ratios_h, images = [], [], []
    for row in range(rows):
        row += 1
        for col in range(columns):
            col += 1
            img = PIL.open(os.path.join(path, image_name + _tiletag + _get_row_letter(row) + str(col) + ext))
            if len(ratios_w) < columns:
                ratios_w.append(img.width)
            if col == 0 or col % columns == 0:
                ratios_h.append(img.height)
            images.append(img)
    return images, rows, columns, ratios_w, ratios_h

def stitch(tiles: list, row_length: int) -> PIL:
    """
    Merges the list of PIL.Images `tiles` back into 1 large image.
        `tiles`: A list of PIL.Images that are the tiles.
        `row_length`: The number of tiles per row in the resulting image.
    Returns: A PIL.Image
    """
    width = 0
    for i in range(row_length):
        (w, h) = tiles[i].size
        width += w
    height = 0
    for i in range(int(len(tiles)/row_length)):
        (w, h) = tiles[i * row_length].size
        height += h
    result = PIL.new("RGB", (width, height), "black")
    count, x, y = 0, 0, 0
    for i in range(len(tiles)):
        image = tiles[i]
        result.paste(image, (x, y))
        count += 1
        (w, h) = image.size
        x += w
        if count == row_length:
            count = 0
            x = 0
            y += h
    return result

def split_single(image_path: str, size: int) -> tuple:
    """
    Divides the image at `image_path` into a number of equally large tiles of roughly the size specified by `size`.
        `image_path` The path to the image to split.
        `size`: The approximate target size for the tiles as the square root of the number of pixels, so for example 1024 for tiles roughly a square of 1024 by 1024. It will allow slightly larger tiles.
    Returns: A list of PIL.Image (tiles), the number of rows, the number columns.
    """
    image = PIL.open(image_path)
    (width, height) = image.size
    vertical_num = int(width / size)
    vertical_size = int(width / vertical_num)
    num_vertical_lines = vertical_num -1
    vertical_lines = []
    for i in range(1, num_vertical_lines +1):
        line = i * vertical_size
        vertical_lines.append(line)
    vertical_lines.append(width)

    horizontal_num = int(height / size)
    horizontal_size = int(height / horizontal_num)
    num_horizontal_lines = horizontal_num -1
    horizontal_lines = []
    for i in range(1, num_horizontal_lines +1):
        line = i * horizontal_size
        horizontal_lines.append(line)
    horizontal_lines.append(height)
    prev_v = 0
    prev_h = 0
    row = 0
    images = []
    for h in horizontal_lines:
        number = 0
        row = row + 1
        for v in vertical_lines:
            number = number +1
            new_image = image.crop((prev_v, prev_h, v, h))
            images.append(new_image)
            prev_v = v
        prev_h = h
        prev_v = 0
    return images, len(horizontal_lines) , len(vertical_lines)