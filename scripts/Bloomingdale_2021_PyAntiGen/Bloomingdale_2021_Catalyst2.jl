using Catalyst
using DifferentialEquations
using SBMLImporter
using ModelingToolkit
using Plots
using DataFrames
using CSV

function main()
    # ---------------------------------------------------------------------------
    # 1. Load SBML model
    # ---------------------------------------------------------------------------
    path_sbml = "C:\\Users\\elber\\Documents\\git\\Bloomingdale_2021_PyAntiGen\\SBML_models\\Bloomingdale_2021_PyAntiGen\\Bloomingdale_2021_PyAntiGen.xml"



    # path_sbml = joinpath(@__DIR__, "Models/Bloomingdale_2021_PyAntiGen.xml")

    rn, cb = load_SBML(path_sbml)


    sys = mtkcompile(ode_model(rn))

    u0 = get_u0_map(rn)
    ps = get_parameter_map(rn)
    tspan = (0.0, 10.0)
    oprob = ODEProblem(sys, merge(Dict(u0), Dict(ps)), tspan, jac=true)

    solve(oprob, Rodas5P())

    # Plot the result for Antibody_Plasma
    ab_plasma_state = nothing
    for s in species(rn)
        if replace(string(s), "(t)" => "") == "Antibody_Plasma"
            ab_plasma_state = s
            break
        end
    end

    path_data = "C:\\Users\\elber\\Documents\\git\\Bloomingdale_2021_PyAntiGen\\data\\PK_Predictions.csv"
    df_data = CSV.read(path_data, DataFrame)
    if ab_plasma_state !== nothing
        p1 = plot(sol, idxs=[ab_plasma_state], xlabel="Time", ylabel="Concentration",
            title="Antibody Plasma", lw=10, legend=:topright)
        scatter!(p1, df_data.Time, df_data."[Antibody_Plasma]" .* 3.1258535, label="Data", color=:red, marker=:circle)

        display(p1)
    end

    println("✅ Simulation complete!")
end

main()
