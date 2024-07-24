import ifcopenshell

def NormalSolarTransmittanceTransformation(ifc_file_path, idf_file_path):

    ifc_file = ifcopenshell.open(ifc_file_path)
    extracted_normal_solar_transmittance = None

    for property in ifc_file.by_type('IfcPropertySingleValue'):
        if property.Name == 'NormalSolarTransmittance':
            extracted_normal_solar_transmittance = property.NominalValue.wrappedValue if property.NominalValue else 'None'
            break

    if extracted_normal_solar_transmittance is None:
        raise ValueError("Failed to extract the Normal Solar Transmittance property value from the IFC file")

    with open(idf_file_path, 'r') as file:
        lines = file.readlines()

    normal_solar_transmittance_line_index = -1
    for i, line in enumerate(lines):
        if "!- Solar Transmittance at Normal Incidence" in line:
            normal_solar_transmittance_line_index = i
            break

    if normal_solar_transmittance_line_index == -1:
        raise ValueError("Failed to find the 'Solar Transmittance at Normal Incidence' line in the IDF file")

    line_parts = lines[normal_solar_transmittance_line_index].split(',')
    if len(line_parts) > 0:
        line_parts[0] = f'{extracted_normal_solar_transmittance}'
        lines[normal_solar_transmittance_line_index] = ','.join(line_parts)

    with open(idf_file_path, 'w') as file:
        file.writelines(lines)

    print("Successfully replaced the normal solar transmittance value in the IDF file")

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
NormalSolarTransmittanceTransformation(ifc_file_path, idf_file_path)
