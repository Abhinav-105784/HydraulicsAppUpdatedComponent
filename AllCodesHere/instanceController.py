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

def instance_circular_orifice_within_pipe(item, water: water):

    circular_orifice = hydraulics.CircularEdgedOrifice(
        flow_rate=item.circular_orifice_flow_rate,
        diametre=item.pipe_diametre,
        orifice_diametre=item.orifice_diametre,
        ds_energy_level = item.orifice_ds_energy_level,
        orifice_thickness=item.orifice_thickness,
        orifice_edge_radius=item.orifice_edge_radius,
        orifice_centerline=item.orifice_centreline,
    )
    return circular_orifice

def instance_Rectangular_orifice_within_pipe(item, water: water):
    rectangular_orifice = hydraulics.RectangularEdgedOrifice(
        flow_rate=item.Rectangular_orifice_flow_rate,
        width=item.pipe_width,
        height = item.pipe_height,
        orifice_width=item.orifice_width,
        orifice_height = item.orifice_height,
        ds_energy_level = item.orifice_ds_energy_level,
        orifice_thickness=item.orifice_thickness,
        orifice_edge_radius=item.orifice_edge_radius,
        orifice_centerline=item.orifice_centreline,
    )
    return rectangular_orifice

def instance_circular_orifice_within_Rectangular_pipe(item, water: water):

    circular_orifice = hydraulics.CircularEdgedOrificeInRectangularPipe(
        flow_rate=item.circular_orifice_flow_rate,
        width=item.width,
        height=item.height,
        orifice_diametre=item.orifice_diametre,
        ds_energy_level = item.orifice_ds_energy_level,
        orifice_thickness=item.orifice_thickness,
        orifice_edge_radius=item.orifice_edge_radius,
        orifice_centerline=item.orifice_centreline,
    )
    return circular_orifice

def instance_Rectangular_orifice_within_Circular_pipe(item, water: water):
    rectangular_orifice = hydraulics.RectangularEdgedOrificeInCircularPipe(
        flow_rate=item.Rectangular_orifice_flow_rate,
        diametre = item.diametre,
        orifice_width=item.orifice_width,
        orifice_height = item.orifice_height,
        ds_energy_level = item.orifice_ds_energy_level,
        orifice_thickness=item.orifice_thickness,
        orifice_edge_radius=item.orifice_edge_radius,
        orifice_centerline=item.orifice_centreline,
    )
    return rectangular_orifice