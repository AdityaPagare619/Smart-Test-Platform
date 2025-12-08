-- CR-V4 PHASE 1: COMPLETE SQL SEED DATA
-- Database Population Script
-- Created: December 7, 2025
-- Status: PRODUCTION READY

-- ============================================
-- FILE 1: seed_concepts_mathematics.sql
-- ============================================

INSERT INTO concepts (
  concept_id, 
  name, 
  subject, 
  layer_level, 
  difficulty, 
  exam_weightage, 
  typical_mastery_time_hours,
  nta_frequency_papers,
  irt_difficulty,
  description,
  learning_outcomes
) VALUES

-- LAYER 1: FOUNDATION (8 concepts)
('MATH_001', 'Number System', 'Mathematics', 1, 0.20, 0.015, 2, 22, 0.30, 'Integers, rationals, irrationals, real numbers', 'Understand number properties'),
('MATH_002', 'Sets & Relations', 'Mathematics', 1, 0.25, 0.018, 2, 20, 0.35, 'Set operations, relations, functions basics', 'Operate on sets effectively'),
('MATH_003', 'Number Theory', 'Mathematics', 1, 0.30, 0.021, 2.5, 12, 0.45, 'Divisibility, primes, modular arithmetic', 'Apply number theory to problems'),
('MATH_004', 'Linear Equations', 'Mathematics', 1, 0.35, 0.025, 3, 25, 0.40, 'Single and multiple variable equations', 'Solve linear systems'),
('MATH_005', 'Quadratic Equations', 'Mathematics', 1, 0.40, 0.032, 3.5, 28, 0.50, 'Quadratic equations, nature of roots', 'Solve and analyze quadratics'),
('MATH_006', 'Inequalities & Modulus', 'Mathematics', 1, 0.35, 0.028, 3, 18, 0.45, 'Linear and quadratic inequalities, modulus', 'Solve inequalities systematically'),
('MATH_007', 'Permutations & Combinations', 'Mathematics', 1, 0.45, 0.035, 4, 16, 0.55, 'Counting principles, nPr, nCr', 'Apply counting principles'),
('MATH_008', 'Probability', 'Mathematics', 1, 0.50, 0.038, 4, 10, 0.60, 'Classical probability, conditional probability', 'Calculate probabilities'),

-- LAYER 2: SEQUENCES & SERIES (4 concepts)
('MATH_009', 'Arithmetic Progression', 'Mathematics', 2, 0.35, 0.022, 2.5, 15, 0.40, 'AP formulas, sum formulas', 'Work with AP problems'),
('MATH_010', 'Geometric Progression', 'Mathematics', 2, 0.40, 0.025, 3, 14, 0.45, 'GP formulas, infinite series', 'Solve GP applications'),
('MATH_011', 'Harmonic Progression', 'Mathematics', 2, 0.45, 0.018, 2.5, 8, 0.50, 'HP formulas and applications', 'Apply HP concepts'),
('MATH_012', 'Sum Formulas & Series', 'Mathematics', 2, 0.40, 0.020, 2.5, 10, 0.45, 'Sigma notation, series summation', 'Evaluate series'),

-- LAYER 3: FUNCTIONS & RELATIONS (6 concepts)
('MATH_013', 'Functions', 'Mathematics', 2, 0.40, 0.025, 3, 15, 0.50, 'Domain, range, classification', 'Analyze functions'),
('MATH_014', 'Composite & Inverse', 'Mathematics', 2, 0.45, 0.023, 3, 11, 0.55, 'Function composition, inverse', 'Find composite and inverse'),
('MATH_015', 'Function Transformations', 'Mathematics', 2, 0.35, 0.015, 2, 6, 0.40, 'Shifts, stretches, reflections', 'Transform functions'),
('MATH_016', 'Periodic & Even-Odd', 'Mathematics', 2, 0.40, 0.018, 2.5, 9, 0.45, 'Even, odd, periodic functions', 'Classify functions'),
('MATH_017', 'Logarithmic & Exponential', 'Mathematics', 2, 0.50, 0.030, 3.5, 14, 0.60, 'Log and exponential properties', 'Solve exponential/log equations'),
('MATH_018', 'Binomial Theorem', 'Mathematics', 2, 0.45, 0.028, 3, 13, 0.55, 'Binomial expansion, general term', 'Apply binomial theorem'),

-- TRIGONOMETRY (6 concepts)
('MATH_019', 'Trigonometric Ratios', 'Mathematics', 3, 0.35, 0.020, 3, 21, 0.40, 'Trig ratios, unit circle', 'Use trig ratios'),
('MATH_020', 'Trigonometric Identities', 'Mathematics', 3, 0.50, 0.025, 4, 12, 0.60, 'Trig identities and equations', 'Prove and use identities'),
('MATH_021', 'Inverse Trigonometric', 'Mathematics', 3, 0.55, 0.022, 4, 9, 0.65, 'Inverse trig functions', 'Find inverse trig values'),
('MATH_022', 'Height & Distance', 'Mathematics', 3, 0.40, 0.015, 2.5, 5, 0.45, 'Applied trig problems', 'Solve height/distance problems'),
('MATH_023', 'Compound Angles', 'Mathematics', 3, 0.50, 0.020, 3.5, 8, 0.60, 'Compound angle formulas', 'Apply compound angle formulas'),
('MATH_024', 'General Solution', 'Mathematics', 3, 0.55, 0.018, 3, 6, 0.65, 'General solution of trig equations', 'Find general solutions'),

-- COORDINATE GEOMETRY (10 concepts)
('MATH_025', 'Distance & Section', 'Mathematics', 4, 0.30, 0.015, 2, 18, 0.35, 'Distance formula, section formula', 'Apply distance/section formulas'),
('MATH_026', 'Straight Line', 'Mathematics', 4, 0.35, 0.020, 2.5, 22, 0.40, 'Line equations, slope', 'Find line equations'),
('MATH_027', 'Circle', 'Mathematics', 4, 0.40, 0.023, 3, 20, 0.50, 'Circle equation, properties', 'Work with circles'),
('MATH_028', 'Circle Tangents & Chords', 'Mathematics', 4, 0.50, 0.020, 3.5, 11, 0.60, 'Tangent and chord properties', 'Solve tangent/chord problems'),
('MATH_029', 'Pair of Lines', 'Mathematics', 4, 0.45, 0.018, 3, 8, 0.55, 'Pair of lines, angle', 'Handle pair of lines'),
('MATH_030', 'Parabola', 'Mathematics', 4, 0.50, 0.020, 3.5, 10, 0.60, 'Parabola equation, properties', 'Apply parabola concepts'),
('MATH_031', 'Ellipse', 'Mathematics', 4, 0.50, 0.018, 3.5, 9, 0.60, 'Ellipse equation, properties', 'Use ellipse concepts'),
('MATH_032', 'Hyperbola', 'Mathematics', 4, 0.55, 0.015, 4, 6, 0.65, 'Hyperbola equation, properties', 'Apply hyperbola concepts'),
('MATH_033', 'Parametric Forms', 'Mathematics', 4, 0.60, 0.012, 3, 4, 0.70, 'Parametric equations', 'Use parametric forms'),
('MATH_034', 'Reflection & Rotation', 'Mathematics', 4, 0.55, 0.008, 2.5, 3, 0.65, 'Axis rotation, reflection', 'Rotate and reflect curves'),

-- CALCULUS - LIMITS & DERIVATIVES (7 concepts)
('MATH_035', 'Limits', 'Mathematics', 5, 0.40, 0.022, 3, 12, 0.50, 'Limit definition, evaluation', 'Evaluate limits'),
('MATH_036', 'Continuity & Differentiability', 'Mathematics', 5, 0.45, 0.025, 3.5, 11, 0.55, 'Continuity, differentiability conditions', 'Check continuity/differentiability'),
('MATH_037', 'MVT & Rolles', 'Mathematics', 5, 0.55, 0.018, 3, 7, 0.65, 'Mean value theorem, Rolles theorem', 'Apply MVT and Rolles'),
('MATH_038', 'Derivatives', 'Mathematics', 5, 0.40, 0.028, 3.5, 23, 0.50, 'Derivative rules, chain rule', 'Differentiate functions'),
('MATH_039', 'Parametric Differentiation', 'Mathematics', 5, 0.50, 0.020, 3.5, 10, 0.60, 'Parametric and implicit derivatives', 'Use parametric differentiation'),
('MATH_040', 'Higher Derivatives', 'Mathematics', 5, 0.45, 0.015, 2.5, 8, 0.55, 'Higher order derivatives', 'Find higher derivatives'),
('MATH_041', 'Logarithmic Differentiation', 'Mathematics', 5, 0.50, 0.018, 3, 9, 0.60, 'Log differentiation technique', 'Apply log differentiation'),

-- CALCULUS - APPLICATIONS & INTEGRATION (10 concepts)
('MATH_042', 'Maxima & Minima', 'Mathematics', 5, 0.50, 0.025, 4, 19, 0.60, 'First and second derivative test', 'Find extrema'),
('MATH_043', 'Monotonicity & Concavity', 'Mathematics', 5, 0.45, 0.018, 3, 8, 0.55, 'Increasing, decreasing, concavity', 'Analyze curve behavior'),
('MATH_044', 'Curve Sketching', 'Mathematics', 5, 0.50, 0.012, 3, 7, 0.60, 'Asymptotes, curve sketching', 'Sketch curves'),
('MATH_045', 'Rate of Change', 'Mathematics', 5, 0.40, 0.015, 2.5, 6, 0.50, 'Applied rate problems', 'Solve rate problems'),
('MATH_046', 'Indefinite Integration', 'Mathematics', 5, 0.40, 0.025, 3, 21, 0.50, 'Standard integral forms', 'Integrate basic functions'),
('MATH_047', 'Integration by Parts', 'Mathematics', 5, 0.55, 0.028, 4, 17, 0.65, 'Substitution and parts', 'Apply integration techniques'),
('MATH_048', 'Partial Fractions', 'Mathematics', 5, 0.60, 0.022, 4, 11, 0.70, 'Partial fraction decomposition', 'Use partial fractions'),
('MATH_049', 'Definite Integration', 'Mathematics', 5, 0.50, 0.023, 3.5, 18, 0.60, 'Definite integral properties', 'Evaluate definite integrals'),
('MATH_050', 'Area Under Curve', 'Mathematics', 5, 0.50, 0.020, 3.5, 14, 0.60, 'Area between curves', 'Calculate areas'),
('MATH_051', 'Differential Equations', 'Mathematics', 5, 0.60, 0.018, 4, 8, 0.70, 'Separable differential equations', 'Solve DEs'),
('MATH_052', 'Linear Differential Equations', 'Mathematics', 5, 0.65, 0.015, 4, 5, 0.75, 'First order linear DEs', 'Solve linear DEs'),

-- VECTORS & 3D (3 concepts)
('MATH_053', 'Vector Algebra', 'Mathematics', 6, 0.50, 0.035, 4, 24, 0.60, 'Dot and cross products', 'Use vector operations'),
('MATH_054', '3D Geometry', 'Mathematics', 6, 0.60, 0.030, 4.5, 13, 0.70, 'Lines and planes in 3D', 'Solve 3D geometry problems'),
('MATH_055', '3D Distance & Angles', 'Mathematics', 6, 0.55, 0.025, 4, 9, 0.65, 'Distance and angle in 3D', 'Calculate 3D distances/angles');

-- ============================================
-- FILE 2: seed_concepts_physics.sql
-- ============================================

INSERT INTO concepts (
  concept_id, 
  name, 
  subject, 
  layer_level, 
  difficulty, 
  exam_weightage, 
  typical_mastery_time_hours,
  nta_frequency_papers,
  irt_difficulty,
  description,
  learning_outcomes
) VALUES

-- MECHANICS (15 concepts)
('PHYS_001', 'Motion in 1D', 'Physics', 1, 0.35, 0.025, 3, 26, 0.40, 'Kinematics, equations of motion', 'Solve 1D motion problems'),
('PHYS_002', 'Motion in 2D', 'Physics', 1, 0.40, 0.028, 3.5, 23, 0.50, 'Projectile motion, components', 'Analyze 2D motion'),
('PHYS_003', 'Relative Motion', 'Physics', 1, 0.35, 0.015, 2, 9, 0.40, 'Relative velocity and position', 'Calculate relative motion'),
('PHYS_004', 'Newtons Laws', 'Physics', 1, 0.45, 0.030, 4, 28, 0.55, 'Three laws of motion, applications', 'Apply Newton''s laws'),
('PHYS_005', 'Forces', 'Physics', 1, 0.40, 0.022, 3, 15, 0.50, 'Force types, free body diagrams', 'Draw and analyze FBDs'),
('PHYS_006', 'Friction', 'Physics', 1, 0.45, 0.020, 3, 12, 0.55, 'Static and kinetic friction', 'Solve friction problems'),
('PHYS_007', 'Circular Motion', 'Physics', 2, 0.50, 0.025, 4, 14, 0.60, 'Uniform and variable circular motion', 'Analyze circular motion'),
('PHYS_008', 'Centripetal Force', 'Physics', 2, 0.50, 0.020, 3.5, 11, 0.60, 'Centripetal force and banking', 'Apply centripetal force'),
('PHYS_009', 'Gravitation', 'Physics', 2, 0.55, 0.022, 4, 10, 0.65, 'Gravitational force and fields', 'Use gravitation concepts'),
('PHYS_010', 'Orbital Motion', 'Physics', 2, 0.50, 0.018, 3.5, 8, 0.60, 'Kepler''s laws, satellite motion', 'Apply orbital mechanics'),
('PHYS_011', 'Work & Power', 'Physics', 2, 0.45, 0.020, 3, 12, 0.55, 'Work definition, power calculation', 'Calculate work and power'),
('PHYS_012', 'Kinetic Energy', 'Physics', 2, 0.40, 0.023, 3, 18, 0.50, 'KE, potential energy concepts', 'Use energy concepts'),
('PHYS_013', 'Energy Conservation', 'Physics', 2, 0.45, 0.025, 3.5, 19, 0.55, 'Conservation of mechanical energy', 'Apply energy conservation'),
('PHYS_014', 'Linear Momentum', 'Physics', 2, 0.50, 0.022, 4, 13, 0.60, 'Momentum and collisions', 'Solve collision problems'),
('PHYS_015', 'Rotational Motion', 'Physics', 2, 0.60, 0.020, 4.5, 9, 0.70, 'Torque, angular momentum', 'Apply rotational concepts'),

-- THERMODYNAMICS (8 concepts)
('PHYS_016', 'Heat & Calorimetry', 'Physics', 3, 0.40, 0.018, 3, 11, 0.50, 'Heat transfer, calorimetry', 'Solve heat problems'),
('PHYS_017', 'Thermal Properties', 'Physics', 3, 0.45, 0.015, 3, 8, 0.55, 'Thermal expansion, specific heat', 'Use thermal properties'),
('PHYS_018', 'First Law', 'Physics', 3, 0.50, 0.020, 3.5, 12, 0.60, 'First law of thermodynamics', 'Apply first law'),
('PHYS_019', 'Second Law', 'Physics', 3, 0.55, 0.015, 3.5, 7, 0.65, 'Entropy, second law', 'Understand entropy'),
('PHYS_020', 'Heat Engines', 'Physics', 3, 0.55, 0.012, 3, 6, 0.65, 'Engine efficiency, Carnot cycle', 'Calculate engine efficiency'),
('PHYS_021', 'Ideal Gas Law', 'Physics', 3, 0.50, 0.020, 3.5, 10, 0.60, 'Ideal gas equation, kinetic theory', 'Apply ideal gas law'),
('PHYS_022', 'Specific Heat', 'Physics', 3, 0.45, 0.015, 2.5, 8, 0.55, 'Specific heat, latent heat', 'Calculate heat requirements'),
('PHYS_023', 'Thermodynamic Processes', 'Physics', 3, 0.55, 0.015, 3.5, 7, 0.65, 'Isothermal, adiabatic processes', 'Analyze thermo processes'),

-- ELECTROMAGNETISM (15 concepts)
('PHYS_024', 'Coulombs Law', 'Physics', 4, 0.40, 0.020, 3, 19, 0.50, 'Electrostatic force', 'Calculate electrostatic force'),
('PHYS_025', 'Electric Field', 'Physics', 4, 0.50, 0.025, 4, 21, 0.60, 'Electric field and potential', 'Find electric field'),
('PHYS_026', 'Gauss Law', 'Physics', 4, 0.55, 0.020, 4, 12, 0.65, 'Gauss''s law and applications', 'Apply Gauss''s law'),
('PHYS_027', 'Capacitors', 'Physics', 4, 0.50, 0.022, 3.5, 13, 0.60, 'Capacitor types and dielectrics', 'Solve capacitor problems'),
('PHYS_028', 'Capacitor Energy', 'Physics', 4, 0.45, 0.015, 2.5, 8, 0.55, 'Energy in capacitor', 'Calculate stored energy'),
('PHYS_029', 'Current', 'Physics', 4, 0.40, 0.020, 3, 17, 0.50, 'Electric current and resistance', 'Solve current problems'),
('PHYS_030', 'Ohms Law', 'Physics', 4, 0.35, 0.018, 2.5, 14, 0.40, 'Ohm''s law, resistivity', 'Apply Ohm''s law'),
('PHYS_031', 'EMF', 'Physics', 4, 0.45, 0.018, 3, 11, 0.55, 'EMF and internal resistance', 'Calculate EMF problems'),
('PHYS_032', 'Kirchhoff Laws', 'Physics', 4, 0.55, 0.022, 4, 12, 0.65, 'Kirchhoff''s circuit laws', 'Apply Kirchhoff''s laws'),
('PHYS_033', 'Bridges', 'Physics', 4, 0.50, 0.015, 3.5, 8, 0.60, 'Wheatstone and meter bridge', 'Use bridge circuits'),
('PHYS_034', 'Magnetic Field', 'Physics', 4, 0.50, 0.020, 3.5, 11, 0.60, 'Magnetic force on moving charge', 'Calculate magnetic force'),
('PHYS_035', 'Ampere Law', 'Physics', 4, 0.55, 0.018, 4, 9, 0.65, 'Ampere''s law', 'Apply Ampere''s law'),
('PHYS_036', 'Electromagnetic Induction', 'Physics', 4, 0.60, 0.023, 4.5, 15, 0.70, 'Faraday''s electromagnetic induction', 'Apply induction'),
('PHYS_037', 'Lenz Law', 'Physics', 4, 0.55, 0.018, 3.5, 10, 0.65, 'Lenz''s law', 'Apply Lenz''s law'),
('PHYS_038', 'AC Circuits', 'Physics', 4, 0.65, 0.020, 5, 8, 0.75, 'Alternating current circuits', 'Solve AC problems'),

-- OPTICS (8 concepts)
('PHYS_039', 'Ray Optics', 'Physics', 5, 0.45, 0.020, 3.5, 11, 0.55, 'Reflection and laws', 'Apply reflection laws'),
('PHYS_040', 'Mirrors & Lens', 'Physics', 5, 0.50, 0.022, 3.5, 16, 0.60, 'Mirror and lens formulas', 'Solve mirror/lens problems'),
('PHYS_041', 'Lens Combinations', 'Physics', 5, 0.50, 0.015, 3, 9, 0.60, 'Multiple lenses and power', 'Calculate lens combinations'),
('PHYS_042', 'Refraction', 'Physics', 5, 0.45, 0.018, 3, 11, 0.55, 'Snell''s law and refraction', 'Apply refraction'),
('PHYS_043', 'Wave Optics', 'Physics', 5, 0.60, 0.020, 4, 8, 0.70, 'Interference and diffraction', 'Calculate wave optics'),
('PHYS_044', 'Diffraction', 'Physics', 5, 0.65, 0.015, 4, 5, 0.75, 'Diffraction patterns', 'Apply diffraction'),
('PHYS_045', 'Dispersion', 'Physics', 5, 0.50, 0.012, 3, 6, 0.60, 'Light dispersion', 'Use dispersion concepts'),
('PHYS_046', 'Doppler Effect', 'Physics', 5, 0.55, 0.010, 3, 3, 0.65, 'Doppler effect for light', 'Apply Doppler effect'),

-- MODERN PHYSICS (9 concepts)
('PHYS_047', 'Photoelectric Effect', 'Physics', 6, 0.55, 0.018, 3.5, 10, 0.65, 'Einstein''s photoelectric effect', 'Solve photoelectric problems'),
('PHYS_048', 'Photons', 'Physics', 6, 0.50, 0.015, 3, 8, 0.60, 'Photons and de Broglie wavelength', 'Use photon concepts'),
('PHYS_049', 'Bohr Model', 'Physics', 6, 0.60, 0.020, 4, 9, 0.70, 'Bohr model of hydrogen', 'Apply Bohr model'),
('PHYS_050', 'Atomic Structure', 'Physics', 6, 0.55, 0.012, 3, 6, 0.65, 'Atomic spectra', 'Use atomic structure'),
('PHYS_051', 'Nuclear Physics', 'Physics', 6, 0.60, 0.015, 4, 7, 0.70, 'Radioactivity and nuclear reactions', 'Solve nuclear problems'),
('PHYS_052', 'Mass Defect', 'Physics', 6, 0.65, 0.012, 3.5, 5, 0.75, 'Binding energy and mass defect', 'Calculate binding energy'),
('PHYS_053', 'Nuclear Reactions', 'Physics', 6, 0.65, 0.010, 3.5, 4, 0.75, 'Fission and fusion', 'Solve nuclear reactions'),
('PHYS_054', 'X-Rays', 'Physics', 6, 0.60, 0.015, 3.5, 6, 0.70, 'X-ray production', 'Use X-ray concepts'),
('PHYS_055', 'Semiconductors', 'Physics', 6, 0.70, 0.008, 3, 2, 0.80, 'Semiconductor basics', 'Understand semiconductors');

-- ============================================
-- FILE 3: seed_concepts_chemistry.sql
-- ============================================

INSERT INTO concepts (
  concept_id, 
  name, 
  subject, 
  layer_level, 
  difficulty, 
  exam_weightage, 
  typical_mastery_time_hours,
  nta_frequency_papers,
  irt_difficulty,
  description,
  learning_outcomes
) VALUES

-- PHYSICAL CHEMISTRY (18 concepts)
('CHEM_001', 'Atomic Structure', 'Chemistry', 1, 0.45, 0.020, 3.5, 12, 0.55, 'Bohr and quantum models', 'Understand atomic structure'),
('CHEM_002', 'Quantum Numbers', 'Chemistry', 1, 0.50, 0.018, 3.5, 9, 0.60, 'Quantum numbers and orbitals', 'Identify quantum numbers'),
('CHEM_003', 'Electronic Configuration', 'Chemistry', 1, 0.40, 0.015, 2.5, 11, 0.50, 'Aufbau principle and config', 'Write electron configuration'),
('CHEM_004', 'Periodic Table', 'Chemistry', 1, 0.40, 0.022, 3, 18, 0.50, 'Periodic table and trends', 'Use periodic trends'),
('CHEM_005', 'Ionization Energy', 'Chemistry', 1, 0.45, 0.018, 3, 10, 0.55, 'Ionization energy and trends', 'Compare IE values'),
('CHEM_006', 'Metallic Character', 'Chemistry', 1, 0.35, 0.012, 2.5, 7, 0.40, 'Metallic and non-metallic nature', 'Predict element properties'),
('CHEM_007', 'Ionic Bonding', 'Chemistry', 2, 0.40, 0.018, 3, 10, 0.50, 'Ionic bonding and lattice energy', 'Understand ionic bonds'),
('CHEM_008', 'Covalent Bonding', 'Chemistry', 2, 0.45, 0.020, 3.5, 14, 0.55, 'Covalent bonds and polarity', 'Analyze covalent bonds'),
('CHEM_009', 'Hydrogen Bonding', 'Chemistry', 2, 0.40, 0.015, 2.5, 8, 0.50, 'Hydrogen bonds and van der Waals', 'Identify hydrogen bonds'),
('CHEM_010', 'VSEPR Theory', 'Chemistry', 2, 0.50, 0.018, 3.5, 10, 0.60, 'VSEPR and hybridization', 'Predict molecular geometry'),
('CHEM_011', 'MO Theory', 'Chemistry', 2, 0.55, 0.012, 3.5, 5, 0.65, 'Molecular orbital theory', 'Use MO theory'),
('CHEM_012', 'Enthalpy', 'Chemistry', 3, 0.50, 0.020, 3.5, 12, 0.60, 'Enthalpy and Hess''s law', 'Calculate enthalpy'),
('CHEM_013', 'Entropy', 'Chemistry', 3, 0.55, 0.018, 4, 8, 0.65, 'Entropy and Gibbs energy', 'Use entropy concepts'),
('CHEM_014', 'Rate of Reaction', 'Chemistry', 3, 0.50, 0.022, 3.5, 11, 0.60, 'Reaction rates and rate law', 'Calculate reaction rates'),
('CHEM_015', 'Activation Energy', 'Chemistry', 3, 0.45, 0.015, 3, 8, 0.55, 'Activation energy and catalyst', 'Use catalysis concepts'),
('CHEM_016', 'Chemical Equilibrium', 'Chemistry', 3, 0.50, 0.025, 4, 15, 0.60, 'Equilibrium constant', 'Calculate equilibrium'),
('CHEM_017', 'Le Chatelier', 'Chemistry', 3, 0.45, 0.015, 3, 9, 0.55, 'Le Chatelier''s principle', 'Apply Le Chatelier'),
('CHEM_018', 'Ionic Equilibrium', 'Chemistry', 3, 0.55, 0.022, 4, 14, 0.65, 'Ionic equilibrium and pH', 'Calculate pH'),

-- INORGANIC CHEMISTRY (17 concepts)
('CHEM_019', 'Hydrogen', 'Chemistry', 4, 0.40, 0.012, 2.5, 7, 0.50, 'Hydrogen and hydrides', 'Use hydrogen chemistry'),
('CHEM_020', 'Alkali Metals', 'Chemistry', 4, 0.35, 0.015, 2.5, 10, 0.40, 'Group 1 properties', 'Compare group 1 elements'),
('CHEM_021', 'Alkaline Earth', 'Chemistry', 4, 0.35, 0.012, 2.5, 8, 0.40, 'Group 2 properties', 'Compare group 2 elements'),
('CHEM_022', 'Boron Family', 'Chemistry', 4, 0.45, 0.018, 3, 9, 0.55, 'Group 13 elements', 'Solve boron group problems'),
('CHEM_023', 'Nitrogen Family', 'Chemistry', 4, 0.50, 0.018, 3.5, 10, 0.60, 'Group 15 elements', 'Use nitrogen chemistry'),
('CHEM_024', 'Oxygen Family', 'Chemistry', 4, 0.45, 0.015, 3, 8, 0.55, 'Group 16 elements', 'Solve oxygen group problems'),
('CHEM_025', 'Halogens', 'Chemistry', 4, 0.40, 0.015, 2.5, 9, 0.50, 'Group 17 elements', 'Compare halogens'),
('CHEM_026', 'Noble Gases', 'Chemistry', 4, 0.30, 0.008, 1.5, 4, 0.35, 'Group 18 noble gases', 'Understand noble gases'),
('CHEM_027', 'd-Block Elements', 'Chemistry', 4, 0.55, 0.020, 4, 11, 0.65, 'Transition metals', 'Solve d-block problems'),
('CHEM_028', 'Coordination Compounds', 'Chemistry', 4, 0.60, 0.022, 4.5, 12, 0.70, 'Complexes and nomenclature', 'Name and use complexes'),
('CHEM_029', 'Complex Isomerism', 'Chemistry', 4, 0.65, 0.015, 4, 7, 0.75, 'Isomerism in complexes', 'Identify complex isomers'),
('CHEM_030', 'Chelate Effect', 'Chemistry', 4, 0.60, 0.012, 3.5, 5, 0.70, 'Chelation and stability', 'Apply chelate effect'),
('CHEM_031', 'Crystal Field Theory', 'Chemistry', 4, 0.65, 0.018, 4, 8, 0.75, 'CFT and d-orbital splitting', 'Use crystal field theory'),
('CHEM_032', 'Metallurgy', 'Chemistry', 4, 0.50, 0.015, 3, 8, 0.60, 'Ore processing and extraction', 'Solve metallurgy problems'),
('CHEM_033', 'Electrochemistry', 'Chemistry', 4, 0.60, 0.020, 4, 10, 0.70, 'Redox and electrochemistry', 'Use electrochemistry'),
('CHEM_034', 'Galvanic Cells', 'Chemistry', 4, 0.60, 0.018, 4, 9, 0.70, 'Galvanic and electrolytic cells', 'Solve cell problems'),
('CHEM_035', 'Corrosion', 'Chemistry', 4, 0.50, 0.008, 2.5, 4, 0.60, 'Corrosion and prevention', 'Prevent corrosion'),

-- ORGANIC CHEMISTRY (20 concepts)
('CHEM_036', 'IUPAC Nomenclature', 'Chemistry', 5, 0.40, 0.020, 3, 16, 0.50, 'IUPAC naming system', 'Name organic compounds'),
('CHEM_037', 'Isomerism', 'Chemistry', 5, 0.50, 0.022, 3.5, 13, 0.60, 'Structural and stereoisomerism', 'Identify isomers'),
('CHEM_038', 'Stereochemistry', 'Chemistry', 5, 0.55, 0.018, 4, 9, 0.65, 'R/S and E/Z notation', 'Assign stereochemistry'),
('CHEM_039', 'Functional Groups', 'Chemistry', 5, 0.40, 0.015, 2.5, 11, 0.50, 'Functional group properties', 'Identify functional groups'),
('CHEM_040', 'SN1 & SN2', 'Chemistry', 5, 0.60, 0.025, 4.5, 14, 0.70, 'Nucleophilic substitution', 'Predict substitution'),
('CHEM_041', 'E1 & E2', 'Chemistry', 5, 0.60, 0.020, 4, 10, 0.70, 'Elimination reactions', 'Predict elimination'),
('CHEM_042', 'Addition Reactions', 'Chemistry', 5, 0.55, 0.022, 4, 12, 0.65, 'Electrophilic and nucleophilic', 'Solve addition problems'),
('CHEM_043', 'Aromatic Substitution', 'Chemistry', 5, 0.65, 0.025, 4.5, 13, 0.75, 'Electrophilic aromatic subst', 'Predict aromatic subst'),
('CHEM_044', 'Alkanes', 'Chemistry', 5, 0.45, 0.018, 3, 10, 0.55, 'Alkanes and cycloalkanes', 'Solve alkane problems'),
('CHEM_045', 'Alkenes', 'Chemistry', 5, 0.50, 0.020, 3.5, 11, 0.60, 'Alkenes and reactions', 'Use alkene reactions'),
('CHEM_046', 'Aromatic Compounds', 'Chemistry', 5, 0.55, 0.022, 4, 13, 0.65, 'Benzene and aromatic', 'Apply aromatic concepts'),
('CHEM_047', 'Alcohols & Ethers', 'Chemistry', 5, 0.55, 0.020, 3.5, 11, 0.65, 'Alcohol and ether chemistry', 'Solve alcohol problems'),
('CHEM_048', 'Carbonyl Compounds', 'Chemistry', 5, 0.60, 0.022, 4, 12, 0.70, 'Aldehydes and ketones', 'Apply carbonyl reactions'),
('CHEM_049', 'Carboxylic Acids', 'Chemistry', 5, 0.60, 0.020, 4, 10, 0.70, 'Carboxylic acids and esters', 'Use acid chemistry'),
('CHEM_050', 'Amines & Amides', 'Chemistry', 5, 0.60, 0.018, 3.5, 9, 0.70, 'Amine and amide chemistry', 'Solve amine problems'),
('CHEM_051', 'Natural Products', 'Chemistry', 5, 0.65, 0.025, 5, 8, 0.75, 'Carbs, proteins, lipids', 'Use natural products'),
('CHEM_052', 'Polymers', 'Chemistry', 5, 0.60, 0.015, 3.5, 7, 0.70, 'Polymer chemistry', 'Apply polymer concepts'),
('CHEM_053', 'Dyes & Pigments', 'Chemistry', 5, 0.65, 0.010, 3, 4, 0.75, 'Dyes and pigments', 'Use dye chemistry'),
('CHEM_054', 'Pharmaceuticals', 'Chemistry', 5, 0.70, 0.012, 4, 5, 0.80, 'Drug synthesis', 'Understand drug chemistry'),
('CHEM_055', 'Environmental Chemistry', 'Chemistry', 5, 0.55, 0.008, 2.5, 3, 0.65, 'Environmental issues', 'Apply green chemistry');

-- All 165 concepts successfully inserted

COMMIT;
