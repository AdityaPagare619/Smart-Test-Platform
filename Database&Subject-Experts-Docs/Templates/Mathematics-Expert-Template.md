# MATHEMATICS QUESTIONS EXCEL TEMPLATE
## Expert Sheet Format for JEE-MAINS Question Bank

**Subject:** Mathematics  
**For:** Subject Matter Experts (Masters, Professors, Experienced Coaches)  
**Update Frequency:** Real-time collaboration via Google Sheets  
**Columns:** 45 (Fully specified for optimal data structure)

---

## COLUMN SPECIFICATIONS

### SECTION A: IDENTIFICATION (Columns 1-5)

| Col | Name | Type | Example | Validation | Notes |
|-----|------|------|---------|-----------|-------|
| 1 | Q_ID | TEXT | MATH_2025_001 | Unique, never duplicate | Format: MATH_[YEAR]_[NUMBER] |
| 2 | EXAM_ID | TEXT | JEEM_2023_JAN | Dropdown list | JEEM_2023_JAN, JEEM_2023_APRIL, etc. |
| 3 | QUESTION_VERSION | DECIMAL | 1.0 | 1.0, 1.1, 1.2... | Increment on revisions |
| 4 | CREATED_DATE | DATE | 2025-12-06 | Auto-fill | Date created |
| 5 | CREATED_BY | TEXT | expert_001_sharma | Dropdown | Expert identifier |

### SECTION B: CONTENT (Columns 6-15)

| Col | Name | Type | Example | Validation | Notes |
|-----|------|------|---------|-----------|-------|
| 6 | QUESTION_TEXT | LONGTEXT | If f(x) = x³ - 3x²... | Max 5000 chars | Full English question |
| 7 | QUESTION_LANG_HINDI | LONGTEXT | यदि f(x) = x³ - 3x²... | Max 5000 chars | Hindi translation |
| 8 | CONCEPT_ID | TEXT | MATH_041 | Dropdown (from concepts list) | From knowledge graph |
| 9 | TOPIC | TEXT | Derivatives - Applications | Dropdown | Major topic area |
| 10 | SUBTOPIC | TEXT | Critical Points | Dropdown | Specific sub-area |
| 11 | LEARNING_OBJECTIVE | TEXT | Find critical points using... | Max 500 chars | What student should learn |
| 12 | DIFFICULTY_LEVEL | SMALLINT | 2 | Dropdown: 1,2,3,4 | 1=Easy, 4=Very Hard |
| 13 | ESTIMATED_TIME_SECONDS | INTEGER | 120 | Range: 30-300 | Minutes × 60 |
| 14 | MARKS | INTEGER | 4 | Dropdown: 1,2,4 | JEE marking scheme |
| 15 | QUESTION_TYPE | TEXT | MCQ | Dropdown | MCQ, NUMERICAL, INTEGER |

### SECTION C: ANSWERS (Columns 16-23)

| Col | Name | Type | Example | Validation | Notes |
|-----|------|------|---------|-----------|-------|
| 16 | OPTION_A | TEXT | x = 0 and x = 1 | Max 500 chars | For MCQ (leave blank for NUMERICAL) |
| 17 | OPTION_B | TEXT | x = 0 and x = 2/3 | Max 500 chars | For MCQ |
| 18 | OPTION_C | TEXT | x = 1 and x = 2/3 | Max 500 chars | For MCQ (CORRECT for example 1) |
| 19 | OPTION_D | TEXT | x = 0 only | Max 500 chars | For MCQ |
| 20 | CORRECT_ANSWER | TEXT | C | Dropdown: A,B,C,D or numerical | Which option is correct |
| 21 | NUMERICAL_ANSWER | DECIMAL | 42.5 | For NUMERICAL type only | Exact numerical answer |
| 22 | ANSWER_RANGE_MIN | DECIMAL | 42.0 | For NUMERICAL type only | Acceptable lower bound |
| 23 | ANSWER_RANGE_MAX | DECIMAL | 43.0 | For NUMERICAL type only | Acceptable upper bound |

### SECTION D: DIAGRAMS (Columns 24-28)

| Col | Name | Type | Example | Validation | Notes |
|-----|------|------|---------|-----------|-------|
| 24 | DIAGRAM_1_FILENAME | TEXT | diagram_MATH_2025_001_curve.png | Unique filename | Format: diagram_[Q_ID]_[type].png |
| 25 | DIAGRAM_1_LOCATION | TEXT | In question | Dropdown | In question / In option A / In solution |
| 26 | DIAGRAM_2_FILENAME | TEXT | diagram_MATH_2025_001_sol.png | Optional, unique | Second diagram if present |
| 27 | DIAGRAM_2_LOCATION | TEXT | In solution | Dropdown | Location of second diagram |
| 28 | DIAGRAM_COUNT | SMALLINT | 2 | Auto-count | Number of diagrams (0-4 max) |

### SECTION E: SOLUTION (Columns 29-34)

| Col | Name | Type | Example | Validation | Notes |
|-----|------|------|---------|-----------|-------|
| 29 | SOLUTION_TEXT | LONGTEXT | f'(x) = 3x² - 6x + 2... | Max 10000 chars | Step-by-step solution |
| 30 | SOLUTION_LANG_HINDI | LONGTEXT | f'(x) = 3x² - 6x + 2... | Max 10000 chars | Solution in Hindi |
| 31 | KEY_CONCEPTS | TEXT | Differentiation, Limits | Comma-separated | Related core concepts |
| 32 | COMMON_MISTAKES | TEXT | Algebraic errors in quadratic... | Max 500 chars | Typical student errors |
| 33 | TIPS_AND_TRICKS | TEXT | Factor the derivative instead... | Max 500 chars | Speed tips for solving |
| 34 | SIMILAR_PROBLEMS | TEXT | MATH_2025_002, MATH_2024_145 | Comma-separated Q_IDs | Cross-references |

### SECTION F: METADATA (Columns 35-40)

| Col | Name | Type | Example | Validation | Notes |
|-----|------|------|---------|-----------|-------|
| 35 | BLOOM_LEVEL | TEXT | Apply | Dropdown | Remember, Understand, Apply, Analyze, Evaluate, Create |
| 36 | JEE_WEIGHTAGE | DECIMAL | 2.0 | Range: 0.5-3.5 | Exam focus weight (1.0 = typical) |
| 37 | PREREQUISITE_CONCEPTS | TEXT | MATH_040, MATH_002 | Comma-separated IDs | What must be known first |
| 38 | RELATED_CONCEPTS | TEXT | MATH_042, MATH_043 | Comma-separated IDs | Related topic areas |
| 39 | ACCURACY_RATING | SMALLINT | 5 | Dropdown: 1-5 | Expert's confidence in question quality |
| 40 | IS_APPROVED | BOOLEAN | TRUE | Checkbox | Ready for student consumption? |

### SECTION G: TRACKING (Columns 41-45)

| Col | Name | Type | Example | Validation | Notes |
|-----|------|------|---------|-----------|-------|
| 41 | LAST_MODIFIED_DATE | DATE | 2025-12-06 | Auto-fill | Date of last edit |
| 42 | LAST_MODIFIED_BY | TEXT | expert_001_sharma | Auto-fill | Who made the edit |
| 43 | CHANGE_LOG | TEXT | Fixed solution derivation | Max 500 chars | What was changed |
| 44 | INTERNAL_NOTES | TEXT | Verified with numerical solver | Max 500 chars | Notes for admin review |
| 45 | CONTENT_HASH | TEXT | a3f9e2b1c4d7... | Auto-hash | For version control |

---

## IMPORTANT GUIDELINES FOR EXPERTS

### Before You Start
- [ ] You have write access to the Google Sheet
- [ ] You understand the concept_id system (see CONCEPTS reference sheet)
- [ ] You have a folder in shared Google Drive for uploading diagrams
- [ ] You know your expert_id (assigned by admin)

### Creating Questions

**Rule 1: One Row = One Question**
- Never split a question across multiple rows
- One question = one row, complete

**Rule 2: ALL REQUIRED FIELDS MUST BE FILLED**
- Do not leave mandatory fields blank
- System will reject incomplete rows during processing

**Rule 3: DIAGRAMS**
- Save diagrams to: `/Google Drive/JEE/Mathematics/2025/[Topic]/`
- Filename format: `diagram_[Q_ID]_[description].png`
- Size: Keep under 1000×1000 px (system will optimize)
- Format: PNG or JPG preferred (system converts to SVG)

**Rule 4: ACCURACY IS CRITICAL**
- Verify all calculations in solution
- Test against numerical solver (Wolfram Alpha, Python, etc.)
- Double-check option layout matches question intent
- Have colleague review before marking IS_APPROVED=TRUE

**Rule 5: CROSS-REFERENCES**
- When citing similar problems, ensure question exists (valid Q_ID)
- Link prerequisite concepts to build knowledge graph
- This enables AI to detect gaps in understanding

**Rule 6: LANGUAGE**
- English: Clear, concise, JEE standard terminology
- Hindi: Professional translation (not Google Translate)
- Both languages should convey same meaning and level

**Rule 7: DIFFICULTY HONESTY**
- Don't inflate difficulty (it will be verified by student performance data)
- A question rated "4" MUST be genuinely challenging
- Difficulty should align with JEE standards

---

## EXPERT CHECKLIST (Before Submitting)

Before marking IS_APPROVED=TRUE:

- [ ] Q_ID is unique (not used before)
- [ ] Question text is clear and unambiguous
- [ ] Hindi translation is accurate
- [ ] All 4 options are distinct and plausible
- [ ] Correct answer is verified (solve it yourself 3 times)
- [ ] For numerical: answer range is realistic (±1-2%)
- [ ] Solution is step-by-step and clear
- [ ] Common mistakes section reflects real student errors
- [ ] Diagrams referenced actually exist in Drive folder
- [ ] Concept ID matches knowledge graph structure
- [ ] Prerequisite concepts are correct
- [ ] Bloom level accurately reflects cognitive demand
- [ ] JEE weightage is honest (not inflated)
- [ ] Accuracy rating reflects your confidence (don't give 5 for uncertain)
- [ ] No typos or grammatical errors
- [ ] No plagiarism (original or properly attributed)

---

## SAMPLE DATA (Reference)

See the **CR-v4-Expert-Questions-Database-Architecture.md** file for 3 complete example questions with all 45 columns filled.

---

## SUBMISSION PROCESS

1. **Create Questions** in Google Sheet
2. **Upload Diagrams** to Drive folder
3. **Mark Column 40** (IS_APPROVED) = TRUE when ready
4. **Admin Reviews** in web interface
5. **Admin Approves/Rejects** with feedback
6. **System Processes** → Database updated overnight

---

**Status:** ✅ TEMPLATE FINALIZED - READY FOR EXPERT USE