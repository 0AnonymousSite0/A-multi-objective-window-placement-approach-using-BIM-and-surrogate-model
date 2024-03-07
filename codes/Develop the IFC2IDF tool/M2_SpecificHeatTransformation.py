import ifcopenshell

def SpecificHeatTransformation(ifc_file_path, idf_file_path):
    ifc_file = ifcopenshell.open(ifc_file_path)
    extracted_specific_heat = None

    for property in ifc_file.by_type('IfcPropertySingleValue'):
        if property.Name == 'SpecificHeat':
            extracted_specific_heat = property.NominalValue.wrappedValue if property.NominalValue else 'None'
            break
    if extracted_specific_heat is None:
        raise ValueError("Failed to extract the Specific Heat property value from the IFC file")

    with open(idf_file_path, 'r') as file:
        lines = file.readlines()

    specific_heat_line_index = -1
    for i, line in enumerate(lines):
        if "!- Specific Heat {J/kg-K}" in line:
            specific_heat_line_index = i
            break

    if specific_heat_line_index == -1:
        raise ValueError("Failed to find the 'Specific Heat' line in the IDF file")

    line_parts = lines[specific_heat_line_index].split(',')
    if len(line_parts) > 0:
        line_parts[0] = f'{extracted_specific_heat}'
        lines[specific_heat_line_index] = ','.join(line_parts)

    with open(idf_file_path, 'w') as file:
        file.writelines(lines)

    print("Successfully replaced the specific heat value in the IDF file")

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
SpecificHeatTransformation(ifc_file_path, idf_file_path)
