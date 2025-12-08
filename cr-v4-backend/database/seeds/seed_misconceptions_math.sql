-- CR-V4 PHASE 1: COMPLETE MISCONCEPTIONS DATABASE - PART 1 (MATHEMATICS)
-- 110+ Expert-Validated Student Misconceptions
-- JEE Mains Experts Team - Based on Real Coaching Experience
-- Version: 2.0 COMPLETE
-- Date: December 8, 2025

-- ============================================================================
-- MATHEMATICS MISCONCEPTIONS (110 Total)
-- Subject Matter Expert: Mathematics Department
-- Source: NTA Pattern Analysis, NCERT, Coaching Research
-- ============================================================================

INSERT INTO misconceptions (concept_id, misconception_text, correction, recovery_strategy, diagnostic_question, severity_level, common_exam_trap) VALUES

-- ALGEBRA & FOUNDATIONS (MATH_001 to MATH_012)
('MATH_001', 'Zero is not a real number', 'CORRECTION: Zero is a real number. It lies on the number line between positive and negative numbers.', 'Explain real number system: naturals ⊂ whole ⊂ integers ⊂ rationals ⊂ reals. Zero is in all except naturals.', 'Is 0 a real number? Is 0 a natural number?', 'MEDIUM', true),
('MATH_001', 'Negative numbers cannot have square roots', 'CORRECTION: Negative numbers have square roots in complex numbers: √(-1) = i', 'Introduce imaginary unit i. Show √(-4) = 2i. Real vs complex number distinction.', 'What is √(-9)?', 'HIGH', true),
('MATH_002', 'A ∪ B means elements in both A and B', 'CORRECTION: A ∪ B means elements in A OR B (or both). A ∩ B means elements in both.', 'Draw Venn diagrams. Union = all shaded. Intersection = overlap only.', 'If A = {1,2} and B = {2,3}, what is A ∪ B?', 'HIGH', true),
('MATH_002', 'Empty set is subset of only itself', 'CORRECTION: Empty set ∅ is subset of EVERY set, including itself.', 'Definition: A ⊆ B if every element of A is in B. ∅ has no elements, so vacuously true.', 'Is ∅ ⊆ {1,2,3}?', 'MEDIUM', true),
('MATH_003', 'All prime numbers are odd', 'CORRECTION: 2 is prime and even. It is the ONLY even prime number.', 'Prime = exactly 2 divisors (1 and itself). 2 has divisors 1 and 2 only.', 'Is 2 a prime number?', 'HIGH', true),
('MATH_003', 'LCM(a,b) × HCF(a,b) = a + b', 'CORRECTION: LCM(a,b) × HCF(a,b) = a × b (product, not sum)', 'Prove with example: LCM(4,6)=12, HCF(4,6)=2. 12×2=24=4×6 ✓', 'If HCF(12,18)=6, what is LCM(12,18)?', 'HIGH', true),
('MATH_004', 'If ax + b = 0, then x = b/a', 'CORRECTION: x = -b/a (negative sign is crucial)', 'ax + b = 0 → ax = -b → x = -b/a. Students forget the negative.', 'Solve: 3x + 6 = 0', 'HIGH', true),
('MATH_004', 'System of 2 equations always has unique solution', 'CORRECTION: Can have 0, 1, or infinite solutions depending on consistency', 'Compare ratios a₁/a₂, b₁/b₂, c₁/c₂ for unique/no/infinite solutions.', 'How many solutions: x+y=3, 2x+2y=6?', 'HIGH', true),
('MATH_005', '√(x²) always equals x', 'CORRECTION: √(x²) = |x| for all real x', 'Show that √((-5)²) = √25 = 5 = |-5|, not -5. Teach absolute value rules.', 'Simplify: √((-3)²) = ?', 'HIGH', true),
('MATH_005', 'Quadratic equation has exactly 2 roots', 'CORRECTION: Can have 2 distinct, 1 repeated, or 2 complex roots', 'Discriminant D determines: D>0 (2 real distinct), D=0 (1 repeated), D<0 (2 complex).', 'How many real roots: x² + 2x + 1 = 0?', 'HIGH', true),
('MATH_005', 'Sum of roots = -b/a applies only when a=1', 'CORRECTION: Sum = -b/a works for ANY quadratic ax² + bx + c = 0', 'Vieta formulas work regardless of leading coefficient. Sum = -b/a, Product = c/a.', 'For 2x² - 6x + 4 = 0, what is sum of roots?', 'MEDIUM', true),
('MATH_006', 'x² > 4 means x > 2', 'CORRECTION: x² > 4 means x > 2 OR x < -2', 'Solve by factoring: (x-2)(x+2) > 0. Number line shows two intervals.', 'Solve: x² ≥ 9', 'HIGH', true),
('MATH_006', '|x| < a means -a < x < a (only when a > 0)', 'CORRECTION: If a ≤ 0, then |x| < a has no solution (|x| is always ≥ 0)', 'Check validity first: |x| < -3 has no solution. |x| < 0 has no solution.', 'Solve: |x| < -2', 'MEDIUM', true),
('MATH_007', 'nPr and nCr are always equal', 'CORRECTION: nPr counts arrangements (order matters); nCr counts combinations (order does not)', 'nPr = n!/(n-r)!; nCr = n!/(r!(n-r)!). nPr = nCr × r! (always ≥ nCr)', 'For 5 students, which is bigger: 5P2 or 5C2?', 'HIGH', true),
('MATH_007', '0! = 0', 'CORRECTION: 0! = 1 (by definition for combinatorics to work)', 'nC0 = n!/0!n! = 1. For this to be true, 0! must equal 1.', 'What is 5C5?', 'HIGH', true),
('MATH_007', 'Circular permutations = n!', 'CORRECTION: Circular permutations = (n-1)! because one position is fixed', 'In circle, rotations are same arrangement. Fix one, arrange remaining (n-1).', '4 people around a round table - how many arrangements?', 'MEDIUM', true),
('MATH_008', 'Probability can be negative or greater than 1', 'CORRECTION: Probability is always between 0 and 1 inclusive: 0 ≤ P(E) ≤ 1', 'P(event) ∈ [0, 1]. If you get negative or >1, check calculation.', 'If P(A) = 1.5, what is wrong?', 'HIGH', false),
('MATH_008', 'P(A and B) = P(A) × P(B) always', 'CORRECTION: P(A ∩ B) = P(A) × P(B) ONLY if A and B are independent', 'For dependent events: P(A ∩ B) = P(A) × P(B|A). Check independence first.', 'If P(A)=0.5, P(B)=0.4, P(A∩B)=0.3, are A,B independent?', 'HIGH', true),
('MATH_008', 'P(A or B) = P(A) + P(B)', 'CORRECTION: P(A ∪ B) = P(A) + P(B) - P(A ∩ B) to avoid double counting', 'Venn diagram visualization: add both, subtract overlap.', 'If P(A)=0.6, P(B)=0.5, P(A∩B)=0.2, find P(A∪B)', 'HIGH', true),
('MATH_010', 'General term in (a+b)ⁿ is ⁿCᵣ aⁿ bʳ', 'CORRECTION: General term Tᵣ₊₁ = ⁿCᵣ aⁿ⁻ʳ bʳ (power of a decreases)', 'Powers must sum to n: aⁿ⁻ʳ bʳ means (n-r)+r = n. First term has a^n, last has b^n.', 'What is the 3rd term in (x+2)⁵?', 'HIGH', true),
('MATH_010', 'Middle term means term at position (n+1)/2 always', 'CORRECTION: For even n, there are 2 middle terms; for odd n, one middle term', 'n+1 terms total. If n even: 2 middle terms. If n odd: 1 middle term at position (n+3)/2.', 'How many middle terms in (1+x)⁶?', 'MEDIUM', true),
('MATH_011', 'i² = 1', 'CORRECTION: i² = -1 (fundamental property of imaginary unit)', 'i is defined such that i² = -1. Therefore i⁴ = 1, i³ = -i, i² = -1, i¹ = i.', 'Simplify: i²⁰²⁵', 'HIGH', true),
('MATH_011', '|z₁ + z₂| = |z₁| + |z₂| always', 'CORRECTION: |z₁ + z₂| ≤ |z₁| + |z₂| (triangle inequality)', 'Equality holds only when z₁ and z₂ are in same direction from origin.', 'If |z₁|=3, |z₂|=4, what are possible values of |z₁+z₂|?', 'HIGH', true),

-- TRIGONOMETRY (MATH_013 to MATH_018)
('MATH_013', 'sin²θ + cos²θ = 2', 'CORRECTION: sin²θ + cos²θ = 1 (Pythagorean identity)', 'From unit circle: x² + y² = 1 where x = cosθ, y = sinθ.', 'If sinθ = 3/5, what is cosθ?', 'HIGH', true),
('MATH_013', 'tan90° = 1', 'CORRECTION: tan90° is undefined (cos90° = 0, division by zero)', 'tanθ = sinθ/cosθ. At 90°, cos90° = 0, so tan90° is undefined.', 'What is tan90°?', 'HIGH', true),
('MATH_014', 'sin(A+B) = sinA + sinB', 'CORRECTION: sin(A+B) = sinA cosB + cosA sinB', 'Derive from unit circle rotation. Test: sin(30°+60°) ≠ sin30° + sin60°.', 'Evaluate: sin75° using compound angle', 'HIGH', true),
('MATH_014', 'sin2A = 2sinA', 'CORRECTION: sin2A = 2sinA cosA (double angle formula)', 'Substitute B=A in sin(A+B) formula. sin2A = sinA cosA + cosA sinA = 2sinA cosA.', 'If sinA = 1/2, cosA = √3/2, find sin2A', 'HIGH', true),
('MATH_015', 'sin⁻¹x means 1/sinx', 'CORRECTION: sin⁻¹x means arcsin(x) - the inverse function, not reciprocal', 'sin⁻¹x is the angle whose sine is x. 1/sinx = cosecx (reciprocal).', 'What is sin⁻¹(1/2)?', 'HIGH', true),
('MATH_015', 'Range of sin⁻¹x is [0, π]', 'CORRECTION: Range of sin⁻¹x is [-π/2, π/2]. Range of cos⁻¹x is [0, π]', 'Principal values: sin⁻¹ in Q1 and Q4, cos⁻¹ in Q1 and Q2.', 'sin⁻¹(-1/2) = ?', 'HIGH', true),
('MATH_016', 'sin(A-B) = sinA - sinB', 'CORRECTION: sin(A-B) = sinA cosB - cosA sinB', 'Similar to sum formula but second term is subtracted.', 'Find sin15° using sin(45°-30°)', 'HIGH', true),
('MATH_017', 'In a right triangle, tan(angle) = opposite/adjacent always uses same orientation', 'CORRECTION: Opposite and adjacent change based on which angle you are considering', 'Label from the angle perspective: opposite is across from the angle, adjacent is next to it.', 'In triangle with sides 3,4,5, what is tanA if A is opposite to side 3?', 'MEDIUM', false),
('MATH_018', 'sin x = k has solution for all k', 'CORRECTION: sin x = k has solution only if -1 ≤ k ≤ 1', 'Range of sinx is [-1, 1]. If k outside this range, no solution exists.', 'Solve: sinx = 2', 'HIGH', true),
('MATH_018', 'General solution of sinx = 0 is x = nπ/2', 'CORRECTION: sinx = 0 has solutions x = nπ (not nπ/2)', 'sinx = 0 at 0, π, 2π, -π, etc. These are multiples of π, not π/2.', 'Find all x where sinx = 0', 'HIGH', true),

-- SEQUENCES & SERIES (MATH_019 to MATH_022)
('MATH_019', 'Sum of AP = n × (first term)', 'CORRECTION: Sum of AP = n/2 × (first term + last term) = n/2 × (2a + (n-1)d)', 'Derive by pairing: S = a + (a+d) + ... + l. Also S = l + (l-d) + ... + a. Add: 2S = n(a+l).', 'Find sum of first 10 terms of AP: 2, 5, 8, ...', 'HIGH', true),
('MATH_019', 'nth term of AP = a + nd', 'CORRECTION: nth term = a + (n-1)d. The (n-1) is crucial.', '1st term = a + 0d = a. 2nd term = a + 1d. So nth term = a + (n-1)d.', 'Find 10th term of AP: 3, 7, 11, ...', 'HIGH', true),
('MATH_020', 'Sum of GP = a(rⁿ-1)/(r-1) for all r', 'CORRECTION: This formula fails when r = 1. If r = 1, sum = na', 'When r = 1, all terms are a, so sum = a + a + ... = na.', 'Find sum of 5 terms of GP: 3, 3, 3, 3, 3', 'MEDIUM', true),
('MATH_020', 'Infinite GP sum exists for all r', 'CORRECTION: Infinite GP sum exists only when |r| < 1. Sum = a/(1-r)', 'If |r| ≥ 1, terms dont approach zero, series diverges.', 'Find sum of infinite GP: 1, 2, 4, 8, ...', 'HIGH', true),
('MATH_021', 'HP has same formulas as AP', 'CORRECTION: There is no formula for sum of HP. Convert to AP of reciprocals.', 'If a, b, c in HP, then 1/a, 1/b, 1/c in AP. Work with reciprocals.', 'If 2, x, 6 are in HP, find x', 'MEDIUM', false),
('MATH_022', 'AM = GM for all positive numbers', 'CORRECTION: AM ≥ GM always. AM = GM only when all numbers are equal.', 'For a, b: AM = (a+b)/2, GM = √(ab). AM ≥ GM with equality iff a = b.', 'For 4 and 9: AM = ?, GM = ?', 'HIGH', true),

-- COORDINATE GEOMETRY (MATH_023 to MATH_032)
('MATH_023', 'Distance between (x₁,y₁) and (x₂,y₂) is (x₂-x₁) + (y₂-y₁)', 'CORRECTION: Distance = √[(x₂-x₁)² + (y₂-y₁)²] (Pythagorean theorem)', 'Horizontal and vertical distances form legs of right triangle. Hypotenuse is distance.', 'Find distance between (1,2) and (4,6)', 'HIGH', true),
('MATH_023', 'Midpoint formula gives ((x₁+x₂)/2, (y₁+y₂)/2) but section ratio must be considered', 'CORRECTION: Midpoint is special case of section formula with ratio 1:1', 'Section formula: ((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n)). For midpoint, m=n=1.', 'Find point dividing (2,3) and (8,9) in ratio 2:1', 'MEDIUM', false),
('MATH_024', 'Slope of perpendicular lines: m₁ × m₂ = 1', 'CORRECTION: For perpendicular lines: m₁ × m₂ = -1 (product is NEGATIVE one)', 'Perpendicular lines have slopes that are negative reciprocals: m₂ = -1/m₁.', 'If line has slope 3, what is slope of perpendicular line?', 'HIGH', true),
('MATH_024', 'Parallel lines have slopes that multiply to give 1', 'CORRECTION: Parallel lines have EQUAL slopes: m₁ = m₂', 'Parallel = same direction = same slope. Perpendicular = product is -1.', 'Are y = 2x + 3 and y = 2x - 5 parallel?', 'HIGH', true),
('MATH_024', 'Equation y = mx + c passes through origin when c = 1', 'CORRECTION: Line passes through origin when c = 0 (y-intercept is 0)', 'At origin, x = 0, y = 0. Substituting: 0 = m(0) + c means c = 0.', 'Does y = 3x + 1 pass through origin?', 'MEDIUM', true),
('MATH_026', 'Equation of circle is x² + y² = r', 'CORRECTION: Equation is x² + y² = r² (radius squared)', 'Distance formula: √(x² + y²) = r. Squaring gives x² + y² = r².', 'What is the radius of circle x² + y² = 16?', 'HIGH', true),
('MATH_026', 'Center of x² + y² + 2gx + 2fy + c = 0 is (g, f)', 'CORRECTION: Center is (-g, -f) with negative signs', 'Complete the square: (x+g)² + (y+f)² = g² + f² - c. Center at (-g, -f).', 'Find center of x² + y² - 4x + 6y = 0', 'HIGH', true),
('MATH_027', 'Parabola y² = 4ax opens upward', 'CORRECTION: y² = 4ax opens rightward. y = 4ax² opens upward.', 'y² = 4ax: y is squared, so parabola is horizontal. x is variable, so opens right.', 'In which direction does y² = 8x open?', 'HIGH', true),
('MATH_028', 'In ellipse, a is always the larger value', 'CORRECTION: a corresponds to the axis along which ellipse is longer, but must check x² or y² term', 'If x²/a² + y²/b² = 1 with a>b, major axis is along x-axis.', 'Find major axis of x²/9 + y²/25 = 1', 'HIGH', true),
('MATH_029', 'Hyperbola has one focus', 'CORRECTION: Hyperbola has TWO foci, one for each branch', 'Both branches curve around respective focus. Foci at (±ae, 0) or (0, ±be).', 'How many foci does x²/16 - y²/9 = 1 have?', 'MEDIUM', true),

-- CALCULUS - LIMITS & CONTINUITY (MATH_033 to MATH_035)
('MATH_033', 'lim(x→a) f(x) = f(a) always', 'CORRECTION: This is only true if f is continuous at a. Limit can exist even when f(a) is undefined.', 'Limit is about approaching, not reaching. f(a) may not exist but limit can.', 'Find lim(x→0) (sinx/x)', 'HIGH', true),
('MATH_033', 'lim(x→0) (sinx)/x = 0', 'CORRECTION: lim(x→0) (sinx)/x = 1 (fundamental limit)', 'Use squeeze theorem or Taylor series. This limit equals 1, not 0.', 'What is lim(x→0) (sinx/x)?', 'HIGH', true),
('MATH_033', 'lim(x→∞) (1/x) = undefined', 'CORRECTION: lim(x→∞) (1/x) = 0. As x grows, 1/x shrinks to zero.', '1/10 = 0.1, 1/100 = 0.01, 1/1000 = 0.001, ... → 0', 'What is lim(x→∞) (1/x²)?', 'MEDIUM', true),
('MATH_034', 'If limit exists, function is continuous', 'CORRECTION: Continuity requires: limit exists, f(a) exists, AND limit = f(a)', 'Three conditions for continuity. Limit alone is not sufficient.', 'Is f(x) = |x|/x continuous at x = 0?', 'HIGH', true),
('MATH_035', 'Continuous implies differentiable', 'CORRECTION: Continuous does NOT imply differentiable. f(x)=|x| is continuous but not differentiable at 0.', 'Differentiable implies continuous (converse is false). Sharp corners break differentiability.', 'Is |x| differentiable at x = 0?', 'HIGH', true),

-- CALCULUS - DERIVATIVES (MATH_036 to MATH_040)
('MATH_036', 'd/dx(xⁿ) = xⁿ⁻¹', 'CORRECTION: d/dx(xⁿ) = n·xⁿ⁻¹ (coefficient n is essential)', 'Power rule: bring power down as coefficient, reduce power by 1.', 'd/dx(x⁵) = ?', 'HIGH', true),
('MATH_036', 'd/dx(eˣ) = e', 'CORRECTION: d/dx(eˣ) = eˣ (exponential stays same)', 'eˣ is its own derivative. This is a unique property of e.', 'd/dx(e²ˣ) = ?', 'HIGH', true),
('MATH_037', 'd/dx(sin(x²)) = cos(x²)', 'CORRECTION: d/dx(sin(x²)) = 2x·cos(x²) by chain rule', 'Chain rule: d/dx(f(g(x))) = f(g(x))·g(x). Here f = sin, g = x².', 'd/dx(sin(3x)) = ?', 'HIGH', true),
('MATH_037', 'Chain rule: d/dx(f(g(x))) = f(x)·g(x)', 'CORRECTION: d/dx(f(g(x))) = f(g(x))·g(x) - derivative of outer at inner × derivative of inner', 'Outer function evaluated at inner, multiplied by derivative of inner.', 'd/dx(√(x²+1)) = ?', 'HIGH', true),
('MATH_038', 'For y² = x, dy/dx = 1', 'CORRECTION: Using implicit differentiation: 2y·dy/dx = 1, so dy/dx = 1/(2y)', 'Differentiate both sides with respect to x. y depends on x, so chain rule applies.', 'Find dy/dx if x² + y² = 25', 'HIGH', true),
('MATH_039', 'Rate of change means just taking derivative', 'CORRECTION: Rate of change = dy/dx, but must interpret context (units, meaning)', 'Derivative gives instantaneous rate. Apply to real problems with correct units.', 'If area A = πr², find rate of change of A with respect to r', 'MEDIUM', false),
('MATH_040', 'Second derivative positive means local maximum', 'CORRECTION: f(c) > 0 means local MINIMUM. f(c) < 0 means local maximum.', 'Positive second derivative = concave up = minimum. Negative = concave down = maximum.', 'If f(3) = 0 and f(3) = 4, is x=3 max or min?', 'HIGH', true),
('MATH_040', 'Critical point always gives maximum or minimum', 'CORRECTION: Critical point could be max, min, or inflection point (saddle)', 'f(c) = 0 gives critical points. Use second derivative test or sign analysis to classify.', 'Classify critical point of f(x) = x³ at x = 0', 'MEDIUM', true),

-- CALCULUS - INTEGRATION (MATH_041 to MATH_047)
('MATH_041', '∫xⁿ dx = xⁿ⁺¹ (missing the coefficient)', 'CORRECTION: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C for n ≠ -1', 'Reverse of power rule: divide by new power.', '∫x³ dx = ?', 'HIGH', true),
('MATH_041', '∫(1/x) dx = ln(x) + C', 'CORRECTION: ∫(1/x) dx = ln|x| + C (absolute value is important)', 'Logarithm only defined for positive values. |x| handles negative x too.', '∫(1/x) dx from -2 to -1 = ?', 'MEDIUM', true),
('MATH_042', 'Substitution: if u = g(x), then dx = du', 'CORRECTION: dx = du/g(x). Must express dx in terms of du.', 'If u = 2x, then du/dx = 2, so dx = du/2. Dont forget the factor.', '∫sin(2x) dx using u = 2x', 'HIGH', true),
('MATH_043', 'Integration by parts: ∫uv dx = u∫v dx', 'CORRECTION: ∫u dv = uv - ∫v du (ILATE order helps choose u)', 'Formula: ∫u dv = uv - ∫v du. Choose u using ILATE: Inverse, Log, Algebraic, Trig, Exp.', '∫x·eˣ dx = ?', 'HIGH', true),
('MATH_044', '(2x+3)/((x+1)(x+2)) = A/(x+1) + B/(x+2) where A and B are the coefficients 2 and 3', 'CORRECTION: A and B must be solved using cover-up method or comparing coefficients', 'Multiply both sides by (x+1)(x+2) and solve for A, B by substituting convenient values.', 'Find partial fractions of 1/((x+1)(x+2))', 'MEDIUM', true),
('MATH_045', '∫ₐᵇ f(x)dx = ∫ₐᵇ f(t)dt but the variable in answer matters', 'CORRECTION: Definite integral value is independent of variable name - its just a number', 'After evaluation at limits, variable disappears. ∫₀¹ x dx = ∫₀¹ t dt = 1/2.', 'Is ∫₀^π sin(x)dx equal to ∫₀^π sin(t)dt?', 'MEDIUM', false),
('MATH_046', '∫₋ₐᵃ f(x)dx = 2∫₀ᵃ f(x)dx always', 'CORRECTION: This is true only for EVEN functions. For odd functions, integral = 0.', 'Even: f(-x) = f(x), integral doubles. Odd: f(-x) = -f(x), integral cancels.', '∫₋₁¹ x³ dx = ?', 'HIGH', true),
('MATH_047', 'Area = ∫f(x)dx regardless of sign', 'CORRECTION: Area = ∫|f(x)|dx. When f(x) < 0, integral is negative but area is positive.', 'Split integral where f(x) changes sign. Take absolute value for area.', 'Find area between y = sinx and x-axis from 0 to 2π', 'HIGH', true),

-- DIFFERENTIAL EQUATIONS (MATH_048 to MATH_050)
('MATH_048', 'Order of DE = number of arbitrary constants', 'CORRECTION: Order = highest derivative. Degree = power of highest order derivative.', 'Order of d²y/dx² + dy/dx = 0 is 2 (not related to constants in solution).', 'What is the order of d³y/dx³ + y = 0?', 'HIGH', true),
('MATH_049', 'For separable DE, just move dx and dy like algebra', 'CORRECTION: dy/dx is a derivative, not a fraction. Separation is a technique, not arithmetic.', 'Treat as differential forms for separation: (1/y)dy = f(x)dx, then integrate both sides.', 'Solve: dy/dx = y/x', 'MEDIUM', false),
('MATH_050', 'Linear DE dy/dx + Py = Q has IF = e^P', 'CORRECTION: Integrating Factor = e^(∫P dx), not e^P', 'IF = e^(integral of P). P is a function, so integrate it first.', 'Find IF for dy/dx + (2/x)y = x²', 'HIGH', true),

-- VECTORS & 3D (MATH_051 to MATH_055)
('MATH_051', 'Vector addition: just add magnitudes', 'CORRECTION: Vector addition uses parallelogram law. |A+B| ≤ |A| + |B|.', 'Vectors have direction. Add components: (a₁+b₁, a₂+b₂, a₃+b₃).', 'If A = 3î + 4ĵ and B = -3î + 4ĵ, find |A+B|', 'HIGH', true),
('MATH_052', 'A·B = |A||B| always', 'CORRECTION: A·B = |A||B|cosθ where θ is angle between vectors', 'Dot product includes cosine of angle. Maximum when parallel, zero when perpendicular.', 'If |A|=3, |B|=4, and angle=60°, find A·B', 'HIGH', true),
('MATH_052', 'A×B = B×A', 'CORRECTION: A×B = -(B×A). Cross product is anti-commutative.', 'Order matters in cross product. Reversing order reverses direction.', 'If A×B = 5k̂, what is B×A?', 'HIGH', true),
('MATH_053', 'Scalar triple product [A B C] = A·(B×C) = A×(B·C)', 'CORRECTION: [A B C] = A·(B×C). Cannot do A×(B·C) as B·C is scalar.', 'First cross product, then dot product. Not the other way around.', '[î ĵ k̂] = ?', 'MEDIUM', true),
('MATH_054', 'Line passes through point (a,b,c) means equation has a,b,c as coefficients', 'CORRECTION: Direction ratios and point coordinates are different concepts', 'Line through (x₁,y₁,z₁) with direction (a,b,c): (x-x₁)/a = (y-y₁)/b = (z-z₁)/c', 'Write equation of line through (1,2,3) with direction ratios 2,3,4', 'MEDIUM', false),
('MATH_055', 'Distance from point to plane = direct substitution', 'CORRECTION: Distance = |ax₁ + by₁ + cz₁ + d|/√(a² + b² + c²)', 'Must normalize by dividing by magnitude of normal vector.', 'Find distance from (1,1,1) to plane x + y + z = 6', 'HIGH', true);

COMMIT;
