from ..Information import hydraulics as hydraulics

def df_SharpEdgedOrifice(df, flow_rate: float, diametre: float, orifice_diametre: float,
                         pipe_width : float, pipe_height : float, orifice_width : float, orifice_height : float,
                          ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float, orifice_centerline :float):
    
    orificeTube = hydraulics.SharpEdgedOrifice(flow_rate, diametre, orifice_diametre,pipe_width,
    pipe_height,
    orifice_width, orifice_height ,ds_energy_level, orifice_thickness, orifice_edge_radius, orifice_centerline)
    df.loc[len(df)] = [orificeTube.ds_energy_level,"NA","NA","NA",orificeTube.component_type,orificeTube.data]
    return df

def df_known_water_conditions(df, flow_rate, hydraulic_level, energy_level):
    df.loc[len(df)] = ["N/a", "N/a", energy_level, hydraulic_level, "Known downstream conditions", "N/a"]
    return df

# def df_RectangularOrifice(df,flow_rate: float, pipe_width: float, pipe_height:float, orifice_width: float, orifice_height: float,ds_energy_level:float, orifice_thickness:float, orifice_edge_radius: float, orifice_centerline: float):
#     orificeTube = hydraulics.RectangularEdgedOrifice(flow_rate, pipe_width, pipe_height, orifice_width, orifice_height,ds_energy_level, orifice_thickness, orifice_edge_radius, orifice_centerline)
#     df.loc[len(df)] = [orificeTube.ds_energy_level,"NA","NA","NA",orificeTube.component_type,orificeTube.data]
#     return df

# def df_SharpEdgedCircularOrificeRectPipe(df, flow_rate: float, width: float, height: float ,orifice_diametre: float, ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float, orifice_centerline :float):
    
#     orificeTube = hydraulics.CircularEdgedOrificeInRectangularPipe(flow_rate, width, height, orifice_diametre, ds_energy_level, orifice_thickness, orifice_edge_radius, orifice_centerline)
#     df.loc[len(df)] = [orificeTube.ds_energy_level,"NA","NA","NA",orificeTube.component_type,orificeTube.data]
#     return df

# def df_SharpEdgedRectangularOrificeCircularPipe(df, flow_rate: float, diametre: float ,orifice_width: float,orifice_height: float, ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float, orifice_centerline :float):
    
#     orificeTube = hydraulics.RectangularEdgedOrificeInCircularPipe(flow_rate, diametre, orifice_width,orifice_height, ds_energy_level, orifice_thickness, orifice_edge_radius, orifice_centerline)
#     df.loc[len(df)] = [orificeTube.ds_energy_level,"NA","NA","NA",orificeTube.component_type,orificeTube.data]
#     return df


def df_GeneralSubmergedConstrict(df, flow_rate: float, diametre1: float, diametre2: float,orifice_diametre: float, width1: float,
    height1: float,
    width2: float,
    height2: float,
    orifice_width: float,
    orifice_height: float,ds_energy_level:float,orifice_thickness: float, orifice_edge_radius:float):

    SGC = hydraulics.GeneralSubmergedConstriction(flow_rate,diametre1,diametre2,orifice_diametre,width1,height1,width2,height2,orifice_width,orifice_height,ds_energy_level,orifice_thickness,orifice_edge_radius)
    df.loc[len(df)]=[SGC.ds_energy_level,"NA","NA","NA",SGC.component_type,SGC.data]
    return df

# def df_RectangularSGC(df, flow_rate: float, width1: float, height1: float, width2: float, height2: float ,orifice_width: float, orifice_height : float,ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float ):
#     RectangularSGC = hydraulics.GeneralSubmergedConstriction(flow_rate,0,0,0,width1,height1,width2,height2,orifice_width,orifice_height,ds_energy_level,orifice_thickness,orifice_edge_radius)
#     df.loc[len(df)]= [RectangularSGC.ds_energy_level,"NA","NA","NA","Rectangular General Submerged Constriction",RectangularSGC.data2]
#     return df

# def df_case3SGC(df,flow_rate: float, width1: float, height1: float,diametre2: float,orifice_diametre: float, ds_energy_level:float,orifice_thickness: float, orifice_edge_radius:float):
#     case3SGC = hydraulics.GeneralSubmergedConstriction(flow_rate,0,diametre2,orifice_diametre,width1,height1,0,0,0,0,ds_energy_level,orifice_thickness,orifice_edge_radius)
#     df.loc[len(df)]=[case3SGC.ds_energy_level,"NA","NA","NA","Upstream Rectangular rest Circular",case3SGC.data3]
#     return df

# def  df_case4SGC(df,flow_rate: float, width1: float, height1: float, diametre2: float,orifice_width: float, orifice_height : float,ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float ):
#     case4SGC = hydraulics.GeneralSubmergedConstriction(flow_rate,0,diametre2,0,width1,height1,0,0,orifice_width,orifice_height,ds_energy_level,orifice_thickness,orifice_edge_radius)
#     df.loc[len(df)]= [case4SGC.ds_energy_level,"NA","NA","NA","Downstream Circular Rest Rectangular", case4SGC.data4]
#     return df

# def df_case5SGC(df,flow_rate: float, diametre1: float,width2: float, height2: float,orifice_diametre: float, ds_energy_level:float,orifice_thickness: float, orifice_edge_radius:float):
#     case5SGC = hydraulics.GeneralSubmergedConstriction(flow_rate,diametre1,0,orifice_diametre,0,0,width2,height2,0,0,ds_energy_level,orifice_thickness,orifice_edge_radius)
#     df.loc[len(df)]= [case5SGC.ds_energy_level,"NA","NA","NA","Downstream Rectangular Rest Circular",case5SGC.data5]
#     return df

# def df_case6SGC(df,flow_rate: float, diametre1: float,width2: float, height2: float,orifice_width: float, orifice_height : float,ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float ):
#     case6SGC = hydraulics.GeneralSubmergedConstriction(flow_rate,diametre1,0,0,0,0,width2,height2,orifice_width,orifice_height,ds_energy_level,orifice_thickness,orifice_edge_radius)
#     df.loc[len(df)]=[case6SGC.ds_energy_level,"NA","NA","NA","Upstream Circular Rest Rectangular",case6SGC.data6]
#     return df

# def df_case7SGC(df,flow_rate: float, diametre1: float, diametre2: float,orifice_width: float, orifice_height : float,ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float ): 
#     case7SGC = hydraulics.GeneralSubmergedConstriction(flow_rate,diametre1,diametre2,0,0,0,0,0,orifice_width,orifice_height,ds_energy_level,orifice_thickness,orifice_edge_radius)
#     df.loc[len(df)]= [case7SGC.ds_energy_level,"NA","NA","NA","Only Orifice Rectangular",case7SGC.data7]
#     return df

# def df_case8SGC(df,flow_rate: float, width1: float, height1: float, width2: float, height2: float,orifice_diametre : float,ds_energy_level:float, orifice_thickness: float, orifice_edge_radius:float ): 
#     case8SGC = hydraulics.GeneralSubmergedConstriction(flow_rate,0,0,orifice_diametre,width1,height1,width2,height2,0,0,ds_energy_level,orifice_thickness,orifice_edge_radius)
#     df.loc[len(df)] = [case8SGC.ds_energy_level,"NA","NA","NA","Only Orifice Circular",case8SGC.data8]
#     return df

def df_criticalDepthControlCircular(df,flow_rate: float, ds_energy_level: float, invertLevel: float, copingLevel: float, modularLimit: float, diameter: float):
    criticalDepthControlCircular = hydraulics.CriticalDepthControl(flow_rate, ds_energy_level, invertLevel, copingLevel, modularLimit, 0, diameter, 0)
    df.loc[len(df)] = [criticalDepthControlCircular.ds_energy_level,"NA","NA","NA","Circular channel critical depth", criticalDepthControlCircular.dataCircular]
    return df

