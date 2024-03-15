import sys

sys.path.insert(0, 'EnergyPlus_path')
import re
import numpy
import pandas as pd
from pyenergyplus.api import EnergyPlusAPI


class Final_House:
    def environment_handler(self, _state) -> None:
        print("OH HAI ENVIRONMENT")
        sys.stdout.flush()

    def progress_handler(self, progress: int) -> None:
        if 49 < progress < 51:
            print("HALFWAY THERE!!")
            sys.stdout.flush()

    def error_handler(self, severity: int, message: bytes) -> None:
        if b'Warning' in message:
            print("GOT A WARNING UH OH!")
            sys.stdout.flush()

    def process(self, start, end):
        filename_to_run = 'idf_file_path'
        output_path = "./"
        self.window_param = []

        self.total_lighting = pd.DataFrame()
        lines = []
        with open('idf_file_path', 'r') as f:
            for line in f:
                lines.append(line)

        a = 0
        index = 0
        # Iterate over each line in the file to find the line containing the identifier 'Aperture_e627b0ed'
        # This identifier marks the beginning of a window definition
        for Aperture_ in lines:
            IDF = re.search('Aperture_e627b0ed', Aperture_)
            index += 1
            if IDF is not None:
                break
        # Iterate through a set of predefined combinations of window positions and dimensions
        for positiony in numpy.round(numpy.arange(start, end, 0.2), 2):
            for positionz in numpy.round(numpy.arange(19.7, 20.2, 0.2), 2):
                for windoww in numpy.round(numpy.arange(1.2, 4.0, 0.3), 2):
                    for windowh in numpy.round(numpy.arange(0.9, 1.3, 0.1), 2):
                        print(positiony)
                        # Calculate the vertex coordinates based on the window position and dimensions, and convert them to strings
                        vertex1 = str(round(positiony + windoww, 2))
                        vertex2 = str(round(positionz + windowh, 2))
                        vertex3 = str(round(positiony, 2))
                        vertex4 = str(round(positionz, 2))
                        # Update the lines in the IDF file that correspond to the window's vertex coordinates
                        lines[index + 9] = "    " + str(
                            round(positiony + windoww, 2)) + ",                     !- Vertex 1 Y-coordinate {m}\n"
                        lines[index + 10] = "    " + str(
                            round(positionz + windowh, 2)) + ",                     !- Vertex 1 Z-coordinate {m}\n"
                        lines[index + 12] = "    " + str(
                            round(positiony + windoww, 2)) + ",                     !- Vertex 2 Y-coordinate {m}\n"
                        lines[index + 13] = "    " + str(
                            round(positionz, 2)) + ",                     !- Vertex 2 Z-coordinate {m}\n"
                        lines[index + 15] = "    " + str(
                            round(positiony, 2)) + ",                     !- Vertex 3 Y-coordinate {m}\n"
                        lines[index + 16] = "    " + str(
                            round(positionz, 2)) + ",                     !- Vertex 3 Z-coordinate {m}\n"
                        lines[index + 18] = "    " + str(
                            round(positiony, 2)) + ",                     !- Vertex 4 Y-coordinate {m}\n"
                        lines[index + 19] = "    " + str(
                            round(positionz + windowh, 2)) + ";                     !- Vertex 4 Z-coordinate {m}\n"
                        # Calculate the window area
                        window_area = float(windowh) * float(windoww)
                        # Write the modified content back to the IDF file for simulation
                        with open('idf_file_path', 'w') as f:
                            for line in lines:
                                f.write(line)


                        api = EnergyPlusAPI()
                        state = api.state_manager.new_state()

                        api.runtime.callback_begin_new_environment(
                            state, self.environment_handler)
                        api.runtime.callback_progress(state, self.progress_handler)
                        api.functional.callback_error(state, self.error_handler)
                        # Define the path to the weather file
                        weather = r'weather_file_path'
                        argvList = [
                            '-w', weather,
                            '-d', 'out',
                            filename_to_run]
                        api.runtime.run_energyplus(state, argvList)

                        # Read the simulation output file
                        f = open("eso_file_path", "r", encoding="utf-8")
                        eso = f.readlines()
                        f.close()

                        illuminance = []

                        for line in eso:

                            if line.startswith("201") and "[" not in line:
                                illuminance.append(float(line.strip().split(",")[1]))

                            elif line.startswith("202") and "[" not in line:
                                illuminance.append(float(line.strip().split(",")[1]))
                            elif line.startswith("287") and "[" not in line:
                                illuminance.append(float(line.strip().split(",")[1]))


                        window = (vertex1, vertex2, vertex3, vertex4, window_area)
                        self.window_param.append(window)


                        print("aa has {} items.".format(len(self.window_param)))
                        print("=================")

                        a += 1
                        data = {'right_point_illu' + str(a): illuminance}
                        self.lighting = pd.DataFrame(data)
                        # Merge the current data DataFrame with the previous aggregate data
                        result = pd.concat([self.total_lighting, self.lighting], axis=1)
                        self.total_lighting = pd.concat([self.total_lighting, self.lighting], axis=1)


    def deal(self, a):
        data = self.window_param
        df1 = pd.DataFrame(
            data, columns=['x1', 'x2', 'x3', 'x4', 'window_area'], dtype=float)
        df1.to_excel("46ROOMwindowdesign" + a + ".xlsx", index=False)
        self.total_lighting.to_excel("46ROOMDaylightingANDenergy" + a + ".xlsx", index=False)


if __name__ == '__main__':
    import sys

    args = sys.argv
    start = round(float(args[1]), 2)
    end = round(start + 0.19, 2)
    print(start)
    print(end)
    house = Final_House()
    house.process(start, end)
    house.deal(str(start))
