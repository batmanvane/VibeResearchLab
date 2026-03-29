#!/usr/bin/env python3
"""
Mathematical Model Generator for Research Productivity Simulation
Uses SymPy to derive analytical expressions for the emergent activity model.
"""

import sympy as sp

# =============================================================================
# SYMBOLS DEFINITION
# =============================================================================

# Time and duration symbols
t = sp.symbols('t', positive=True, real=True)
T = sp.symbols('T', positive=True, real=True)  # Total simulation time
dt = sp.symbols('\\Delta t', positive=True, real=True)  # Time step

# Lab composition
n_phd = sp.symbols('n_{PhD}', integer=True, positive=True)  # Number of PhDs
n_pi = sp.symbols('n_{PI}', integer=True, positive=True)  # Number of PIs (typically 1)

# Skill distribution parameters (for augmented lab)
mu_s = sp.symbols('\\mu_s', real=True)  # Mean skill level
sigma_s = sp.symbols('\\sigma_s', real=True, positive=True)  # Skill std dev

# Task-specific speedup parameters
# For each task type k: s_k = speedup factor (time reduction)
s_boiler = sp.symbols('s_{boiler}', positive=True, real=True)  # Boilerplate code
s_custom = sp.symbols('s_{custom}', positive=True, real=True)  # Custom code
s_debug = sp.symbols('s_{debug}', positive=True, real=True)  # Debugging
s_write = sp.symbols('s_{write}', positive=True, real=True)  # Writing
s_lit = sp.symbols('s_{lit}', positive=True, real=True)  # Literature review
s_data = sp.symbols('s_{data}', positive=True, real=True)  # Data analysis
s_sim = sp.symbols('s_{sim}', positive=True, real=True)  # Simulation
s_valid = sp.symbols('s_{valid}', positive=True, real=True)  # Validation (slowdown)

# Task time allocation (fraction of total time)
f_boiler, f_custom, f_debug = sp.symbols('f_{boiler} f_{custom} f_{debug}', real=True, nonnegative=True)
f_write, f_lit, f_data = sp.symbols('f_{write} f_{lit} f_{data}', real=True, nonnegative=True)
f_sim, f_valid = sp.symbols('f_{sim} f_{valid}', real=True, nonnegative=True)

# Failure and success rates
p_success = sp.symbols('p_{success}', real=True, nonnegative=True)  # Base success probability
p_halluc = sp.symbols('p_{halluc}', real=True, nonnegative=True)  # AI hallucination probability
p_dead_end = sp.symbols('p_{dead}', real=True, nonnegative=True)  # Dead end probability
p_validation = sp.symbols('p_{valid}', real=True, nonnegative=True)  # Validation needed

# Learning rate
eta = sp.symbols('\\eta', real=True, nonnegative=True)  # Learning rate per year
eta_aug = sp.symbols('\\eta_{aug}', real=True, nonnegative=True)  # Augmented learning rate
eta_trad = sp.symbols('\\eta_{trad}', real=True, nonnegative=True)  # Traditional learning rate

# Output and productivity symbols
P = sp.symbols('P', integer=True, nonnegative=True)  # Publications output
E = sp.symbols('E', integer=True, nonnegative=True)  # Total events/tasks completed
R = sp.symbols('R', real=True, nonnegative=True)  # Output ratio (augmented/traditional)

# =============================================================================
# SECTION 1: TASK COMPLETION RATE MODEL
# =============================================================================

print("=" * 80)
print("SECTION 1: TASK COMPLETION RATE MODEL")
print("=" * 80)

# Base task completion rate (tasks per unit time per researcher)
lambda_0 = sp.symbols('\\lambda_0', positive=True, real=True)

# Time-weighted average speedup
# E[Speedup] = sum_k f_k * s_k (expectation over task mix)
avg_speedup = sp.Symbol('\\bar{s}')
speedup_expr = f_boiler * s_boiler + f_custom * s_custom + f_debug * s_debug + \
               f_write * s_write + f_lit * s_lit + f_data * s_data + \
               f_sim * s_sim + f_valid * s_valid

print(f"\nAverage Speedup (time-weighted):")
print(f"  \\bar{{s}} = \\sum_k f_k \\cdot s_k")
print(f"  = {speedup_expr}")

# =============================================================================
# SECTION 2: SKILL-BIASED EFFECTIVENESS MODEL
# =============================================================================

print("\n" + "=" * 80)
print("SECTION 2: SKILL-BIASED EFFECTIVENESS MODEL")
print("=" * 80)

# Skill level of a researcher (0 = novice, 1 = expert)
skill = sp.symbols('\\sigma', real=True, nonnegative=True)

# Skill-biased speedup modifier
# effective_speedup = base_speedup * (1 + alpha * (1 - skill))
# where alpha controls the skill-bias strength
alpha = sp.symbols('\\alpha', real=True, nonnegative=True)

# Effective speedup for a task with base speedup s
effective_s = sp.Function('s_{eff}')
effective_s_expr = s_boiler * (1 + alpha * (1 - skill))
print(f"\nSkill-Biased Speedup Modifier:")
print(f"  s_{{eff}}(\\sigma) = s \\cdot (1 + \\alpha \\cdot (1 - \\sigma))")
print(f"  = {effective_s_expr}")

print(f"\nInterpretation:")
print(f"  - If \\sigma = 0 (novice): s_{{eff}} = s \\cdot (1 + \\alpha)")
print(f"  - If \\sigma = 1 (expert): s_{{eff}} = s")
print(f"  - Alpha from Noy & Zhang 2023: \\alpha \\approx 0.4")

# Expected speedup over skill distribution N(mu_s, sigma_s^2)
# E[s_eff] = s * (1 + alpha * (1 - E[skill])) = s * (1 + alpha * (1 - mu_s))
expected_speedup = sp.Symbol('\\bar{s}_{eff}')
expected_speedup_expr = avg_speedup * (1 + alpha * (1 - mu_s))
print(f"\nExpected Speedup Over Skill Distribution:")
print(f"  E[s_{{eff}}] = \\bar{{s}} \\cdot (1 + \\alpha \\cdot (1 - \\mu_s))")
print(f"  = {expected_speedup_expr}")

# =============================================================================
# SECTION 3: OUTPUT FACTOR DERIVATION
# =============================================================================

print("\n" + "=" * 80)
print("SECTION 3: OUTPUT FACTOR DERIVATION")
print("=" * 80)

# Task completion over time T
# Traditional: E_trad(T) = lambda_0 * T * n_phd * (1 + eta_trad * T/2)
# Augmented: E_aug(T) = lambda_0 * T * n_phd * (1 + eta_aug * T/2) * E[s_eff]

E_trad = sp.Symbol('E_{trad}')
E_aug = sp.Symbol('E_{aug}')

# Traditional output (no AI multiplier)
E_trad_expr = lambda_0 * T * n_phd * (1 + eta_trad * T / 2)
print(f"\nTraditional Lab Task Completion (T years):")
print(f"  E_{{trad}}(T) = \\lambda_0 \\cdot T \\cdot n_{{PhD}} \\cdot (1 + \\eta_{{trad}} \\cdot T/2)")
print(f"  = {E_trad_expr}")

# Augmented output with skill-biased speedup
E_aug_expr = lambda_0 * T * n_phd * (1 + eta_aug * T / 2) * expected_speedup_expr
print(f"\nAugmented Lab Task Completion (T years):")
print(f"  E_{{aug}}(T) = \\lambda_0 \\cdot T \\cdot n_{{PhD}} \\cdot (1 + \\eta_{{aug}} \\cdot T/2) \\cdot E[s_{{eff}}]")
print(f"  = {E_aug_expr}")

# Output ratio R = E_aug / E_trad
R_expr = sp.simplify(E_aug_expr / E_trad_expr)
print(f"\nOutput Ratio (Augmented / Traditional):")
print(f"  R(T) = E_{{aug}}(T) / E_{{trad}}(T)")
print(f"  = {sp.simplify(R_expr)}")

# For small T (short time horizon), simplify
R_small_T = sp.series(R_expr, T, 0, 3).removeO()
print(f"\nFor small T (T << 1 year):")
print(f"  R(T) \\approx {R_small_T}")

# =============================================================================
# SECTION 4: PUBLICATION OUTPUT MODEL
# =============================================================================

print("\n" + "=" * 80)
print("SECTION 4: PUBLICATION OUTPUT MODEL")
print("=" * 80)

# Each task has a probability of leading to a publication
# This follows a cascade: idea -> method -> experiment -> analysis -> writing -> publication
# At each stage, there's a failure probability

# Stage probabilities (from Open Science Collaboration 2015, etc.)
p_idea = sp.symbols('p_{idea}', real=True, nonnegative=True)  # Idea is promising
p_method = sp.symbols('p_{method}', real=True, nonnegative=True)  # Method works
p_experiment = sp.symbols('p_{exp}', real=True, nonnegative=True)  # Experiment yields results
p_analysis = sp.symbols('p_{analysis}', real=True, nonnegative=True)  # Results are publishable
p_write = sp.symbols('p_{write}', real=True, nonnegative=True)  # Draft is completed
p_submit = sp.symbols('p_{submit}', real=True, nonnegative=True)  # Submitted
p_accept = sp.symbols('p_{accept}', real=True, nonnegative=True)  # Accepted

# Overall publication probability = product of stage probabilities
P_pub = sp.Symbol('P_{pub}')
P_pub_expr = p_idea * p_method * p_experiment * p_analysis * p_write * p_submit * p_accept
print(f"\nPublication Probability Cascade:")
print(f"  P_{{pub}} = p_{{idea}} \\cdot p_{{method}} \\cdot p_{{exp}} \\cdot p_{{analysis}} \\cdot p_{{write}} \\cdot p_{{submit}} \\cdot p_{{accept}}")
print(f"  = {P_pub_expr}")

# Expected publications over T
E_P_trad = sp.Symbol('E[P]_{trad}')
E_P_aug = sp.Symbol('E[P]_{aug}')

E_P_trad_expr = E_trad_expr * P_pub_expr
E_P_aug_expr = E_aug_expr * P_pub_expr * (1 - p_halluc)  # Hallucinations reduce effective output

print(f"\nExpected Publications (Traditional):")
print(f"  E[P]_{{trad}} = E_{{trad}}(T) \\cdot P_{{pub}}")
print(f"  = {sp.simplify(E_P_trad_expr)}")

print(f"\nExpected Publications (Augmented):")
print(f"  E[P]_{{aug}} = E_{{aug}}(T) \\cdot P_{{pub}} \\cdot (1 - p_{{halluc}})")
print(f"  = {sp.simplify(E_P_aug_expr)}")

# Publication output ratio
R_pub_expr = sp.simplify(E_P_aug_expr / E_P_trad_expr)
print(f"\nPublication Output Ratio:")
print(f"  R_{{pub}}(T) = {sp.simplify(R_pub_expr)}")

# =============================================================================
# SECTION 5: DEAD END AND HALLUCINATION MODEL
# =============================================================================

print("\n" + "=" * 80)
print("SECTION 5: DEAD END AND HALLUCINATION MODEL")
print("=" * 80)

# AI introduces new failure modes:
# 1. Hallucinations (false positive "results")
# 2. Dead ends from following AI-suggested wrong directions

# New symbols for dead end model
beta = sp.symbols('\\beta', real=True, nonnegative=True)  # AI pre-screening benefit
gamma = sp.symbols('\\gamma', real=True, nonnegative=True)  # Hallucination penalty

# Effective dead end rate for augmented lab
p_dead_aug = sp.Symbol('p_{dead,aug}')
p_dead_trad = sp.Symbol('p_{dead,trad}')

# Dead end probability increases with AI reliance on novel problems
# but decreases with AI pre-screening of obvious dead ends
p_dead_aug_expr = p_dead_trad * (1 - beta) + gamma * p_halluc
print(f"\nAugmented Dead End Probability:")
print(f"  p_{{dead,aug}} = p_{{dead,trad}} \\cdot (1 - \\beta) + \\gamma \\cdot p_{{halluc}}")
print(f"  where \\beta = AI pre-screening benefit, \\gamma = hallucination penalty")

# Time lost to dead ends
T_dead_trad = sp.Symbol('T_{dead,trad}')
T_dead_aug = sp.Symbol('T_{dead,aug}')

# Time lost proportional to dead end probability and time per direction
T_dead_trad_expr = T * p_dead_trad
T_dead_aug_expr = T * p_dead_aug_expr
print(f"\nTime Lost to Dead Ends:")
print(f"  Traditional: T_{{dead,trad}} = T \\cdot p_{{dead,trad}}")
print(f"  Augmented:    T_{{dead,aug}} = T \\cdot p_{{dead,aug}}")

# =============================================================================
# SECTION 6: SENSITIVITY ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("SECTION 6: SENSITIVITY ANALYSIS")
print("=" * 80)

# Partial derivatives of R with respect to key parameters
print("\nSensitivity: Output ratio R to skill distribution")

# Substitute realistic values for sensitivity analysis
param_subs = {
    mu_s: 0.5,      # Mean skill level
    eta_trad: 0.15, # Traditional learning rate
    eta_aug: 0.20,  # Augmented learning rate
    alpha: 0.4,    # Skill-bias strength (from Noy & Zhang 2023)
}

# For the base case, use realistic per-task speedups from RCTs
# Boilerplate: 1.55 (Peng et al.), Writing: 1.40 (Noy & Zhang)
# Validation: 0.90 (slowdown), Custom code: 1.00 (METR 2025)
task_subs = {
    s_boiler: 1.55,
    s_write: 1.40,
    s_debug: 1.30,
    s_lit: 1.30,
    s_data: 1.15,
    s_custom: 1.00,
    s_sim: 1.00,
    s_valid: 0.90,
}

# Typical task mix for research PhD (from Feldon et al. 2017)
mix_subs = {
    f_boiler: 0.15,
    f_custom: 0.20,
    f_debug: 0.10,
    f_write: 0.15,
    f_lit: 0.10,
    f_data: 0.15,
    f_sim: 0.10,
    f_valid: 0.05,
}

all_subs = {**param_subs, **task_subs, **mix_subs}

# Compute expected speedup with substitutions - use direct numerical values
# Typical task mix for research PhD (from Feldon et al. 2017) - normalized
task_mix = {
    'boiler': 0.15,
    'custom': 0.20,
    'debug': 0.10,
    'write': 0.15,
    'lit': 0.10,
    'data': 0.15,
    'sim': 0.10,
    'valid': 0.05,
}

# Task speedups from RCTs
task_speedups = {
    'boiler': 1.55,   # Peng et al. 2023 (55.8% faster)
    'custom': 1.00,   # METR 2025 (0% for skilled)
    'debug': 1.30,    # Microsoft internal
    'write': 1.40,    # Noy & Zhang 2023
    'lit': 1.30,      # Self-report
    'data': 1.15,     # Conservative
    'sim': 1.00,      # No AI for wet lab
    'valid': 0.90,    # Hallucination checking
}

# Compute average speedup
avg_speedup = sum(task_mix[k] * task_speedups[k] for k in task_mix)

# Skill-bias parameters from Noy & Zhang 2023
alpha = 0.40  # Skill-bias strength
mu_s = 0.50   # Mean skill level

# Expected effective speedup
expected_speedup = avg_speedup * (1 + alpha * (1 - mu_s))

# Learning rates
eta_trad = 0.15
eta_aug = 0.20

# Output ratio at T=2 years
T = 2
R_trad = 1 + eta_trad * T / 2
R_aug = (1 + eta_aug * T / 2) * expected_speedup
R_at_2yr = R_aug / R_trad

print(f"\nWith empirical parameters:")
print(f"  Average speedup \\bar{{s}} = {avg_speedup:.3f}")
print(f"  Expected effective speedup = {expected_speedup:.3f}")
print(f"  Output ratio at T={T} years: R = {R_at_2yr:.3f}")

# =============================================================================
# SECTION 7: FORMAL MODEL SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("SECTION 7: FORMAL MODEL SUMMARY")
print("=" * 80)

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EMERGENT ACTIVITY MODEL - EQUATIONS                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║ 1. TASK COMPLETION RATE                                                       ║
║    λ(t) = λ₀ · (1 + η · t) · [task mix weighted speedup]                     ║
║                                                                              ║
║ 2. SKILL-BIASED EFFECTIVENESS                                                 ║
║    s_eff(σ) = s_base · (1 + α · (1 - σ))                                     ║
║    where σ ~ N(μ_s, σ_s²), α ≈ 0.4 (from Noy & Zhang 2023)                   ║
║                                                                              ║
║ 3. OUTPUT FACTOR                                                              ║
║    R(T) = (1 + η_aug·T/2) / (1 + η_trad·T/2) · E[s_eff]                      ║
║                                                                              ║
║ 4. PUBLICATION OUTPUT                                                         ║
║    E[P]_trad = λ₀·T·n_PhD·(1+η_trad·T/2)·P_pub                               ║
║    E[P]_aug  = λ₀·T·n_PhD·(1+η_aug·T/2)·P_pub·(1-p_halluc)                  ║
║                                                                              ║
║ 5. DEAD END DYNAMICS                                                          ║
║    p_dead,aug = p_dead,trad·(1-β) + γ·p_halluc                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# EMPIRICAL PARAMETER VALUES (from research agents)
# =============================================================================

print("\n" + "=" * 80)
print("EMPIRICAL PARAMETER VALUES (from RCTs)")
print("=" * 80)

empirical_params = """
| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Boilerplate code speedup | s_boiler | 1.55x | Peng et al. 2023 (55.8% faster) |
| Writing speedup | s_write | 1.40x | Noy & Zhang 2023 (40% for below-median) |
| Debugging speedup | s_debug | 1.30x | Microsoft internal |
| Custom code speedup | s_custom | 1.00x | METR 2025 (0% for skilled) |
| Validation slowdown | s_valid | 0.90x | Hallucination checking |
| Skill-bias strength | α | 0.40 | Noy & Zhang 2023 |
| Mean skill level | μ_s | 0.50 | Normal distribution N(0.5, 0.15) |
| Traditional learning rate | η_trad | 0.15/yr | Literature familiarity |
| Augmented learning rate | η_aug | 0.20/yr | AI tool learning |
| Hallucination rate (science) | p_halluc | 0.10-0.20 | SimpleQA, PersonQA |
| Traditional dead end rate | p_dead,trad | 0.33 | Open Science 2015 |
| Publication cascade success | P_pub | ~0.12 | ~12% of directions → publication |
"""
print(empirical_params)

# Output for HTML generation
output_data = {
    'avg_speedup': float(avg_speedup),
    'expected_speedup': float(expected_speedup),
    'R_at_2yr': float(R_at_2yr),
}

print("\n✓ Model generation complete")
print(f"\nKey outputs for HTML:")
print(f"  - Average speedup: {output_data['avg_speedup']:.3f}x")
print(f"  - Expected effective speedup: {output_data['expected_speedup']:.3f}x")
print(f"  - Output ratio at 2 years: {output_data['R_at_2yr']:.3f}x")
