# CHIEF ARCHITECT COUNCIL DISCUSSION & DECISIONS
## Questions Database System - Final Specifications

**Meeting Date:** December 6, 2025, 3:45 PM IST  
**Participants:** Chief Database Architect, 3 Subject Experts (Math/Physics/Chemistry), CTO, Systems Lead  
**Duration:** 90-minute intensive technical council  
**Outcome:** UNANIMOUS APPROVAL OF ARCHITECTURE

---

## AGENDA ITEM 1: DATA STORAGE CHALLENGE

### Problem Statement
*Chief Architect Opens:*

"We're building a platform that will scale to 100,000+ questions with diagrams. The naive approach—storing images in databases—would cost us:"

**Cost Analysis:**
```
Naive Approach (Image in Database):
- 1 question with 2 diagrams = ~800KB average (after compression)
- 10,000 questions = 8GB just for images
- 100,000 questions = 80GB
- Database overhead = 2-3x → 240GB total database
- Query speed: SLOW (images must load with question)
- Disk I/O bottleneck at scale
- Estimated cost: ₹50L+/year in infrastructure
```

### Expert Council Decision

**Mathematics Expert (Prof. Sharma):** "For mathematics, diagrams are essential—coordinate systems, graphs, geometric figures. But we don't need original resolution in the database. We need fast delivery."

**Physics Expert (Dr. Patel):** "Physics diagrams include vectors, field lines, circuits. SVG is perfect because we can preserve precision without bulk. My suggestion: convert all to vector format."

**Chemistry Expert (Dr. Desai):** "Chemistry actually has the most complex diagrams—molecular structures, reaction mechanisms. But organic structures convert beautifully to vector. Better than raster."

**CTO (Technical Lead):** "My recommendation: **Original → SVG (vector) → WebP (optimized raster for compatibility) → Progressive loading (LQI first)**. This gives us:"

✅ **DATABASE APPROACH:**
```
Instead of storing images:
- Database stores ONLY filename references (45 bytes)
- Example: "diagram_MATH_2025_001_curve.svg"
- CDN stores actual images
- Database stores metadata about images:
  ├── Original filename
  ├── Dimensions
  ├── Size after optimization
  ├── Storage URLs (SVG + WebP)
  └── Accessibility alt-text
```

✅ **SIZE REDUCTION:**
```
BEFORE:  450 KB (original PNG)
AFTER:   45 KB (SVG) = 90% reduction
FURTHER: 35 KB (WebP) = 92% reduction
DATABASE: 0.045 KB (just filename) = 99.99% reduction

10,000 questions with 2 diagrams each:
Before: 8 GB
After database: 45 MB (just references)
After CDN: 700 MB (actual images, optimized)
```

**UNANIMOUS DECISION:** ✅ **ACCEPTED**

---

## AGENDA ITEM 2: DATABASE SEPARATION ARCHITECTURE

### Problem Statement
*Chief Architect:*

"If we keep student data and question data in the same database, we'll face scaling issues. A student taking a test hits the database constantly (tracking progress), while questions are static content. These are fundamentally different access patterns."

### Expert Council Analysis

**Database Principal (Lead):** "Let's think about access patterns:"

```
STUDENT DATA:
- Write-heavy (every answer recorded)
- Frequent updates (mastery levels, progress)
- User-specific queries (need student_id)
- Sensitive (personal data)
- Small result sets (individual student)
- Real-time requirements

QUESTION DATA:
- Read-heavy (question delivery)
- Static/infrequent updates
- Agnostic to user (same questions for all)
- Public (can be cached globally)
- Large result sets (batches of questions)
- Can tolerate slight delays
```

**Chief Architect's Recommendation:**

"These are DIFFERENT databases with DIFFERENT optimization strategies. Separating them gives us:"

✅ **THREE DATABASE LAYERS:**

**Layer 1: STUDENT_DATA (Supabase PostgreSQL - Auth Integrated)**
```
PURPOSE: User profiles, mastery, progress
OPTIMIZATION: Write-optimized with indexes on user_id
SECURITY: Highest (PII + authentication)
SCALE: One database, sharded by user_id
SIZE: 1GB per 1M users
BACKUP: Real-time replicas
EXAMPLE QUERIES:
  - Get student profile (fast: indexed by user_id)
  - Update mastery (fast: simple update)
  - Get test results (fast: user_id index)
```

**Layer 2: QUESTIONS_DATA (Separate PostgreSQL - Subject-Partitioned)**
```
PURPOSE: Question bank, diagrams metadata, concepts
OPTIMIZATION: Read-optimized with indexes on subject, concept
SECURITY: Medium (public content, audit trail)
SCALE: Replicas in 3 regions (globally distributed)
SIZE: ~50MB per 10,000 questions
BACKUP: Standard PostgreSQL backup
EXAMPLE QUERIES:
  - Get question by Q_ID (instant: direct lookup)
  - Get all Math questions, difficulty 3 (fast: indexed)
  - Get questions by concept (fast: indexed)
  - Diagram metadata (fast: simple join)
```

**Layer 3: ANALYTICS_DATA (TimescaleDB - Time-Series Optimized)**
```
PURPOSE: Telemetry, burnout detection, trends
OPTIMIZATION: Time-series compression (auto-purges old data)
SECURITY: Low (aggregated, anonymized)
SCALE: Auto-shards by time
SIZE: 300MB per year (with compression)
BACKUP: Immutable snapshots
EXAMPLE QUERIES:
  - Burnout risk for user (aggregation: slow but analytical)
  - Performance trends over time (time-range: efficient)
  - Learning curve analysis (group by: analytical)
```

**Mathematics Expert:** "This makes sense. Questions don't change per student. A student in Delhi solving a calculus problem needs the SAME question and diagrams as a student in Mumbai. But their progress is completely different."

**Chemistry Expert:** "Exactly. And for compliance—if we need to audit who created which question, that's separate from tracking which student attempted it."

**Physics Expert:** "Plus, we can replicate the questions database globally (cache it everywhere) without replicating sensitive student data. That's a huge security win."

**UNANIMOUS DECISION:** ✅ **ACCEPTED - THREE DATABASE ARCHITECTURE**

---

## AGENDA ITEM 3: EXCEL-BASED EXPERT WORKFLOW

### Problem Statement
*Chief Architect:*

"Experts are teachers/professors, not software engineers. We can't ask them to use a custom database tool. But we need structured data. How do we bridge this gap?"

### Expert Council Discussion

**Mathematics Expert:** "Google Sheets. Teachers already use Google Workspace. Real-time collaboration built-in. Version history tracked."

**Physics Expert:** "Agreed. But we need STRUCTURE. Random columns = garbage in, garbage out. I suggest a very detailed template with:"
- Mandatory columns
- Dropdown lists (not free text)
- Data validation
- Comments for guidance
- Locked columns (system-managed)

**Chemistry Expert:** "And the template should be subject-specific. Chemistry diagrams need different metadata than math diagrams."

**Database Principal:** "I propose three separate Google Sheets, one per subject. Each with:"

✅ **GOOGLE SHEETS ARCHITECTURE:**

```
ONE SHEET PER SUBJECT:
├── MATHEMATICS_QUESTIONS_2025
│   ├── 45 columns (fully specified)
│   ├── Data validation on every column
│   ├── Dropdown lists (concept_id, topic, difficulty)
│   ├── Required fields marked
│   └── Access: All Math experts can edit
│
├── PHYSICS_QUESTIONS_2025
│   ├── 45 columns (same structure, physics-specific terms)
│   ├── Data validation
│   ├── Dropdown lists (physics concepts)
│   └── Access: All Physics experts can edit
│
└── CHEMISTRY_QUESTIONS_2025
    ├── 45 columns (same structure, chemistry-specific terms)
    ├── Data validation
    ├── Dropdown lists (chemistry concepts)
    └── Access: All Chemistry experts can edit

SHARED REFERENCE SHEETS:
├── CONCEPTS (Read-only for experts)
│   └── concept_id → name → layer → weight
├── EXPERTS (Read-only)
│   └── expert_id → name → subject
└── EXAMS (Read-only)
    └── exam_id → date → official_name
```

**Data Validation Example:**
```
Column: DIFFICULTY_LEVEL
Type: Dropdown
Options: 1 (Easy), 2 (Medium), 3 (Hard), 4 (Very Hard)
Notes: "Don't inflate. Difficulty will be verified by student performance data."

Column: CONCEPT_ID
Type: Dropdown
Data Source: CONCEPTS!A:A
Notes: "Must match knowledge graph. If not listed, request new concept from admin."

Column: QUESTION_TEXT
Type: Text
Min Length: 50 chars
Max Length: 5000 chars
Format: English, clear, JEE standard terminology

Column: IS_APPROVED
Type: Checkbox
Default: FALSE
Notes: "Only mark TRUE when you've verified the question 3+ times"
```

**CTO:** "Each sheet has Google Apps Script that validates data before submission. Expert clicks 'SUBMIT TO ADMIN' button, which:"
1. Validates all required fields
2. Checks for duplicates (Q_ID)
3. Verifies referenced diagrams exist
4. Creates a review request for admin
5. Logs timestamp and expert_id

**UNANIMOUS DECISION:** ✅ **ACCEPTED - GOOGLE SHEETS + SCRIPTS**

---

## AGENDA ITEM 4: EXPERT SHEET COLUMN DESIGN

### Problem Statement
*Chief Architect:*

"We need 45 columns per question. If we get this wrong, we'll either have too much data (expert burden) or too little (poor AI engine later). Let's scrutinize each column."

### Expert Council Detailed Review

**Round 1: Identification Columns (5 columns)**
```
Q_ID             ← Must be unique, format specified
EXAM_ID          ← Which exam/year this question targets
QUESTION_VERSION ← For revision tracking
CREATED_DATE     ← When was it created
CREATED_BY       ← Which expert created it
```
**Mathematics Expert:** "This is good. Helps us track who creates quality questions."
**Decision:** ✅ APPROVED

**Round 2: Content Columns (10 columns)**
```
QUESTION_TEXT       ← English question
QUESTION_LANG_HINDI ← Hindi translation
CONCEPT_ID          ← Links to knowledge graph
TOPIC               ← Major category
SUBTOPIC            ← Specific area
LEARNING_OBJECTIVE  ← What should student understand
DIFFICULTY_LEVEL    ← 1-4 scale
ESTIMATED_TIME_SEC  ← Expected solve time
MARKS               ← JEE marking
QUESTION_TYPE       ← MCQ, NUMERICAL, INTEGER
```
**Physics Expert:** "I like that we have both topic and subtopic. Math has 'Derivatives - Applications' as topic but 'Critical Points' as subtopic. That's useful for adaptive recommendations."

**Chemistry Expert:** "The LEARNING_OBJECTIVE is crucial. It forces us to think 'what does student actually learn from this question' not just 'can they solve it'. I've seen many questions that test procedure but teach nothing."

**Decision:** ✅ APPROVED

**Round 3: Answer Columns (8 columns)**
```
OPTION_A              ← MCQ option 1
OPTION_B              ← MCQ option 2
OPTION_C              ← MCQ option 3
OPTION_D              ← MCQ option 4
CORRECT_ANSWER        ← Which is correct (A/B/C/D)
NUMERICAL_ANSWER      ← For numerical questions
ANSWER_RANGE_MIN      ← Acceptable lower bound
ANSWER_RANGE_MAX      ← Acceptable upper bound
```
**Mathematics Expert:** "The answer range is important. For a question asking for √2, is 1.414 acceptable? Is 1.41 acceptable? This field decides."

**Database Principal:** "Exactly. This prevents borderline cases where a student gets marked wrong for rounding."

**Decision:** ✅ APPROVED

**Round 4: Diagram Columns (5 columns)**
```
DIAGRAM_1_FILENAME   ← First diagram filename
DIAGRAM_1_LOCATION   ← Is it in question or solution
DIAGRAM_2_FILENAME   ← Second diagram (if needed)
DIAGRAM_2_LOCATION   ← Location of second
DIAGRAM_COUNT        ← Total number of diagrams
```
**Physics Expert:** "Why only 2 diagrams? Some circuit problems need 3."

**Chief Architect:** "Good point. Let's make it flexible: DIAGRAM_COUNT can go up to 4, and add DIAGRAM_3_FILENAME, DIAGRAM_3_LOCATION, DIAGRAM_4_FILENAME, DIAGRAM_4_LOCATION. Experts fill only what they need."

**Updated columns: 9 instead of 5 for diagram section**

**Decision:** ✅ APPROVED (with expansion to 4 diagrams)

**Round 5: Solution Columns (6 columns)**
```
SOLUTION_TEXT          ← Step-by-step solution
SOLUTION_LANG_HINDI    ← Hindi solution
KEY_CONCEPTS           ← Related core concepts
COMMON_MISTAKES        ← What students get wrong
TIPS_AND_TRICKS        ← How to solve faster
SIMILAR_PROBLEMS       ← Cross-references to other Q_IDs
```
**Chemistry Expert:** "The COMMON_MISTAKES field is genius. It teaches us what misconceptions our questions are hitting. This is valuable for the burnout detection layer later."

**Mathematics Expert:** "And TIPS_AND_TRICKS helps the engine understand if a question rewards speed or conceptual understanding."

**Decision:** ✅ APPROVED

**Round 6: Metadata Columns (6 columns)**
```
BLOOM_LEVEL           ← Remember, Understand, Apply, Analyze, Evaluate, Create
JEE_WEIGHTAGE         ← How often this concept appears in JEE (0.5-3.5 scale)
PREREQUISITE_CONCEPTS ← What must be known first
RELATED_CONCEPTS      ← Related topics
ACCURACY_RATING       ← Expert confidence (1-5 stars)
IS_APPROVED           ← Ready for students?
```
**Physics Expert:** "BLOOM_LEVEL is beautiful. It tells us the cognitive demand. A question that tests 'Remember' shouldn't be weighted same as one testing 'Analyze'."

**Mathematics Expert:** "And JEE_WEIGHTAGE—this is the weight in actual exams. Derivatives appear in ~15% of questions (weightage ~1.5), Trigonometry in ~20% (weightage ~2.0)."

**Database Principal:** "This feeds the adaptive engine. We want to give students more practice on high-weightage concepts."

**Decision:** ✅ APPROVED

**Round 7: Tracking Columns (5 columns)**
```
LAST_MODIFIED_DATE ← Date of last change
LAST_MODIFIED_BY   ← Who modified it
CHANGE_LOG         ← What changed
INTERNAL_NOTES     ← For admin review
CONTENT_HASH       ← For version control
```
**Chemistry Expert:** "This is audit trail. Crucial for compliance if a question becomes controversial or if we need to roll back."

**Decision:** ✅ APPROVED

**FINAL TALLY: 45 COLUMNS APPROVED**

---

## AGENDA ITEM 5: DATABASE SCHEMA VERIFICATION

### Chief Database Principal Presents

"I've designed the PostgreSQL schema with these tables:"

✅ **TABLE: questions** (Core question data)
```sql
Indexes:
- subject (fast filtering by Math/Physics/Chemistry)
- concept_id (fast filtering by concept)
- exam_id (fast filtering by exam)
- approved (fast filtering for unapproved questions)
- difficulty (fast filtering by difficulty)

Size estimate: 50 bytes per question × 100,000 = 5 MB
```

✅ **TABLE: question_options** (MCQ options)
```sql
Relationship: Many options per question
Indexes:
- question_id (fast lookup of options for a question)

Size estimate: 200 bytes per option × 4 × 100,000 = 80 MB
```

✅ **TABLE: diagram_metadata** (Image references)
```sql
Relationship: Many diagrams per question
Indexes:
- question_id (fast lookup of diagrams)
- filename (fast direct access)

Size estimate: 500 bytes per diagram × 100,000 = 50 MB
```

✅ **TABLE: question_performance** (Student attempt data)
```sql
Relationship: Created post-exam when students have attempted questions
Indexes:
- question_id (fast performance lookup)
- data_collection_period (fast time-range queries)

Size estimate: Grows with attempts (~1 row per 100 attempts)
```

✅ **TABLE: concept_prerequisites** (Knowledge graph)
```sql
Relationship: Shows dependencies between concepts
Example:
- Derivatives (MATH_041) requires Limits (MATH_040)
- Integration (MATH_043) requires Differentiation (MATH_041)

This enables the knowledge graph to detect gaps.
```

**Mathematics Expert:** "So if a student is weak in Limits, the system detects it, and when they try Derivatives questions, it recommends Limit review?"

**Chief Architect:** "Exactly. This is where the AI gets smart—not guessing, but following the actual prerequisites."

**Decision:** ✅ DATABASE SCHEMA APPROVED

---

## AGENDA ITEM 6: IMAGE OPTIMIZATION STRATEGY

### Problem: Images = Storage + Bandwidth + Latency

**CTO Presents:**

"Current ed-tech platforms embed images in databases or store them inefficiently. We're doing something smarter:"

### Step 1: Original → SVG Conversion

**Mathematics Expert:** "How do you convert a hand-drawn graph to SVG?"

**Chief Architect:** "We use a combination of:"
1. **For geometric diagrams** (exact): Export from Geogebra/Desmos as SVG
2. **For hand-drawn** (approximate): AI auto-tracing service (Adobe, Potrace)
3. **For complex diagrams** (manual): Expert redraws in vector format

```
Example:
Original: diagram.png (450 KB)
Auto-traced SVG: diagram.svg (45 KB) - 90% reduction
Manual quality check: Verify vectors match original
```

**Physics Expert:** "And for circuit diagrams?"

**Chief Architect:** "Circuits are perfect for SVG—they're already vector-like. We can export directly from circuit simulation software."

**Chemistry Expert:** "Molecular structures?"

**Chief Architect:** "Chemistry is ideal. Programs like ChemDraw natively export SVG. A benzene ring drawing (650 KB PNG) becomes 8 KB SVG."

### Step 2: SVG → WebP (Raster Backup)

**Database Principal:** "Not all browsers support SVG equally. We also generate WebP (modern raster format):"

```
Original PNG:        450 KB
SVG:                 45 KB
WebP:                35 KB
Compression ratio:   92.2%
```

### Step 3: Progressive Image Loading (LQI)

**CTO:** "When a student opens a question with diagram, we:"
1. **Display LQI (Low Quality Image)** - 5 KB, loads instantly
2. **In background:** Load full-quality SVG/WebP
3. **On display:** Swap LQI → full quality seamlessly

Result: Student perceives instant load time.

### Step 4: CDN Delivery

**Chief Architect:** "Images stored on CDN (Cloudflare, Bunny, etc.), NOT in database:"

```
Database: "Store filename reference only"
  Example: "diagram_MATH_2025_001_curve.svg"
  Size: 45 bytes

CDN: Store actual SVG/WebP files
  With global replication (Tokyo, London, Sydney, etc.)
  With compression enabled
  With 1-year caching (questions rarely change)
```

**Cost Analysis:**
```
Database approach: ₹50L+/year (storage + queries)
CDN approach:      ₹5-10L/year (CDN transfer)
Savings:           ₹40L+/year
```

**Decision:** ✅ IMAGE OPTIMIZATION STRATEGY APPROVED

---

## AGENDA ITEM 7: DATA FLOW SECURITY

### Problem: How do we ensure data integrity without chaos?

**Database Principal:**

"Expert creates in Google Sheets → CSV upload → Database. At each step, we validate and scan for issues."

### The Pipeline

```
STEP 1: Expert fills Google Sheet
├── Data validation at sheet level (dropdowns, required fields)
└── Automatic version history (Google Workspace)

STEP 2: Expert clicks "SUBMIT"
├── Google Apps Script validates complete submission
├── Checks for Q_ID uniqueness
├── Verifies diagrams exist in Drive
├── Creates admin review request
└── Logs timestamp + expert_id

STEP 3: Admin reviews in web interface
├── Preview question + diagrams
├── See expert notes + history
├── Approve / Reject / Request changes
└── Admin signature logged

STEP 4: Approved → CSV Export
├── Only approved questions exported
├── Validation run #2 (integrity checks)
└── Ready for processing

STEP 5: Nightly Batch Job
├── CSV parser (validate format)
├── Duplicate check (already in DB?)
├── Diagram validation (files exist?)
├── Image optimization (PNG → SVG → WebP)
├── Database insertion (with rollback on error)
├── CDN sync (upload images)
└── Performance logging
```

**Mathematics Expert:** "So a corrupted CSV or bad diagram doesn't break the database?"

**Database Principal:** "Correct. Batch job validates everything before touching the database. If any step fails, the entire transaction rolls back. We log everything."

**Decision:** ✅ DATA FLOW SECURITY APPROVED

---

## AGENDA ITEM 8: SEPARATION OF STUDENT DATA

### Critical Decision: Student Data ≠ Expert Data

**Chief Architect:**

"This is non-negotiable for privacy and performance:"

✅ **WHAT'S SEPARATED:**

```
STUDENT DATA DATABASE:
├── User profiles (email, name, standard)
├── Authentication (encrypted passwords)
├── Progress tracking (which questions attempted)
├── Mastery levels (computed from attempts)
├── Test results (scores, time taken)
└── Personal preferences (notification settings)

NEVER in student DB:
❌ Expert comments about questions
❌ Question creation metadata
❌ Content audits
❌ Performance metrics for questions

QUESTION DATA DATABASE:
├── Question text + options
├── Solution explanation
├── Diagram metadata
├── Concept links
├── Expert notes
└── Performance metrics (student aggregate only)

NEVER in questions DB:
❌ Individual student attempts
❌ Personal progress data
❌ Authentication credentials
❌ Student preferences
```

**Benefits:**

```
1. SECURITY:
   - Student data encrypted separately
   - Question data can be public/cached
   - No mixing of sensitive + non-sensitive

2. COMPLIANCE:
   - GDPR: Easy to delete student data without touching content
   - Audit: Separate audit trails for content vs student data
   - Transparency: Show students exactly what's stored

3. PERFORMANCE:
   - Student DB optimized for writes (progress updates)
   - Question DB optimized for reads (content delivery)
   - No contention on shared locks

4. SCALING:
   - Replicate question DB globally (students in any country get same content)
   - Keep student DB in India (regulatory requirement)
   - Time-series DB auto-compresses (old analytics purged)
```

**Chemistry Expert:** "So if a student exercises their right to be forgotten (GDPR), we delete them from student DB but keep questions?"

**Chief Architect:** "Exactly. Their progress, scores, all personal data gone. But the questions they studied remain in the system for other students."

**Decision:** ✅ SEPARATION APPROVED (CRITICAL SECURITY REQUIREMENT)

---

## AGENDA ITEM 9: EXPERT QUALITY ASSURANCE

### Problem: How do we ensure experts create high-quality questions?

**Chief Architect:**

"We implement multiple layers of quality control:"

### Layer 1: Pre-Submission (Expert Self-Check)

```
Google Sheet has hints:
├── Column header notes explaining each field
├── Example values (templates)
├── Links to guidance documents
└── Validation warnings (red highlight if invalid)

Checklist for expert before marking IS_APPROVED=TRUE:
├── Q_ID unique?
├── Question clear and unambiguous?
├── All 4 options distinct?
├── Correct answer verified 3x?
├── Diagrams exist and match descriptions?
├── Solution step-by-step?
├── No typos or grammar errors?
└── Accuracy rating honest (1-5)?
```

### Layer 2: Admin Review (Manual)

```
Admin in web interface:
├── Preview full question
├── Check solution quality
├── Verify diagrams render correctly
├── Look for ambiguity or errors
├── Check expert's accuracy rating
└── Approve or Request Changes (with specific feedback)

Turnaround: 24 hours typical
```

### Layer 3: Post-Exam Analysis (Data-Driven)

```
After enough students attempt a question:
├── Calculate actual difficulty (should match expert's claim)
├── Calculate discrimination index (good Qs separate strong/weak)
├── Check for misinterpretation signals
├── Flag questions that don't match patterns
├── Notify expert: "Your question is performing differently than expected"

System can auto-detect if:
❌ Most students pick wrong answer (ambiguous question?)
❌ Smart students picking wrong answer (answer key wrong?)
❌ Everyone gets it right (too easy or missing distractors?)
❌ Difficulty rating not matching student data (miscalibrated)
```

### Accuracy Rating System

```
ACCURACY_RATING column:
5 = I've verified this 10+ times. Impossible to be wrong.
4 = I've verified thoroughly. Very confident.
3 = I've verified multiple times. Reasonably confident.
2 = I've verified once. Some doubt.
1 = I haven't verified. Unsure.

These ratings feed into:
- Admin priority for review (1-2 = review first)
- Question weighting (5-rated questions weighted higher initially)
- Expert reputation (consistently high ratings = trusted expert)
```

**Mathematics Expert:** "So a new expert creating their first question might get lower rating even if correct?"

**Database Principal:** "Exactly. It's not about being wrong. It's about confidence level. Admin sees both the question AND the rating, and can decide if they trust the expert."

**Decision:** ✅ QUALITY ASSURANCE LAYERS APPROVED

---

## AGENDA ITEM 10: CONCEPT MAPPING (KNOWLEDGE GRAPH)

### How Concepts Link Together

**Chief Architect:**

"Each question links to a CONCEPT_ID. These concepts form a directed graph showing prerequisites:"

```
Example: Mathematics Prerequisites

CALCULUS
├── Derivatives (MATH_041)
│   ├── Requires: Limits (MATH_040)
│   └── Requires: Functions (MATH_030)
├── Integration (MATH_043)
│   ├── Requires: Derivatives (MATH_041)
│   └── Requires: Antiderivatives (MATH_042)
└── Differential Equations (MATH_045)
    └── Requires: Integration (MATH_043)

DATABASE:
concept_prerequisites table tracks each arrow:
MATH_041 (Derivatives) requires MATH_040 (Limits)
  - criticality: HARD (can't understand without)
  - weight: 0.9 (strong dependency)
  - transfer_coefficient: 0.7 (learning Limits helps 70% with Derivatives)
```

**Physics Expert:** "This is how your engine detects gaps, right?"

**Chief Architect:** "Yes. When a student struggles with Newton's Second Law (PHY_015), the engine checks prerequisites—Forces (PHY_010), Vectors (PHY_005)—and recommends review."

**Chemistry Expert:** "For chemistry, many concepts are independent. Like electrochemistry vs organic chemistry."

**Database Principal:** "Exactly. That's why we have 'weight' field. Some prerequisites are HARD (must know), others are SOFT (helpful but not mandatory)."

**Decision:** ✅ CONCEPT MAPPING APPROVED

---

## FINAL DECISION: ARCHITECTURE APPROVED ✅

### Summary of Decisions

| Item | Decision | Status |
|------|----------|--------|
| **Database Separation** | Student ≠ Question ≠ Analytics | ✅ APPROVED |
| **Question Excel Template** | 45 columns, Google Sheets, 3 subjects | ✅ APPROVED |
| **Image Optimization** | Original → SVG → WebP (92% reduction) | ✅ APPROVED |
| **Data Flow Security** | CSV → validation → batch → database with rollback | ✅ APPROVED |
| **Expert Quality Assurance** | Pre-submit check + admin review + post-exam analysis | ✅ APPROVED |
| **Concept Mapping** | Directed graph with prerequisites and transfer coefficients | ✅ APPROVED |
| **Diagram Storage** | CDN only, database stores filenames (not images) | ✅ APPROVED |
| **Progressive Loading** | LQI (Low Quality Image) first, HQ loads in background | ✅ APPROVED |
| **Expert Separation** | No mixing expert data with student data | ✅ APPROVED |
| **Column Specification** | All 45 columns with validation rules detailed | ✅ APPROVED |

---

## IMPLEMENTATION TIMELINE

### Phase 1: Setup (Week 1-2)
- [ ] Create Google Sheets templates (3 subjects)
- [ ] Build Google Apps Scripts (validation + submission)
- [ ] Design PostgreSQL schema
- [ ] Set up CDN for images

### Phase 2: Admin Panel (Week 3-4)
- [ ] Build admin review interface
- [ ] Set up approval workflow
- [ ] Create batch processing job
- [ ] Build image conversion pipeline

### Phase 3: Testing (Week 5-6)
- [ ] Load test with 1000 sample questions
- [ ] Verify image optimization pipeline
- [ ] Test batch processing
- [ ] Admin panel usability testing

### Phase 4: Launch (Week 7)
- [ ] Expert training session
- [ ] Go live with 3 expert teams
- [ ] Monitor quality metrics
- [ ] Iterate on feedback

---

## NEXT STEPS (IMMEDIATE)

1. **Aditya (CTO):** Build Google Sheets templates with Apps Script validation
2. **Math Expert:** Create 10 sample questions to test pipeline
3. **Database Team:** Deploy PostgreSQL schema + indexing
4. **DevOps:** Set up image conversion pipeline (PNG → SVG)
5. **Admin Panel Team:** Build review interface

---

**FINAL STATUS: ✅ 100% AGREED BY CHIEF ARCHITECT COUNCIL**

**Ready to proceed with implementation.**

---

**Prepared by:** Chief Database Architect + Chief Experts Council
**Date:** December 6, 2025, 5:00 PM IST
**Next Review:** December 10, 2025 (after first 10 questions processed)