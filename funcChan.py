"""
Functions based on Chan 1985 kinetic reaction scheme for biomass pyrolysis. 
Reactions evaluated at some temperature.

Functions:
chan1 - primary reactions only
chan2 - primary reactions without moisture
chan3 - primary and secondary reactions
chan4 - primary and secondary reactions without moisture

Reference:
Chan, Kelbon, Krieger, 1985. Fuel, 64(11), pp.1505–1513.
"""

# Modules
# -----------------------------------------------------------------------------

import numpy as np

# Function - primary kinetic reactions from Table 2
# -----------------------------------------------------------------------------

def chan1(T, pw, pg, pt, pc, pm, pv, dt, i):
    """
    Primary kinetic reactions from Table 2.
    INPUTS:
    T = temperature, K
    pw = wood concentration, kg/m^3
    pg = gas concentration, kg/m^3
    pt = tar concentration, kg/m^3
    pc = char concentration, kg/m^3
    pm = moisture concentration, kg/m^3
    pv = water vapor concentration, kg/m^3
    dt = delta time, s
    i = index    
    OUTPUTS:
    pww = wood
    pgg = gas
    ptt = tar
    pcc = char
    pmm = moisture
    pvv = water vapor
    """
    
    R = 0.008314 # universal gas constant, kJ/mol*K
    
    # A = pre-factor (1/s) and E = activation energy (kJ/mol)
    A1 = 1.3e8;     E1 = 140    # wood -> gas
    A2 = 2e8;       E2 = 133    # wood -> tar
    A3 = 1.08e7;    E3 = 121    # wood -> char
    A4 = 5.13e6;    E4 = 87.9   # moisture -> water vapor
    
    # reaction rate constant for each reaction, 1/s
    K1 = A1 * np.exp(-E1 / (R * T))  # wood -> gas
    K2 = A2 * np.exp(-E2 / (R * T))  # wood -> tar
    K3 = A3 * np.exp(-E3 / (R * T))  # wood -> char
    K4 = A4 * np.exp(-E4 / (R * T))  # moisture -> water vapor
    
    # reaction rate for each reaction, rho/s
    rww = -(K1+K2+K3) * pw[i-1]     # wood rate
    rwg = K1 * pw[i-1]              # wood -> gas rate
    rwt = K2 * pw[i-1]              # wood -> tar rate
    rwc = K3 * pw[i-1]              # wood -> char rate
    rmw = K4 * pm[i-1]              # moisture -> water vapor rate
    
    # wood, gas, tar, char, moisture, water vapor concentrations 
    # as a density, kg/m^3
    pww = pw[i-1] + rww*dt          # wood
    pgg = pg[i-1] + rwg*dt          # gas
    ptt = pt[i-1] + rwt*dt          # tar
    pcc = pc[i-1] + rwc*dt          # char
    pmm = pm[i-1] - rmw*dt          # moisture
    pvv = pv[i-1] + rmw*dt          # water vapor
    
    # return the wood, gas, tar, char, moisture, water vapor concentrations 
    # as a density, kg/m^3
    return pww, pgg, ptt, pcc, pmm, pvv
    

# Function - primary kinetic reactions w/o moisture from Table 2
# -----------------------------------------------------------------------------

def chan2(T, pw, pg, pt, pc, dt, i):
    """
    Primary kinetic reactions w/o moisture from Table 2.
    INPUTS:
    T = temperature, K
    pw = wood concentration, kg/m^3
    pg = gas concentration, kg/m^3
    pt = tar concentration, kg/m^3
    pc = char concentration, kg/m^3
    dt = delta time, s
    i = index    
    OUTPUTS:
    pww = wood
    pgg = gas
    ptt = tar
    pcc = char
    """
    
    R = 0.008314 # universal gas constant, kJ/mol*K
    
    # A = pre-factor (1/s) and E = activation energy (kJ/mol)
    A1 = 1.3e8;     E1 = 140    # wood -> gas
    A2 = 2e8;       E2 = 133    # wood -> tar
    A3 = 1.08e7;    E3 = 121    # wood -> char
    
    # reaction rate constant for each reaction, 1/s
    K1 = A1 * np.exp(-E1 / (R * T))  # wood -> gas
    K2 = A2 * np.exp(-E2 / (R * T))  # wood -> tar
    K3 = A3 * np.exp(-E3 / (R * T))  # wood -> char
    
    # reaction rate for each reaction, rho/s
    rww = -(K1+K2+K3) * pw[i-1]     # wood rate
    rwg = K1 * pw[i-1]              # wood -> gas rate
    rwt = K2 * pw[i-1]              # wood -> tar rate
    rwc = K3 * pw[i-1]              # wood -> char rate
    
    # wood, gas, tar, char, moisture, water vapor concentrations 
    # as a density, kg/m^3
    pww = pw[i-1] + rww*dt          # wood
    pgg = pg[i-1] + rwg*dt          # gas
    ptt = pt[i-1] + rwt*dt          # tar
    pcc = pc[i-1] + rwc*dt          # char
    
    # return the wood, gas, tar, char, moisture, water vapor concentrations 
    # as a density, kg/m^3
    return pww, pgg, ptt, pcc


# Function - primary and secondary reactions from Table 2
# -----------------------------------------------------------------------------

def chan3(T, pw, pg, pt, pc, pm, pv, dt, i):
    """
    Primary and secondary reactions from Table 2.
    INPUTS:
    T = temperature, K
    pw = wood concentration, kg/m^3
    pg = gas concentration, kg/m^3
    pt = tar concentration, kg/m^3
    pc = char concentration, kg/m^3
    pm = moisture concentration, kg/m^3
    pv = water vapor concentration, kg/m^3
    dt = delta time, s
    i = index    
    OUTPUTS:
    pww = wood
    pgg = gas
    ptt = tar
    pcc = char
    pmm = moisture
    pvv = water vapor
    """
    
    R = 0.008314 # universal gas constant, kJ/mol*K
    
    # A = pre-factor (1/s) and E = activation energy (kJ/mol)
    A1 = 1.3e8;     E1 = 140    # wood -> gas1
    A2 = 2e8;       E2 = 133    # wood -> tar1
    A3 = 1.08e7;    E3 = 121    # wood -> char
    A4 = 5.13e6;    E4 = 87.9   # moisture -> water vapor
    A5 = 1.48e6;    E5 = 144    # tar -> gas2 + tar2
    
    # reaction rate constant for each reaction, 1/s
    K1 = A1 * np.exp(-E1 / (R * T))  # wood -> gas1
    K2 = A2 * np.exp(-E2 / (R * T))  # wood -> tar1
    K3 = A3 * np.exp(-E3 / (R * T))  # wood -> char
    K4 = A4 * np.exp(-E4 / (R * T))  # moisture -> water vapor
    K5 = A5 * np.exp(-E5 / (R * T))  # tar -> gas2 + tar2
    
    # reaction rate for each reaction, rho/s
    rww = -(K1+K2+K3) * pw[i-1]     # wood rate
    rwg = K1 * pw[i-1]              # wood -> gas rate
    rwt = K2 * pw[i-1]              # wood -> tar rate
    rwc = K3 * pw[i-1]              # wood -> char rate
    rmw = K4 * pm[i-1]              # moisture -> water vapor rate
    rtt = K5 * pt[i-1]              # tar -> gas2 + tar2 rate
    
    # wood, gas, tar, char, moisture, water vapor concentrations 
    # as a density, kg/m^3
    pww = pw[i-1] + rww*dt              # wood
    pgg = pg[i-1] + (rwg + 0.9*rtt)*dt  # gas
    ptt = pt[i-1] + (rwt + 0.1*rtt)*dt  # tar
    pcc = pc[i-1] + rwc*dt              # char
    pmm = pm[i-1] - rmw*dt              # moisture
    pvv = pv[i-1] + rmw*dt              # water vapor
    
    # return the wood, gas, tar, char, moisture, water vapor concentrations 
    # as a density, kg/m^3
    return pww, pgg, ptt, pcc, pmm, pvv
    
    
# Function - primary and secondary reactions w/o moisture from Table 2
# -----------------------------------------------------------------------------

def chan4(T, pw, pg, pt, pc, dt, i):
    """
    Primary and secondary reactions from Table 2.
    INPUTS:
    T = temperature, K
    pw = wood concentration, kg/m^3
    pg = gas concentration, kg/m^3
    pt = tar concentration, kg/m^3
    pc = char concentration, kg/m^3
    dt = delta time, s
    i = index    
    OUTPUTS:
    pww = wood
    pgg = gas
    ptt = tar
    pcc = char
    """
    
    R = 0.008314 # universal gas constant, kJ/mol*K
    
    # A = pre-factor (1/s) and E = activation energy (kJ/mol)
    A1 = 1.3e8;     E1 = 140    # wood -> gas1
    A2 = 2e8;       E2 = 133    # wood -> tar1
    A3 = 1.08e7;    E3 = 121    # wood -> char
    A5 = 1.48e6;    E5 = 144    # tar -> gas2 + tar2
    
    # reaction rate constant for each reaction, 1/s
    K1 = A1 * np.exp(-E1 / (R * T))  # wood -> gas1
    K2 = A2 * np.exp(-E2 / (R * T))  # wood -> tar1
    K3 = A3 * np.exp(-E3 / (R * T))  # wood -> char
    K5 = A5 * np.exp(-E5 / (R * T))  # tar -> gas2 + tar2
    
    # reaction rate for each reaction, rho/s
    rww = -(K1+K2+K3) * pw[i-1]     # wood rate
    rwg = K1 * pw[i-1]              # wood -> gas rate
    rwt = K2 * pw[i-1]              # wood -> tar rate
    rwc = K3 * pw[i-1]              # wood -> char rate
    rtt = K5 * pt[i-1]              # tar -> gas2 + tar2 rate
    
    # wood, gas, tar, char, moisture, water vapor concentrations 
    # as a density, kg/m^3
    pww = pw[i-1] + rww*dt              # wood
    pgg = pg[i-1] + (rwg + 0.9*rtt)*dt  # gas
    ptt = pt[i-1] + (rwt + 0.1*rtt)*dt  # tar
    pcc = pc[i-1] + rwc*dt              # char
    
    # return the wood, gas, tar, char, moisture, water vapor concentrations 
    # as a density, kg/m^3
    return pww, pgg, ptt, pcc
    
    