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
    'Sharp Edged Circular Orifice and Circular Pipe Passage',
    'Sharp Edged Rectangular Orifice and Rectangular Pipe Passage',
    'Sharp Edged Circular Orifice and Rectangular Pipe Passage',
    'Sharp Edged Rectangular Orifice and Circular Pipe Passage'
]
is_sharp_Edged_Circular_Orifice = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'Sharp Edged Circular Orifice Passage'))
is_sharp_Edged_Rectangular_Orifice = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'Sharp Edged Rectangular Orifice Passage'))
is_Circular_Orifice_in_Rectangular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'Sharp Edged Circular Orifice and Rectangular Pipe Passage'))
is_Rectangular_Orifice_in_Circular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'Sharp Edged Rectangular Orifice and Circular Pipe Passage'))
# is_sharp_Edged_Orifice = DynamicArrayConstraint('calc_page.tab_1.array',IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage'))
# is_Circular_orifice = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.orifice_shape'),'Circular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
# is_Rectangular_orifice = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.orifice_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
# is_Circular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.pipe_shape'),'Circular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
# is_Rectangular_Pipe = DynamicArrayConstraint('calc_page.tab_1.array',And(IsEqual(Lookup('$row.pipe_shape'),'Rectangular'),IsEqual(Lookup('$row.component'),'Sharp Edged Orifice Passage')))
_is_known_water_conditions = DynamicArrayConstraint('calc_page.tab_1.array', IsEqual(Lookup('$row.component'), 'Known Water Conditions'))
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
    #calc_page.tab_1.array.orifice_shape = OptionField('Orifice Shape', visible= is_sharp_Edged_Orifice,options= ['Circular','Rectangular'], default='Circular')
    calc_page.tab_1.array.orifice_diametre = NumberField('Orifice Diametre', suffix= 'm', visible=is_sharp_Edged_Circular_Orifice,default=.2)
    # calc_page.tab_1.array.pipe_shape = OptionField('Pipe Shape',visible=is_sharp_Edged_Orifice,options=['Circular','Rectangular'],default='Circular')
    calc_page.tab_1.array.pipe_diametre = NumberField('Pipe Diametre',suffix='m',default=.4,visible=is_sharp_Edged_Circular_Orifice)
    calc_page.tab_1.array.ds_energy = NumberField('D/S Energy(H2)', suffix='m',default=0,visible=is_sharp_Edged_Circular_Orifice)
    calc_page.tab_1.array.orifice_thickness = NumberField('Orifice Thicknes', suffix='m',default=.01,visible=is_sharp_Edged_Circular_Orifice)
    calc_page.tab_1.array.edge_Radius = NumberField('Orifice Edge Radius', suffix='m',default=0,visible=is_sharp_Edged_Circular_Orifice)
    calc_page.tab_1.array.orifice_centreline = NumberField('Orifice Centreline elevation', suffix='m', default=0,visible=is_sharp_Edged_Circular_Orifice)
    calc_page.tab_1.array.known_water_conditions_water_level = NumberField('Hydraulic Level', suffix='m', visible=_is_known_water_conditions)
    calc_page.tab_1.array.known_water_conditions_energy_level = NumberField('Energy level', suffix='m', visible=_is_known_water_conditions)
    calc_page.tab_1.lb2 = LineBreak()
    calc_page.tab_1.array.orifice_width = NumberField('orifice Width', suffix= 'm',default=.2, visible= is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.array.orifice_height = NumberField('orifice Height', suffix='m', default=.2, visible=is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.array.pipe_width = NumberField('Pipe Width', suffix= 'm',default=.4, visible= is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.array.pipe_height = NumberField('Pipe Height', suffix='m', default=.4, visible=is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.array.ds_energy_1 = NumberField('D/S Energy(H2)', suffix='m',default=0,visible= is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.array.orifice_thickness_1 = NumberField('Orifice Thicknes', suffix='m',default=.01,visible= is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.array.edge_Radius_1 = NumberField('Orifice Edge Radius', suffix='m',default=0,visible=is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.array.orifice_centreline_1 = NumberField('Orifice Centreline elevation', suffix='m', default=0,visible=is_sharp_Edged_Rectangular_Orifice)
    calc_page.tab_1.lb3 = LineBreak()
    calc_page.tab_1.array.orifice_diametre_1 = NumberField('Orifice Diametre', suffix= 'm', visible=is_Circular_Orifice_in_Rectangular_Pipe,default=.2) 
    calc_page.tab_1.array.pipe_Width_1 = NumberField('Pipe Width',suffix='m',default=.4,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    calc_page.tab_1.array.pipe_height_1 = NumberField('Pipe Height', suffix='m', default=.4, visible=is_Circular_Orifice_in_Rectangular_Pipe)
    calc_page.tab_1.array.ds_energy_2 = NumberField('D/S Energy(H2)', suffix='m',default=0,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    calc_page.tab_1.array.orifice_thickness_2 = NumberField('Orifice Thicknes', suffix='m',default=.01,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    calc_page.tab_1.array.edge_Radius_2 = NumberField('Orifice Edge Radius', suffix='m',default=0,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    calc_page.tab_1.array.orifice_centreline_2 = NumberField('Orifice Centreline elevation', suffix='m', default=0,visible=is_Circular_Orifice_in_Rectangular_Pipe)
    calc_page.tab_1.lb4 = LineBreak()
    calc_page.tab_1.array.orifice_width_1 = NumberField('orifice Width', suffix= 'm',default=.1, visible= is_Rectangular_Orifice_in_Circular_Pipe)
    calc_page.tab_1.array.orifice_height_1 = NumberField('orifice Height', suffix='m', default=.1, visible=is_Rectangular_Orifice_in_Circular_Pipe)
    calc_page.tab_1.array.pipe_diametre_1 = NumberField('Pipe Diameter', suffix= 'm',default=.4, visible= is_Rectangular_Orifice_in_Circular_Pipe)
    calc_page.tab_1.array.ds_energy_3 = NumberField('D/S Energy(H2)', suffix='m',default=0,visible= is_Rectangular_Orifice_in_Circular_Pipe)
    calc_page.tab_1.array.orifice_thickness_3 = NumberField('Orifice Thicknes', suffix='m',default=.01,visible= is_Rectangular_Orifice_in_Circular_Pipe)
    calc_page.tab_1.array.edge_Radius_3 = NumberField('Orifice Edge Radius', suffix='m',default=0,visible=is_Rectangular_Orifice_in_Circular_Pipe)
    calc_page.tab_1.array.orifice_centreline_3 = NumberField('Orifice Centreline elevation', suffix='m', default=0,visible=is_Rectangular_Orifice_in_Circular_Pipe)

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
            elif component == 'Sharp Edged Circular Orifice Passage':
                controller = instance.instance_circular_orifice_within_pipe(item)
                controllers.append(controller)
            elif component == 'Sharp Edged Rectangular Orifice Passage' :
                controller = instance.instance_Rectangular_orifice_within_pipe(item)
                controller.append(controller)
            elif component == 'Sharp Edged Circular Orifice and Rectangular Pipe Passage':
                controller==instance.instance_circular_orifice_within_Rectangular_pipe(item)
                controllers.append(controller)
            elif component == 'Sharp Edged Rectangular Orifice and Circular Pipe Passage':
                controller= instance.instance_Rectangular_orifice_within_Circular_pipe(item)
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
            elif component == 'Sharp Edged Circular Orifice Passage':
                diametre = item.pipe_diametre
                orifice_diametre = item.orifice_diametre
                ds_energy=item.ds_energy
                orifice_thickness = item.orifice_thickness
                edge_radius = item.edge_Radius
                orifice_centreline = item.orifice_centreline
                df = dfd.df_SharpEdgedOrifice(df,flow_rate,diametre,orifice_diametre,ds_energy,orifice_thickness,edge_radius,orifice_centreline)
            elif component == 'Sharp Edged Rectangular Orifice Passage':
                width=item.pipe_width
                height = item.pipe_height
                orifice_width=item.orifice_width
                orifice_height = item.orifice_height
                ds_energy = item.ds_energy_1
                orifice_thickness=item.orifice_thickness_1
                edge_radius=item.edge_Radius_1
                orifice_centerline=item.orifice_centreline_1
                df = dfd.df_RectangularOrifice(df, flow_rate,width,height,orifice_width,orifice_height,ds_energy,orifice_thickness,edge_radius,orifice_centerline)
            elif component == 'Sharp Edged Circular Orifice and Rectangular Pipe Passage':
                width=item.pipe_Width_1
                height = item.pipe_height_1
                orifice_diametre=item.orifice_diametre_1
                ds_energy = item.ds_energy_2
                orifice_thickness=item.orifice_thickness_2
                edge_radius=item.edge_Radius_2
                orifice_centerline=item.orifice_centreline_2
                df = dfd.df_SharpEdgedCircularOrificeRectPipe(df, flow_rate,width,height,orifice_diametre,ds_energy,orifice_thickness,edge_radius,orifice_centerline)
            elif component =='Sharp Edged Rectangular Orifice and Circular Pipe Passage':
                diametre = item.pipe_diametre_1
                orifice_width=item.orifice_width_1
                orifice_height = item.orifice_height_1
                ds_energy = item.ds_energy_3
                orifice_thickness=item.orifice_thickness_3
                edge_radius=item.edge_Radius_3
                orifice_centerline=item.orifice_centreline_3
                df = dfd.df_SharpEdgedRectangularOrificeCircularPipe(df,flow_rate,diametre,orifice_width,orifice_height,ds_energy,orifice_thickness,edge_radius,orifice_centerline)

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
    

        


            
