import ifcopenshell

def MaterialNameTransformation(ifc_file_path, idf_file_path):
  
    ifc_file = ifcopenshell.open(ifc_file_path)
    extracted_name = None

    for property in ifc_file.by_type('IfcPropertySingleValue'):
        if property.Name == 'Name':
            extracted_name = property.NominalValue.wrappedValue if property.NominalValue else 'None'
            break

    if extracted_name is None:
        raise ValueError("Failed to extract the Name property value from the IFC file")

    with open(idf_file_path, 'r') as file:
        lines = file.readlines()

    material_index = None
    for i, line in enumerate(lines):
        if "Material" in line:
            material_index = i + 1
            break

    if material_index is None or material_index >= len(lines):
        raise ValueError("Failed to find the 'Material' keyword or its subsequent line for replacement")

    line_parts = lines[material_index].split(',')
    if len(line_parts) > 0:
        line_parts[0] = extracted_name
        lines[material_index] = ','.join(line_parts)

    with open(idf_file_path, 'w') as file:
        file.writelines(lines)

    print("Successfully replaced the name value in the IDF file based on 'Material' location")

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
MaterialNameTransformation(ifc_file_path, idf_file_path)
