import ifcopenshell

def get_wall_dimensions(shape):
    for representation in shape.Representations:
        if representation.RepresentationType == 'SweptSolid':
            for solid in representation.Items:
                if solid.is_a('IfcExtrudedAreaSolid'):
                    length = solid.Depth
                    profile = solid.SweptArea
                    if profile.is_a('IfcRectangleProfileDef'):
                        width = profile.XDim
                        height = profile.YDim
                        return length, width, height
    return None, None, None

def extract_coordinates(placement):
    if placement is None:
        return 'No location'
    if hasattr(placement, 'Location'):
        return placement.Location.Coordinates
    if hasattr(placement, 'RelativePlacement'):
        return extract_coordinates(placement.RelativePlacement)
    if hasattr(placement, 'PlacementRelTo'):
        return extract_coordinates(placement.PlacementRelTo)
    return 'Unknown location structure'

def update_vertex_in_idf(idf_path, coordinates):
    with open(idf_path, 'r') as file:
        lines = file.readlines()

    vertex_markers = [
        "!- Vertex 3 X-coordinate {m}",
        "!- Vertex 2 X-coordinate {m}",
        "!- Vertex 1 X-coordinate {m}",
        "!- Vertex 4 X-coordinate {m}"
    ]

    for i, line in enumerate(lines):
        if 'RoofName' in line:
            for marker in vertex_markers:
                for j in range(i+1, len(lines)):
                    if marker in lines[j]:
                        x, y, z = coordinates[vertex_markers.index(marker)]
                        lines[j] = '    ' + str(x) + ',                       !- Vertex X-coordinate {m}\n'
                        lines[j+1] = '    ' + str(y) + ',                       !- Vertex Y-coordinate {m}\n'
                        lines[j+2] = '    ' + str(z) + ',                       !- Vertex Z-coordinate {m}\n'
                        break

    with open(idf_path, 'w') as file:
        file.writelines(lines)

def RoofGeometryInformationTransformation(ifc_file_path, idf_file_path):
    file = ifcopenshell.open(ifc_file_path)
    roofs = file.by_type('IfcRoof')

    for roof in roofs:
        global_id = roof.GlobalId
        name = roof.Name if roof.Name else 'Unnamed'
        placement = roof.ObjectPlacement
        coordinates = extract_coordinates(placement)
        shape = roof.Representation
        length, width, height = get_wall_dimensions(shape) if shape else (None, None, None)
        print(f'Roof ID: {global_id}, Name: {name}, Location: {coordinates}, Dimensions: {length}x{width}x{height}')

    example_coordinates = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
    update_vertex_in_idf(idf_file_path, example_coordinates)

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
RoofGeometryInformationTransformation(ifc_file_path, idf_file_path)
