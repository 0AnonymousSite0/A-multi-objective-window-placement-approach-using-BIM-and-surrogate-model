import ifcopenshell

def extract_property_value_from_ifc(ifc_file_path, property_name):
    ifc_file = ifcopenshell.open(ifc_file_path)
    property_sets = ifc_file.by_type("IfcPropertySet")
    for property_set in property_sets:
        for property in property_set.HasProperties:
            if property.Name == property_name and property.is_a("IfcPropertySingleValue"):
                return property.NominalValue.wrappedValue
    return None


def replace_value_in_idf_near_marker(idf_file_path, marker, lines_below_marker, new_value):
    with open(idf_file_path, 'r') as file:
        lines = file.readlines()

    marker_line_index = None
    for i, line in enumerate(lines):
        if marker in line:
            marker_line_index = i + lines_below_marker
            break

    if marker_line_index is not None and marker_line_index < len(lines):
        line_content = lines[marker_line_index]
        parts = line_content.split(',')
        if len(parts) > 0:
            parts[0] = f"    {new_value}"
            lines[marker_line_index] = ','.join(parts)

        with open(idf_file_path, 'w') as file:
            file.writelines(lines)
        print(f"Value replaced with {new_value} in IDF file.")
    else:
        print("Marker not found or not enough lines below marker.")


def LightsPowerDensityTransformation(ifc_file_path, idf_file_path):
    property_name = "LightsPowerDensity"
    property_value = extract_property_value_from_ifc(ifc_file_path, property_name)

    if property_value is not None:
        replace_value_in_idf_near_marker(idf_file_path, "Lights", 6, property_value)
    else:
        print("Property not found in IFC file.")

ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
LightsPowerDensityTransformation(ifc_file_path, idf_file_path)
