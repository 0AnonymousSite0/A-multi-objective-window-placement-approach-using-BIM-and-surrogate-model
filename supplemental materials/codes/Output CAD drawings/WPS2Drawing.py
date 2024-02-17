from pyautocad import Autocad, APoint


def draw_rectangle(diagonal_point1, diagonal_point2):
    acad = Autocad(create_if_not_exists=True)
    acad.prompt("Drawing a rectangle in AutoCAD using Python")

    p1 = APoint(diagonal_point1[0], diagonal_point1[1])
    p2 = APoint(diagonal_point2[0], diagonal_point1[1])
    p3 = APoint(diagonal_point2[0], diagonal_point2[1])
    p4 = APoint(diagonal_point1[0], diagonal_point2[1])

    acad.model.AddLine(p1, p2)
    acad.model.AddLine(p2, p3)
    acad.model.AddLine(p3, p4)
    acad.model.AddLine(p4, p1)


def read_rectangles_from_file(file_path):
    rectangles = []
    with open(file_path, 'r') as file:
        for line in file:
            points = line.strip().split(';')
            point1 = tuple(map(float, points[0].split(',')))
            point2 = tuple(map(float, points[1].split(',')))
            rectangles.append((point1, point2))
    return rectangles


if __name__ == "__main__":
    file_path = 'the file path to the rectangles data'  
    rectangles = read_rectangles_from_file(file_path)

    for diagonal_points in rectangles:
        draw_rectangle(diagonal_points[0], diagonal_points[1])
