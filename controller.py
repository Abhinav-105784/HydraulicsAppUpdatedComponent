import viktor as vkt
from viktor import ViktorController
from viktor.views import DataGroup, DataItem,DataResult, DataView, PlotlyResult, PlotlyView, TableResult, TableView, PDFView, PDFResult
from viktor import DownloadResult
from viktor.parametrization import ViktorParametrization, ActionButton, And, BooleanField, DownloadButton, DynamicArray,DynamicArrayConstraint, FunctionLookup, HiddenField, Image, IsEqual, IsFalse, IsTrue, LineBreak, Lookup, MultiFileField,NumberField,OptionField,Or, Page, RowLookup, Section, Tab, Table, Text,TextField
import copy
import plotly.graph_objects as go
import math as math
import pandas as pd
from datetime import date as date
from pathlib import Path

from ..Information import hydraulics as hydraulics
from ..my_folder import instanceController as instance
from ..my_folder import Dataframe as dfd

components = [
    'Known Water Conditions',
    'Sharp Edged Orifice Passage',
    'General Submerged Constriction',
    'Circular Critical Depth'

]
######## Sharp Edged Orifice passage
is_sharpEdged_Orifice = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage'))
is_sharp_Edged_Circular_Orifice = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.orifice_shape'),'Circular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
is_sharp_Edged_Rectangular_Orifice = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.orifice_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
is_circular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.pipe_shape'),'Circular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
is_Rectangular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.pipe_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
# is_sharp_Edged_Rectangular_Orifice = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual,(Lookup('$.orifice_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
# is_Circular_Orifice_in_Rectangular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'Sharp Edged Circular Orifice and Rectangular Pipe Passage'))
# is_Rectangular_Orifice_in_Circular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'Sharp Edged Rectangular Orifice and Circular Pipe Passage'))

is_CriticalDepth_Circular = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'Circular Critical Depth'))
# is_Circular_orifice = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.orifice_shape'),'Circular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
# is_Rectangular_orifice = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.orifice_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
# is_Circular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.pipe_shape'),'Circular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
# is_Rectangular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.pipe_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
###### General Submerged Constricts
is_General_Submerged_Constrict = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'General Submerged Constriction'))
_is_known_water_conditions = DynamicArrayConstraint('calc_page.tab_1.array', IsEqual(Lookup('$row.component'), 'Known Water Conditions'))
is_Circular_upstream_Constrict = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.upstream_section_shape'),'Circular'),IsEqual(Lookup('$row.component'),'General Submerged Constriction')))
is_Circular_downstream_Constrict = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.downstream_section_shape'),'Circular'),IsEqual(Lookup('$row.component'),'General Submerged Constriction')))
is_Circular_orifice_Constrict = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.Orifice_shape'),'Circular'),IsEqual(Lookup('$row.component'),'General Submerged Constriction')))
is_Retangular_upstream_Constrict = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.upstream_section_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'General Submerged Constriction')))
is_Rectangular_downstream_Constrict = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.downstream_section_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'General Submerged Constriction')))
is_Rectangular_orifice_Constrict = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.Orifice_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'General Submerged Constriction')))

class Parametrization(ViktorParametrization):
    cover_page = Page('COVER PAGE')
    cover_page.logo = Image(path="Primary Logo 1 Full Color RGB HighRes.jpg",align="left",flex=20)
    cover_page.text = Text("""
### Welcome to the Hydraulic Calculations App
This app allows you to perform 1-dimensional hydraulic modelling for a variety of components in a network.
                           
#### Warning
                           
Please note that this app is in development.
All calculations must be verified by another means.
If you find an error, please report it to the developer.
                           
#### App development record
                           
Please refer to the App development record for current version status and information.

#### Instructions

1. Enter the flow rate in the 'Hydraulic Model Inputs' tab.
2. Add components to the array in the 'Hydraulic Model Inputs' tab.
3. Select the component type from the dropdown list.
4. Fill in the required fields for the selected component.
5. Click 'Download Calculations' to download the results as a CSV file.
                           
#### Components

Please see below documentation for the components available in the app.
""")
    
    calc_page = Page('Hydraulic Calculations', views= ["table_view"])
    calc_page.tab_1 = Tab('Hydraulic Model Inputs')
    calc_page.tab_1.flow_rate =NumberField('Flow rate', suffix= 'm³/s', default=1)
    calc_page.tab_1.download_calculations = DownloadButton('Download Calculations', method = "download_calculations")
    calc_page.tab_1.array = DynamicArray('Hydraulic Components')
    calc_page.tab_1.array.component = OptionField('component', options=components)
    calc_page.tab_1.array.lb1 = LineBreak()
    calc_page.tab_1.array.orifice_shape = OptionField('Orifice Shape', visible= is_sharpEdged_Orifice,options= ['Circular','Rectangular'], default='Circular')
    calc_page.tab_1.array.orifice_diametre = NumberField('Orifice Diametre', suffix= 'm', visible=is_sharp_Edged_Circular_Orifice,default= None)
    calc_page.tab_1.array.orifice_width1 = NumberField('orifice Width', suffix= 'm',default= None, visible= is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.array.orifice_height1 = NumberField('orifice Height', suffix='m', default= None, visible=is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.array.pipe_shape = OptionField('Pipe Shape',visible=is_sharpEdged_Orifice,options=['Circular','Rectangular'],default='Circular')
    calc_page.tab_1.array.pipe_diametre = NumberField('Pipe Diametre',suffix='m',default= None,visible=is_circular_Pipe)
    calc_page.tab_1.array.pipe_width = NumberField('Pipe Width', suffix= 'm',default= None, visible= is_Rectangular_Pipe)
    calc_page.tab_1.array.pipe_height = NumberField('Pipe Height', suffix='m', default= None, visible=is_Rectangular_Pipe)
    calc_page.tab_1.array.ds_energy = NumberField('D/S Energy(H2)', suffix='m',default=0,visible=is_sharpEdged_Orifice)
    calc_page.tab_1.array.orifice_thickness = NumberField('Orifice Thicknes', suffix='m',default=.01,visible=is_sharpEdged_Orifice)
    calc_page.tab_1.array.edge_Radius = NumberField('Orifice Edge Radius', suffix='m',default=0,visible=is_sharpEdged_Orifice)
    calc_page.tab_1.array.orifice_centreline = NumberField('Orifice Centreline elevation', suffix='m', default=0,visible=is_sharpEdged_Orifice)
    

     ######## Known Water Conditions 
    calc_page.tab_1.array.known_water_conditions_water_level = NumberField('Hydraulic Level', suffix='m', visible=_is_known_water_conditions)
    calc_page.tab_1.array.known_water_conditions_energy_level = NumberField('Energy level', suffix='m', visible=_is_known_water_conditions)
    #_1.array.edge_Radius_1 = NumberField('Orifice Edge Radius', suffix='m',default=0,visible=is_sharp_Edged_Rectangular_Orifice)
    # calc_page.tab_1.array.orifice_centreline_1 = NumberField('Orifice Centreline elevation', suffix='m', default=0,visible=is_sharp_Edged_Rectangular_Orifice)
    # calc_page.tab_1.lb3 = LineBreak()
    # calc_page.tab_1.array.orifice_diametre_1 = NumberField('Orifice Diametre', suffix= 'm', visible=is_Circular_Orifice_in_Rectangular_Pipe,default=.2) 
    # calc_page.tab_1.array.pipe_Width_1 = NumberField('Pipe Width',suffix='m',default=.4,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    # calc_page.tab_1.array.pipe_height_1 = NumberField('Pipe Height', suffix='m', default=.4, visible=is_Circular_Orifice_in_Rectangular_Pipe)
    # calc_page.tab_1.array.ds_energy_2 = NumberField('D/S Energy(H2)', suffix='m',default=0,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    # calc_page.tab_1.array.orifice_thickness_2 = NumberField('Orifice Thicknes', suffix='m',default=.01,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    # calc_page.tab_1.array.edge_Radius_2 = NumberField('Orifice Edge Radius', suffix='m',default=0,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    # calc_page.tab_1.array.orifice_centreline_2 = NumberField('Orifice Centreline elevation', suffix='m', default=0,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    # calc_page.tab_1.lb4 = LineBreak()
    # calc_page.tab_1.array.orifice_width_1 = NumberField('orifice Width', suffix= 'm',default=.1, visible= is_Rectangular_Orifice_in_Circular_Pipe)
    # calc_page.tab_1.array.orifice_height_1 = NumberField('orifice Height', suffix='m', default=.1, visible=is_Rectangular_Orifice_in_Circular_Pipe)
    # calc_page.tab_1.array.pipe_diametre_1 = NumberField('Pipe Diameter', suffix= 'm',default=.4, visible= is_Rectangular_Orifice_in_Circular_Pipe)
    # calc_page.tab_1.array.ds_energy_3 = NumberField('D/S Energy(H2)', suffix='m',default=0,visible= is_Rectangular_Orifice_in_Circular_Pipe)
    # calc_page.tab_1.array.orifice_thickness_3 = NumberField('Orifice Thicknes', suffix='m',default=.01,visible= is_Rectangular_Orifice_in_Circular_Pipe)
    # calc_page.tab_1.array.edge_Radius_3 = NumberField('Orifice Edge Radius', suffix='m',default=0,visible=is_Rectangular_Orifice_in_Circular_Pipe)
    # calc_page.tab_1.array.orifice_centreline_3 = NumberField('Orifice Centreline elevation', suffix='m', default=0,visible=is_Rectangular_Orifice_in_Circular_Pipe)
    ####GeneralSubmergedConstriction
    calc_page.tab_1.array.upstream_section_shape = OptionField('Upstream Section Shape',options=['Circular','Rectangular'],default='Circular',visible=is_General_Submerged_Constrict)
    calc_page.tab_1.array.Orifice_shape = OptionField('Orifice Shape',options=['Circular','Rectangular'],default='Circular',visible=is_General_Submerged_Constrict)
    calc_page.tab_1.array.downstream_section_shape = OptionField('Downstream Section Shape',options=['Circular','Rectangular'],default='Circular',visible=is_General_Submerged_Constrict) 
    calc_page.tab_1.array.pipe1_diametre = NumberField('Upstream Pipe Diametre', suffix='m',default = None,visible=is_Circular_upstream_Constrict)
    calc_page.tab_1.array.pipe1_width = NumberField('Upstream Pipe Width', suffix='m',default = None,visible=is_Retangular_upstream_Constrict)
    calc_page.tab_1.array.pipe1_height = NumberField('Upstream Pipe Height', suffix='m',default = None,visible=is_Retangular_upstream_Constrict)
    calc_page.tab_1.array.pipe2_diametre = NumberField('Downstream Pipe Diametre', suffix='m',default = None,visible=is_Circular_downstream_Constrict)
    calc_page.tab_1.array.pipe2_width = NumberField('Downstream Pipe Width', suffix='m',default = None,visible=is_Rectangular_downstream_Constrict)
    calc_page.tab_1.array.pipe2_height = NumberField('Downstream Pipe Height', suffix='m',default = None,visible=is_Rectangular_downstream_Constrict)
    calc_page.tab_1.array.orifice_dia = NumberField('Orifice Pipe Diametre', suffix='m',default = None,visible=is_Circular_orifice_Constrict)
    calc_page.tab_1.array.orifice_width = NumberField('Orifice Pipe Width', suffix='m',default = None,visible=is_Rectangular_orifice_Constrict)
    calc_page.tab_1.array.orifice_height = NumberField('Orifice Pipe Height', suffix='m',default = None,visible=is_Rectangular_orifice_Constrict)
    calc_page.tab_1.array.ds_energy_4 = NumberField('D/S Energy(H2)', suffix='m',default=0,visible=is_General_Submerged_Constrict)
    calc_page.tab_1.array.orifice_thickness_4 = NumberField('Orifice Thicknes', suffix='m',default=.01,visible=is_General_Submerged_Constrict)
    calc_page.tab_1.array.edge_Radius_4 = NumberField('Orifice Edge Radius', suffix='m',default=0,visible=is_General_Submerged_Constrict)
    calc_page.tab_1.lb5 = LineBreak()
    ####CriticalDepth
    calc_page.tab_1.array.sectionDiameter = NumberField('Section Diameter', suffix= 'm', default=0.5,visible= is_CriticalDepth_Circular)
    


class Controller(ViktorController):
    label = 'My Folder'
    children = ['MyEntityType']
    show_children_as = 'Cards'
    parametrization = Parametrization

    def calculation(self, params, **kwargs):
        hydraulic_models_inputs = params.array
        if not hydraulic_models_inputs:
            return
        
        controllers =[]
        water_components = []
        water = hydraulics.water()

        for item in hydraulic_models_inputs:
            component = item.component
            if component == 'Known Water Conditions':
                controller = instance.instance_known_water_conditions(item)
                controllers.append(controller)
            elif component == 'Sharp Edged Orifice Passage':
                controller = instance.instance_SharpEgde_orifice_within_pipe(item)
                controllers.append(controller)
            elif component =='General Submerged Constriction':
                controller = instance.instance_General_Submerged_Constriction(item)
                controllers.append(controller)
            else:
                print(f"Component: {component} not recognised")
            
            method_to_run =  getattr(controller,'Modify_Water',None)
            if method_to_run is not None:
                method_to_run(water)
                water_components.append(copy.deepcopy(water))
            else:
                print(f"Method: {method_to_run} not recognised for component: {component}")

        return controllers, water_components
    
    def calculate_df_results(self, params, **kwargs):
        hydraulic_models_input = params.calc_page.tab_1.array
        flow_rate = params.calc_page.tab_1.flow_rate
        df = pd.DataFrame(columns=["DS Energy Level", "DS Hydraulic level", "US Energy Level", "US Hydraulic level", "component", "Data"])

        if not hydraulic_models_input:
            return
        for item in hydraulic_models_input:
            component = item.component
            if component == 'Known Water Conditions':
                hydraulic_level = item.known_water_conditions_water_level
                energy_level = item.known_water_conditions_energy_level
                df = dfd.df_known_water_conditions(df, flow_rate, hydraulic_level, energy_level)
            elif component == 'Sharp Edged Orifice Passage':
                diametre = item.pipe_diametre
                orifice_diametre = item.orifice_diametre
                width=item.pipe_width
                height = item.pipe_height
                orifice_width=item.orifice_width1
                orifice_height = item.orifice_height1
                ds_energy=item.ds_energy
                orifice_thickness = item.orifice_thickness
                edge_radius = item.edge_Radius
                orifice_centreline = item.orifice_centreline
                df = dfd.df_SharpEdgedOrifice(df,flow_rate,diametre,orifice_diametre,width, height, orifice_width, orifice_height,ds_energy,orifice_thickness,edge_radius,orifice_centreline)
            elif component =='General Submerged Constriction':
                diametre1 = item.pipe1_diametre
                diametre2 = item.pipe2_diametre
                orifice_diametre = item.orifice_dia
                width1 = item.pipe1_width
                height1 = item.pipe1_height
                width2 = item.pipe2_width
                height2 = item.pipe2_height
                orifice_width = item.orifice_width
                orifice_height = item.orifice_height
                ds_energy = item.ds_energy_4
                orifice_thickness =item.orifice_thickness_4
                edge_radius = item.edge_Radius_4
                df = dfd.df_GeneralSubmergedConstrict(df,flow_rate,diametre1,diametre2,orifice_diametre,width1,height1, width2,height2,orifice_width,orifice_height,ds_energy,orifice_thickness,edge_radius)

            else:
                print(f"Component: {component} not recognised")
        return df

    def download_calculations(self,params, **kwargs):
        df = self.calculate_df_results(params)
        combined_csv_data = ""
        data_entries = df["Data"].tolist()
        for data in data_entries:
            if isinstance(data, pd.DataFrame):
                data_csv_data = data.to_csv(index=False)
                combined_csv_data += data_csv_data
        csv_data = combined_csv_data
        #csv_data = df.to_csv(index=False)
        file = vkt.File.from_data(csv_data)
        return DownloadResult(file, 'file_name.csv')
    
    @TableView("Results", duration_guess=1)
    def table_view(self, params, **kwargs):
        df = self.calculate_df_results(params)
        df.drop(columns=["Data"], inplace=True)
        return TableResult(df)
    

        


            
