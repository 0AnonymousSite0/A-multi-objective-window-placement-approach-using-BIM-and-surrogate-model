import ifcopenshell

def ThermalAbsorptanceTransformation(ifc_file_path, idf_file_path):
    ifc_file = ifcopenshell.open(ifc_file_path)
    extracted_thermal_absorptance = None

    for property in ifc_file.by_type('IfcPropertySingleValue'):
        if property.Name == 'ThermalAbsorptance':
            extracted_thermal_absorptance = property.NominalValue.wrappedValue if property.NominalValue else 'None'
            break

    if extracted_thermal_absorptance is None:
        raise ValueError("Failed to extract the Thermal Absorptance property value from the IFC file")

    with open(idf_file_path, 'r') as file:
        lines = file.readlines()

    thermal_absorptance_line_index = -1
    for i, line in enumerate(lines):
        if "!- Thermal Absorptance" in line:
            thermal_absorptance_line_index = i
            break

    if thermal_absorptance_line_index == -1:
        raise ValueError("Failed to find the 'Thermal Absorptance' line in the IDF file")

    line_parts = lines[thermal_absorptance_line_index].split(',')
    if len(line_parts) > 0:
        line_parts[0] = f'{extracted_thermal_absorptance}'
        lines[thermal_absorptance_line_index] = ','.join(line_parts)

    with open(idf_file_path, 'w') as file:
        file.writelines(lines)

    print("Successfully replaced the thermal absorptance value in the IDF file")

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
ThermalAbsorptanceTransformation(ifc_file_path, idf_file_path)
