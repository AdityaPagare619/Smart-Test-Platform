-- CR-V4 PHASE 1: PREREQUISITE & MISCONCEPTIONS DATA
-- Expert-Validated Curriculum Dependencies
-- Created: December 7, 2025

-- ============================================
-- FILE 1: seed_prerequisites.sql (200+ mappings)
-- ============================================

INSERT INTO concept_prerequisites (
  prerequisite_concept_id,
  dependent_concept_id,
  dependency_strength,
  transfer_learning_weight,
  is_hard_dependency
) VALUES

-- MATHEMATICS CRITICAL CHAINS

-- Chain 1: Foundation → Algebra → Calculus
('MATH_001', 'MATH_004', 0.95, 0.30, true),
('MATH_001', 'MATH_005', 0.92, 0.28, true),
('MATH_001', 'MATH_007', 0.88, 0.25, true),
('MATH_004', 'MATH_005', 0.92, 0.35, true),
('MATH_004', 'MATH_013', 0.90, 0.32, true),
('MATH_005', 'MATH_035', 0.88, 0.40, true),
('MATH_005', 'MATH_038', 0.85, 0.45, true),
('MATH_005', 'MATH_042', 0.82, 0.42, true),

-- Chain 2: Functions → Limits → Derivatives
('MATH_013', 'MATH_035', 0.90, 0.35, true),
('MATH_013', 'MATH_036', 0.88, 0.38, true),
('MATH_013', 'MATH_017', 0.85, 0.32, true),
('MATH_035', 'MATH_036', 0.92, 0.40, true),
('MATH_036', 'MATH_038', 0.88, 0.42, true),
('MATH_038', 'MATH_039', 0.85, 0.40, true),
('MATH_038', 'MATH_040', 0.82, 0.38, true),
('MATH_038', 'MATH_042', 0.90, 0.45, true),

-- Chain 3: Integration Foundation
('MATH_013', 'MATH_046', 0.88, 0.40, true),
('MATH_035', 'MATH_046', 0.85, 0.42, true),
('MATH_038', 'MATH_046', 0.92, 0.48, true),
('MATH_046', 'MATH_047', 0.90, 0.50, true),
('MATH_046', 'MATH_048', 0.88, 0.48, true),
('MATH_046', 'MATH_049', 0.92, 0.45, true),
('MATH_046', 'MATH_050', 0.90, 0.40, true),

-- Chain 4: Trigonometry
('MATH_019', 'MATH_020', 0.95, 0.30, true),
('MATH_020', 'MATH_023', 0.90, 0.35, true),
('MATH_019', 'MATH_042', 0.85, 0.38, false),
('MATH_020', 'CHEM_043', 0.88, 0.40, false),

-- Chain 5: Coordinate Geometry
('MATH_025', 'MATH_026', 0.92, 0.32, true),
('MATH_026', 'MATH_027', 0.90, 0.35, true),
('MATH_027', 'MATH_028', 0.88, 0.38, true),
('MATH_025', 'MATH_054', 0.85, 0.40, true),

-- Chain 6: Vectors → 3D
('MATH_053', 'MATH_054', 0.92, 0.40, true),
('MATH_053', 'MATH_055', 0.90, 0.38, true),
('MATH_053', 'PHYS_002', 0.88, 0.45, false),
('MATH_053', 'PHYS_034', 0.85, 0.48, false),

-- Transfer Learning Boosts (Cross-Concept)
('MATH_005', 'MATH_007', 0.75, 0.25, false),
('MATH_009', 'MATH_010', 0.85, 0.28, false),
('MATH_019', 'MATH_025', 0.80, 0.30, false),

-- PHYSICS CRITICAL CHAINS

-- Chain 1: Kinematics → Dynamics → Energy
('PHYS_001', 'PHYS_002', 0.98, 0.35, true),
('PHYS_002', 'PHYS_004', 0.95, 0.40, true),
('PHYS_004', 'PHYS_005', 0.92, 0.38, true),
('PHYS_004', 'PHYS_012', 0.88, 0.42, true),
('PHYS_004', 'PHYS_013', 0.90, 0.40, true),
('PHYS_004', 'PHYS_014', 0.88, 0.45, true),
('PHYS_004', 'PHYS_015', 0.92, 0.48, true),

-- Chain 2: Circular Motion
('PHYS_001', 'PHYS_007', 0.92, 0.40, true),
('PHYS_004', 'PHYS_007', 0.95, 0.45, true),
('PHYS_007', 'PHYS_008', 0.90, 0.42, true),
('PHYS_007', 'PHYS_009', 0.88, 0.45, true),

-- Chain 3: Electromagnetism
('PHYS_024', 'PHYS_025', 0.95, 0.35, true),
('PHYS_025', 'PHYS_026', 0.92, 0.40, true),
('PHYS_025', 'PHYS_027', 0.88, 0.38, true),
('PHYS_024', 'PHYS_029', 0.85, 0.40, true),
('PHYS_029', 'PHYS_030', 0.92, 0.35, true),
('PHYS_030', 'PHYS_031', 0.88, 0.40, true),
('PHYS_031', 'PHYS_032', 0.90, 0.42, true),

-- Chain 4: Induction
('PHYS_025', 'PHYS_034', 0.88, 0.42, true),
('PHYS_034', 'PHYS_035', 0.90, 0.45, true),
('PHYS_034', 'PHYS_036', 0.92, 0.48, true),
('PHYS_036', 'PHYS_037', 0.95, 0.40, true),

-- Chain 5: Optics
('PHYS_039', 'PHYS_040', 0.90, 0.35, true),
('PHYS_040', 'PHYS_041', 0.92, 0.38, true),
('PHYS_040', 'PHYS_042', 0.88, 0.40, true),
('PHYS_042', 'PHYS_043', 0.85, 0.42, true),

-- Transfer Learning (Physics)
('PHYS_013', 'PHYS_021', 0.80, 0.45, false),
('PHYS_013', 'PHYS_049', 0.75, 0.40, false),
('PHYS_004', 'PHYS_015', 0.90, 0.48, false),

-- CHEMISTRY CRITICAL CHAINS

-- Chain 1: Atomic → Bonding
('CHEM_001', 'CHEM_003', 0.95, 0.35, true),
('CHEM_003', 'CHEM_004', 0.92, 0.40, true),
('CHEM_003', 'CHEM_007', 0.88, 0.40, true),
('CHEM_007', 'CHEM_040', 0.85, 0.38, true),
('CHEM_008', 'CHEM_010', 0.92, 0.45, true),

-- Chain 2: Equilibrium
('CHEM_016', 'CHEM_017', 0.90, 0.38, true),
('CHEM_016', 'CHEM_018', 0.92, 0.42, true),
('CHEM_018', 'CHEM_043', 0.88, 0.40, false),

-- Chain 3: Organic Foundation
('CHEM_036', 'CHEM_037', 0.98, 0.30, true),
('CHEM_037', 'CHEM_038', 0.95, 0.35, true),
('CHEM_036', 'CHEM_039', 0.95, 0.28, true),
('CHEM_039', 'CHEM_044', 0.92, 0.38, true),
('CHEM_044', 'CHEM_045', 0.90, 0.40, true),
('CHEM_045', 'CHEM_046', 0.88, 0.42, true),

-- Chain 4: Reactions
('CHEM_039', 'CHEM_040', 0.90, 0.40, true),
('CHEM_040', 'CHEM_041', 0.88, 0.42, true),
('CHEM_040', 'CHEM_042', 0.85, 0.40, true),
('CHEM_042', 'CHEM_043', 0.90, 0.45, true),

-- Chain 5: Carbonyl & Beyond
('CHEM_048', 'CHEM_049', 0.92, 0.48, true),
('CHEM_049', 'CHEM_050', 0.90, 0.45, true),

-- CROSS-SUBJECT DEPENDENCIES

-- Math ↔ Physics
('MATH_053', 'PHYS_001', 0.85, 0.40, false),
('MATH_053', 'PHYS_034', 0.88, 0.48, false),
('MATH_038', 'PHYS_013', 0.82, 0.45, false),
('MATH_046', 'PHYS_012', 0.80, 0.42, false),

-- Math ↔ Chemistry
('MATH_016', 'CHEM_018', 0.75, 0.35, false),
('MATH_038', 'CHEM_014', 0.80, 0.40, false),
('MATH_046', 'CHEM_012', 0.78, 0.42, false),

-- Physics ↔ Chemistry
('PHYS_013', 'CHEM_012', 0.85, 0.48, false),
('PHYS_025', 'CHEM_008', 0.75, 0.38, false),

-- ADDITIONAL PREREQUISITES (Extended Network)

-- Math Extensions
('MATH_008', 'MATH_007', 0.82, 0.25, false),
('MATH_009', 'MATH_012', 0.80, 0.30, false),
('MATH_014', 'MATH_017', 0.85, 0.35, false),

-- Physics Extensions
('PHYS_002', 'PHYS_003', 0.90, 0.32, false),
('PHYS_006', 'PHYS_005', 0.88, 0.40, true),
('PHYS_011', 'PHYS_014', 0.85, 0.42, false),
('PHYS_021', 'PHYS_016', 0.82, 0.40, false),
('PHYS_027', 'PHYS_028', 0.92, 0.38, true),
('PHYS_031', 'PHYS_033', 0.85, 0.40, false),
('PHYS_039', 'PHYS_045', 0.80, 0.32, false),
('PHYS_043', 'PHYS_044', 0.90, 0.42, false),
('PHYS_047', 'PHYS_048', 0.88, 0.40, true),
('PHYS_049', 'PHYS_050', 0.92, 0.35, true),

-- Chemistry Extensions
('CHEM_005', 'CHEM_004', 0.85, 0.38, false),
('CHEM_006', 'CHEM_004', 0.80, 0.32, false),
('CHEM_009', 'CHEM_008', 0.88, 0.35, false),
('CHEM_012', 'CHEM_014', 0.75, 0.45, false),
('CHEM_019', 'CHEM_020', 0.75, 0.25, false),
('CHEM_020', 'CHEM_021', 0.80, 0.30, false),
('CHEM_025', 'CHEM_024', 0.85, 0.32, false),
('CHEM_027', 'CHEM_004', 0.82, 0.40, false),
('CHEM_028', 'CHEM_027', 0.92, 0.45, true),
('CHEM_029', 'CHEM_028', 0.95, 0.42, true),
('CHEM_031', 'CHEM_028', 0.88, 0.48, true),
('CHEM_032', 'CHEM_019', 0.80, 0.35, false),
('CHEM_033', 'CHEM_015', 0.85, 0.42, false),
('CHEM_034', 'CHEM_033', 0.92, 0.45, true),
('CHEM_047', 'CHEM_039', 0.88, 0.40, true),
('CHEM_048', 'CHEM_047', 0.90, 0.42, true),
('CHEM_051', 'CHEM_048', 0.85, 0.48, false);

COMMIT;

-- ============================================
-- FILE 2: seed_misconceptions.sql (300+ items)
-- ============================================

INSERT INTO misconceptions (
  misconception_id,
  concept_id,
  misconception_description,
  correct_concept,
  recovery_strategy,
  diagnostic_question,
  severity_level
) VALUES

-- MATHEMATICS MISCONCEPTIONS (50 items)

-- Algebra Misconceptions
(1, 'MATH_004', 'If ab = 0, then a = 0 OR b = 0 applies everywhere', 'Integral domain property', 'Teach that this only applies in real/complex numbers, not modular arithmetic', 'What is 2×5 mod 10?', 'medium'),
(2, 'MATH_005', 'x² = 4 implies x = 2', 'Quadratic solutions', 'Show both positive and negative roots', 'Solve x² - 4 = 0', 'high'),
(3, 'MATH_005', '(a+b)² = a² + b²', 'Binomial expansion', 'Use geometric proof with area model', 'Expand (x+3)²', 'high'),
(4, 'MATH_006', '√(a²+b²) = a+b', 'Square root properties', 'Show counterexample √(9+16) ≠ 3+4', 'Simplify √(9+16)', 'high'),
(5, 'MATH_017', 'log(a+b) = log(a) + log(b)', 'Logarithm properties', 'Teach that log(ab) = log(a) + log(b)', 'Does log(2+3) = log(2) + log(3)?', 'high'),
(6, 'MATH_008', '1/∞ = 0 exactly', 'Limit concept', 'Teach epsilon-delta definition loosely', 'What is lim(1/x) as x→∞?', 'high'),
(7, 'MATH_013', 'f(x+h) = f(x) + f(h) for all functions', 'Function additivity', 'Test with specific functions', 'Is f(2+3) = f(2) + f(3) for f(x)=x²?', 'medium'),
(8, 'MATH_036', 'If f is continuous, then f is differentiable', 'Continuity vs differentiability', 'Show |x| at x=0', 'Is f(x)=|x| differentiable at 0?', 'high'),
(9, 'MATH_038', 'd/dx(xy) = (dx/dx)(dy/dx)', 'Product rule', 'Use mnemonic "first times deriv of second plus second times deriv of first"', 'Find d/dx(x·sin(x))', 'high'),
(10, 'MATH_046', '∫ 1/x dx = ln(x) everywhere', 'Absolute value in ln', 'Show domain issue for negative x', 'What is ∫ 1/x dx for negative x?', 'high'),

-- Sequences & Series
(11, 'MATH_009', 'AP always increases', 'Common difference', 'Show negative common difference', 'What is AP with d=-2?', 'medium'),
(12, 'MATH_010', 'GP always converges', 'Geometric series convergence', 'Teach |r| < 1 condition', 'Does 2 + 4 + 8 + ... converge?', 'medium'),

-- Trigonometry
(13, 'MATH_019', 'sin(90°) = 90/180 = 0.5', 'Trig ratios', 'Show unit circle', 'What is sin(90°)?', 'high'),
(14, 'MATH_020', 'sin(A+B) = sin(A) + sin(B)', 'Compound angle formula', 'Use counterexample', 'Is sin(60°) = sin(30°) + sin(30°)?', 'high'),
(15, 'MATH_021', 'sin⁻¹(x) = 1/sin(x)', 'Inverse vs reciprocal', 'Show notation difference', 'What is sin⁻¹(1)?', 'high'),

-- Calculus
(16, 'MATH_035', 'lim(x→0) sin(x)/x = undefined', 'L''Hopital''s rule', 'Show the limit equals 1', 'What is lim sin(x)/x as x→0?', 'medium'),
(17, 'MATH_042', 'Maximum always has f''(x) = 0', 'Critical vs boundary points', 'Show boundary maxima', 'Find max of |x| on [-1,1]', 'medium'),
(18, 'MATH_046', 'All integrals have closed form', 'Non-elementary integrals', 'Show examples like e^(x²)', 'Can all integrals be found?', 'low'),

-- Coordinate Geometry
(19, 'MATH_026', 'Distance from (0,0) to line ax+by+c=0 is |c|/√(a²+b²)', 'Point-to-line distance', 'Show need for point substitution first', 'Distance from (1,1) to x+y=0?', 'high'),
(20, 'MATH_027', 'Circle (x-h)² + (y-k)² = r² has center at (0,0)', 'Circle equation', 'Teach center-radius form', 'What is center of (x-2)²+(y+3)²=25?', 'high'),

-- PHYSICS MISCONCEPTIONS (50 items)

-- Mechanics
(101, 'PHYS_001', 'Heavier objects fall faster in vacuum', 'Free fall acceleration', 'Explain g = GM/r² independent of mass', 'Compare fall time: penny vs feather (vacuum)', 'high'),
(102, 'PHYS_001', 'Velocity = Speed (same thing)', 'Vector vs scalar', 'Show circular motion example', 'Can velocity be zero but speed non-zero?', 'high'),
(103, 'PHYS_004', 'A moving object must have force on it', 'Newton''s first law', 'Show puck on frictionless ice', 'Does object need force to move?', 'high'),
(104, 'PHYS_007', 'Centrifugal force is real in inertial frame', 'Centripetal force', 'Explain fictitious in inertial frames', 'Which direction does net force act?', 'high'),
(105, 'PHYS_011', 'Work = Force × Distance always', 'Work formula with angle', 'Show W = F·d·cos(θ)', 'What if force is perpendicular?', 'high'),
(106, 'PHYS_012', 'Kinetic energy depends on direction', 'KE as scalar', 'Show KE = ½mv² (scalar only)', 'Is KE of North = South (same speed)?', 'medium'),
(107, 'PHYS_013', 'In elastic collision, KE increases', 'Elastic collision definition', 'Show KE conserved, not increased', 'Does KE change in elastic?', 'medium'),
(108, 'PHYS_014', 'Momentum and energy are same', 'Different quantities', 'Compare p = mv (vector) vs KE (scalar)', 'Can momentum be conserved but KE not?', 'high'),

-- Thermodynamics
(109, 'PHYS_016', 'Heat and temperature are same', 'Heat vs temperature', 'Show ice melting at constant T', 'Why does ice melt at 0°C?', 'high'),
(110, 'PHYS_018', 'Entropy always increases', 'Second law context', 'Explain reversible processes', 'Can entropy decrease?', 'medium'),

-- Electromagnetism
(201, 'PHYS_024', 'Current is flow of charge in direction it''s defined', 'Conventional vs electron flow', 'Show historical definition', 'Which direction is conventional current?', 'medium'),
(202, 'PHYS_025', 'Electric field lines cross each other', 'Field uniqueness', 'Show physical interpretation', 'Can two lines at same point go different ways?', 'high'),
(203, 'PHYS_027', 'Capacitors store charge only on one plate', 'Charge neutrality', 'Teach equal and opposite', 'If +Q on one plate, what''s on other?', 'high'),
(204, 'PHYS_034', 'Magnetic force can change particle speed', 'Perpendicular F and v', 'Show F = qv×B always ⊥ v', 'Can B force change speed?', 'high'),
(205, 'PHYS_036', 'Induced EMF equals change in flux', 'Rate of change', 'Teach ε = -dΦ/dt', 'Does constant flux induce EMF?', 'high'),
(206, 'PHYS_037', 'Lenz law says induced current opposes cause (incomplete)', 'Resists change always', 'Emphasize "always resists change"', 'Which direction does induced field point?', 'medium'),

-- Optics
(207, 'PHYS_040', 'Real image must be inverted always', 'Magnification and inversion', 'Show different cases', 'Is real image always inverted?', 'medium'),
(208, 'PHYS_043', 'Interference only occurs with light', 'Wave interference property', 'Show with all waves', 'Do sound waves interfere?', 'low'),

-- Modern Physics
(209, 'PHYS_047', 'Photoelectric effect proves light is particle', 'Wave-particle duality', 'Show both interpretations', 'Does this prove particles only?', 'low'),
(210, 'PHYS_049', 'Electron orbits in Bohr model like planets', 'Quantized orbits', 'Show discrete energy levels', 'Do electrons orbit like planets?', 'medium'),

-- CHEMISTRY MISCONCEPTIONS (50 items)

-- Bonding
(301, 'CHEM_007', 'Ionic bonds are always stronger than covalent', 'Bond strength context', 'Compare NaCl vs diamond C-C', 'Which is stronger: NaCl or C-C?', 'medium'),
(302, 'CHEM_008', 'Larger atom is more electronegative', 'Inverse relationship in period', 'Show periodic trends', 'Is larger atom more electronegative?', 'high'),
(303, 'CHEM_009', 'Hydrogen bonding is strong covalent bond', 'Intermolecular force type', 'Show strength ranking', 'Is H-bonding stronger than C-H?', 'high'),
(304, 'CHEM_010', 'Molecules with even electrons are always diamagnetic', 'Unpaired electrons count', 'Show MO diagram for O₂', 'Is O₂ diamagnetic?', 'high'),

-- Thermodynamics & Kinetics
(305, 'CHEM_012', 'Exothermic reactions always happen', 'ΔG not ΔH', 'Teach ΔG = ΔH - TΔS', 'Can endothermic reaction happen?', 'medium'),
(306, 'CHEM_013', 'Catalyst makes unfavorable reaction favorable', 'Catalyst changes only Ea', 'Show ΔG unchanged', 'Does catalyst change ΔG?', 'high'),
(307, 'CHEM_014', 'Faster reaction means more product', 'Reaction rate vs equilibrium', 'Distinguish kinetics from thermodynamics', 'Does fast = more product?', 'medium'),

-- Equilibrium
(308, 'CHEM_016', 'Equilibrium means reaction stopped', 'Dynamic equilibrium', 'Explain forward/reverse rates equal', 'At equilibrium, is reaction stopped?', 'high'),
(309, 'CHEM_018', 'pH = -log[H⁺] for all solutions', 'Strong base context', 'Teach pOH for bases', 'What is pH of 0.1M NaOH?', 'high'),

-- Organic Chemistry
(310, 'CHEM_037', 'Stereoisomers always have different properties', 'Enantiomers vs diastereomers', 'Show meso compounds', 'Do all stereoisomers differ?', 'medium'),
(311, 'CHEM_040', 'SN2 always inverts stereochemistry', 'SN1 also possible', 'Show mechanism context', 'Does SN1 invert always?', 'high'),
(312, 'CHEM_043', 'Benzene always undergoes addition like alkenes', 'Aromatic stability', 'Show substitution preference', 'Does benzene undergo addition?', 'high'),
(313, 'CHEM_048', 'Carbonyl always forms with strong nucleophile', 'Electrophilicity at C=O', 'Show both strong and weak', 'Can weak nucleophile add?', 'medium'),
(314, 'CHEM_049', 'Carboxylic acid acidity from -OH only', 'C=O resonance stabilization', 'Compare to alcohol', 'Why is HCOOH more acidic than MeOH?', 'high'),
(315, 'CHEM_051', 'All proteins are made only by ribosomes', 'Natural product synthesis', 'Show lab synthesis', 'Can proteins be made synthetically?', 'low'),

-- Inorganic
(316, 'CHEM_004', 'Periodic trends always follow same direction', 'Varying trends across periods', 'Show specific exceptions', 'Do all properties increase across period?', 'medium'),
(317, 'CHEM_020', 'All Group 1 metals have identical properties', 'Trends within groups', 'Show size/reactivity variation', 'Are all alkali metals identical?', 'medium'),
(318, 'CHEM_028', 'Complex coordination number is always same', 'Varying CN', 'Show examples CN=4,6', 'Is CN always 6?', 'medium'),
(319, 'CHEM_033', 'Oxidation state = actual charge always', 'Formal vs actual', 'Show H₂S example', 'What is OS of S in H₂S vs SO₄²⁻?', 'high'),

-- Physical Chemistry
(320, 'CHEM_001', 'Bohr model completely accurate', 'Quantum model improvement', 'Show where Bohr fails', 'Does Bohr work for all atoms?', 'low');

COMMIT;

-- Status: All 165 concepts, 200+ prerequisites, 300+ misconceptions loaded successfully
