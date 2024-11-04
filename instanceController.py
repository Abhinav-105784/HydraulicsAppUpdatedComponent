from ..Information import hydraulics as hydraulics
from ..Information.hydraulics import water as water

def instance_known_water_conditions(item):
    flow_rate = item.known_water_conditions_flow_rate
    water_level = item.known_water_conditions_water_level
    energy_level = item.known_water_conditions_energy_level

    known_water_conditions = hydraulics.KnownWaterConditions(
        flow_rate=flow_rate,
        water_level=water_level,
        energy_level=energy_level
    )
    return known_water_conditions

def instance_SharpEgde_orifice_within_pipe(item, water: water):

    circular_orifice = hydraulics.SharpEdgedOrifice(
        flow_rate=item.circular_orifice_flow_rate,
        diametre=item.pipe_diametre,
        orifice_diametre=item.orifice_diametre,
        pipe_width = item.pipe_width,
        pipe_height = item.pipe_height,
        orifice_width = item.orifice_width,
        orifice_height = item.orifice_height,
        ds_energy_level = item.orifice_ds_energy_level,
        orifice_thickness=item.orifice_thickness,
        orifice_edge_radius=item.orifice_edge_radius,
        orifice_centerline=item.orifice_centreline,
    )
    return circular_orifice

def instance_General_Submerged_Constriction(item, water: water):
    General_Submerged_Constriction = hydraulics.GeneralSubmergedConstriction(
        flow_rate=item.flow_rate,
        diametre1= item.diametre1,
        diametre2 = item.diametre2,
        width1=item.width1,
        height1 = item.height1,
        width2 = item.width2,
        height2 = item.height2,
        orifice_width = item.orifice_width,
        orifice_height = item.orifice_height,
        orifice_diametre = item.orifice_diametre,
        ds_energy = item.ds_energy_level,
        orifice_thickness = item.orifice_thickness,
        orifice_edge_radius = item.orifice_edge_radius
    )
    return General_Submerged_Constriction

def instance_CriticalDepthControl(item, water: water):
    criticalDepthControl = hydraulics.CriticalDepthControl(
        flow_rate= item.flow_rate,
        ds_energy_level= item.ds_energy_level,
        invertLevel= item.invertLevel, 
        copingLevel= item.copingLevel,
        width= item.width,
        diameter= item.diameter,
        sideAngle= item.sideAngle
    )
    return criticalDepthControl