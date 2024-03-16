# A multi-objective window placement approach using BIM and surrogate model
 
## !!! As the paper is under review, all contents in this repository currently are not allowed to be re-used by anyone until this announcement is deleted.

# 1 Summary of supplemental materials
This table below shows all supplemental materials. All sheets in Tables S1, S2, and S3 are arranged in the order shown in this table.

![image](Image/Inventory%20of%20supplemental%20materials.png)

# 2 General Introduction

2.1 This repository aims at providing the codes and data regarding the paper entitled “……” for the public, and it is developed by University of XXX in UK,  The University of XXX in Hong Kong SAR, and XXX University in China.

2.2 We greatly appreciate the selfless spirits of these voluntary contributors of a series of open python libraries, including ifcopenshell (https://github.com/stefkeB/ifcopenshell_examples), pyautocad (https://github.com/reclosedev/pyautocad), and so on. Our work stands on the shoulders of these giants.

2.3 As for anything regarding the copyright, please refer to the MIT License or contact the authors.
# 3 The time consumption comparison
 
3.1 The EnergyPlus simulation software necessitates 0.46 seconds for a singular WPS simulation, whereas the surrogate model requires only 0.0005 seconds with the same computer configurations when assessing the TEC and UDI of WPSs.
![image](Image/Video%20S1%20Time%20for%20software%20simulation%20to%20process%20one%20WPS%20of%20one%20room.gif)
↑↑↑Time for software simulation to process one WPS of one room

![image](Image/Video%20S2%20Time%20for%20surrogate%20model%20to%20process%20one%20WPS%20of%20one%20room.gif)
↑↑↑Time for surrogate model to process one WPS of one room

3.2 The surrogate model averages 14.79 seconds for the entire WPS optimization process for the case building, while API-based automatic simulation is expected to take up to 12420 seconds (about 3.45 hours) for an equivalent number of WPSs.

![image](Image/Video%20S3%20Time%20for%20deriving%20one%20building-level%20WPS%20using%20surrogate%20model-based%20approach.gif)
↑↑↑Time for deriving one building-level WPS using surrogate model-based approach

# 4 Methodology 
## 4.1 BIM-based WPS-related building information transformation 
The data transformation from BIM’s IFC format to EnergyPlus’s IDF format aims to avoid manually and repeatedly establishing the building model for WPS-conditioned simulations. This process involves three main steps: (i) clarifying the data items related to WPS, (ii) devising the mapping schema between IFC and IDF, and (iii) developing the WPS-oriented IFC2IDF data transformation function library. 


This library includes 18 functions to ensure the transformation of object attributes from IFC  to their counterparts in IDF.


![image](Image/IFC2IDF.png)
↑↑↑Codes for IFC2IDF function library


## 4.2 Surrogate model development for assessing WPS performance

4.2.1 Generate dataset for surrogate model development

The dataset formulation consists of generating WPSs with the grid method and obtaining the energy consumption and natural lighting performance of corresponding WPSs.

![image](Image/Grid-based%20dataset%20generation.png)
↑↑↑Codes for grid-based dataset generation

4.2.2 Train the surrogate model

The training of the surrogate model primarily starts with designing the structure of the deep-learning-based surrogate model. This surrogate model is designed as a multi-layer fully connected network (FCN). It utilizes a WPS at the input layer, producing TEC and UDI as the outputs.

![image](Image/Surrogate%20model%20training.png)
↑↑↑Codes for Surrogate model training
## 4.3 Multi-objective optimization of WPSs
4.3.1 Optimize WPSs multi-objectively by NSGA-II
An algorithm based on NSGA-II has been devised for WPS optimization. The NSGA-II-based WPS multi-objective optimization algorithm is structured into 10 steps. The coordinates of the window’s diagonals and  are skillfully transformed into a four-gene chromosome to represent a WPS.

![image](Image/NSGA-II-based%20WPS%20optimization%20algorithm.png)
↑↑↑Codes for NSGA-II-based WPS optimization algorithm

4.3.2 Write the optimized WPSs into deliverable drawings

In contrast to existing studies that only deliver certain parameters (e.g., WWR), a WPS2Drawing conversion tool has been developed. This tool can transcribe the optimized WPSs into drawings for WPS delivery, recognizing that drawings continue to be the primary medium for conveying design information in real-world engineering projects. The WPS2Drawing process entails defining the coordinate system for the blank drawing, reading the WPSs generated through multi-objective optimization, and transcribing these WPSs into drawings.
![image](Image/WPS2Drawing.png)
↑↑↑Codes for WPS2Drawing