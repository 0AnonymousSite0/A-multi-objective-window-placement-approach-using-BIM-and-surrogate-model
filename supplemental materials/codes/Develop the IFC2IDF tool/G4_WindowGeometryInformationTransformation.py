import ifcopenshell
import numpy as np

def get_transformation_matrix(placement):
    matrix = np.eye(4)
    if hasattr(placement, 'PlacementRelTo') and placement.PlacementRelTo:
        matrix = np.dot(matrix, get_transformation_matrix(placement.PlacementRelTo))
    if hasattr(placement, 'RelativePlacement') and placement.RelativePlacement:
        rel_placement = placement.RelativePlacement
        if hasattr(rel_placement, 'Location') and rel_placement.Location:
            for i, coord in enumerate(rel_placement.Location.Coordinates):
                matrix[i, 3] = coord
    return matrix

def transform_point(point, transformation_matrix):
    homogeneous_point = np.ones(4)
    homogeneous_point[:3] = point
    transformed_point = transformation_matrix.dot(homogeneous_point)
    return transformed_point[:3]

def get_window_vertices(window):
    if not window.Representation or not window.ObjectPlacement:
        return []
    local_placement_matrix = get_transformation_matrix(window.ObjectPlacement)
    vertices = []
    for representation in window.Representation.Representations:
        if representation.RepresentationType == 'SweptSolid':
            for solid in representation.Items:
                if solid.is_a('IfcExtrudedAreaSolid'):
                    profile = solid.SweptArea
                    if profile.is_a('IfcRectangleProfileDef'):
                        width = profile.XDim / 2
                        height = profile.YDim / 2
                        depth = solid.Depth / 2
                        for dx in [-width, width]:
                            for dy in [-height, height]:
                                point = np.array([dx, dy, depth])
                                transformed_point = transform_point(point, local_placement_matrix)
                                vertices.append(transformed_point.tolist())
    return vertices

def update_window_in_idf_v2(idf_path, window_vertices):
    with open(idf_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        updated_lines.append(line)
        if "FenestrationSurface:Detailed" in line:
            while "!- Vertex 1 X-coordinate {m}" not in lines[i]:
                i += 1
                updated_lines.append(lines[i])
            for vertex in window_vertices:
                x, y, z = vertex
                vertex_line_x = f"    {x}, !- Vertex X-coordinate {{m}}\n"
                updated_lines.append(vertex_line_x)
                i += 1
                updated_lines.append(lines[i])
                i += 1
                updated_lines.append(lines[i])
        i += 1

    with open(idf_path, 'w') as file:
        file.writelines(updated_lines)

def WindowGeometryInformationTransformation(ifc_file_path, idf_file_path):
    file = ifcopenshell.open(ifc_file_path)
    windows = file.by_type('IfcWindow')
    for window in windows:
        vertices = get_window_vertices(window)
        update_window_in_idf_v2(idf_file_path, vertices)

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
WindowGeometryInformationTransformation(ifc_file_path, idf_file_path)
