import time

def simulate(r):
    r.setIntegrator('cvode')
    r.integrator.absolute_tolerance = 1e-6
    r.integrator.relative_tolerance = 1e-8
    r.integrator.setValue('stiff', True)
    r.integrator.variable_step_size = True
    print(r.integrator)

    observed_species = ['time', '[Antibody_BBB]','[Antibody_BCSFB]','[Antibody_BrainISF]','[Antibody_BrainVascular]','[Antibody_CSF]',
    '[Antibody_Lymph]','[Antibody_Plasma]','[Antibody_TissueEndosomal]','[Antibody_TissueISF]','[Antibody_TissueVascular]',
    '[Antibody__FcRn_BBB]','[Antibody__FcRn_BCSFB]','[Antibody__FcRn_TissueEndosomal]','[FcRn_BBB]','[FcRn_BCSFB]','[FcRn_TissueEndosomal]']


    print("Running simulation...")
    t0 = time.perf_counter()

    result0 = r.simulate(0, 1000, 1001, observed_species)
    
    elapsed = time.perf_counter() - t0
    print(f"Simulation time: {elapsed:.3f} s")
    print(f"CVODE took {len(result0)} steps.")

    return result0,observed_species
