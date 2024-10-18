from ..Information import hydraulics as hydraulics

def df_SharpEdgedOrifice(df, flow_rate: float, diametre: float, orifice_diametre: float, ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float, orifice_centerline :float):
    
    orificeTube = hydraulics.CircularEdgedOrifice(flow_rate, diametre, orifice_diametre, ds_energy_level, orifice_thickness, orifice_edge_radius, orifice_centerline)
    df.loc[len(df)] = [orificeTube.ds_energy_level,"NA","NA","NA",orificeTube.component_type,orificeTube.data]
    return df

def df_known_water_conditions(df, flow_rate, hydraulic_level, energy_level):
    df.loc[len(df)] = ["N/a", "N/a", energy_level, hydraulic_level, "Known downstream conditions", "N/a"]
    return df

def df_RectangularOrifice(df,flow_rate: float, pipe_width: float, pipe_height:float, orifice_width: float, orifice_height: float,ds_energy_level:float, orifice_thickness:float, orifice_edge_radius: float, orifice_centerline: float):
    orificeTube = hydraulics.RectangularEdgedOrifice(flow_rate, pipe_width, pipe_height, orifice_width, orifice_height,ds_energy_level, orifice_thickness, orifice_edge_radius, orifice_centerline)
    df.loc[len(df)] = [orificeTube.ds_energy_level,"NA","NA","NA",orificeTube.component_type,orificeTube.data]
    return df

def df_SharpEdgedCircularOrificeRectPipe(df, flow_rate: float, width: float, height: float ,orifice_diametre: float, ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float, orifice_centerline :float):
    
    orificeTube = hydraulics.CircularEdgedOrificeInRectangularPipe(flow_rate, width, height, orifice_diametre, ds_energy_level, orifice_thickness, orifice_edge_radius, orifice_centerline)
    df.loc[len(df)] = [orificeTube.ds_energy_level,"NA","NA","NA",orificeTube.component_type,orificeTube.data]
    return df

def df_SharpEdgedRectangularOrificeCircularPipe(df, flow_rate: float, diametre: float ,orifice_width: float,orifice_height: float, ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float, orifice_centerline :float):
    
    orificeTube = hydraulics.RectangularEdgedOrificeInCircularPipe(flow_rate, diametre, orifice_width,orifice_height, ds_energy_level, orifice_thickness, orifice_edge_radius, orifice_centerline)
    df.loc[len(df)] = [orificeTube.ds_energy_level,"NA","NA","NA",orificeTube.component_type,orificeTube.data]
    return df