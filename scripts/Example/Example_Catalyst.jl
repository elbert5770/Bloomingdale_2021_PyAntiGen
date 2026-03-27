using Catalyst
using DifferentialEquations
using SBMLImporter
using ModelingToolkit
using Plots
using DataFrames
using CSV

# ---------------------------------------------------------------------------
# 1. Load SBML model
# ---------------------------------------------------------------------------
path_sbml = "C:\\Users\\elber\\Documents\\git\\Bloomingdale_2021_PyAntiGen\\SBML_models\\Example\\Example.xml"

prn, cb = load_SBML(path_sbml)

# Extract the Catalyst ReactionSystem
rn = prn.rn

# (Optional) Print some verification
println("\n✅ Successfully loaded SBML model!")
println("Reactions: ", equations(rn))
println("Species: ", species(rn))
println("Parameters: ", parameters(rn))

# Convert ReactionSystem to ODESystem
@named sys = convert(ODESystem, rn)

# ---------------------------------------------------------------------------
# 8. Setup and solve ODE Problem
# ---------------------------------------------------------------------------
path_params = "C:\\Users\\elber\\Documents\\git\\Bloomingdale_2021_PyAntiGen\\antimony_models\\Example\\Example_parameters.csv"
df_params = CSV.read(path_params, DataFrame)

# Parameter dictionary
p_vals = Dict{String,Float64}()
for row in eachrow(df_params)
    if !ismissing(row.Value) && string(row.Value) != ""
        val = row.Value
        if val isa Number
            p_vals[string(row.Parameter)] = Float64(val)
        else
            sval = string(val)
            v = tryparse(Float64, sval)
            if v !== nothing
                p_vals[string(row.Parameter)] = v
            elseif haskey(p_vals, sval)
                p_vals[string(row.Parameter)] = p_vals[sval]
            end
        end
    end
end



# We need to map species (states) exactly as string to match them.
u0_vals = Dict()
for s in species(rn)
    # Remove "(t)" for easier matching
    s_name = replace(string(s), "(t)" => "")


    u0_vals[s] = 0.0

end

# Map parameters
p_map = Dict()
for p in parameters(sys)
    p_name = string(p)
    if haskey(p_vals, p_name)
        p_map[p] = p_vals[p_name]
    end
end

# Create ODE problem
prob = ODEProblem(complete(sys), u0_vals, (0.0, 100.0), p_map)

# Solve the ODE problem
sol = solve(prob, Tsit5(), saveat=1.0)

# Plot the result for Antibody_Plasma
ab_plasma_state = nothing
for s in species(rn)
    if replace(string(s), "(t)" => "") == "Antibody_Plasma"
        ab_plasma_state = s
        break
    end
end

if ab_plasma_state !== nothing
    p1 = plot(sol, idxs=[ab_plasma_state], xlabel="Time", ylabel="Concentration",
        title="Antibody Plasma", lw=2, legend=:topright)
    display(p1)
end

println("✅ Simulation complete!")
