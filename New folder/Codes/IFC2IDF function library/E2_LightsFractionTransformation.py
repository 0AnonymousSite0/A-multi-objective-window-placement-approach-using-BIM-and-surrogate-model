import ifcopenshell

def LightsFractionTransformation(ifc_file_path, idf_file_path):
    def extract_property_value_from_ifc(ifc_file_path, property_name):
        ifc_file = ifcopenshell.open(ifc_file_path)
        extracted_value = None
        property_sets = ifc_file.by_type("IfcPropertySet")
        for property_set in property_sets:
            for property in property_set.HasProperties:
                if property.Name == property_name and property.is_a("IfcPropertySingleValue"):
                    extracted_value = property.NominalValue.wrappedValue if property.NominalValue else None
                    return extracted_value
        return None

    def replace_value_in_idf_near_marker(idf_file_path, marker, lines_below_marker, new_value):
        with open(idf_file_path, 'r') as file:
            lines = file.readlines()

        marker_index = None
        for i, line in enumerate(lines):
            if marker in line:
                marker_index = i + lines_below_marker
                break

        if marker_index is not None and marker_index < len(lines):
            line_parts = lines[marker_index].split(',')
            if len(line_parts) > 0:
                line_parts[0] = f"    {new_value}"
                lines[marker_index] = ','.join(line_parts)

            with open(idf_file_path, 'w') as file:
                file.writelines(lines)
            print(f"Successfully replaced the value with {new_value} near the marker '{marker}'.")
        else:
            print("Marker not found or insufficient lines below marker.")

    property_name = "LightsFraction"
    property_value = extract_property_value_from_ifc(ifc_file_path, property_name)

    if property_value is not None:
        # Assuming we want to replace the value 9 lines below the "Lights" marker
        replace_value_in_idf_near_marker(idf_file_path, "Lights", 9, property_value)
    else:
        print("Property not found in IFC file.")


ifc_file_path = r'path of ifc file'
idf_file_path = r'path of idf file'
LightsFractionTransformation(ifc_file_path, idf_file_path)
