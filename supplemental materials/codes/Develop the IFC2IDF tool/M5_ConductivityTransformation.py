import ifcopenshell

def ConductivityTransformation(ifc_file_path, idf_file_path):

    ifc_file = ifcopenshell.open(ifc_file_path)
    extracted_conductivity = None

    for property in ifc_file.by_type('IfcPropertySingleValue'):
        if property.Name == 'Conductivity':
            extracted_conductivity = property.NominalValue.wrappedValue if property.NominalValue else 'None'
            break

    if extracted_conductivity is None:
        raise ValueError("Failed to extract the Conductivity property value from the IFC file")

    with open(idf_file_path, 'r') as file:
        lines = file.readlines()

    conductivity_line_index = -1
    for i, line in enumerate(lines):
        if "!- Conductivity {W/m-K}" in line:
            conductivity_line_index = i
            break

    if conductivity_line_index == -1:
        raise ValueError("Failed to find the 'Conductivity' line in the IDF file")

    line_parts = lines[conductivity_line_index].split(',')
    if len(line_parts) > 1:
        line_parts[0] = f'{extracted_conductivity}'
        lines[conductivity_line_index] = ','.join(line_parts)

    with open(idf_file_path, 'w') as file:
        file.writelines(lines)

    print("Successfully replaced the conductivity value in the IDF file")

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
ConductivityTransformation(ifc_file_path, idf_file_path)
