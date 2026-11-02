"""Calculations for the lab: synthesis masses, washing solutions, electrode sheet casting."""

import numpy as np


def Calculate_NCM_Mass_For_AES(CAM_informations):
    """Mass of NCM (g) to weigh in for AES solutions with the target concentrations of B, Ni, Li and Zn that are set in the code (mg/L, mL); results are printed.
    CAM_informations = [Ni ratio, Co ratio, Mn ratio] (molar, sum 1)."""
    nickel_ratio = CAM_informations[0]
    cobalt_ratio = CAM_informations[1]
    manganese_ratio = CAM_informations[2]
        
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_tantalum = 180.94788 # g/mol
    molar_mass_bor = 10.811 # g/mol
    molar_mass_zinc = 65.409 # g/mol
    
    # Information
    print('---------------------------------------')
    print('Claculating the Amount of NCM neccesary to obtain a 5-50 mg/L Solution of Bor within 25 mL')
    
    # Mol of Bor in 10 mL solution
    concentration_bor_in_mgL = 25
    concentration_bor_in_gL = concentration_bor_in_mgL/1000
    volume_solution_in_mL = 25
    volume_solution_in_L = volume_solution_in_mL/1000
    mass_bor = concentration_bor_in_gL * volume_solution_in_L
    mol_bor = mass_bor/molar_mass_bor
    print('This amount of Bor is needed for a concetration of %s mg/L and a Volume of %s mL : %s mol' %(concentration_bor_in_mgL, volume_solution_in_mL, mol_bor))
    
    # Amount of NCM needed
    molar_mass_NCM = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + 2 * molar_mass_oxygen + molar_mass_lithium
    expected_ratio_of_TM_and_bor = 0.02
    mol_NCM = mol_bor / expected_ratio_of_TM_and_bor
    mass_NCM = mol_NCM * molar_mass_NCM
    print('the expected amount of Bor in the sample is set to: %s molPercent' %(expected_ratio_of_TM_and_bor * 100))
    print("Mass of NCM needed in g: %s" %(mass_NCM))
    print('---------------------------------------')
    
    
    # Mol of Ni in 20 mL solution
    concentration_Element_in_mgL = 25
    concentration_Element_in_gL = concentration_Element_in_mgL/1000
    volume_solution_in_mL = 25
    volume_solution_in_L = volume_solution_in_mL/1000
    mass_Element = concentration_bor_in_gL * volume_solution_in_L
    mol_Ni = mass_bor/molar_mass_nickel
    mol_Li = mass_Element/molar_mass_lithium
    mol_Zn = (mass_Element/molar_mass_zinc)/0.02
    print('This amount of Nickel is needed for a concetration of %s mg/L and a Volume of %s mL : %s mol' %(concentration_Element_in_mgL, volume_solution_in_mL, mol_Ni))
    print('This amount of Lithium is needed for a concetration of %s mg/L and a Volume of %s mL : %s mol' %(concentration_Element_in_mgL, volume_solution_in_mL, mol_Li))
    print('This amount of Zinc is needed for a concetration of %s mg/L and a Volume of %s mL : %s mol' %(concentration_Element_in_mgL, volume_solution_in_mL, mol_Zn))
    
    # Amount of NCM needed for ...
    molar_mass_NCM = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + 2 * molar_mass_oxygen + molar_mass_lithium
    # Ni
    mass_NCM_Ni = mol_Ni * molar_mass_NCM
    print("Mass of NCM needed in g: %s" %(mass_NCM_Ni))
    # Li
    mass_NCM_Li = mol_Li * molar_mass_NCM
    print("Mass of NCM needed in g: %s" %(mass_NCM_Li))
    # Zn
    mass_NCM_Zn = mol_Zn * molar_mass_NCM
    print("Mass of NCM needed in g: %s" %(mass_NCM_Zn))
    print('---------------------------------------')
    
    return


def Calculate_Mol_NCM(CAM_informations, additional_informations=True, Coating_to_NCM_ratio=0.01):
    """Amount of NCM (mol) and the masses of coating reagents (e.g. Ta(EtO)5, Li metal / EtOLi in EtOH, Li3InCl6, LiCl); results are printed.
    CAM_informations = [NCM mass in g, Ni ratio, Co ratio, Mn ratio]; Coating_to_NCM_ratio = coating amount relative to NCM (0.01 = 1 %);
    additional_informations = print more details."""
    mass_NCM = CAM_informations[0]
    nickel_ratio = CAM_informations[1]
    cobalt_ratio = CAM_informations[2]
    manganese_ratio = CAM_informations[3]
        
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_tantalum = 180.94788
    molar_mass_indium = 114.818 # g/mol
    molar_mass_chloride = 35.453 # g/mol
    molar_mass_bor = 10.811 # g/mol
    molar_mass_zinc = 65.409 # g/mol
    
    # Information
    print('Claculating the Amount of coating Material')
    print('------------------------------------------')
    
    
    # densities
    density_ethanol = 0.789 # g/mL
    density_water = 1.000 # g/mL
        
    # molar mass and mol of the wanted NCM
    molar_mass_NCM = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + 2 * molar_mass_oxygen + molar_mass_lithium
    
    mol_NCM = mass_NCM / molar_mass_NCM
    
    # mol and weight of the TaEtO5 correspodning to 20%mol Ta:Tm ratio
    print('The Coating to NCM ratio is set to %s percent' %(Coating_to_NCM_ratio*100))
    print('------------------------------------------')
    
    print('Ta(EtO)5 coating:')
    mol_tantalum = mol_NCM * Coating_to_NCM_ratio
    molar_mass_TaEtO5 = molar_mass_tantalum + 5 * (2 * molar_mass_carbon + 5 * molar_mass_hydrogen + molar_mass_oxygen)
    mass_TaEtO5 = mol_tantalum * molar_mass_TaEtO5
    print('The mass for Ta(EtO)5 is: %s g' %(mass_TaEtO5))
    
    # mol and weight of the lithium corresponding to 1:1 Ta:Li ratio
    mol_Li = mol_tantalum
    mass_Li = mol_Li * molar_mass_lithium
    print('mass Li metal %s g' %(mass_Li))
    
    # mass and volume of Ethanol for converting all Li to pure LiEtO
    mass_EtOH =  mol_Li * (2 * molar_mass_carbon + 6 * molar_mass_hydrogen + molar_mass_oxygen)
    volume_EtOH_for_LiEtO = mass_EtOH / density_ethanol
    print('Volume of EtOH to produce EtOLi %s mL' %(volume_EtOH_for_LiEtO))
    
    # volume of ethanol which must be added to the LiEtO to obatin a 1 M solution
    concentration_LiEtO_in_EtOH = 1
    print('The concentration EtOLi in EtOH is set to %s mol/L' %(concentration_LiEtO_in_EtOH))
    volume_EtOH = mol_Li / concentration_LiEtO_in_EtOH 
    volume_EtOH_in_mL = (volume_EtOH * 1000)
    print('Volume of EtOH for producing 1 M EtOLi Solution out of Ethanol and Li metal is %s mL' %(volume_EtOH_in_mL))
 
    print('------------------------------------------')
    
    
    print('Li3InCl6 coating:')
    mol_indium = mol_NCM * Coating_to_NCM_ratio
    mol_lithium = mol_indium * 3
    molar_mass_Li3InCl6 = molar_mass_indium +  molar_mass_lithium * 3 +  molar_mass_chloride * 6
    mass_Li3InCl6 = mol_indium * molar_mass_Li3InCl6
    molar_mass_LiCl = molar_mass_lithium + molar_mass_chloride
    mass_LiCl = molar_mass_LiCl * mol_lithium
    molar_mass_InCl3 = molar_mass_indium + molar_mass_chloride * 3
    mass_InCl3 = mol_indium * molar_mass_InCl3
    print('The mass for Li3InCl6 is: %s g' %(mass_Li3InCl6))
    print('The mass for LiCl is: %s g' %(mass_LiCl))
    print('The mass for InCl3 is: %s g' %(mass_InCl3))
    print('------------------------------------------')
    
    print('H3BO3 coating:')
    mol_bor = mol_NCM * Coating_to_NCM_ratio

    molar_mass_H3BO3 = molar_mass_bor +  molar_mass_hydrogen * 3 +  molar_mass_oxygen * 3
    mass_H3BO3 = mol_bor * molar_mass_H3BO3
    print('The mass for H3BO3 is: %s g' %(mass_H3BO3))
    print('------------------------------------------')
    
    print('ZnCl2 coating:')
    mol_Zn = mol_NCM * Coating_to_NCM_ratio

    molar_mass_ZnCl2 = molar_mass_zinc + 2 * molar_mass_chloride 
    mass_ZnCl2 = mol_Zn * molar_mass_ZnCl2
    print('The mass for ZnCl2  is: %s g' %(mass_ZnCl2 ))
    print('------------------------------------------')
   
    # printing additional informations
    if additional_informations == True:
        print("Mol NCM for coating process: %s \nMol Ta: %s \nMass TaEtO5: %s \nMass Li: %s \nVolume EtOH in mL: %s" %(mol_NCM, mol_tantalum, mass_TaEtO5, mass_Li, volume_EtOH_in_mL))
 
    return


def Calculate_Mass_NCM(CAM_informations):
    """Mass (g) and concentration (mg/L) of Ni, Li and Zn in an AES sample solution of dissolved NCM; results are printed.
    CAM_informations = [NCM mass in g, solution volume in mL, Ni ratio, Co ratio, Mn ratio]."""
    mass_NCM = CAM_informations[0]
    volume_solution = CAM_informations[1]
    nickel_ratio = CAM_informations[2]
    cobalt_ratio = CAM_informations[3]
    manganese_ratio = CAM_informations[4]
        
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_tantalum = 180.94788 # g/mol
    molar_mass_bor = 10.811 # g/mol
    molar_mass_zinc = 65.409 # g/mol
    
    # Calculating the mol of the Elements in the sampel weight
    molar_mass_NCM = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + 2 * molar_mass_oxygen + molar_mass_lithium
    mol_NCM = mass_NCM/molar_mass_NCM
    mol_Ni = mol_NCM * nickel_ratio
    mol_Li = mol_NCM
    mol_Zn = mol_NCM * 0.02
    
    # Calculating the mass of the Elemetns in the sample weight
    mass_Ni = mol_Ni * molar_mass_nickel
    mass_Li = mol_Li * molar_mass_lithium
    mass_Zn = mol_Zn * molar_mass_zinc
    
    # Calculating the volume ratio between the sample volume and 1 Litre
    volume_solution_in_L = volume_solution/1000
    volume_ratio = 1/volume_solution_in_L
    
    # Calculating the Masses of the Elements per Litre
    mass_Ni_per_L = mass_Ni * volume_ratio * 1000
    mass_Li_per_L = mass_Li * volume_ratio * 1000
    mass_Zn_per_L = mass_Zn * volume_ratio * 1000
    
    print('The amount of Nickel is %s g in %s mL sample solution and the concetration is %s mg/L' %(mass_Ni, volume_solution, mass_Ni_per_L))
    print('The amount of Lithium is %s g in %s mL sample solution and the concetration is %s mg/L' %(mass_Li, volume_solution, mass_Li_per_L))
    print('The amount of Zinc is %s g in %s mL sample solution and the concetration is %s mg/L' %(mass_Zn, volume_solution, mass_Zn_per_L))
    
    return


def Calculate_HNO3_Dilution(informations):
    """Volume (mL) of HNO3 stock solution needed for a diluted solution; results are printed.
    informations = [stock concentration in mol/L, wanted concentration in mol/L, wanted volume in mL]."""
    concentration_HNO3_base_solution = informations[0]
    wanted_concetration = informations[1]
    volume = informations[2]
        
    # molar masses of the elements in the substances
    molar_mass_nitrogen = 14.0067 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    
    # Mol of HNO3
    volume_in_litre = volume * 0.001
    mol_HNO3 = wanted_concetration * volume_in_litre
    print('Amount of HNO3 needed is %s mol for a volume of %s mL and a concetration of %s mol/L' %(mol_HNO3, volume, wanted_concetration))
    
    # HNO3 acid volume
    volume_HNO3_acid = mol_HNO3 / concentration_HNO3_base_solution
    volume_HNO3_acid_mL = volume_HNO3_acid * 1000
    print('The amount of %s mol/L HNO3 acid is %s mL' %(concentration_HNO3_base_solution , volume_HNO3_acid_mL))
    
    return


def Calculate_NCM_Mass_For_Boron_AES_Solution(informations):
    """Boron content of a coated NCM sample from its AES result (weight % and mol %); results are printed.
    informations = [boron concentration in mg/L, sample volume in mL, sample weight in g, Ni ratio, Co ratio, Mn ratio]."""

    concenration_boron = informations[0]
    sample_volume = informations[1]
    sample_weight = informations[2]
    nickel_ratio = informations[3]
    cobalt_ratio = informations[4]
    manganese_ratio = informations[5]

    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_boron = 10.811 # g/mol
    
    # Calculating mol Boron
    weight_boron = concenration_boron * 0.001 # in gram in 1 litre of solution
    print('The amount of Boron in 1 Litre Solution is %s g' %(weight_boron))
    mol_boron = (weight_boron/molar_mass_boron)
    
    # Calculationg mol NCM
    molar_mass_NCM = molar_mass_lithium + nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + 2 * molar_mass_oxygen
    ratio_volume = 1000 / sample_volume
    mol_NCM = (sample_weight*ratio_volume) / molar_mass_NCM # in 1 L sample volume
    weight_NCM = mol_NCM * molar_mass_NCM
    print('The amount of NCM in 1 Litre Solution is %s g' %(weight_NCM))
    
    #Calculating weight% Boron
    weight_percent_boron_compared_to_sample_weight =  weight_boron/(sample_weight*ratio_volume)
    print('The amount of Boron in the Material is %s WeightPercent' %(weight_percent_boron_compared_to_sample_weight))
    
    # Calculating mol% Boron
    percent_boron = (mol_boron/mol_NCM)*100
    print('The amount of Boron in the Material is %s MolPercent' %(percent_boron))


def Calculate_Masses_For_Cathode_Sheet_Casting(variables):
    """Masses (g) of carbon, PVdF/NMP solution and additional NMP for a cathode slurry (NCM:PVdF:carbon ratio and solid content set in the code); results are printed.
    variables = [NCM mass in g]."""
    weight_NCM_powder = variables[0]
    
    # Information
    print('Selected Parameters:')
    print('Calculating Masses for %s g of NCM' %(weight_NCM_powder))
    
    # Cathode Compositon in weight ratio
    NCM_weight_ratio = 0.94
    PVdF_weight_ratio = 0.03
    Carbon_weight_ratio = 0.03
    print('NCM:PVdF:Carbon-Ratio is set to: %s : %s : %s' %(NCM_weight_ratio*100, PVdF_weight_ratio*100, Carbon_weight_ratio*100))
    
    # Solution used and their composition
    PVdF_weightpercent_solution = 0.050
    print('PVdF-WeightPercent is set to: %s Percent' %(PVdF_weightpercent_solution*100))
    
    # Solid content in the sheet
    Solid_per_totalSlurry_ratio = 0.55
    print('The Solid/Liquid-Ratio (Solid Content) is set to: %s' %(Solid_per_totalSlurry_ratio))
    print('----------------------------------------------------------------------------------------------------------')
    
    # NMP/Solid-Ration (old values used
    #NMP_Solid_ratio = 0.8
    #NMP_Solid_ratio = 1.06
    #NMP_Solid_ratio = 1.235
    #print('The NMP/Solid-Ration is set to: %s' %(NMP_Solid_ratio))
    #print('The Solid/Liquid-Ratio (Solid Content) is set to: %s' %(Solid_per_Liquid_ratio))
    #print('----------------------------------------------------------------------------------------------------------')
    
    # Calculating the total amount weight when only pure NCM, PVdF, Carbon is used
    total_weight_solids = weight_NCM_powder * (1+(1-NCM_weight_ratio))
    
    # Calcualting the carbon weight
    carbon_weight = total_weight_solids * Carbon_weight_ratio
    
    # Calculating the PVdF weight
    PVdF_weight = total_weight_solids * PVdF_weight_ratio
    # Calculating the amount of the PVdF 5% solution is needed
    PVdF_weight_solution = PVdF_weight * (1/PVdF_weightpercent_solution)
    
    # Calculating the amount of NMP
    total_weight_slurry = total_weight_solids / Solid_per_totalSlurry_ratio
    total_weight_liquid = total_weight_slurry * (1 - Solid_per_totalSlurry_ratio)
    NMP_weight = total_weight_liquid - (PVdF_weight_solution - PVdF_weight)
    # Corrected NMP weight when the NMP from the PVdF Solution is substracted
    #NMP_weight = NMP_weight - (PVdF_weight_solution-(PVdF_weight_solution*PVdF_weightpercent_solution))
    
    # Weight of all NMP in the slurry
    #total_NMP_weight = (NMP_weight + PVdF_weight_solution - PVdF_weight)
    
    # Result
    print('Calculated Masses:')
    print('NCM: %s g' %(weight_NCM_powder))
    print('Carbon: %s g' %(carbon_weight))
    print('PVdF NMP Solution: %s g' %(PVdF_weight_solution))
    print('additional NMP: %s g' %(NMP_weight))
    print('----------------------------------------------------------------------------------------------------------')
    print('Info:')
    print('PVdF: %s g' %(PVdF_weight))
    print('total amount of Solids: %s g' %(total_weight_solids))
    print('total amount of Liquid: %s g' %(total_weight_liquid))
    print('Solid-Content is: %s Percent' %(total_weight_solids/total_weight_slurry))
 
    return


def Calculate_Masses_For_Anode_Sheet_Casting(variables):
    """Masses (g) of NaCMC/H2O solution and additional water for a graphite anode slurry (ratios set in the code); results are printed.
    variables = [graphite mass in g]."""
    weight_Graphite_powder = variables[0]
    
    # Information
    print('Selected Parameters:')
    print('Calculating Masses for %s g of Graphite' %(weight_Graphite_powder))
    
    # Cathode Compositon in weight ratio
    Graphite_weight_ratio = 0.95
    NaCMC_weight_ratio = 0.05
    print('Graphite:NaCMC-Ratio is set to: %s : %s' %(Graphite_weight_ratio*100, NaCMC_weight_ratio*100))
    
    # Solution used and their composition
    NaCMC_weightpercent_solution = 0.025
    NaCMC_weightpercent_solution = 0.015
    print('NaCMC-WeightPercent is set to: %s Percent' %(NaCMC_weightpercent_solution*100))
    
    # Solid content in the sheet
    #Solid_per_totalSlurry_ratio = 0.33898
    Solid_per_totalSlurry_ratio = 0.2335
    print('The Solid/Liquid-Ratio (Solid Content) is set to: %s' %(Solid_per_totalSlurry_ratio))
    print('----------------------------------------------------------------------------------------------------------')
    
    # NMP/Solid-Ration (old values used
    #NMP_Solid_ratio = 0.8
    #NMP_Solid_ratio = 1.06
    #NMP_Solid_ratio = 1.235
    #print('The NMP/Solid-Ration is set to: %s' %(NMP_Solid_ratio))
    #print('The Solid/Liquid-Ratio (Solid Content) is set to: %s' %(Solid_per_Liquid_ratio))
    #print('----------------------------------------------------------------------------------------------------------')
    
    # Calculating the total amount weight when only pure NCM, PVdF, Carbon is used
    total_weight_solids = weight_Graphite_powder * (1+(1-Graphite_weight_ratio))
    
    # Calcualting the carbon weight
    NaCMC_weight = total_weight_solids * NaCMC_weight_ratio
    # Calculating the amount of the PVdF 5% solution is needed
    NaCMC_weight_solution = NaCMC_weight * (1/NaCMC_weightpercent_solution)
    
    # Calculating the amount of NMP
    total_weight_slurry = total_weight_solids / Solid_per_totalSlurry_ratio
    total_weight_liquid = total_weight_slurry * (1 - Solid_per_totalSlurry_ratio)
    H2O_weight = total_weight_liquid - (NaCMC_weight_solution - NaCMC_weight)
    # Corrected NMP weight when the NMP from the PVdF Solution is substracted
    #NMP_weight = NMP_weight - (PVdF_weight_solution-(PVdF_weight_solution*PVdF_weightpercent_solution))
    
    # Weight of all NMP in the slurry
    #total_NMP_weight = (NMP_weight + PVdF_weight_solution - PVdF_weight)
    
    # Result
    print('Calculated Masses:')
    print('Graphite: %s g' %(weight_Graphite_powder))
    print('NaCMC H2O Solution: %s g' %(NaCMC_weight_solution))
    print('additional H2O: %s g' %(H2O_weight))
    print('----------------------------------------------------------------------------------------------------------')
    print('Info:')
    print('NaCMC: %s g' %(NaCMC_weight))
    print('total amount of Solids: %s g' %(total_weight_solids))
    print('total amount of Liquid: %s g' %(total_weight_liquid))
    print('Solid-Content is: %s Percent' %(total_weight_solids/total_weight_slurry))
 
    return


def Calculate_Masses_For_CAM_Synthesis_From_Hydroxide_Precursor(Synthesis_parameter):
    """Masses (g) of hydroxide precursor and Li salt (LiOH*H2O or Li2CO3) to synthesise a given mass of NCM; results are printed.
    Synthesis_parameter = [wanted CAM mass in g, Ni ratio, Co ratio, Mn ratio, Li:TM molar ratio, Li precursor : flux molar ratio]."""
    # Read defined Synthesis Parameter based on User Input
    wanted_CAM_mass = Synthesis_parameter[0]
    nickel_ratio = Synthesis_parameter[1]
    cobalt_ratio = Synthesis_parameter[2]
    manganese_ratio = Synthesis_parameter[3]
    Li_TM_ratio = Synthesis_parameter[4]
    Li_precursor_flux_molar_ratio = Synthesis_parameter[5]
    
    # Print some Information
    print('Calculating the Amount of Li-Precursor and Hydroxide Precursor needed to synthesise %s g CAM ..........' %(wanted_CAM_mass))
    print('----------------------------------------------------------------------------------------------------------')
    print('CAM Element Ratio is set to: Ni = %s , Co = %s , Mn = %s ' %(nickel_ratio, cobalt_ratio, manganese_ratio))
    print('Lithium-Transition Metal Atom Ratio is set to: %s ' %(Li_TM_ratio))
    print('Lithium-Transition Metal Atom Ratio is set to: %s ' %(Li_precursor_flux_molar_ratio))
        
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_sodium = 22.98976928 # g/mol
    molar_mass_chlorid = 35.453 # g/mol
    
    ######################
    ##### Mol of NCM #####
    ######################
    
    # calculating Molar Mass CAM and Mol of TM
    molar_mass_CAM = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + molar_mass_lithium + 2 * molar_mass_oxygen
    mol_CAM = wanted_CAM_mass / molar_mass_CAM
    mol_TM = mol_CAM
    
    ##########################################
    ##### Masses for NCM Hydroxide Precursor #####
    ##########################################
    
    molar_mass_NCM_HydroxidePrecursor = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + 2 * molar_mass_oxygen + 2 * molar_mass_hydrogen
    
    # Calculating the masses of NCM Hydroxide Precursors
    mass_NCM_HydroxidePrecursor_g = molar_mass_NCM_HydroxidePrecursor * mol_TM
    
    print('----------------------------------------------------------------------------------------------------------')
    print('Mass NCM Hydroxide Precursor: %s g' %(mass_NCM_HydroxidePrecursor_g))
    print('----------------------------------------------------------------------------------------------------------')
    
    ###############################
    ##### Li Precursor Masses #####
    ###############################
    print('----------------------------------------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------------------------------------')
    print('Li zu TM Ratio is set to %s' %(Li_TM_ratio))
    
    # calculating amount of Lithum ions neccesary
    mol_Li = mol_TM * Li_TM_ratio
    
    # molar amounts of the precursor substances
    mol_LiOH = mol_Li
    mol_Li2CO3 = mol_Li * 0.5
          
    # molar masses of the precursor substances
    molar_mass_LiOHH2O = molar_mass_lithium + 2 * molar_mass_oxygen + 3 * molar_mass_hydrogen 
    molar_mass_Li2CO3 =  2 * molar_mass_lithium + 3 * molar_mass_oxygen + molar_mass_carbon
        
    # masses of the Lithium salts
    mass_LiOHH2O = mol_LiOH * molar_mass_LiOHH2O
    mass_Li2CO3 = mol_Li2CO3 * molar_mass_Li2CO3
    print('Mass LiOH * H2O: %s g' %(mass_LiOHH2O))
    print('OR')
    print('Mass Li2CO3: %s g' %(mass_Li2CO3))
    
    
    ############################
    ##### Flux Salt Masses #####
    ############################
    print('----------------------------------------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------------------------------------')
    print('Flux zu CAM Ratio is set to %s' %(Li_precursor_flux_molar_ratio ))
    mol_Flux = mol_CAM *Li_precursor_flux_molar_ratio 
    
    molar_mass_LiCl = molar_mass_lithium + molar_mass_chlorid
    mass_LiCl = mol_Flux * molar_mass_LiCl
    print('Mass LiCl: %s g' %(mass_LiCl))
    
    # Mass Li2CO3
    mass_Li2CO3 = mol_Flux * molar_mass_Li2CO3
    print('Mass Li2CO3: %s g' %(mass_Li2CO3))
    
    return


def Calculate_Masses_For_CAM_Synthesis_From_Oxide_Precursor(Synthesis_parameter):
    """Like Calculate_Masses_For_CAM_Synthesis_From_Hydroxide_Precursor with NiO, Co3O4 and MnO as precursors; results are printed.
    Synthesis_parameter = [wanted CAM mass in g, Ni ratio, Co ratio, Mn ratio, Li:TM molar ratio, Li precursor : flux molar ratio]."""
    # Read defined Synthesis Parameter based on User Input
    wanted_CAM_mass = Synthesis_parameter[0]
    nickel_ratio = Synthesis_parameter[1]
    cobalt_ratio = Synthesis_parameter[2]
    manganese_ratio = Synthesis_parameter[3]
    Li_TM_ratio = Synthesis_parameter[4]
    Li_precursor_flux_molar_ratio = Synthesis_parameter[5]
    
    # Print some Information
    print('Calculating the Amount of Li-Precursor and Oxide Precursor needed to synthesise %s g CAM ..........' %(wanted_CAM_mass))
    print('----------------------------------------------------------------------------------------------------------')
    print('CAM Element Ratio is set to: Ni = %s , Co = %s , Mn = %s ' %(nickel_ratio, cobalt_ratio, manganese_ratio))
    print('Lithium-Transition Metal Atom Ratio is set to: %s ' %(Li_TM_ratio))
    print('Lithium-Transition Metal Atom Ratio is set to: %s ' %(Li_precursor_flux_molar_ratio))
    print('----------------------------------------------------------------------------------------------------------')
        
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_sodium = 22.98976928 # g/mol
    
    ######################
    ##### Mol of NCM #####
    ######################
    
    # calculating Molar Mass CAM and Mol of TM
    molar_mass_CAM = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + molar_mass_lithium + 2 * molar_mass_oxygen
    mol_CAM = wanted_CAM_mass / molar_mass_CAM
    mol_TM = mol_CAM
    
    ######################################
    ##### Masses for Oxide Precursor #####
    ######################################
    
    # mol of different TM Metals
    mol_Ni = mol_TM * nickel_ratio 
    mol_Co = mol_TM * cobalt_ratio 
    mol_Mn = mol_TM * manganese_ratio
    
    # mol of different Oxide Precursors
    mol_NiO = mol_Ni
    mol_Co3O4 = mol_Co * (1/3)
    mol_MnO = mol_Mn
    
    # molar mass and mol of the wanted NCM
    molar_mass_NiO = molar_mass_nickel + molar_mass_oxygen
    molar_mass_Co3O4 = 3 * molar_mass_cobalt + 4 * molar_mass_oxygen
    molar_mass_MnO =  molar_mass_manganese + molar_mass_oxygen
    
    # Calculating the masses of Oxide Precursors
    mass_NiO_g = molar_mass_NiO * mol_NiO
    mass_Co3O4_g = molar_mass_Co3O4 * mol_Co3O4
    mass_MnO_g = molar_mass_MnO * mol_MnO
    
    print('----------------------------------------------------------------------------------------------------------')
    print('Mass NiO: %s g' %(mass_NiO_g))
    print('Mass Co3O4: %s g' %(mass_Co3O4_g))
    print('Mass MnO: %s g' %(mass_MnO_g))
    print('----------------------------------------------------------------------------------------------------------')
    
    ###############################
    ##### Li Precursor Masses #####
    ###############################
    
    # calculating amount of Lithum ions neccesary
    mol_Li = mol_TM * Li_TM_ratio
    
    # molar amounts of the precursor substances
    mol_LiOH = mol_Li
    mol_Li2CO3 = mol_Li * 0.5
          
    # molar masses of the precursor substances
    molar_mass_LiOHH2O = molar_mass_lithium + 2 * molar_mass_oxygen + 3 * molar_mass_hydrogen 
    molar_mass_Li2CO3 =  2 * molar_mass_lithium + 3 * molar_mass_oxygen + molar_mass_carbon
        
    # masses of the Lithium salts
    mass_LiOHH2O = mol_LiOH * molar_mass_LiOHH2O
    mass_Li2CO3 = mol_Li2CO3 * molar_mass_Li2CO3
    
    print('----------------------------------------------------------------------------------------------------------')
    print('Mass LiOH * H2O: %s g' %(mass_LiOHH2O))
    print('OR')
    print('Mass Li2CO3: %s g' %(mass_Li2CO3))
    print('----------------------------------------------------------------------------------------------------------')
    
    
    ############################
    ##### Flux Salt Masses #####
    ############################

    # Code not yet written
    
    return


def Calculate_Washing_Solution_Volume(CAM_informations):
    """Water volume (mL) to wash the excess lithium off a synthesised NCM (for LiOH and for Li2CO3 as Li source); results are printed.
    CAM_informations = [NCM mass in g, Ni ratio, Co ratio, Mn ratio, lithium residuals in mol per mol NCM]."""
    mass_NCM = CAM_informations[0]
    nickel_ratio = CAM_informations[1]
    cobalt_ratio = CAM_informations[2]
    manganese_ratio = CAM_informations[3]
    lithium_residual_ratio = CAM_informations[4]
    
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_sodium = 22.98976928 # g/mol
    molar_mass_bor = 10.811 # g/mol
    molar_mass_sulfur = 32.065 # g/mol
    molar_mass_chlorid = 35.453 # g/mol
    molar_mass_potassium = 39.0983 # g/mol
    molar_mass_calcium = 40.078 # g/mol
    
    # densities
    density_water = 1 # g/cm3
    
    # Solubility products
    solubility_product_LiOH_in_water = 113 # g/l (20 °C) - https://gestis.dguv.de/data?name=005650
    solubility_product_Li2CO3_in_water = 13 # g/l (20 °C) - gestis
    solubility_product_Na2CO3_in_water = 217 #g/l (20 °C) - gestis
    solubility_product_H3BO3_in_water = 49.5 #g/l (20 °C) - gestis
    solubility_product_B2O3_in_water = 36 #g/l (20 °C) - gestis
    solubility_product_Li2SO4_in_water = 340 #g/l (20 °C) - gestis
    solubility_product_NaOH_in_water = 1090 #g/l (20 °C) - gestis
    solubility_product_KCl_in_water = 347 # g/l (20 °C) - gestis
    solubility_product_CaCl2_in_water = 740 # g/l (20 °C) - gestis
      
    # molar mass and mol of the wanted NCM
    molar_mass_NCM = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + molar_mass_lithium + 2 * molar_mass_oxygen
    mol_NCM = mass_NCM / molar_mass_NCM
    
    # Amount of Li Residuals on the NCM
    mol_Li_residuals = mol_NCM * lithium_residual_ratio
    
    # molar amounts of the precursor substances
    mol_LiOH = mol_Li_residuals
    mol_Li2CO3 = mol_Li_residuals * 0.5
    
    ### Amount of water to wash Li source residuals away 
    ## when LiOH is used
    # molar amount of excess lithium oxide from the lithium hydroxide (LiOH becomes Li2O during the synthesis)
    mol_excess_Li2O_from_excess_LiOH = 0.5 * mol_LiOH
    # Li2O reacts back to LiOH in air
    mol_excess_LiOH_from_reaction_of_H2O_and_LiO2 = mol_excess_Li2O_from_excess_LiOH * 2
    mass_excess_LiOH_from_reaction_of_H2O_and_LiO2 = mol_excess_LiOH_from_reaction_of_H2O_and_LiO2 * (molar_mass_lithium  + molar_mass_oxygen + molar_mass_hydrogen)
    volume_water_for_Li2O_to_LiOH_reaction = (mol_excess_Li2O_from_excess_LiOH * (2 * molar_mass_hydrogen + molar_mass_oxygen))/density_water 
    volume_washing_water_for_LiOH_in_millilitre = (mass_excess_LiOH_from_reaction_of_H2O_and_LiO2/solubility_product_LiOH_in_water)*1000
    volume_total_water_for_LiOH_in_millilitre = volume_washing_water_for_LiOH_in_millilitre +  volume_water_for_Li2O_to_LiOH_reaction
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess lithium away, LiOH is used as Li source: %s mL" %(volume_total_water_for_LiOH_in_millilitre))
    
    ### when Li2CO3 is used
    molar_mass_Li2CO3 = 2 * molar_mass_lithium +  molar_mass_carbon + 3 * molar_mass_oxygen
    mass_Li2CO3 = mol_Li2CO3 * molar_mass_Li2CO3
    
    # volume water for washing
    volume_washing_water_for_Li2CO3_in_millilitre = (mass_Li2CO3/solubility_product_Li2CO3_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess lithium away, when Li2CO3 was the lithiation salt: %s mL" %(volume_washing_water_for_Li2CO3_in_millilitre))
          
    return


def Calculate_Masses_For_Precursor_Synthesis(Precursor_informations, additional_informations=False):
    """Masses (g) of NiO, Co3O4 and MnO for a given mass of mixed oxide precursor.
    Precursor_informations = ['NCM', Ni ratio, Co ratio, Mn ratio, precursor mass in g]; additional_informations = print more details.
    Returns (mass NiO, mass Co3O4, mass MnO) in g."""
    if Precursor_informations[0] == "NCM": # If only two parameters are given, an RC model is used
        nickel_ratio = Precursor_informations[1]   # define the list entries as parameters of the function
        cobalt_ratio = Precursor_informations[2]
        manganese_ratio = Precursor_informations[3]
        mass_in_g = Precursor_informations[4]
        
        # Information
        print('This function is writen to calculate the Masses of NiO, Co3O4, and MnO for synthsising a TM(II)O precursor')
        print('----------------------------------------------------------------------------------------------------------')
        print('Calculating Masses for: NCM%s%s%s' %(int(nickel_ratio*100), int(cobalt_ratio*100), int(manganese_ratio*100)))
        print("and the resulting mass of the precursor is set to: ", mass_in_g, "g")
        print('----------------------------------------------------------------------------------------------------------')
        
        
        # molar masses of the elements in the substances
        molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
        molar_mass_cobalt = 58.933195 # g/mol
        molar_mass_manganese = 54.938045 # g/mol
        molar_mass_oxygen = 15.9994 # g/mol
        
        # molar mass and mol of the wanted NCM
        molar_mass_Precursor = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + molar_mass_oxygen
        mol_Precursor = mass_in_g / molar_mass_Precursor
        
        # molar masses of the precursor substances
        molar_mass_NiO = molar_mass_nickel + molar_mass_oxygen
        molar_mass_Co3O4 =  3 * molar_mass_cobalt + 4 * molar_mass_oxygen
        molar_mass_MnO = molar_mass_manganese + molar_mass_oxygen
         
        # molar amounts of the elements for synthesis
        mol_Ni = mol_Precursor * nickel_ratio 
        mol_Co =  mol_Precursor * cobalt_ratio 
        mol_Mn = mol_Precursor * manganese_ratio
        
        if additional_informations == True:
            print('----------------------------------------------------------------------------------------------------------')
            print('Additional Information:')
            print("molar mass of the precursor is %s g" %molar_mass_Precursor)
            print("amount of the precursor is %s mol" %mol_Precursor)
            print("molar mass of NiO is %s g/mol" %molar_mass_NiO)
            print("molar mass of Co3O4 is %s g/mol" %molar_mass_Co3O4)
            print("molar mass of MnO is %s g/mol" %molar_mass_MnO)
            print("amount of the Ni is %s mol" %mol_Ni)
            print("amount of the Co is %s mol" %mol_Co)
            print("amount of the Mn is %s mol" %mol_Mn)
            print('----------------------------------------------------------------------------------------------------------')
        
        
        # molar amounts of the precursor substances
        mol_NiO = mol_Ni
        mol_Co3O4 = mol_Co * 1/3
        mol_MnO = mol_Mn
        
        # masses of the precursor substances
        mass_NiO = mol_NiO * molar_mass_NiO
        mass_Co3O4 = mol_Co3O4 * molar_mass_Co3O4
        mass_MnO = mol_MnO * molar_mass_MnO
    
        print('----------------------------------------------------------------------------------------------------------')
        print('Result:')
        print("NiO: %s g \nCo3O4: %s g \nMnO: %s g" %(mass_NiO, mass_Co3O4, mass_MnO))
        
        return mass_NiO, mass_Co3O4, mass_MnO


def Calculate_Masses_For_CAM_Synthesis_From_Oxides(CAM_informations, additional_informations = False):
    """Masses (g) of LiOH*H2O or Li2CO3 and Na2CO3 flux for given masses of NiO, Co3O4 and MnO, the expected NCM mass and the washing water (mL); results are printed.
    CAM_informations = [Li:TM molar ratio, NiO in g, Co3O4 in g, MnO in g, Li2CO3 : Na2CO3 flux ratio]."""
    Li_TM_ratio = CAM_informations[0] # If only two parameters are given, an RC model is used
    mass_NiO_g = CAM_informations[1]   # define the list entries as parameters of the function
    mass_Co3O4_g = CAM_informations[2]
    mass_MnO_g = CAM_informations[3]
    Li_precursor_flux_ratio = CAM_informations[4]

    # Information
    print('This function is writen to calculate the Masses of Li2CO3 or LiOH x H2O for a given mass of defined NCM-oxide precursor r')
    print('----------------------------------------------------------------------------------------------------------')
    print('Calculating Masses for a Lithium to transition metal ratio of %s' %(Li_TM_ratio))
    print('----------------------------------------------------------------------------------------------------------')
        
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_sodium = 22.98976928 # g/mol
    
    # densities
    density_water = 1 # g/cm3
    
    # Solubility products
    solubility_product_LiOH_in_water = 113 # g/l (20 °C) - https://gestis.dguv.de/data?name=005650
    solubility_product_Li2CO3_in_water = 13 # g/l (20 °C) - gestis
    # Li2O reacts with water to LiOH and H2 and H2O, so more water is needed for washing, so that Li2O can first react to LiOH and is then washed away
        
    # molar mass and mol of the wanted NCM
    molar_mass_NiO = molar_mass_nickel + molar_mass_oxygen
    molar_mass_Co3O4 = 3 * molar_mass_cobalt + 4 * molar_mass_oxygen
    molar_mass_MnO =  molar_mass_manganese + molar_mass_oxygen
    
    mol_NiO = mass_NiO_g/molar_mass_NiO
    mol_Co3O4 = mass_Co3O4_g/molar_mass_Co3O4
    mol_MnO = mass_MnO_g/molar_mass_MnO
    
    mol_Ni = mol_NiO
    mol_Co = 3 * mol_Co3O4
    mol_Mn = mol_MnO
    mol_TM = mol_Ni + mol_Co + mol_Mn
    
    ratio_Ni = mol_Ni/mol_TM
    ratio_Co = mol_Co/mol_TM
    ratio_Mn = mol_Mn/mol_TM
    print('The TM ratios should are: Ni = %s , Co = %s , Mn = %s ' %(ratio_Ni, ratio_Co, ratio_Mn))
    
    # calculating mass of the resulting NCM
    molar_mass_NCM = ratio_Ni * molar_mass_nickel + ratio_Co * molar_mass_cobalt + ratio_Mn * molar_mass_manganese + molar_mass_lithium + 2 * molar_mass_oxygen
    mol_NCM = mol_TM
    mass_NCM = molar_mass_NCM * mol_NCM
    #print('Mass of the resulting NCM should be %s g' %(mass_NCM))
    
    # calculating amount of Lithum ions neccesary
    mol_Li = mol_NCM * Li_TM_ratio
    
    # molar amounts of the precursor substances
    mol_LiOH = mol_Li
    mol_Li2CO3 = mol_Li * 0.5
    
    # molar amounts of flux
    # calculates the amount of flux based on the ratio between the precursor Li substance and not the amount of Lithium itself
    mol_flux = mol_Li2CO3 * (2-Li_precursor_flux_ratio)
    molar_mass_Na2CO3 = 2 * molar_mass_sodium + molar_mass_carbon + 3 * molar_mass_oxygen
    molar_mass_flux = molar_mass_Na2CO3
    mass_flux = mol_flux * molar_mass_flux
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of flux (Na2CO3) reagent for a Li2CO3 : Na2CO3 ratio of %s : %s g' %(Li_precursor_flux_ratio, mass_flux))
          
    # molar masses of the precursor substances
    molar_mass_LiOHH2O = molar_mass_lithium + 2 * molar_mass_oxygen + 3 * molar_mass_hydrogen 
    molar_mass_Li2CO3 =  2 * molar_mass_lithium + 3 * molar_mass_oxygen + molar_mass_carbon
        
    # masses of the Lithium salts
    mass_LiOHH2O = mol_LiOH * molar_mass_LiOHH2O
    mass_Li2CO3 = mol_Li2CO3 * molar_mass_Li2CO3
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of LiOH*H2O %s g or amount of Li2CO3 %s g for a Li:TM ratio of %s .' %(mass_LiOHH2O, mass_Li2CO3, Li_TM_ratio))
    
    # molar amount of excess Lihtium oxide from the Lthium hydroxide
    mol_excess_Li2O_from_excess_LiOH = 0.5 * mol_LiOH * (Li_TM_ratio - 1)
    mol_excess_LiOH_from_reaction_of_H2O_and_LiO2 = mol_excess_Li2O_from_excess_LiOH * 2
    
    # masses of the theoretical lithium residuals
    mass_excess_Li2CO3 = mass_Li2CO3 * (Li_TM_ratio - 1)/Li_TM_ratio
    mass_excess_Li2O_from_excess_LiOH = mol_excess_Li2O_from_excess_LiOH * (2 * molar_mass_lithium  + molar_mass_oxygen)
    mass_excess_LiOH_from_reaction_of_H2O_and_LiO2 = mol_excess_LiOH_from_reaction_of_H2O_and_LiO2 * (molar_mass_lithium  + molar_mass_oxygen + molar_mass_hydrogen)
    
    # volume water for washing
    volume_washing_water_for_Li2CO3_in_millilitre = (mass_excess_Li2CO3/solubility_product_Li2CO3_in_water) * 1000
    volume_water_for_Li2O_to_LiOH_reaction = (mol_excess_Li2O_from_excess_LiOH * (2 * molar_mass_hydrogen + molar_mass_oxygen))/density_water 
    volume_washing_water_for_LiOH_in_millilitre = (mass_excess_LiOH_from_reaction_of_H2O_and_LiO2/solubility_product_LiOH_in_water)*1000
    volume_total_water_for_LiOH_in_millilitre = volume_washing_water_for_LiOH_in_millilitre +  volume_water_for_Li2O_to_LiOH_reaction
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess lithium away, when Li2CO3 was the lithiation salt: %s mL\nWashing with %s mL Water is necessary to remove all Li2O which reacts to LiOH by contace water" %(volume_washing_water_for_Li2CO3_in_millilitre, volume_total_water_for_LiOH_in_millilitre))
 
    
    # mass of the resulting NCM material
    mass_NCM = mol_NCM * molar_mass_NCM
    print('----------------------------------------------------------------------------------------------------------') 
    print('The resulting mass of the pure NCM should be %s g,but in practice this is higher because residual lithium is present.' %(mass_NCM))
    
    if additional_informations == True:
        print('----------------------------------------------------------------------------------------------------------')
        print('Additional Information:')
        print("molar mass of NiO is %s g/mol" %molar_mass_NiO)
        print("molar mass of Co3O4 is %s g/mol" %molar_mass_Co3O4)
        print("molar mass of MnO is %s g/mol" %molar_mass_MnO)
        print("amount of the Ni is %s mol" %mol_Ni)
        print("amount of the Co is %s mol" %mol_Co)
        print("amount of the Mn is %s mol" %mol_Mn)
        print('----------------------------------------------------------------------------------------------------------')
               
    return


def Calculate_Flux_Ratio_And_Washing_Solution(CAM_informations, additional_informations = False):
    """Like Calculate_Masses_For_CAM_Synthesis_From_Oxides with a CaCl2-KCl eutectic as flux: masses of Li2CO3, KCl and CaCl2 (g) and the washing water (mL); results are printed.
    CAM_informations = [Li:TM molar ratio, NiO in g, Co3O4 in g, MnO in g, flux : NCM ratio]."""
    Li_TM_ratio = CAM_informations[0] # If only two parameters are given, an RC model is used
    mass_NiO_g = CAM_informations[1]   # define the list entries as parameters of the function
    mass_Co3O4_g = CAM_informations[2]
    mass_MnO_g = CAM_informations[3]
    flux_ratio = CAM_informations[4]
    
    # Information
    # Information
    print('Function for Calculating the Flux Ratio for a given Precursor mass')
    print('----------------------------------------------------------------------------------------------------------')
    print('Calculating Masses for a Lithium to transition metal ratio of %s' %(Li_TM_ratio))
    print("and the Flux Ratio: ", flux_ratio)
    print('----------------------------------------------------------------------------------------------------------')
        
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_sodium = 22.98976928 # g/mol
    molar_mass_bor = 10.811 # g/mol
    molar_mass_sulfur = 32.065 # g/mol
    molar_mass_chlorid = 35.453 # g/mol
    molar_mass_potassium = 39.0983 # g/mol
    molar_mass_calcium = 40.078 # g/mol
    
    
    # densities
    density_water = 1 # g/cm3
    
    # Solubility products
    solubility_product_LiOH_in_water = 113 # g/l (20 °C) - https://gestis.dguv.de/data?name=005650
    solubility_product_Li2CO3_in_water = 13 # g/l (20 °C) - gestis
    solubility_product_Na2CO3_in_water = 217 #g/l (20 °C) - gestis
    solubility_product_H3BO3_in_water = 49.5 #g/l (20 °C) - gestis
    solubility_product_B2O3_in_water = 36 #g/l (20 °C) - gestis
    solubility_product_Li2SO4_in_water = 340 #g/l (20 °C) - gestis
    solubility_product_NaOH_in_water = 1090 #g/l (20 °C) - gestis
    solubility_product_KCl_in_water = 347 # g/l (20 °C) - gestis
    solubility_product_CaCl2_in_water = 740 # g/l (20 °C) - gestis
      
    # molar mass and mol of the wanted NCM
    molar_mass_NiO = molar_mass_nickel + molar_mass_oxygen
    molar_mass_Co3O4 = 3 * molar_mass_cobalt + 4 * molar_mass_oxygen
    molar_mass_MnO =  molar_mass_manganese + molar_mass_oxygen
    
    mol_NiO = mass_NiO_g/molar_mass_NiO
    mol_Co3O4 = mass_Co3O4_g/molar_mass_Co3O4
    mol_MnO = mass_MnO_g/molar_mass_MnO
    
    mol_Ni = mol_NiO
    mol_Co = 3 * mol_Co3O4
    mol_Mn = mol_MnO
    mol_TM = mol_Ni + mol_Co + mol_Mn
    
    ratio_Ni = mol_Ni/mol_TM
    ratio_Co = mol_Co/mol_TM
    ratio_Mn = mol_Mn/mol_TM
    print('The TM ratios should are: Ni = %s , Co = %s , Mn = %s ' %(ratio_Ni, ratio_Co, ratio_Mn))    
        
    # calculating mass of the resulting NCM
    molar_mass_NCM = ratio_Ni * molar_mass_nickel + ratio_Co * molar_mass_cobalt + ratio_Mn * molar_mass_manganese + molar_mass_lithium + 2 * molar_mass_oxygen
    mol_NCM = mol_TM
    mass_NCM = molar_mass_NCM * mol_NCM
    print('Mass of the resulting NCM should be %s g' %(mass_NCM))
    
    # calculating amount of Lithum ions neccesary
    mol_Li = mol_NCM * Li_TM_ratio
    
    # molar amounts of the precursor substances
    mol_LiOH = mol_Li
    mol_Li2CO3 = mol_Li * 0.5
    
    ### Calculating the amount of Li source salt
    # molar masses of the precursor substances
    #molar_mass_LiOHH2O = molar_mass_lithium + 2 * molar_mass_oxygen + 3 * molar_mass_hydrogen 
    molar_mass_Li2CO3 =  2 * molar_mass_lithium + 3 * molar_mass_oxygen + molar_mass_carbon
        
    # masses of the Lithium salts
    #mass_LiOHH2O = mol_LiOH * molar_mass_LiOHH2O
    #print('----------------------------------------------------------------------------------------------------------') 
    #print('amount of LiOH*H2O is %s g for a Li:TM ratio of %s .' %(mass_LiOHH2O, Li_TM_ratio))
    mass_Li2CO3 = mol_Li2CO3 * molar_mass_Li2CO3
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of Li2CO3 is %s g for a Li:TM ratio of %s .' %(mass_Li2CO3, Li_TM_ratio))
    
    
    ### Amount of water to wash Li source residuals away 
#     ## when LiOH is used
#     # molar amount of excess lithium oxide from the lithium hydroxide (LiOH becomes Li2O during the synthesis)
#     mol_excess_Li2O_from_excess_LiOH = 0.5 * mol_LiOH * (Li_TM_ratio - 1)
#     # Li2O reacts back to LiOH in air
#     mol_excess_LiOH_from_reaction_of_H2O_and_LiO2 = mol_excess_Li2O_from_excess_LiOH * 2
#     mass_excess_LiOH_from_reaction_of_H2O_and_LiO2 = mol_excess_LiOH_from_reaction_of_H2O_and_LiO2 * (molar_mass_lithium  + molar_mass_oxygen + molar_mass_hydrogen)
#     volume_water_for_Li2O_to_LiOH_reaction = (mol_excess_Li2O_from_excess_LiOH * (2 * molar_mass_hydrogen + molar_mass_oxygen))/density_water 
#     volume_washing_water_for_LiOH_in_millilitre = (mass_excess_LiOH_from_reaction_of_H2O_and_LiO2/solubility_product_LiOH_in_water)*1000
#     volume_total_water_for_LiOH_in_millilitre = volume_washing_water_for_LiOH_in_millilitre +  volume_water_for_Li2O_to_LiOH_reaction
#     print('----------------------------------------------------------------------------------------------------------') 
#     print("Volume of the Water for washing the excess lithium away, LiOH is used as Li source: %s mL" %(volume_total_water_for_LiOH_in_millilitre))
    
    ## when Li2CO3 is used
    # masses of the theoretical lithium residuals
    mass_excess_Li2CO3 = mass_Li2CO3 * (Li_TM_ratio - 1)/Li_TM_ratio
    
    # volume water for washing
    volume_washing_water_for_Li2CO3_in_millilitre = (mass_excess_Li2CO3/solubility_product_Li2CO3_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess lithium away, when Li2CO3 was the lithiation salt: %s mL" %(volume_washing_water_for_Li2CO3_in_millilitre))
    
    
    ### calculating the amount of flux salt
    # calculates the amount of flux based on the ratio between the precursor Li substance and not the amount of Lithium itself
    mol_flux = mol_NCM * flux_ratio
#     # for Li2CO3
#     molar_mass_Li2CO3 = 2 * molar_mass_lithium + molar_mass_carbon + 3 * molar_mass_oxygen
#     molar_mass_flux_Li2CO3 = molar_mass_Li2CO3
#     mass_flux_Li2CO3 = mol_flux * molar_mass_flux_Li2CO3
#     print('----------------------------------------------------------------------------------------------------------') 
#     print('amount of flux (Li2CO3) reagent for a Li2CO3 : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_Li2CO3))
#     # for Na2CO3
#     molar_mass_Na2CO3 = 2 * molar_mass_sodium + molar_mass_carbon + 3 * molar_mass_oxygen
#     molar_mass_flux_Na2CO3 = molar_mass_Na2CO3
#     mass_flux_Na2CO3 = mol_flux * molar_mass_flux_Na2CO3
#     print('----------------------------------------------------------------------------------------------------------') 
#     print('amount of flux (Na2CO3) reagent for a Na2CO3 : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_Na2CO3))
#     # for H3BO3
#     molar_mass_H3BO3 = 3 * molar_mass_hydrogen + molar_mass_bor + 3 * molar_mass_oxygen
#     molar_mass_flux_H3BO3 = molar_mass_H3BO3
#     mass_flux_H3BO3 = mol_flux * molar_mass_flux_H3BO3 * 2 # (multiplied by two, so that the R factor fits the formed B2O3)
#     print('----------------------------------------------------------------------------------------------------------') 
#     print('amount of flux (H3BO3) reagent for a B2O3 : NCM flux ratio of %s is %s g based on the formed amount of B2O3' %(flux_ratio, mass_flux_H3BO3))
#     # for Li2SO4
#     molar_mass_Li2SO4 = 2 * molar_mass_lithium + molar_mass_sulfur + 4 * molar_mass_oxygen
#     molar_mass_flux_Li2SO4 = molar_mass_Li2SO4
#     mass_flux_Li2SO4 = mol_flux * molar_mass_flux_Li2SO4
#     print('----------------------------------------------------------------------------------------------------------') 
#     print('amount of flux (Li2SO4) reagent for a Li2SO4 : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_Li2SO4))
#     # for NaOH
#     molar_mass_NaOH = molar_mass_sodium + molar_mass_hydrogen + molar_mass_oxygen
#     molar_mass_flux_NaOH = molar_mass_NaOH
#     mass_flux_NaOH = mol_flux * molar_mass_flux_NaOH
#     print('----------------------------------------------------------------------------------------------------------') 
#     print('amount of flux (NaOH) reagent for a NaOH : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_NaOH))
#     # for LiOH
#     molar_mass_LiOH = molar_mass_lithium + molar_mass_hydrogen + molar_mass_oxygen
#     molar_mass_flux_LiOH = molar_mass_LiOH
#     mass_flux_LiOH = mol_flux * molar_mass_flux_LiOH
#     print('----------------------------------------------------------------------------------------------------------') 
#     print('amount of flux (LiOH) reagent for a LiOH : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_LiOH))
    # for CaCl2 - KCl Eutektikum
    molar_mass_KCl = molar_mass_potassium + molar_mass_chlorid
    molar_mass_CaCl2 = molar_mass_calcium + 2 * molar_mass_chlorid
    # inserting the eutektikum ratios
    mol_KCl = mol_flux * 0.75046
    mol_CaCl2 = mol_flux * (1-0.75046)
    mass_flux_KCl_part = molar_mass_KCl * mol_KCl
    mass_flux_CaCl2_part = molar_mass_CaCl2 * mol_CaCl2
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of flux (Eutektikum CaCl2-KCl) reagent for a Eutektikum CaCl2-KCl : NCM flux ratio of %s is %s g KCl and %s g CaCl2' %(flux_ratio, mass_flux_KCl_part, mass_flux_CaCl2_part))

        
#     ### Amount of water to wash Flux salt away
#     ## when Li2CO3 is used
#     # volume water for washing
#     volume_washing_water_for_Li2CO3_in_millilitre = (mass_flux_Li2CO3/solubility_product_Li2CO3_in_water) * 1000
#     print('----------------------------------------------------------------------------------------------------------') 
#     print("Volume of the Water for washing the excess Flux away, when Li2CO3 was the used: %s mL" %(volume_washing_water_for_Li2CO3_in_millilitre))
#     ## when Na2CO3 is used
#     # volume water for washing
#     volume_washing_water_for_Na2CO3_in_millilitre = (mass_flux_Na2CO3/solubility_product_Na2CO3_in_water) * 1000
#     print('----------------------------------------------------------------------------------------------------------') 
#     print("Volume of the Water for washing the excess Flux away, when Na2CO3 was the used: %s mL" %(volume_washing_water_for_Na2CO3_in_millilitre))
#     # for H3BO3
#     volume_washing_water_for_H3BO3_in_millilitre = (mass_flux_H3BO3/solubility_product_H3BO3_in_water) * 1000
#     print('----------------------------------------------------------------------------------------------------------') 
#     print("Volume of the Water for washing the excess Flux away, when H3BO3 was the used: %s mL" %(volume_washing_water_for_H3BO3_in_millilitre))
#     # for Li2SO4
#     volume_washing_water_for_Li2SO4_in_millilitre = (mass_flux_Li2SO4/solubility_product_Li2SO4_in_water) * 1000
#     print('----------------------------------------------------------------------------------------------------------') 
#     print("Volume of the Water for washing the excess Flux away, when Li2SO4 was the used: %s mL" %(volume_washing_water_for_Li2SO4_in_millilitre))
#     # for NaOH    
#     volume_washing_water_for_NaOH_in_millilitre = (mass_flux_NaOH/solubility_product_NaOH_in_water) * 1000
#     print('----------------------------------------------------------------------------------------------------------') 
#     print("Volume of the Water for washing the excess Flux away, when NaOH was the used: %s mL" %(volume_washing_water_for_NaOH_in_millilitre))
#     # for LiOH    
#     volume_washing_water_for_LiOH_in_millilitre = (mass_flux_LiOH/solubility_product_LiOH_in_water) * 1000
#     print('----------------------------------------------------------------------------------------------------------') 
#     print("Volume of the Water for washing the excess Flux away, when LiOH was the used: %s mL" %(volume_washing_water_for_LiOH_in_millilitre))
    # for Eutektikum CaCl2-KCl 
    volume_washing_water_for_CaCl2KCl_in_millilitre = (mass_flux_KCl_part/solubility_product_KCl_in_water) * 1000 + (mass_flux_CaCl2_part/solubility_product_CaCl2_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess Flux away, when Eutektikum CaCl2-KCl  was the used: %s mL" %(volume_washing_water_for_CaCl2KCl_in_millilitre))
      
          
        
        
    # mass of the resulting NCM material
    mass_NCM = mol_NCM * molar_mass_NCM
    print('----------------------------------------------------------------------------------------------------------') 
    print('The resulting mass of the pure NCM should be %s g,but in practice this is higher because residual lithium is present.' %(mass_NCM))
    
    if additional_informations == True:
        print('----------------------------------------------------------------------------------------------------------')
        print('Additional Information:')
        print("molar mass of NiO is %s g/mol" %molar_mass_NiO)
        print("molar mass of Co3O4 is %s g/mol" %molar_mass_Co3O4)
        print("molar mass of MnO is %s g/mol" %molar_mass_MnO)
        print("amount of the Ni is %s mol" %mol_Ni)
        print("amount of the Co is %s mol" %mol_Co)
        print("amount of the Mn is %s mol" %mol_Mn)
        print('----------------------------------------------------------------------------------------------------------')
               
    return


def Calculate_Masses_For_CAM_Synthesis(CAM_informations, additional_informations = False):
    """Masses (g) of Li salts and of several flux options (Li2CO3, Na2CO3, H3BO3, ...) for a given mass of NCM oxide precursor, and the washing water (mL); results are printed.
    CAM_informations = [Li:TM molar ratio, NCM oxide precursor mass in g, Ni ratio, Co ratio, Mn ratio, flux : NCM ratio]."""
    Li_TM_ratio = CAM_informations[0] # If only two parameters are given, an RC model is used
    mass_in_g = CAM_informations[1]   # define the list entries as parameters of the function
    nickel_ratio_precursor = CAM_informations[2]
    cobalt_ratio_precursor = CAM_informations[3]
    manganese_ratio_precursor = CAM_informations[4]
    flux_ratio = CAM_informations[5]
    
    # Information
    # Information
    print('This function is writen to calculate the Masses of Li2CO3 or LiOH x H2O for a given mass of defined NCM-oxide precursor r')
    print('----------------------------------------------------------------------------------------------------------')
    print('Calculating Masses for a Lithium to transition metal ratio of %s' %(Li_TM_ratio))
    print("and the mass of the NCM-oxide precursor is: ", mass_in_g, "g")
    print('----------------------------------------------------------------------------------------------------------')
        
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_sodium = 22.98976928 # g/mol
    molar_mass_bor = 10.811 # g/mol
    molar_mass_sulfur = 32.065 # g/mol
    molar_mass_chlorid = 35.453 # g/mol
    molar_mass_potassium = 39.0983 # g/mol
    molar_mass_calcium = 40.078 # g/mol
    
    
    # densities
    density_water = 1 # g/cm3
    
    # Solubility products
    solubility_product_LiOH_in_water = 113 # g/l (20 °C) - https://gestis.dguv.de/data?name=005650
    solubility_product_Li2CO3_in_water = 13 # g/l (20 °C) - gestis
    solubility_product_Na2CO3_in_water = 217 #g/l (20 °C) - gestis
    solubility_product_H3BO3_in_water = 49.5 #g/l (20 °C) - gestis
    solubility_product_B2O3_in_water = 36 #g/l (20 °C) - gestis
    solubility_product_Li2SO4_in_water = 340 #g/l (20 °C) - gestis
    solubility_product_NaOH_in_water = 1090 #g/l (20 °C) - gestis
    solubility_product_KCl_in_water = 347 # g/l (20 °C) - gestis
    solubility_product_CaCl2_in_water = 740 # g/l (20 °C) - gestis
      
    # molar mass and mol of the wanted NCM
    molar_mass_precursor = nickel_ratio_precursor * molar_mass_nickel + cobalt_ratio_precursor * molar_mass_cobalt + manganese_ratio_precursor * molar_mass_manganese +  molar_mass_oxygen
    molar_mass_NCM = molar_mass_precursor + molar_mass_lithium + molar_mass_oxygen
    
    mol_precursor = mass_in_g / molar_mass_precursor
    mol_NCM = mol_precursor
    mol_Li = mol_NCM * Li_TM_ratio
    
    # molar amounts of the precursor substances
    mol_LiOH = mol_Li
    mol_Li2CO3 = mol_Li * 0.5
    
    
    ### Calculating the amount of Li source salt
    # molar masses of the precursor substances
    molar_mass_LiOHH2O = molar_mass_lithium + 2 * molar_mass_oxygen + 3 * molar_mass_hydrogen 
    molar_mass_Li2CO3 =  2 * molar_mass_lithium + 3 * molar_mass_oxygen + molar_mass_carbon
        
    # masses of the Lithium salts
    mass_LiOHH2O = mol_LiOH * molar_mass_LiOHH2O
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of LiOH*H2O is %s g for a Li:TM ratio of %s .' %(mass_LiOHH2O, Li_TM_ratio))
    mass_Li2CO3 = mol_Li2CO3 * molar_mass_Li2CO3
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of Li2CO3 is %s g for a Li:TM ratio of %s .' %(mass_Li2CO3, Li_TM_ratio))
    
    
    ### Amount of water to wash Li source residuals away 
    ## when LiOH is used
    # molar amount of excess lithium oxide from the lithium hydroxide (LiOH becomes Li2O during the synthesis)
    mol_excess_Li2O_from_excess_LiOH = 0.5 * mol_LiOH * (Li_TM_ratio - 1)
    # Li2O reacts back to LiOH in air
    mol_excess_LiOH_from_reaction_of_H2O_and_LiO2 = mol_excess_Li2O_from_excess_LiOH * 2
    mass_excess_LiOH_from_reaction_of_H2O_and_LiO2 = mol_excess_LiOH_from_reaction_of_H2O_and_LiO2 * (molar_mass_lithium  + molar_mass_oxygen + molar_mass_hydrogen)
    volume_water_for_Li2O_to_LiOH_reaction = (mol_excess_Li2O_from_excess_LiOH * (2 * molar_mass_hydrogen + molar_mass_oxygen))/density_water 
    volume_washing_water_for_LiOH_in_millilitre = (mass_excess_LiOH_from_reaction_of_H2O_and_LiO2/solubility_product_LiOH_in_water)*1000
    volume_total_water_for_LiOH_in_millilitre = volume_washing_water_for_LiOH_in_millilitre +  volume_water_for_Li2O_to_LiOH_reaction
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess lithium away, LiOH is used as Li source: %s mL" %(volume_total_water_for_LiOH_in_millilitre))
    
    ## when Li2CO3 is used
    # masses of the theoretical lithium residuals
    mass_excess_Li2CO3 = mass_Li2CO3 * (Li_TM_ratio - 1)/Li_TM_ratio
    
    # volume water for washing
    volume_washing_water_for_Li2CO3_in_millilitre = (mass_excess_Li2CO3/solubility_product_Li2CO3_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess lithium away, when Li2CO3 was the lithiation salt: %s mL" %(volume_washing_water_for_Li2CO3_in_millilitre))
    
    
    ### calculating the amount of flux salt
    # calculates the amount of flux based on the ratio between the precursor Li substance and not the amount of Lithium itself
    mol_flux = mol_NCM * flux_ratio
    # for Li2CO3
    molar_mass_Li2CO3 = 2 * molar_mass_lithium + molar_mass_carbon + 3 * molar_mass_oxygen
    molar_mass_flux_Li2CO3 = molar_mass_Li2CO3
    mass_flux_Li2CO3 = mol_flux * molar_mass_flux_Li2CO3
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of flux (Li2CO3) reagent for a Li2CO3 : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_Li2CO3))
    # for Na2CO3
    molar_mass_Na2CO3 = 2 * molar_mass_sodium + molar_mass_carbon + 3 * molar_mass_oxygen
    molar_mass_flux_Na2CO3 = molar_mass_Na2CO3
    mass_flux_Na2CO3 = mol_flux * molar_mass_flux_Na2CO3
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of flux (Na2CO3) reagent for a Na2CO3 : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_Na2CO3))
    # for H3BO3
    molar_mass_H3BO3 = 3 * molar_mass_hydrogen + molar_mass_bor + 3 * molar_mass_oxygen
    molar_mass_flux_H3BO3 = molar_mass_H3BO3
    mass_flux_H3BO3 = mol_flux * molar_mass_flux_H3BO3 * 2 # (multiplied by two, so that the R factor fits the formed B2O3)
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of flux (H3BO3) reagent for a B2O3 : NCM flux ratio of %s is %s g based on the resulting amount of B2O3' %(flux_ratio, mass_flux_H3BO3))
    # for Li2SO4
    molar_mass_Li2SO4 = 2 * molar_mass_lithium + molar_mass_sulfur + 4 * molar_mass_oxygen
    molar_mass_flux_Li2SO4 = molar_mass_Li2SO4
    mass_flux_Li2SO4 = mol_flux * molar_mass_flux_Li2SO4
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of flux (Li2SO4) reagent for a Li2SO4 : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_Li2SO4))
    # for NaOH
    molar_mass_NaOH = molar_mass_sodium + molar_mass_hydrogen + molar_mass_oxygen
    molar_mass_flux_NaOH = molar_mass_NaOH
    mass_flux_NaOH = mol_flux * molar_mass_flux_NaOH
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of flux (NaOH) reagent for a NaOH : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_NaOH))
    # for LiOH
    molar_mass_LiOH = molar_mass_lithium + molar_mass_hydrogen + molar_mass_oxygen
    molar_mass_flux_LiOH = molar_mass_LiOH
    mass_flux_LiOH = mol_flux * molar_mass_flux_LiOH
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of flux (LiOH) reagent for a LiOH : NCM flux ratio of %s is %s g' %(flux_ratio, mass_flux_LiOH))
    # for CaCl2 - KCl Eutektikum
    molar_mass_KCl = molar_mass_potassium + molar_mass_chlorid
    molar_mass_CaCl2 = molar_mass_calcium + 2 * molar_mass_chlorid
    # inserting the eutektikum ratios
    mol_KCl = mol_flux * 0.75046
    mol_CaCl2 = mol_flux * (1-0.75046)
    mass_flux_KCl_part = molar_mass_KCl * mol_KCl
    mass_flux_CaCl2_part = molar_mass_CaCl2 * mol_CaCl2
    print('----------------------------------------------------------------------------------------------------------') 
    print('amount of flux (Eutektikum CaCl2-KCl) reagent for a Eutektikum CaCl2-KCl : NCM flux ratio of %s is %s g KCl and %s g CaCl2' %(flux_ratio, mass_flux_KCl_part, mass_flux_CaCl2_part))

        
    ### Amount of water to wash Flux salt away
    ## when Li2CO3 is used
    # volume water for washing
    volume_washing_water_for_Li2CO3_in_millilitre = (mass_flux_Li2CO3/solubility_product_Li2CO3_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess Flux away, when Li2CO3 was the used: %s mL" %(volume_washing_water_for_Li2CO3_in_millilitre))
    ## when Na2CO3 is used
    # volume water for washing
    volume_washing_water_for_Na2CO3_in_millilitre = (mass_flux_Na2CO3/solubility_product_Na2CO3_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess Flux away, when Na2CO3 was the used: %s mL" %(volume_washing_water_for_Na2CO3_in_millilitre))
    # for H3BO3
    volume_washing_water_for_H3BO3_in_millilitre = (mass_flux_H3BO3/solubility_product_H3BO3_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess Flux away, when H3BO3 was the used: %s mL" %(volume_washing_water_for_H3BO3_in_millilitre))
    # for Li2SO4
    volume_washing_water_for_Li2SO4_in_millilitre = (mass_flux_Li2SO4/solubility_product_Li2SO4_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess Flux away, when Li2SO4 was the used: %s mL" %(volume_washing_water_for_Li2SO4_in_millilitre))
    # for NaOH    
    volume_washing_water_for_NaOH_in_millilitre = (mass_flux_NaOH/solubility_product_NaOH_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess Flux away, when NaOH was the used: %s mL" %(volume_washing_water_for_NaOH_in_millilitre))
    # for LiOH    
    volume_washing_water_for_LiOH_in_millilitre = (mass_flux_LiOH/solubility_product_LiOH_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess Flux away, when LiOH was the used: %s mL" %(volume_washing_water_for_LiOH_in_millilitre))
    # for Eutektikum CaCl2-KCl 
    volume_washing_water_for_CaCl2KCl_in_millilitre = (mass_flux_KCl_part/solubility_product_KCl_in_water) * 1000 + (mass_flux_CaCl2_part/solubility_product_CaCl2_in_water) * 1000
    print('----------------------------------------------------------------------------------------------------------') 
    print("Volume of the Water for washing the excess Flux away, when Eutektikum CaCl2-KCl  was the used: %s mL" %(volume_washing_water_for_CaCl2KCl_in_millilitre))
      
          
        
        
    # mass of the resulting NCM material
    mass_NCM = mol_NCM * molar_mass_NCM
    print('----------------------------------------------------------------------------------------------------------') 
    print('The resulting mass of the pure NCM should be %s g,but in practice this is higher because residual lithium is present.' %(mass_NCM))
    
    if additional_informations == True:
        print('----------------------------------------------------------------------------------------------------------')
        print('Additional Information:')
        print("molar mass of the precursor is %s g" %molar_mass_precursor)
        print("amount of the precursor is %s mol" %mol_precursor)
        print('----------------------------------------------------------------------------------------------------------')
               
    return


def Calculate_Li_Residual_Coating(CAM_informations, additional_informations=True):
    """Amount of lithium residuals (mol), the matching mass of Li2CO3 and the mass of H3BO3 (g) to react them into a coating; results are printed.
    CAM_informations = [NCM mass in g, Ni ratio, Co ratio, Mn ratio, lithium residuals in mol per mol NCM]."""
    mass_NCM = CAM_informations[0]
    nickel_ratio = CAM_informations[1]
    cobalt_ratio = CAM_informations[2]
    manganese_ratio = CAM_informations[3]
    lithium_residual_ratio = CAM_informations[4]
        
    # molar masses of the elements in the substances
    molar_mass_nickel = 58.6934 # g/mol from https://pse.merckgroup.com/periodic-table/element/28
    molar_mass_cobalt = 58.933195 # g/mol
    molar_mass_manganese = 54.938045 # g/mol
    molar_mass_oxygen = 15.9994 # g/mol
    molar_mass_carbon = 12.0107 # g/mol
    molar_mass_lithium = 6.941 # g/mol
    molar_mass_hydrogen = 1.00794 # g/mol
    molar_mass_tantalum = 180.94788
    molar_mass_indium = 114.818 # g/mol
    molar_mass_chloride = 35.453 # g/mol
    molar_mass_bor = 10.811 # g/mol
    molar_mass_zinc = 65.409 # g/mol
    
    # Information
    print('Claculating the Amount of coating Material')
    print('------------------------------------------')

    # molar mass and mol of the wanted NCM
    molar_mass_NCM = nickel_ratio * molar_mass_nickel + cobalt_ratio * molar_mass_cobalt + manganese_ratio * molar_mass_manganese + 2 * molar_mass_oxygen + molar_mass_lithium
    
    mol_NCM = mass_NCM / molar_mass_NCM
    
    print('The amount of NCM is: %s mol' %(mol_NCM))
    print('------------------------------------------')
    
    mol_lithium_residuals = mol_NCM * lithium_residual_ratio
    print('The amount of Li-residuals is: %s mol' %(mol_lithium_residuals))
    print('------------------------------------------')
    
    m_Li2CO3 = (mol_lithium_residuals * 73.89)/2
    print('Li2CO3: %s' %m_Li2CO3)
    
    print('H3BO3 coating Material:')
    print('Assuming formation of Li2B4O7 --> 1:2 Li : Boron ratio')
    mol_bor = mol_lithium_residuals * 2

    molar_mass_H3BO3 = molar_mass_bor +  molar_mass_hydrogen * 3 +  molar_mass_oxygen * 3
    mass_H3BO3 = mol_bor * molar_mass_H3BO3
    print('The mass for H3BO3 is: %s g' %(mass_H3BO3))
    print('------------------------------------------')
    
    return


def Calculate_Mole_Exchange_Per_Minute(thickness, gassflow, text=True):
    """Gas amount (mol/min, ideal gas at 1 bar and 20 °C) that flows through 1 cm of a tube.
    thickness = tube diameter in cm, gassflow = gas flow in cm^3/min (mL/min), text = print the result. Returns mol/min."""
    gassflow_in_m3_per_min = gassflow/(100**3)
    area = 2 * np.pi * (thickness/2)**2 # in cm^2
    lenght = 1 # cm
    volume = area * lenght # in cm^3    
    volume_in_meter = volume/(100**3)
    pressure = 10**5 #Pa
    temperature = 293.15 #Kelvin
    R = 8.31446261815324 # J / mol * K
    mole = (volume_in_meter * pressure) / (R * temperature)
    
    volume_exchange_per_minute = gassflow_in_m3_per_min / volume # min^-1
    Calculate_Mole_Exchange_Per_Minute = volume_exchange_per_minute * mole # mol / min 
    
    if text == True:
        print('Mole passing by the Volume %s cm^3 per Minute is: %s mol/min' %(volume, Calculate_Mole_Exchange_Per_Minute))
    
    return Calculate_Mole_Exchange_Per_Minute


def Calculate_Surfactant_Volume(Informations):
    """Volumes (mL and µL) of Triton X-100 and of a 10 % SDS solution to reach their critical micelle concentration in a given water volume; results are printed.
    Informations = [water volume in mL]."""
    # User Infos
    water_volume = Informations[0]
    #Informations[1] = mass_ncm
    
    # General Substance Infos
    molar_mass_tritonX100 = 647
    molar_mass_SDS = 288.38
    molar_mass_H2O = 18

    density_tritonX100 = 1.065 #g/cm3 url: https://www.sigmaaldrich.com/DE/de/sds/sial/x100 or https://www.sigmaaldrich.com/DE/en/product/sial/x100
    density_SDS10percentSolution = 1.010 #g/cm3 url: https://www.sigmaaldrich.com/DE/de/sds/sigma/71736 or https://www.sigmaaldrich.com/DE/en/product/sigma/71736

    cmc_tritonX100 = 0.22 # mM/L
    cmc_SDS = 8.2 # mM/L
    
    # Calculating molecular amount of the surfactant
    mmol_tritonX100 = (water_volume * 0.001) * cmc_tritonX100 
    mmol_SDS = (water_volume * 0.001) * cmc_SDS
    mmol_H2OSolution = mmol_SDS *((1-0.1)+1)
    
    # Calculating the mass
    mass_tritonX100 = (mmol_tritonX100 * 0.001) * molar_mass_tritonX100
    mass_SDS_pure = (mmol_SDS * 0.001) * molar_mass_SDS
    mass_SDS10percentSolution = mass_SDS_pure + ((mmol_H2OSolution * 0.001) * molar_mass_H2O)
    
    # Calculating the Volume
    volume_tritonX100 = mass_tritonX100 / density_tritonX100
    volume_SDS10percentSolution = mass_SDS10percentSolution / density_SDS10percentSolution
    
    # Output
    print('volume_tritonX100: %s mL or %s µL' %(volume_tritonX100, volume_tritonX100*1000))
    print('volume_SDS10percentSolution: %s mL or %s µL' %(volume_SDS10percentSolution, volume_SDS10percentSolution*1000))
    
    return
