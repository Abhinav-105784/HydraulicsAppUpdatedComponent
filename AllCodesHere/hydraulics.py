import math 
import pandas as pd

def calculate_velocity(flow_rate: float, area:float) -> float:
    '''
    calculate velocity of fluid in a pipe

    args:
    flow_rate : The discharge in cubic meters per second
    area : Area of the pipe in square meters

    returns
    float : velocity of fluid
    '''
    return flow_rate/area

def calculate_circular_area(diametre: float) -> float:
    '''
    calculate the area of a circular pipe

    args:
    diametre : The diametre of the pipe in meters

    returns:
    float : Area of cross section of pipe in square meters in decimals

    '''

    return (math.pi) * (diametre**2)/4

def calculate_Rectangular_area(width: float, height : float) -> float:
    '''
    calculate the area of the rectangular pipe 

    args:
    width: width of the pipe in meters
    height: height of the pipe in meters

    returns:
    float: area of cross section of pipe in square meters in decimal 
    '''
    return width*height





class water:

    def set_flow_rate(self, flow_rate):
        self.flow_rate = flow_rate
    def get_flow_rate(self):
        return self.flow_rate
    def set_water_level(self,water_level):
        self.water_level = water_level
    def get_water_level(self):
        return self.water_level
    def set_energy_level(self, level):
        self.energy_level = level
    def get_energy_level(self):
        return self.energy_level
    
def shared_modify_water(self, water: water):
    water.set_energy_level(self.energy_level)
    water.set_flow_rate(self.flow_rate)
    water.set_water_level(self.water_level)

class KnownWaterConditions:
     def __init__(self, flow_rate: float, water_level: float, energy_level: float):
        self.flow_rate = flow_rate
        self.water_level = water_level
        self.energy_level = energy_level
     def modify_water(self, water: water):
            shared_modify_water(self, water)

class knowDownstreamConditions:
    def __init__(self, flow_rate: float, water_level: float, energy_level: float):
        self.flow_rate = flow_rate
        self.water_level = water_level
        self.energy_level = energy_level

    def modify_water(self, water:water):
        shared_modify_water(self, water)

class CircularEdgedOrifice:
    def __init__(self, flow_rate: float, diametre: float, orifice_diametre: float, ds_energy_level:float, orifice_thickness:float, orifice_edge_radius: float, orifice_centerline: float):
        self.flow_rate = flow_rate
        self.diametre = diametre
        self.orifice_diametre = orifice_diametre
        self.ds_energy_level = ds_energy_level
        self.orifice_thickness = orifice_thickness
        self.orifice_edge_radius = orifice_edge_radius
        self.orifice_centerline = orifice_centerline
        
        orifice_df = pd.DataFrame(columns=[

            "t/Dn",
            "Orifice Type",
            "K (based on orifice velocity)",
            "Headloss",
            "Flow Stable?",
            "Cavitation Status",
            "Pipe Velocity (v1)",
            "U/S Energy (H1)"
        ])
        orificeArea = calculate_circular_area(orifice_diametre)
        pipeArea = calculate_circular_area(diametre)
        nominalDia = 4*orificeArea/((math.pi)*orifice_diametre)
        thickness_nominalDiaRatio= orifice_thickness/nominalDia
        orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
        tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
        Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
        sqrt = 2*(Rfactor**.5)
        orifice_pipeAreaRatio = orificeArea/pipeArea
        Permiability = Rfactor*((1-orifice_pipeAreaRatio)**.75)+(1-orifice_pipeAreaRatio)**2 + min(tau,sqrt)*((1-orifice_pipeAreaRatio)**1.375)+(0.01*orifice_thickness/nominalDia)
        print(f"{Permiability}")
        dH = Permiability*(calculate_velocity(flow_rate,orificeArea)**2)/(2*9.81)
        Kin = dH*2*9.81/(calculate_velocity(flow_rate,pipeArea)**2)
        orificeDia_PipeDiaRatio = orifice_diametre/diametre 
        upstream_Energy = dH + ds_energy_level
        hu = upstream_Energy - orifice_centerline
        hv = -8.6
        hs = hu - hv
        ref_IncipientCav = -10.84779 + (orificeDia_PipeDiaRatio*68.5599) + (orificeDia_PipeDiaRatio**2)*(-120.542) + (orificeDia_PipeDiaRatio**3)*86.73617 
        ref_criticalCav = -4.06023 + (orificeDia_PipeDiaRatio*31.04066) + (orificeDia_PipeDiaRatio**2)*-56.82 + (orificeDia_PipeDiaRatio**3)*58.9463
        ref_IncipientDam = -0.23091 + orificeDia_PipeDiaRatio*12.55424 + (orificeDia_PipeDiaRatio**2)*-26.4375 + (orificeDia_PipeDiaRatio**3)*44.71988
        ref_ChokingCav = 11.79863 + orificeDia_PipeDiaRatio*-57.22946 + (orificeDia_PipeDiaRatio**2)*101.5848 + (orificeDia_PipeDiaRatio**3)*-23.2237
        logK = math.log(Kin)
        logD = math.log(diametre)
        c = 0.595916742142878 + (0.0862736628857235*logK) + (-0.321334456683251*logD) + (0.0176435481517691*(logK**2)) + (0.0724573358221047*logK*logD) + (0.159738855911438*(logD**2)) + (0.00811998377973832*(logK**3)) + (0.0399142633228832*logK*logK*logD) + (0.045277311105048*logK*logD*logD) + (0.387474756840927*(logD**3)) + (-0.00419035434959079*(logK**4)) + (-0.00730504428453993*(logK**3)*logD) + (0.0209199559545679*(logD**2)*(logK**2)) +(0.0611565120535794*(logD**3)*logK) + (0.23542141447694*(logD**4))
        act_IncipientCav = ref_IncipientCav*c*((+hs/71.6)**.5)
        act_criticalCav = ref_criticalCav*c*((+hs/71.6)**.5)
        act_IncipientDam = ref_IncipientDam*((+hs/71.6)**.45)
        act_ChokingCav = ref_ChokingCav*((+hs/71.6)**.5)
        orificeType = 'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice'
        Headloss = round(upstream_Energy - ds_energy_level,3)
        flowStable = 'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES'
        cavitation = "NA" if orifice_centerline==0 else "OUTSIDE RANGE" if orificeDia_PipeDiaRatio<0.4 or orificeDia_PipeDiaRatio>0.8 else "No Cavitation" if calculate_velocity(flow_rate, area=calculate_circular_area(diametre))<act_IncipientCav else "Incipient Cavitation" if calculate_velocity(flow_rate, area=calculate_circular_area(diametre))<act_criticalCav else "CRITICAL" if calculate_velocity(flow_rate, area=calculate_circular_area(diametre))<act_IncipientDam else "INCIPIENT DAMAGE" if calculate_velocity(flow_rate, area=calculate_circular_area(diametre))<act_ChokingCav else "CHOKING CAVITATION"

        orifice_df.loc[len(orifice_df)] = [

            round(thickness_nominalDiaRatio,3),
            orificeType,
            round(Permiability,3),
            round(Headloss,3),
            flowStable,
            cavitation,
            round(calculate_velocity(flow_rate, area=calculate_circular_area(diametre)),3),
            round(upstream_Energy,3)
        
        ]
        self.data = orifice_df
        self.component_type = 'Circular Orifice Passage'

class RectangularEdgedOrifice:
    def __init__(self,flow_rate: float, pipe_width: float, pipe_height:float, orifice_width: float, orifice_height: float,ds_energy_level:float, orifice_thickness:float, orifice_edge_radius: float, orifice_centerline: float):
        self.flow_rate = flow_rate
        self.pipe_width = pipe_width
        self.pipe_height = pipe_height
        self.orifice_width = orifice_width
        self.orifice_height = orifice_height
        self.ds_energy_level = ds_energy_level
        self.orifice_thickness = orifice_thickness
        self.orifice_edge_radius = orifice_edge_radius
        self.orifice_centerline = orifice_centerline

        orifice_df = pd.DataFrame(columns=[

            "t/Dn",
            "Orifice Type",
            "K (based on orifice velocity)",
            "Headloss",
            "Flow Stable?",
            "Cavitation Status",
            "Pipe Velocity (v1)",
            "U/S Energy (H1)"
        ])

        orificeArea = calculate_Rectangular_area(orifice_width,orifice_height)
        orificeVelocity = flow_rate/orificeArea
        pipeArea = calculate_Rectangular_area(pipe_width,pipe_height)
        pipeVelocity = flow_rate/pipeArea
        print(f"Pipe Velocity {pipeVelocity}")
        print(f"Orifice Velocity {orificeVelocity}")
        nominalDia = 4*orificeArea/(2*(orifice_width+orifice_height))
        thickness_nominalDiaRatio= orifice_thickness/nominalDia
        orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
        tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
        Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
        sqrt = 2*(Rfactor**.5)
        orifice_pipeAreaRatio = orificeArea/pipeArea
        Permiability = Rfactor*((1-orifice_pipeAreaRatio)**.75)+(1-orifice_pipeAreaRatio)**2 + min(tau,sqrt)*((1-orifice_pipeAreaRatio)**1.375)+(0.01*orifice_thickness/nominalDia)
        print(f"{Permiability}")
        dH = Permiability*(orificeVelocity**2)/(2*9.81)
        Kin = dH*2*9.81/(pipeVelocity**2)
        orificeheight_PipeheightRatio = orifice_height/pipe_height
        upstream_Energy = dH + ds_energy_level
        hu = upstream_Energy - orifice_centerline
        hv = -8.6
        hs = hu - hv
        ref_IncipientCav = -10.84779 + (orificeheight_PipeheightRatio*68.5599) + (orificeheight_PipeheightRatio**2)*(-120.542) + (orificeheight_PipeheightRatio**3)*86.73617 
        ref_criticalCav = -4.06023 + (orificeheight_PipeheightRatio*31.04066) + (orificeheight_PipeheightRatio**2)*-56.82 + (orificeheight_PipeheightRatio**3)*58.9463
        ref_IncipientDam = -0.23091 + orificeheight_PipeheightRatio*12.55424 + (orificeheight_PipeheightRatio**2)*-26.4375 + (orificeheight_PipeheightRatio**3)*44.71988
        ref_ChokingCav = 11.79863 + orificeheight_PipeheightRatio*-57.22946 + (orificeheight_PipeheightRatio**2)*101.5848 + (orificeheight_PipeheightRatio**3)*-23.2237
        logK = math.log(Kin)
        logD = math.log(pipe_height)
        c = 0.595916742142878 + (0.0862736628857235*logK) + (-0.321334456683251*logD) + (0.0176435481517691*(logK**2)) + (0.0724573358221047*logK*logD) + (0.159738855911438*(logD**2)) + (0.00811998377973832*(logK**3)) + (0.0399142633228832*logK*logK*logD) + (0.045277311105048*logK*logD*logD) + (0.387474756840927*(logD**3)) + (-0.00419035434959079*(logK**4)) + (-0.00730504428453993*(logK**3)*logD) + (0.0209199559545679*(logD**2)*(logK**2)) +(0.0611565120535794*(logD**3)*logK) + (0.23542141447694*(logD**4))
        act_IncipientCav = ref_IncipientCav*c*((+hs/71.6)**.5)
        act_criticalCav = ref_criticalCav*c*((+hs/71.6)**.5)
        act_IncipientDam = ref_IncipientDam*((+hs/71.6)**.45)
        act_ChokingCav = ref_ChokingCav*((+hs/71.6)**.5)
        orificeType = 'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice'
        Headloss = upstream_Energy - ds_energy_level
        flowStable = 'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES'
        cavitation = "NA" if orifice_centerline==0 else "OUTSIDE RANGE" if orificeheight_PipeheightRatio<0.4 or orificeheight_PipeheightRatio>0.8 else "No Cavitation" if calculate_velocity(flow_rate, area=calculate_Rectangular_area(pipe_width,pipe_height))<act_IncipientCav else "Incipient Cavitation" if calculate_velocity(flow_rate, area=calculate_Rectangular_area(pipe_width,pipe_height))<act_criticalCav else "CRITICAL" if calculate_velocity(flow_rate, area=calculate_Rectangular_area(pipe_width,pipe_height))<act_IncipientDam else "INCIPIENT DAMAGE" if calculate_velocity(flow_rate, area=calculate_Rectangular_area(pipe_width,pipe_height))<act_ChokingCav else "CHOKING CAVITATION"
        print(f"Pipe Velocity {pipeVelocity}")
        print(f"Orifice Velocity {orificeVelocity}")
        orifice_df.loc[len(orifice_df)] = [

            round(thickness_nominalDiaRatio,3),
            orificeType,
            round(Permiability,3),
            round(Headloss,3),
            flowStable,
            cavitation,
            round(pipeVelocity,3),
            round(upstream_Energy,3)
        
        ]
        self.data = orifice_df
        self.component_type = 'Rectangular Orifice Passage'

class CircularEdgedOrificeInRectangularPipe:
    def __init__(self, flow_rate: float, width: float, height: float ,orifice_diametre: float, ds_energy_level:float, orifice_thickness:float, orifice_edge_radius: float, orifice_centerline: float):
        self.flow_rate = flow_rate
        self.width = width
        self.height = height
        self.orifice_diametre = orifice_diametre
        self.ds_energy_level = ds_energy_level
        self.orifice_thickness = orifice_thickness
        self.orifice_edge_radius = orifice_edge_radius
        self.orifice_centerline = orifice_centerline
        
        orifice_df = pd.DataFrame(columns=[

            "t/Dn",
            "Orifice Type",
            "K (based on orifice velocity)",
            "Headloss",
            "Flow Stable?",
            "Cavitation Status",
            "Pipe Velocity (v1)",
            "U/S Energy (H1)"
        ])
        orificeArea = calculate_circular_area(orifice_diametre)
        pipeArea = calculate_Rectangular_area(width,height)
        nominalDia = 4*orificeArea/((math.pi)*orifice_diametre)
        thickness_nominalDiaRatio= orifice_thickness/nominalDia
        orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
        tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
        Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
        sqrt = 2*(Rfactor**.5)
        orifice_pipeAreaRatio = orificeArea/pipeArea
        Permiability = Rfactor*((1-orifice_pipeAreaRatio)**.75)+(1-orifice_pipeAreaRatio)**2 + min(tau,sqrt)*((1-orifice_pipeAreaRatio)**1.375)+(0.01*orifice_thickness/nominalDia)
        print(f"{Permiability}")
        dH = Permiability*(calculate_velocity(flow_rate,orificeArea)**2)/(2*9.81)
        Kin = dH*2*9.81/(calculate_velocity(flow_rate,pipeArea)**2)
        orificeDia_PipeHeightRatio = orifice_diametre/height
        upstream_Energy = dH + ds_energy_level
        hu = upstream_Energy - orifice_centerline
        hv = -8.6
        hs = hu - hv
        ref_IncipientCav = -10.84779 + (orificeDia_PipeHeightRatio*68.5599) + (orificeDia_PipeHeightRatio**2)*(-120.542) + (orificeDia_PipeHeightRatio**3)*86.73617 
        ref_criticalCav = -4.06023 + (orificeDia_PipeHeightRatio*31.04066) + (orificeDia_PipeHeightRatio**2)*-56.82 + (orificeDia_PipeHeightRatio**3)*58.9463
        ref_IncipientDam = -0.23091 + orificeDia_PipeHeightRatio*12.55424 + (orificeDia_PipeHeightRatio**2)*-26.4375 + (orificeDia_PipeHeightRatio**3)*44.71988
        ref_ChokingCav = 11.79863 + orificeDia_PipeHeightRatio*-57.22946 + (orificeDia_PipeHeightRatio**2)*101.5848 + (orificeDia_PipeHeightRatio**3)*-23.2237
        logK = math.log(Kin)
        logD = math.log(height)
        c = 0.595916742142878 + (0.0862736628857235*logK) + (-0.321334456683251*logD) + (0.0176435481517691*(logK**2)) + (0.0724573358221047*logK*logD) + (0.159738855911438*(logD**2)) + (0.00811998377973832*(logK**3)) + (0.0399142633228832*logK*logK*logD) + (0.045277311105048*logK*logD*logD) + (0.387474756840927*(logD**3)) + (-0.00419035434959079*(logK**4)) + (-0.00730504428453993*(logK**3)*logD) + (0.0209199559545679*(logD**2)*(logK**2)) +(0.0611565120535794*(logD**3)*logK) + (0.23542141447694*(logD**4))
        act_IncipientCav = ref_IncipientCav*c*((+hs/71.6)**.5)
        act_criticalCav = ref_criticalCav*c*((+hs/71.6)**.5)
        act_IncipientDam = ref_IncipientDam*((+hs/71.6)**.45)
        act_ChokingCav = ref_ChokingCav*((+hs/71.6)**.5)
        orificeType = 'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice'
        Headloss = round(upstream_Energy - ds_energy_level,3)
        flowStable = 'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES'
        cavitation = "NA" if orifice_centerline==0 else "OUTSIDE RANGE" if orificeDia_PipeHeightRatio<0.4 or orificeDia_PipeHeightRatio>0.8 else "No Cavitation" if calculate_velocity(flow_rate, calculate_Rectangular_area(width,height))<act_IncipientCav else "Incipient Cavitation" if calculate_velocity(flow_rate, calculate_Rectangular_area(width,height))<act_criticalCav else "CRITICAL" if calculate_velocity(flow_rate, calculate_Rectangular_area(width,height))<act_IncipientDam else "INCIPIENT DAMAGE" if calculate_velocity(flow_rate, calculate_Rectangular_area(width,height))<act_ChokingCav else "CHOKING CAVITATION"

        orifice_df.loc[len(orifice_df)] = [

            round(thickness_nominalDiaRatio,3),
            orificeType,
            round(Permiability,3),
            round(Headloss,3),
            flowStable,
            cavitation,
            round(calculate_velocity(flow_rate, calculate_Rectangular_area(width,height)),3),
            round(upstream_Energy,3)
        
        ]
        self.data = orifice_df
        self.component_type = 'Circular Orifice in a Rectangular Pipe Passage'


class RectangularEdgedOrificeInCircularPipe:
    def __init__(self,flow_rate: float, diametre: float, orifice_width: float, orifice_height: float,ds_energy_level:float, orifice_thickness:float, orifice_edge_radius: float, orifice_centerline: float):
        self.flow_rate = flow_rate
        self.diametre = diametre
        self.orifice_width = orifice_width
        self.orifice_height = orifice_height
        self.ds_energy_level = ds_energy_level
        self.orifice_thickness = orifice_thickness
        self.orifice_edge_radius = orifice_edge_radius
        self.orifice_centerline = orifice_centerline

        orifice_df = pd.DataFrame(columns=[

            "t/Dn",
            "Orifice Type",
            "K (based on orifice velocity)",
            "Headloss",
            "Flow Stable?",
            "Cavitation Status",
            "Pipe Velocity (v1)",
            "U/S Energy (H1)"
        ])

        orificeArea = calculate_Rectangular_area(orifice_width,orifice_height)
        orificeVelocity = flow_rate/orificeArea
        pipeArea = calculate_circular_area(diametre)
        pipeVelocity = flow_rate/pipeArea
        print(f"Pipe Velocity {pipeVelocity}")
        print(f"Orifice Velocity {orificeVelocity}")
        nominalDia = 4*orificeArea/(2*(orifice_width+orifice_height))
        thickness_nominalDiaRatio= orifice_thickness/nominalDia
        orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
        tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
        Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
        sqrt = 2*(Rfactor**.5)
        orifice_pipeAreaRatio = orificeArea/pipeArea
        Permiability = Rfactor*((1-orifice_pipeAreaRatio)**.75)+(1-orifice_pipeAreaRatio)**2 + min(tau,sqrt)*((1-orifice_pipeAreaRatio)**1.375)+(0.01*orifice_thickness/nominalDia)
        print(f"{Permiability}")
        dH = Permiability*(orificeVelocity**2)/(2*9.81)
        Kin = dH*2*9.81/(pipeVelocity**2)
        orificeheight_PipeDiaRatio = orifice_height/diametre
        upstream_Energy = dH + ds_energy_level
        hu = upstream_Energy - orifice_centerline
        hv = -8.6
        hs = hu - hv
        ref_IncipientCav = -10.84779 + (orificeheight_PipeDiaRatio*68.5599) + (orificeheight_PipeDiaRatio**2)*(-120.542) + (orificeheight_PipeDiaRatio**3)*86.73617 
        ref_criticalCav = -4.06023 + (orificeheight_PipeDiaRatio*31.04066) + (orificeheight_PipeDiaRatio**2)*-56.82 + (orificeheight_PipeDiaRatio**3)*58.9463
        ref_IncipientDam = -0.23091 + orificeheight_PipeDiaRatio*12.55424 + (orificeheight_PipeDiaRatio**2)*-26.4375 + (orificeheight_PipeDiaRatio**3)*44.71988
        ref_ChokingCav = 11.79863 + orificeheight_PipeDiaRatio*-57.22946 + (orificeheight_PipeDiaRatio**2)*101.5848 + (orificeheight_PipeDiaRatio**3)*-23.2237
        logK = math.log(Kin)
        logD = math.log(diametre)
        c = 0.595916742142878 + (0.0862736628857235*logK) + (-0.321334456683251*logD) + (0.0176435481517691*(logK**2)) + (0.0724573358221047*logK*logD) + (0.159738855911438*(logD**2)) + (0.00811998377973832*(logK**3)) + (0.0399142633228832*logK*logK*logD) + (0.045277311105048*logK*logD*logD) + (0.387474756840927*(logD**3)) + (-0.00419035434959079*(logK**4)) + (-0.00730504428453993*(logK**3)*logD) + (0.0209199559545679*(logD**2)*(logK**2)) +(0.0611565120535794*(logD**3)*logK) + (0.23542141447694*(logD**4))
        act_IncipientCav = ref_IncipientCav*c*((+hs/71.6)**.5)
        act_criticalCav = ref_criticalCav*c*((+hs/71.6)**.5)
        act_IncipientDam = ref_IncipientDam*((+hs/71.6)**.45)
        act_ChokingCav = ref_ChokingCav*((+hs/71.6)**.5)
        orificeType = 'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice'
        Headloss = upstream_Energy - ds_energy_level
        flowStable = 'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES'
        cavitation = "NA" if orifice_centerline==0 else "OUTSIDE RANGE" if orificeheight_PipeDiaRatio<0.4 or orificeheight_PipeDiaRatio>0.8 else "No Cavitation" if calculate_velocity(flow_rate, calculate_circular_area(diametre))<act_IncipientCav else "Incipient Cavitation" if calculate_velocity(flow_rate, calculate_circular_area(diametre))<act_criticalCav else "CRITICAL" if calculate_velocity(flow_rate, calculate_circular_area(diametre))<act_IncipientDam else "INCIPIENT DAMAGE" if calculate_velocity(flow_rate, calculate_circular_area(diametre))<act_ChokingCav else "CHOKING CAVITATION"
        print(f"Pipe Velocity {pipeVelocity}")
        print(f"Orifice Velocity {orificeVelocity}")
        orifice_df.loc[len(orifice_df)] = [

            round(thickness_nominalDiaRatio,3),
            orificeType,
            round(Permiability,3),
            round(Headloss,3),
            flowStable,
            cavitation,
            round(pipeVelocity,3),
            round(upstream_Energy,3)
        
        ]
        self.data = orifice_df
        self.component_type = 'Rectangular Orifice Passage in Circular Pipe'