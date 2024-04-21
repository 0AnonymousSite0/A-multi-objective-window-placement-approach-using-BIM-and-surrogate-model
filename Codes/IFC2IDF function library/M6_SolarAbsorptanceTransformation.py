import ifcopenshell

def SolarAbsorptanceTransformation(ifc_file_path, idf_file_path):

    ifc_file = ifcopenshell.open(ifc_file_path)
    extracted_solar_absorptance = None

    for property in ifc_file.by_type('IfcPropertySingleValue'):
        if property.Name == 'SolarAbsorptance':
            extracted_solar_absorptance = property.NominalValue.wrappedValue if property.NominalValue else 'None'
            break

    if extracted_solar_absorptance is None:
        raise ValueError("Failed to extract the Solar Absorptance property value from the IFC file")
    with open(idf_file_path, 'r') as file:
        lines = file.readlines()

    solar_absorptance_line_index = -1
    for i, line in enumerate(lines):
        if "!- Solar Absorptance" in line:
            solar_absorptance_line_index = i
            break
    if solar_absorptance_line_index == -1:
        raise ValueError("Failed to find the 'Solar Absorptance' line in the IDF file")

    line_parts = lines[solar_absorptance_line_index].split(',')
    if len(line_parts) > 0:
        line_parts[0] = f'{extracted_solar_absorptance}'
        lines[solar_absorptance_line_index] = ','.join(line_parts)

    with open(idf_file_path, 'w') as file:
        file.writelines(lines)

    print("Successfully replaced the solar absorptance value in the IDF file")

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
SolarAbsorptanceTransformation(ifc_file_path, idf_file_path)
