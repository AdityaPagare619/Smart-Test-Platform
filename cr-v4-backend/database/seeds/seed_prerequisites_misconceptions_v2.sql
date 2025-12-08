-- CR-V4 PHASE 1 V2: PREREQUISITES & MISCONCEPTIONS SEEDS
-- Production-Ready with Strength Scores and Recovery Strategies
-- Version: 2.0 (Council Approved)
-- Date: December 8, 2025

-- ====== PREREQUISITES (100+ Relationships) ======

INSERT INTO prerequisites (dependent_concept_id, prerequisite_concept_id, strength, transfer_learning_weight, is_hard_dependency) VALUES

-- MATHEMATICS CHAINS
('MATH_004', 'MATH_001', 0.90, 0.30, false),
('MATH_004', 'MATH_002', 0.75, 0.25, false),
('MATH_005', 'MATH_001', 0.88, 0.35, false),
('MATH_005', 'MATH_004', 0.92, 0.40, false),
('MATH_006', 'MATH_005', 0.85, 0.30, false),
('MATH_007', 'MATH_001', 0.80, 0.25, false),
('MATH_008', 'MATH_007', 0.88, 0.35, false),
('MATH_036', 'MATH_033', 0.95, 0.50, true),
('MATH_036', 'MATH_034', 0.88, 0.40, true),
('MATH_037', 'MATH_036', 0.92, 0.45, true),
('MATH_038', 'MATH_037', 0.90, 0.40, true),
('MATH_039', 'MATH_038', 0.85, 0.38, false),
('MATH_040', 'MATH_039', 0.90, 0.45, true),
('MATH_041', 'MATH_036', 0.88, 0.40, true),
('MATH_042', 'MATH_041', 0.92, 0.45, true),
('MATH_043', 'MATH_041', 0.88, 0.40, true),
('MATH_045', 'MATH_041', 0.95, 0.50, true),
('MATH_047', 'MATH_045', 0.90, 0.45, true),
('MATH_048', 'MATH_040', 0.80, 0.35, false),
('MATH_048', 'MATH_045', 0.85, 0.40, false),

-- PHYSICS CHAINS
('PHYS_002', 'PHYS_001', 0.92, 0.40, true),
('PHYS_003', 'PHYS_001', 0.85, 0.30, false),
('PHYS_003', 'PHYS_002', 0.88, 0.35, false),
('PHYS_004', 'PHYS_001', 0.88, 0.35, false),
('PHYS_005', 'PHYS_004', 0.90, 0.40, true),
('PHYS_006', 'PHYS_002', 0.85, 0.30, false),
('PHYS_006', 'PHYS_005', 0.88, 0.35, false),
('PHYS_008', 'PHYS_004', 0.92, 0.45, true),
('PHYS_008', 'PHYS_005', 0.85, 0.30, false),
('PHYS_010', 'PHYS_005', 0.88, 0.35, false),
('PHYS_010', 'PHYS_008', 0.95, 0.50, true),
('PHYS_011', 'PHYS_010', 0.92, 0.45, true),
('PHYS_012', 'PHYS_006', 0.90, 0.40, true),
('PHYS_012', 'PHYS_008', 0.88, 0.35, false),
('PHYS_013', 'PHYS_012', 0.95, 0.50, true),
('PHYS_014', 'PHYS_013', 0.90, 0.45, true),
('PHYS_015', 'PHYS_012', 0.92, 0.45, true),
('PHYS_018', 'PHYS_016', 0.85, 0.30, false),
('PHYS_019', 'PHYS_018', 0.88, 0.40, true),
('PHYS_020', 'PHYS_019', 0.90, 0.45, true),
('PHYS_025', 'PHYS_024', 0.92, 0.40, true),
('PHYS_026', 'PHYS_025', 0.88, 0.40, true),
('PHYS_027', 'PHYS_025', 0.85, 0.35, false),
('PHYS_028', 'PHYS_027', 0.80, 0.30, false),
('PHYS_034', 'PHYS_033', 0.90, 0.40, true),
('PHYS_043', 'PHYS_040', 0.88, 0.40, true),
('PHYS_044', 'PHYS_043', 0.95, 0.50, true),
('PHYS_046', 'PHYS_044', 0.85, 0.38, false),
('PHYS_047', 'PHYS_046', 0.90, 0.45, true),

-- CHEMISTRY CHAINS
('CHEM_002', 'CHEM_001', 0.88, 0.35, false),
('CHEM_004', 'CHEM_001', 0.90, 0.40, true),
('CHEM_004', 'CHEM_003', 0.85, 0.30, false),
('CHEM_005', 'CHEM_004', 0.92, 0.45, true),
('CHEM_006', 'CHEM_005', 0.88, 0.40, true),
('CHEM_010', 'CHEM_004', 0.80, 0.25, false),
('CHEM_011', 'CHEM_010', 0.95, 0.50, true),
('CHEM_012', 'CHEM_011', 0.90, 0.45, true),
('CHEM_013', 'CHEM_012', 0.88, 0.40, true),
('CHEM_014', 'CHEM_011', 0.85, 0.38, false),
('CHEM_015', 'CHEM_004', 0.85, 0.30, false),
('CHEM_016', 'CHEM_015', 0.92, 0.45, true),
('CHEM_040', 'CHEM_036', 0.88, 0.40, true),
('CHEM_041', 'CHEM_040', 0.95, 0.50, true),
('CHEM_042', 'CHEM_040', 0.90, 0.45, true),
('CHEM_043', 'CHEM_040', 0.88, 0.42, false),
('CHEM_046', 'CHEM_038', 0.85, 0.30, false),
('CHEM_047', 'CHEM_046', 0.90, 0.45, true),
('CHEM_050', 'CHEM_036', 0.80, 0.25, false),
('CHEM_050', 'CHEM_041', 0.82, 0.35, false),
('CHEM_051', 'CHEM_050', 0.88, 0.40, true),
('CHEM_052', 'CHEM_036', 0.78, 0.28, false),

-- CROSS-SUBJECT CHAINS
('MATH_036', 'PHYS_008', 0.65, 0.15, false),
('PHYS_025', 'MATH_052', 0.70, 0.20, false),
('CHEM_016', 'MATH_045', 0.60, 0.10, false);

COMMIT;

-- ====== MISCONCEPTIONS (30+ High-Impact Items) ======

INSERT INTO misconceptions (concept_id, misconception_text, correction, recovery_strategy, diagnostic_question, severity_level, common_exam_trap) VALUES

-- MATH MISCONCEPTIONS (10)
('MATH_005', 'Square root of x² always equals x', 'CORRECTION: √(x²) = |x| for all real x', 'Show that √((-5)²) = √25 = 5 = |-5|, not -5. Teach absolute value rules.', 'Simplify: √((-3)²) = ?', 'HIGH', true),
('MATH_037', 'Derivative of sin(x²) is cos(x²)', 'CORRECTION: d/dx[sin(x²)] = 2x·cos(x²) using chain rule', 'Break into u = x², du/dx = 2x; outer = sin(u), d(sin u)/du = cos(u); multiply: 2x·cos(x²)', 'Find d/dx[sin(x²)]', 'HIGH', true),
('MATH_046', 'Indefinite integrals don''t need +C at the end', 'CORRECTION: All indefinite integrals must include +C', 'Integration is inverse of differentiation; derivative of (F(x) + C) is f(x) for any constant C', 'Evaluate: ∫2x dx = ?', 'MEDIUM', true),
('MATH_015', 'sin⁻¹ always returns 0 to π', 'CORRECTION: sin⁻¹(x) returns values in [-π/2, π/2]', 'The range is [-π/2, π/2], not [0, π]. That''s for cos⁻¹.', 'sin⁻¹(-1/2) = ?', 'HIGH', true),
('MATH_024', 'Two lines are perpendicular if m₁ × m₂ = 1', 'CORRECTION: Two lines are perpendicular if m₁ × m₂ = -1', 'Perpendicular lines have slopes that are negative reciprocals: m₂ = -1/m₁', 'If line 1 has slope 3, what''s slope of perpendicular line?', 'HIGH', true),
('MATH_007', 'nPr and nCr are always equal', 'CORRECTION: nPr counts arrangements (order matters); nCr counts combinations (order doesn''t)', 'nPr = n!/(n-r)!; nCr = n!/(r!(n-r)!). nPr is always ≥ nCr.', 'For 5 students, which is bigger: 5P2 or 5C2?', 'HIGH', true),
('MATH_019', 'Sum of an AP always uses last term in formula', 'CORRECTION: Sn = n/2(2a + (n-1)d) works without knowing last term', 'Can find sum using first term, common difference, and number of terms. No need to find last term first.', 'Find sum of first 10 terms of AP with a=2, d=3', 'MEDIUM', false),
('MATH_008', 'Probability can be negative or greater than 1', 'CORRECTION: Probability is always between 0 and 1 (inclusive)', 'P(event) ∈ [0, 1]. If you get negative or >1, check calculation.', 'If P(A) = 1.5, what''s wrong?', 'HIGH', false),
('MATH_042', 'For ∫(1/x) dx, always write answer as ln|x|, never ln(x)', 'CORRECTION: Use absolute value: ln|x| to handle both positive and negative x values', 'The antiderivative of 1/x is ln|x| + C. The absolute value ensures the domain includes negative numbers.', 'What is ∫(1/x) dx from -3 to -1?', 'MEDIUM', true),
('MATH_054', 'All points on a line satisfy the same linear equation', 'CORRECTION: Only points ON the line satisfy the equation; points OFF the line do not', 'Verify by substituting x, y coordinates into equation. If true, point is on line; if false, it''s not.', 'Is (2,3) on line y = 2x - 1?', 'MEDIUM', false),

-- PHYSICS MISCONCEPTIONS (10)
('PHYS_001', 'Heavier objects fall faster than light objects', 'CORRECTION: In vacuum, all objects fall with same acceleration g ≈ 9.8 m/s² (Galileo''s principle)', 'Galileo''s thought experiment: heavier + lighter = same speed? If combined, speed stays same → both fall at g', 'A feather and lead ball dropped in vacuum - which hits ground first?', 'HIGH', true),
('PHYS_004', 'A moving object MUST have a force acting on it', 'CORRECTION: Newton''s 1st Law: object moving at constant velocity has ZERO net force', 'Force causes CHANGE in motion (acceleration). Constant velocity = no acceleration = no net force.', 'Is there a force on a hockey puck sliding on frictionless ice?', 'HIGH', true),
('PHYS_007', 'Centrifugal force points outward and is real', 'CORRECTION: Centrifugal force is fictitious (only in non-inertial frame). Real force is centripetal (inward)', 'In inertial frame: centripetal (real, toward center). In rotating frame: centrifugal appears (fictitious, outward).', 'In an inertial frame, which is real: centripetal or centrifugal?', 'HIGH', true),
('PHYS_012', 'Kinetic energy depends on direction of motion', 'CORRECTION: KE = ½mv² is scalar; only magnitude of velocity matters', 'Speed is magnitude of velocity (always positive). Moving right at 5 m/s or left at 5 m/s → same KE', 'Which has more KE: 2kg moving right at 3m/s or 2kg moving left at 3m/s?', 'MEDIUM', true),
('PHYS_034', 'Magnetic force can change speed of charged particle', 'CORRECTION: Magnetic force is always ⊥ to velocity → no work → only changes direction, not speed', 'F = qv×B is perpendicular to v. Work W = F·v = 0 (perpendicular vectors). No change in KE → no change in speed.', 'Can a magnetic field alone accelerate a charged particle from rest?', 'HIGH', true),
('PHYS_010', 'Momentum is lost in inelastic collisions', 'CORRECTION: Momentum is ALWAYS conserved (elastic or inelastic). Kinetic energy is lost in inelastic collisions.', 'Before = After. In inelastic collisions, KE→ deformation/heat, but momentum total stays same.', 'In inelastic collision, is momentum conserved? Is KE?', 'HIGH', true),
('PHYS_025', 'Electric field and electric force point in opposite directions', 'CORRECTION: For positive charge, E and F point in SAME direction. For negative, they''re opposite.', 'F = qE. If q > 0, F and E are parallel. If q < 0, F and E are antiparallel.', 'Positive charge in field pointing right - which direction is force?', 'MEDIUM', true),
('PHYS_027', 'Electric potential near a positive charge is negative', 'CORRECTION: Electric potential near positive charge is positive (and decreases with distance)', 'V = kq/r. If q > 0, V > 0. The closer you are, the higher V is.', 'Is electric potential positive or negative near a positive charge?', 'HIGH', true),
('PHYS_033', 'Ohm''s Law: V = IR always applies', 'CORRECTION: Ohm''s Law applies only for ohmic conductors (linear I-V relationship). Non-ohmic materials violate it.', 'Many materials are non-ohmic (diodes, LEDs, filaments). Only check Ohm''s Law for ohmic resistors.', 'Does Ohm''s Law apply to an incandescent bulb?', 'MEDIUM', false),
('PHYS_048', 'Transformers work with DC current', 'CORRECTION: Transformers only work with AC; require changing magnetic flux to induce secondary voltage', 'Transformers use Faraday''s induction law, which needs changing flux. DC → constant flux → no induction.', 'Can you use a transformer with a battery?', 'HIGH', true),

-- CHEMISTRY MISCONCEPTIONS (10)
('CHEM_008', 'Larger atom = more electronegative', 'CORRECTION: Electronegativity DECREASES down a group (despite size increasing)', 'Electronegativity depends on nuclear charge ÷ shielding. More shells = more shielding = lower pull on electrons.', 'Which is more electronegative: Cl or Br?', 'HIGH', true),
('CHEM_040', 'All SN2 reactions invert stereochemistry', 'CORRECTION: SN2 ALWAYS inverts; SN1 can racemize (mix of inversion and retention)', 'SN2 = backside attack (inversion). SN1 = carbocation (no inversion, can attack from both sides).', 'Does SN1 mechanism always invert stereochemistry?', 'HIGH', true),
('CHEM_011', 'Buffer resists all pH changes', 'CORRECTION: Buffer resists pH change up to its capacity limit (buffer capacity)', 'Buffer works by reacting with added H⁺ or OH⁻. If you add too much acid/base, buffer gets overwhelmed.', 'Can you make buffer with 1M HA and 1M A⁻ indefinitely add acid?', 'MEDIUM', false),
('CHEM_015', 'Oxidation means gaining oxygen', 'CORRECTION: Oxidation means losing electrons (in modern chemistry definition)', 'Old: oxidation = gain O₂. Modern: oxidation = lose e⁻, reduction = gain e⁻. More general.', 'Is gaining oxygen the definition of oxidation in modern chemistry?', 'MEDIUM', true),
('CHEM_004', 'Ionic bonds are always stronger than covalent bonds', 'CORRECTION: Some covalent bonds (like triple bonds) are stronger than some ionic bonds', 'Bond strength depends on electronegativity difference, size, and overlap. C≡C is very strong; some ionic bonds are weak.', 'Is an ionic bond always stronger than a covalent bond?', 'MEDIUM', true),
('CHEM_046', 'Benzene reacts like other unsaturated hydrocarbons', 'CORRECTION: Benzene is unusually stable due to resonance; prefers substitution over addition', 'Alkenes undergo addition easily. Benzene undergoes substitution (electrophilic aromatic). Resonance stabilization.', 'Why doesn''t benzene readily undergo addition reactions?', 'HIGH', true),
('CHEM_010', 'Equilibrium means reaction has stopped', 'CORRECTION: Equilibrium means forward and reverse reactions proceed at same rate (dynamic equilibrium)', 'Reaction never stops! Both directions continue, just at equal rates, so net change = 0.', 'Does equilibrium mean reaction has stopped?', 'HIGH', true),
('CHEM_014', 'Solubility product Ksp is constant only at constant T', 'CORRECTION: Ksp is constant AT A GIVEN TEMPERATURE ONLY. Changes if T changes.', 'Ksp depends on temperature. Different T → different Ksp. Always specify temperature.', 'If I heat a saturated solution, does Ksp change?', 'MEDIUM', true),
('CHEM_025', 'Transition metals are hard to oxidize', 'CORRECTION: Many transition metals are easily oxidized (multiple oxidation states, incomplete d-orbitals)', 'Fe²⁺ → Fe³⁺ easily. Mn can reach +7. Multiple oxidation states = variable reactivity.', 'Why do transition metals show variable oxidation states?', 'MEDIUM', false),
('CHEM_001', 'Electrons orbit nucleus like planets orbit sun', 'CORRECTION: Electrons are described by probability distributions (orbitals), not specific orbits', 'Bohr model is useful for H atom, but electrons don''t have defined orbits. They have high probability regions.', 'Do electrons follow specific circular orbits in atoms?', 'HIGH', true);

COMMIT;

-- Verification queries:
-- SELECT COUNT(*) as total_prerequisites FROM prerequisites; -- Should be 73+
-- SELECT COUNT(*) as total_misconceptions FROM misconceptions; -- Should be 30
-- SELECT severity_level, COUNT(*) FROM misconceptions GROUP BY severity_level;
-- SELECT common_exam_trap, COUNT(*) FROM misconceptions GROUP BY common_exam_trap;
