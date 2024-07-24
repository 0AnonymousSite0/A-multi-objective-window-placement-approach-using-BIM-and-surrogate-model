import ifcopenshell

def ThicknessTransformation(ifc_file_path, idf_file_path):

    ifc_file = ifcopenshell.open(ifc_file_path)
    extracted_thickness = None

    for property in ifc_file.by_type('IfcPropertySingleValue'):
        if property.Name == 'Thickness':
            extracted_thickness = property.NominalValue.wrappedValue if property.NominalValue else 'None'
            break

    if extracted_thickness is None:
        raise ValueError("Failed to extract the Thickness property value from the IFC file")

    with open(idf_file_path, 'r') as file:
        lines = file.readlines()

    thickness_line_index = -1
    for i, line in enumerate(lines):
        if "!- Thickness {m}" in line:
            thickness_line_index = i
            break

    if thickness_line_index == -1:
        raise ValueError("Failed to find the 'Thickness' line in the IDF file")

    line_parts = lines[thickness_line_index].split(',')
    if len(line_parts) > 1:
        line_parts[1] = f' {extracted_thickness}'
        lines[thickness_line_index] = ','.join(line_parts)

    with open(idf_file_path, 'w') as file:
        file.writelines(lines)

    print("Successfully replaced the thickness value in the IDF file")

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
ThicknessTransformation(ifc_file_path, idf_file_path)
