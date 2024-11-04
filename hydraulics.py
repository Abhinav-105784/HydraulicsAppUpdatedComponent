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

class SharpEdgedOrifice:
    def __init__(self, flow_rate: float, diametre, orifice_diametre,pipe_width, pipe_height,orifice_width,orifice_height ,ds_energy_level:float, orifice_thickness:float, orifice_edge_radius: float, orifice_centerline: float):
        self.flow_rate = flow_rate
        self.diametre = diametre
        self.orifice_diametre = orifice_diametre
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
        def CircularEdgeOrifice():
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
         return orifice_df
        

        def RectangularEdgedOrifice():

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
         return orifice_df
        

        def CircularEdgedOrificeInRectangularPipe():
    
         orificeArea = calculate_circular_area(orifice_diametre)
         pipeArea = calculate_Rectangular_area(pipe_width,pipe_height)
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
         orificeDia_PipeHeightRatio = orifice_diametre/pipe_height
         upstream_Energy = dH + ds_energy_level
         hu = upstream_Energy - orifice_centerline
         hv = -8.6
         hs = hu - hv
         ref_IncipientCav = -10.84779 + (orificeDia_PipeHeightRatio*68.5599) + (orificeDia_PipeHeightRatio**2)*(-120.542) + (orificeDia_PipeHeightRatio**3)*86.73617 
         ref_criticalCav = -4.06023 + (orificeDia_PipeHeightRatio*31.04066) + (orificeDia_PipeHeightRatio**2)*-56.82 + (orificeDia_PipeHeightRatio**3)*58.9463
         ref_IncipientDam = -0.23091 + orificeDia_PipeHeightRatio*12.55424 + (orificeDia_PipeHeightRatio**2)*-26.4375 + (orificeDia_PipeHeightRatio**3)*44.71988
         ref_ChokingCav = 11.79863 + orificeDia_PipeHeightRatio*-57.22946 + (orificeDia_PipeHeightRatio**2)*101.5848 + (orificeDia_PipeHeightRatio**3)*-23.2237
         logK = math.log(Kin)
         logD = math.log(pipe_height)
         c = 0.595916742142878 + (0.0862736628857235*logK) + (-0.321334456683251*logD) + (0.0176435481517691*(logK**2)) + (0.0724573358221047*logK*logD) + (0.159738855911438*(logD**2)) + (0.00811998377973832*(logK**3)) + (0.0399142633228832*logK*logK*logD) + (0.045277311105048*logK*logD*logD) + (0.387474756840927*(logD**3)) + (-0.00419035434959079*(logK**4)) + (-0.00730504428453993*(logK**3)*logD) + (0.0209199559545679*(logD**2)*(logK**2)) +(0.0611565120535794*(logD**3)*logK) + (0.23542141447694*(logD**4))
         act_IncipientCav = ref_IncipientCav*c*((+hs/71.6)**.5)
         act_criticalCav = ref_criticalCav*c*((+hs/71.6)**.5)
         act_IncipientDam = ref_IncipientDam*((+hs/71.6)**.45)
         act_ChokingCav = ref_ChokingCav*((+hs/71.6)**.5)
         orificeType = 'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice'
         Headloss = round(upstream_Energy - ds_energy_level,3)
         flowStable = 'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES'
         cavitation = "NA" if orifice_centerline==0 else "OUTSIDE RANGE" if orificeDia_PipeHeightRatio<0.4 or orificeDia_PipeHeightRatio>0.8 else "No Cavitation" if calculate_velocity(flow_rate, pipeArea)<act_IncipientCav else "Incipient Cavitation" if calculate_velocity(flow_rate, pipeArea)<act_criticalCav else "CRITICAL" if calculate_velocity(flow_rate, pipeArea)<act_IncipientDam else "INCIPIENT DAMAGE" if calculate_velocity(flow_rate, pipeArea)<act_ChokingCav else "CHOKING CAVITATION"

         orifice_df.loc[len(orifice_df)] = [

            round(thickness_nominalDiaRatio,3),
            orificeType,
            round(Permiability,3),
            round(Headloss,3),
            flowStable,
            cavitation,
            round(calculate_velocity(flow_rate, pipeArea),3),
            round(upstream_Energy,3)
        
        ]
         return orifice_df

        def RectangularEdgedOrificeInCircularPipe():
    
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
         return orifice_df
        
        if diametre != None and orifice_diametre != None:
            self.data = CircularEdgeOrifice()
            self.component_type = 'Circular Orifice Passage'
        elif pipe_width != None and pipe_height != None and orifice_width != None and orifice_height != None:
            self.data = RectangularEdgedOrifice()
            self.component_type = 'Rectangular Orifice Passage'
        elif pipe_width != None and pipe_height != None and orifice_diametre != None:
            self.data = CircularEdgedOrificeInRectangularPipe()
            self.component_type = 'Circular Orifice in a Rectangular Pipe Passage'
        elif diametre!= None and orifice_width!=None and orifice_height != None:
            self.data = RectangularEdgedOrificeInCircularPipe()
            self.component_type = 'Rectangular Orifice Passage in Circular Pipe'

class GeneralSubmergedConstriction:
    def __init__(self, flow_rate, diametre1, diametre2 ,orifice_diametre,width1, height1,width2,height2 ,orifice_width,orifice_height ,ds_energy_level:float, orifice_thickness:float, orifice_edge_radius: float):
        self.flow_rate = flow_rate
        self.diametre1= diametre1
        self.diametre2 = diametre2
        self.width1=width1
        self.height1 = height1
        self.width2 = width2
        self.height2 = height2
        self.orifice_width = orifice_width
        self.orifice_height = orifice_height
        self.orifice_diametre = orifice_diametre
        self.ds_energy_level = ds_energy_level
        self.orifice_thickness = orifice_thickness
        self.orifice_edge_radius = orifice_edge_radius

        GeneralSubmergedConstriction_df = pd.DataFrame(columns=[
            "t/Dn",
            "Orifice Type",
            "Permiability based on orifice Velocity",
            "Headloss",
            "Flow Stable?",
            "Inlet Velocity(V1)",
            "Upstream Energy(H1)"

        ])
 
        def AllCircular():
         orificeArea = calculate_circular_area(orifice_diametre)
         pipeArea1 = calculate_circular_area(diametre1)
         pipeArea2 = calculate_circular_area(diametre2)
         orificeVelocity = calculate_velocity(flow_rate,orificeArea)
         inletVelocity = calculate_velocity(flow_rate,pipeArea1)
         outletVelocity = calculate_velocity(flow_rate,pipeArea2)
         orifice_inletAreaRatio = orificeArea/pipeArea1
         orifice_outLetAreaRatio = orificeArea/pipeArea2
         nominalDia = 4*orificeArea/((math.pi)*orifice_diametre)
         thickness_nominalDiaRatio= orifice_thickness/nominalDia
         orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
         tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
         Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
         sqrt = 2*(Rfactor**.5)
         permiability = Rfactor*((1-orifice_inletAreaRatio)**.75)+(1-orifice_outLetAreaRatio)**2+min(tau,sqrt)*(((1-orifice_outLetAreaRatio)*(1-orifice_inletAreaRatio))**.375)+(0.01*thickness_nominalDiaRatio)
         dH = permiability*(orificeVelocity**2/(2*9.81))
         Kin = dH*2*9.81/(inletVelocity**2)
         upstream_Energy = dH + ds_energy_level

         GeneralSubmergedConstriction_df.loc[len(GeneralSubmergedConstriction_df)]=[
            round(thickness_nominalDiaRatio,3),
            'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice',
            round(permiability,3),
            round(upstream_Energy-ds_energy_level,3),
            'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES',
            round(inletVelocity,3),
            round(upstream_Energy,3)

        ]
         return GeneralSubmergedConstriction_df
        
        
        def AllRectangular():
          print("hello 2")
          orificeArea = calculate_Rectangular_area(orifice_width,orifice_height)
          pipeArea1 = calculate_Rectangular_area(width1,height1)
          pipeArea2 = calculate_Rectangular_area(width2,height2)
          orificeVelocity = calculate_velocity(flow_rate,orificeArea)
          inletVelocity = calculate_velocity(flow_rate,pipeArea1)
          outletVelocity = calculate_velocity(flow_rate,pipeArea2)
          orifice_inletAreaRatio = orificeArea/pipeArea1
          orifice_outLetAreaRatio = orificeArea/pipeArea2
          nominalDia = 4*orificeArea/(2*(orifice_width+orifice_height))
          thickness_nominalDiaRatio= orifice_thickness/nominalDia
          orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
          tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
          Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
          sqrt = 2*(Rfactor**.5)
          permiability = Rfactor*((1-orifice_inletAreaRatio)**.75)+(1-orifice_outLetAreaRatio)**2+min(tau,sqrt)*(((1-orifice_outLetAreaRatio)*(1-orifice_inletAreaRatio))**.375)+(0.01*thickness_nominalDiaRatio)
          dH = permiability*(orificeVelocity**2/(2*9.81))
          Kin = dH*2*9.81/(inletVelocity**2)
          upstream_Energy = dH + ds_energy_level

          GeneralSubmergedConstriction_df.loc[len(GeneralSubmergedConstriction_df)]=[
            round(thickness_nominalDiaRatio,3),
            'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice',
            round(permiability,3),
            round(upstream_Energy-ds_energy_level,3),
            'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES',
            round(inletVelocity,3),
            round(upstream_Energy,3)

        ]  
          return GeneralSubmergedConstriction_df
        
        def case3():
            orificeArea = calculate_circular_area(orifice_diametre)
            pipeArea1 = calculate_Rectangular_area(width1,height1)
            pipeArea2 = calculate_circular_area(diametre2)
            orificeVelocity = calculate_velocity(flow_rate,orificeArea)
            inletVelocity = calculate_velocity(flow_rate,pipeArea1)
            outletVelocity = calculate_velocity(flow_rate,pipeArea2)
            orifice_inletAreaRatio = orificeArea/pipeArea1
            orifice_outLetAreaRatio = orificeArea/pipeArea2
            nominalDia = 4*orificeArea/((math.pi)*orifice_diametre)
            thickness_nominalDiaRatio= orifice_thickness/nominalDia
            orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
            tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
            Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
            sqrt = 2*(Rfactor**.5)
            permiability = Rfactor*((1-orifice_inletAreaRatio)**.75)+(1-orifice_outLetAreaRatio)**2+min(tau,sqrt)*(((1-orifice_outLetAreaRatio)*(1-orifice_inletAreaRatio))**.375)+(0.01*thickness_nominalDiaRatio)
            dH = permiability*(orificeVelocity**2/(2*9.81))
            Kin = dH*2*9.81/(inletVelocity**2)
            upstream_Energy = dH + ds_energy_level

            GeneralSubmergedConstriction_df.loc[len(GeneralSubmergedConstriction_df)]=[
            round(thickness_nominalDiaRatio,3),
            'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice',
            round(permiability,3),
            round(upstream_Energy-ds_energy_level,3),
            'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES',
            round(inletVelocity,3),
            round(upstream_Energy,3)

        ]  
            return GeneralSubmergedConstriction_df
        
        def case4():
          orificeArea = calculate_Rectangular_area(orifice_width,orifice_height)
          pipeArea1 = calculate_Rectangular_area(width1,height1)
          pipeArea2 = calculate_circular_area(diametre2)
          orificeVelocity = calculate_velocity(flow_rate,orificeArea)
          inletVelocity = calculate_velocity(flow_rate,pipeArea1)
          outletVelocity = calculate_velocity(flow_rate,pipeArea2)
          orifice_inletAreaRatio = orificeArea/pipeArea1
          orifice_outLetAreaRatio = orificeArea/pipeArea2
          nominalDia = 4*orificeArea/(2*(orifice_width+orifice_height))
          thickness_nominalDiaRatio= orifice_thickness/nominalDia
          orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
          tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
          Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
          sqrt = 2*(Rfactor**.5)
          permiability = Rfactor*((1-orifice_inletAreaRatio)**.75)+(1-orifice_outLetAreaRatio)**2+min(tau,sqrt)*(((1-orifice_outLetAreaRatio)*(1-orifice_inletAreaRatio))**.375)+(0.01*thickness_nominalDiaRatio)
          dH = permiability*(orificeVelocity**2/(2*9.81))
          Kin = dH*2*9.81/(inletVelocity**2)
          upstream_Energy = dH + ds_energy_level

          GeneralSubmergedConstriction_df.loc[len(GeneralSubmergedConstriction_df)]=[
            round(thickness_nominalDiaRatio,3),
            'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice',
            round(permiability,3),
            round(upstream_Energy-ds_energy_level,3),
            'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES',
            round(inletVelocity,3),
            round(upstream_Energy,3)

        ]  
          return GeneralSubmergedConstriction_df
        
        
        def case5():
         orificeArea = calculate_circular_area(orifice_diametre)
         pipeArea1 = calculate_circular_area(diametre1)
         pipeArea2 = calculate_Rectangular_area(width2,height2)
         orificeVelocity = calculate_velocity(flow_rate,orificeArea)
         inletVelocity = calculate_velocity(flow_rate,pipeArea1)
         outletVelocity = calculate_velocity(flow_rate,pipeArea2)
         orifice_inletAreaRatio = orificeArea/pipeArea1
         orifice_outLetAreaRatio = orificeArea/pipeArea2
         nominalDia = 4*orificeArea/((math.pi)*orifice_diametre)
         thickness_nominalDiaRatio= orifice_thickness/nominalDia
         orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
         tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
         Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
         sqrt = 2*(Rfactor**.5)
         permiability = Rfactor*((1-orifice_inletAreaRatio)**.75)+(1-orifice_outLetAreaRatio)**2+min(tau,sqrt)*(((1-orifice_outLetAreaRatio)*(1-orifice_inletAreaRatio))**.375)+(0.01*thickness_nominalDiaRatio)
         dH = permiability*(orificeVelocity**2/(2*9.81))
         Kin = dH*2*9.81/(inletVelocity**2)
         upstream_Energy = dH + ds_energy_level

         GeneralSubmergedConstriction_df.loc[len(GeneralSubmergedConstriction_df)]=[
            round(thickness_nominalDiaRatio,3),
            'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice',
            round(permiability,3),
            round(upstream_Energy-ds_energy_level,3),
            'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES',
            round(inletVelocity,3),
            round(upstream_Energy,3)

        ]
         return GeneralSubmergedConstriction_df 
        
        
        def case6():
            orificeArea = calculate_Rectangular_area(orifice_width,orifice_height)
            pipeArea1 = calculate_circular_area(diametre1)
            pipeArea2 = calculate_Rectangular_area(width2,height2)
            orificeVelocity = calculate_velocity(flow_rate,orificeArea)
            inletVelocity = calculate_velocity(flow_rate,pipeArea1)
            outletVelocity = calculate_velocity(flow_rate,pipeArea2)
            orifice_inletAreaRatio = orificeArea/pipeArea1
            orifice_outLetAreaRatio = orificeArea/pipeArea2
            nominalDia = 4*orificeArea/(2*(orifice_width+orifice_height))
            thickness_nominalDiaRatio= orifice_thickness/nominalDia
            orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
            tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
            Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
            sqrt = 2*(Rfactor**.5)
            permiability = Rfactor*((1-orifice_inletAreaRatio)**.75)+(1-orifice_outLetAreaRatio)**2+min(tau,sqrt)*(((1-orifice_outLetAreaRatio)*(1-orifice_inletAreaRatio))**.375)+(0.01*thickness_nominalDiaRatio)
            dH = permiability*(orificeVelocity**2/(2*9.81))
            Kin = dH*2*9.81/(inletVelocity**2)
            upstream_Energy = dH + ds_energy_level

            GeneralSubmergedConstriction_df.loc[len(GeneralSubmergedConstriction_df)]=[
            round(thickness_nominalDiaRatio,3),
            'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice',
            round(permiability,3),
            round(upstream_Energy-ds_energy_level,3),
            'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES',
            round(inletVelocity,3),
            round(upstream_Energy,3)

        ]  
            return GeneralSubmergedConstriction_df
        

        def case7():
           orificeArea = calculate_Rectangular_area(orifice_width,orifice_height)
           pipeArea1 = calculate_circular_area(diametre1)
           pipeArea2 = calculate_circular_area(diametre2)
           orificeVelocity = calculate_velocity(flow_rate,orificeArea)
           inletVelocity = calculate_velocity(flow_rate,pipeArea1)
           outletVelocity = calculate_velocity(flow_rate,pipeArea2)
           orifice_inletAreaRatio = orificeArea/pipeArea1
           orifice_outLetAreaRatio = orificeArea/pipeArea2
           nominalDia = 4*orificeArea/(2*(orifice_width+orifice_height))
           thickness_nominalDiaRatio= orifice_thickness/nominalDia
           orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
           tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
           Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
           sqrt = 2*(Rfactor**.5)
           permiability = Rfactor*((1-orifice_inletAreaRatio)**.75)+(1-orifice_outLetAreaRatio)**2+min(tau,sqrt)*(((1-orifice_outLetAreaRatio)*(1-orifice_inletAreaRatio))**.375)+(0.01*thickness_nominalDiaRatio)
           dH = permiability*(orificeVelocity**2/(2*9.81))
           Kin = dH*2*9.81/(inletVelocity**2)
           upstream_Energy = dH + ds_energy_level

           GeneralSubmergedConstriction_df.loc[len(GeneralSubmergedConstriction_df)]=[
            round(thickness_nominalDiaRatio,3),
            'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice',
            round(permiability,3),
            round(upstream_Energy-ds_energy_level,3),
            'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES',
            round(inletVelocity,3),
            round(upstream_Energy,3)

        ]  
           return GeneralSubmergedConstriction_df
        
        
        def case8():
           orificeArea = calculate_circular_area(orifice_diametre) 
           pipeArea1 = calculate_Rectangular_area(width1,height1)
           pipeArea2 = calculate_Rectangular_area(width2,height2)
           orificeVelocity = calculate_velocity(flow_rate,orificeArea)
           inletVelocity = calculate_velocity(flow_rate,pipeArea1)
           outletVelocity = calculate_velocity(flow_rate,pipeArea2)
           orifice_inletAreaRatio = orificeArea/pipeArea1
           orifice_outLetAreaRatio = orificeArea/pipeArea2
           nominalDia = 4*orificeArea/((math.pi)*orifice_diametre)
           thickness_nominalDiaRatio= orifice_thickness/nominalDia
           orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
           tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
           Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
           sqrt = 2*(Rfactor**.5)
           permiability = Rfactor*((1-orifice_inletAreaRatio)**.75)+(1-orifice_outLetAreaRatio)**2+min(tau,sqrt)*(((1-orifice_outLetAreaRatio)*(1-orifice_inletAreaRatio))**.375)+(0.01*thickness_nominalDiaRatio)
           dH = permiability*(orificeVelocity**2/(2*9.81))
           Kin = dH*2*9.81/(inletVelocity**2)
           upstream_Energy = dH + ds_energy_level

           GeneralSubmergedConstriction_df.loc[len(GeneralSubmergedConstriction_df)]=[
            round(thickness_nominalDiaRatio,3),
            'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice',
            round(permiability,3),
            round(upstream_Energy-ds_energy_level,3),
            'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES',
            round(inletVelocity,3),
            round(upstream_Energy,3)

        ]
           return GeneralSubmergedConstriction_df
        
        if diametre1 != None and diametre2 !=None and orifice_diametre !=None:
            self.component_type = "Circular General Submerged Constriction"
            self.data =  AllCircular
        elif width1!=None and width2 !=None and orifice_width!=None:
            self.component_type = "Rectangular General Submerged Constriction"
            self.data = AllRectangular()
        elif width1!= None and diametre2!=None and orifice_diametre!=None:
            self.component_type = "Upstream Rectangular rest Circular"
            self.data = case3()
        elif width1!=0 and diametre2!=0 and orifice_width!=0:
            self.component_type="Downstream Circular Rest Rectangular"
            self.data = case4()
        elif diametre1!=0 and width2!=0 and orifice_diametre!=0:
            self.component_type="Downstream Rectangular Rest Circular"
            self.data= case5()
        elif diametre1!=0 and width2!=0 and orifice_width!=0:
            self.component_type="Upstream Circular Rest Rectangular"
            self.data = case6()
        elif diametre1!=0 and diametre2!=0 and orifice_width!=0:
            self.component_type="Only Orifice Rectangular"
            self.data = case7()
        elif width1!=0 and width2!=0 and orifice_diametre!=0:
            self.component_type="Only Orifice Circular"
            self.data=case8()
        
        
        
class CriticalDepthControl:
    def __init__(self,flow_rate : float, ds_energy_level: float, invertLevel: float,copingLevel: float, modularLimit: float ,width: float, 
                 diameter: float, sideAngle: float):
        self.flow_rate = flow_rate
        self.ds_energy_level = ds_energy_level
        self.invertLevel = invertLevel
        self.copingLevel = copingLevel
        self.modularLimit = modularLimit
        self.width = width
        self.diameter = diameter
        self.sideAngle = sideAngle

        CriticalDepthControl_df = pd.DataFrame(columns=[
            "Freeboard (m)",
            "Critical Depth (m)",
            "Area",
            "theta_c",
            "Numerator",
            "Denominator",
            "Converged?",
            "Drowned?",
            "Velocity (V1)",
            "Water Level (W1)",
            "Eenergy (E1)"
        ])

        def CircularSection():
            area = calculate_circular_area(diameter)
            y_est = 0.5*diameter*(1-math.cos((math.pi)/2))
            area_est = .125*(diameter**2)*(math.pi- math.sin(math.pi))
            numerator = flow_rate**2*diameter*math.sin(math.pi/2)-(9.81*(area_est**3))
            denominator = flow_rate**2*0.5*diameter*math.cos(math.pi/2) - (.375*9.81*(area_est**2)*(diameter**2)*(1-math.cos(math.pi)))
            theta_est = math.pi-(numerator/denominator)

            tolerance = .000001
            max_iteration = 1000
            iteration = 0

            while(iteration< max_iteration):
               area_est = .125*(diameter**2)*(theta_est-math.sin(theta_est))
               numerator = flow_rate**2*diameter*math.sin(theta_est/2)-(9.81*(area_est**3))
               denominator = flow_rate**2*0.5*diameter*math.cos(theta_est/2) - (.375*9.81*(area_est**2)*(diameter**2)*(1-math.cos(theta_est)))
               y_est = 0.5*diameter*(1-math.cos((theta_est)/2))
               theta_est = theta_est-(numerator/denominator)

               if(abs)(area_est-area)<=tolerance:
                   break
               else:
                   iteration+=1
            criticat_Depth = y_est
            waterLevel = criticat_Depth + invertLevel
            top_width = diameter*math.sin(theta_est/2)
            flow_rate_calc = ((area_est**3)*9.81/top_width)**.5
            velocity = flow_rate_calc/area_est
            energyLevel = waterLevel +((velocity**2)/(2*9.81))

            CriticalDepthControl_df.loc[len(CriticalDepthControl_df)]=[
                "N/A" if copingLevel ==0 else round(copingLevel-waterLevel,3),
                round(y_est,3),
                round(area_est,3),
                round(theta_est,3),
                numerator,
                denominator,
                "Error" if ((flow_rate_calc - flow_rate)/flow_rate) > 0.0001 else "OK",
                "YES " if ((energyLevel-invertLevel)*modularLimit<(ds_energy_level-invertLevel)) else "NO",
                round(velocity,3),
                round(waterLevel,3),
                round(energyLevel,3)
            ]

            return  CriticalDepthControl_df
        
        self.dataCircular = CircularSection()

        def RectangularSection():
            pass

               


               








# class GeneralSubmergedConstrictionRectangular:

#     def __init__(self, flow_rate: float, width1: float, height1:float,width2: float,height2:float ,orifice_width: float,orifice_height:float, ds_energy_level:float, orifice_thickness:float, orifice_edge_radius: float):
#         self.flow_rate = flow_rate
#         self.width1=width1
#         self.height1 = height1
#         self.width2 = width2
#         self.height2 = height2
#         self.orifice_width = orifice_width
#         self.orifice_height = orifice_height
#         self.ds_energy = ds_energy_level
#         self.orifice_thickness = orifice_thickness
#         self.orifice_edge_radius = orifice_edge_radius

#         GeneralSubmergedConstrictionCircular_df = pd.DataFrame(columns=[
#             "t/Dn",
#             "Orifice Type",
#             "Permiability based on orifice Velocity",
#             "Headloss",
#             "Flow Stable?",
#             "Inlet Velocity(V1)",
#             "Upstream Energy(H1)"

#         ])

#         orificeArea = calculate_Rectangular_area(orifice_width,orifice_height)
#         pipeArea1 = calculate_Rectangular_area(width1,height1)
#         pipeArea2 = calculate_Rectangular_area(width2,height2)
#         orificeVelocity = calculate_velocity(flow_rate,orificeArea)
#         inletVelocity = calculate_velocity(flow_rate,pipeArea1)
#         outletVelocity = calculate_velocity(flow_rate,pipeArea2)
#         orifice_inletAreaRatio = orificeArea/pipeArea1
#         orifice_outLetAreaRatio = orificeArea/pipeArea2
#         nominalDia = 4*orificeArea/(2*(orifice_width+orifice_height))
#         thickness_nominalDiaRatio= orifice_thickness/nominalDia
#         orificeRadius_DiametreRatio = orifice_edge_radius/nominalDia
#         tau = max(0,(2.4-thickness_nominalDiaRatio)*(10**(-(.25+(.535*thickness_nominalDiaRatio**8/(.05+(thickness_nominalDiaRatio**8)))))))
#         Rfactor = 0.03+(.47*10**(-7.7*orificeRadius_DiametreRatio))
#         sqrt = 2*(Rfactor**.5)
#         permiability = Rfactor*((1-orifice_inletAreaRatio)**.75)+(1-orifice_outLetAreaRatio)**2+min(tau,sqrt)*(((1-orifice_outLetAreaRatio)*(1-orifice_inletAreaRatio))**.375)+(0.01*thickness_nominalDiaRatio)
#         dH = permiability*(orificeVelocity**2/(2*9.81))
#         Kin = dH*2*9.81/(inletVelocity**2)
#         upstream_Energy = dH + ds_energy_level

#         GeneralSubmergedConstrictionCircular_df.loc[len(GeneralSubmergedConstrictionCircular_df)]=[
#             round(thickness_nominalDiaRatio,3),
#             'Thin Orifice' if thickness_nominalDiaRatio <0.1 else 'Long Orifice',
#             round(permiability,3),
#             round(upstream_Energy-ds_energy_level,3),
#             'NO' if thickness_nominalDiaRatio>=0.1 and thickness_nominalDiaRatio<=.8 else 'YES',
#             round(inletVelocity,3),
#             round(upstream_Energy,3)

#         ]

#         self.data = GeneralSubmergedConstrictionCircular_df
#         self.component_type = 'Rectangular General Submerged Constriction'

# class GeneralSubmergedConstrictionCase3:
#     def __init__():




        