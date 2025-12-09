# COGNITIVE RESONANCE V4.0 - TECHNICAL INFRASTRUCTURE & DEPLOYMENT
## Complete Systems Architecture & DevOps Specification

**Document Type:** Technical Infrastructure Blueprint
**For:** Backend Engineering + DevOps Team
**Prepared By:** Infrastructure Architecture Council
**Date:** December 5, 2025, 9:25 PM IST
**Status:** FINAL - GREEN SIGNAL FOR INFRASTRUCTURE SETUP
**Classification:** CONFIDENTIAL - ENGINEERING ONLY

---

## TABLE OF CONTENTS

### PART A: TECHNOLOGY STACK
1. Database Architecture (Supabase-First)
2. Backend Services & APIs
3. Frontend Architecture
4. Caching & CDN Strategy
5. Message Queue & Background Jobs
6. Search & Indexing Infrastructure

### PART B: SYSTEM DESIGN
7. Complete Data Flow Architecture
8. Real-Time Synchronization Design
9. Authentication & Authorization
10. Data Consistency Guarantees

### PART C: DEPLOYMENT & SCALABILITY
11. Deployment Strategy (4 Phases)
12. Performance Optimization
13. Monitoring & Observability
14. Disaster Recovery & Backup

### PART D: SECURITY & COMPLIANCE
15. Security Architecture
16. Data Protection & Privacy
17. Audit & Compliance
18. Incident Response Plan

---

# PART A: TECHNOLOGY STACK

## 1. DATABASE ARCHITECTURE (SUPABASE-FIRST)

### Why Supabase (Not AWS RDS)

```
COST COMPARISON:

AWS RDS:
  - PostgreSQL db.t3.micro: ₹8,000/month (minimum)
  - Storage (500GB): ₹10,000/month
  - Backups: ₹5,000/month
  - Data transfer: ₹2,000/month
  - Total: ₹25,000/month minimum
  
Supabase (Free Tier):
  - PostgreSQL: ₹0 (up to 500MB)
  - Storage (1GB): ₹0
  - Real-time subscriptions: ₹0
  - API calls: ₹0
  - Auth: ₹0 (unlimited users)
  - Total: ₹0 initially
  
Supabase (Pro at scale):
  - After 500MB: ₹2,000/month for 2GB
  - Overage storage: ₹1/GB
  - Database CPU: Auto-scaled
  - Total: ₹5,000-10,000/month at 1M users

SAVINGS: 60-80% cheaper than AWS
```

### Supabase Schema Design

```sql
-- CORE TABLES (Optimized for Millions of Rows)

-- 1. USERS TABLE
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT auth.uid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(15),
    
    -- Profile
    full_name VARCHAR(255),
    standard SMALLINT CHECK (standard IN (11, 12)),
    coaching_center VARCHAR(255),
    
    -- Join info
    join_date TIMESTAMP DEFAULT NOW(),
    exam_target DATE,
    
    -- Status
    status VARCHAR(50) DEFAULT 'active',
    last_login TIMESTAMP,
    
    -- Flags
    is_premium BOOLEAN DEFAULT FALSE,
    is_dropped BOOLEAN DEFAULT FALSE,
    
    -- Indexed for fast queries
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_standard (standard),
    INDEX idx_join_date (join_date),
    INDEX idx_last_login (last_login),
);

-- 2. STUDENT MASTERY TABLE (Largest Table: 100k students × 250 concepts)
CREATE TABLE student_mastery (
    id BIGSERIAL PRIMARY KEY,
    student_id UUID NOT NULL,
    concept_id VARCHAR(20) NOT NULL,
    
    -- Core metrics
    mastery_level DECIMAL(3, 2),  -- 0.00 to 1.00
    times_attempted INT DEFAULT 0,
    times_correct INT DEFAULT 0,
    accuracy DECIMAL(3, 2),
    
    -- Temporal
    first_attempted TIMESTAMP,
    last_reviewed TIMESTAMP,
    next_review_date TIMESTAMP,
    
    -- Spaced repetition
    review_count INT DEFAULT 0,
    spacing_factor DECIMAL(4, 2) DEFAULT 1.0,
    
    -- Indexed for fast queries
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE (student_id, concept_id),
    INDEX idx_student_id (student_id),
    INDEX idx_concept_id (concept_id),
    INDEX idx_next_review (student_id, next_review_date),
    INDEX idx_mastery_level (student_id, mastery_level),
);

-- 3. TEST RESULTS TABLE
CREATE TABLE test_results (
    id BIGSERIAL PRIMARY KEY,
    student_id UUID NOT NULL,
    test_id VARCHAR(50) NOT NULL,
    test_type VARCHAR(30),  -- WEEKLY, MONTHLY, DIAGNOSTIC
    
    -- Scores
    total_score INT,
    total_marks INT,
    accuracy DECIMAL(3, 2),
    
    -- Time info
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds INT,
    
    -- Results
    estimated_rank INT,
    percentile DECIMAL(5, 2),
    global_rank INT,
    
    -- Metadata
    standard SMALLINT,
    test_date DATE,
    submitted_at TIMESTAMP DEFAULT NOW(),
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_student_id (student_id),
    INDEX idx_test_type (test_type),
    INDEX idx_submitted_at (submitted_at),
    INDEX idx_student_date (student_id, test_date),
);

-- 4. QUESTION RESPONSES TABLE
CREATE TABLE question_responses (
    id BIGSERIAL PRIMARY KEY,
    test_result_id BIGINT NOT NULL,
    student_id UUID NOT NULL,
    question_id VARCHAR(50) NOT NULL,
    
    -- Response data
    student_answer VARCHAR(10),
    correct_answer VARCHAR(10),
    is_correct BOOLEAN,
    marks_awarded INT,
    
    -- Time tracking
    response_time_ms INT,
    is_first_attempt BOOLEAN,
    
    -- Metadata
    concept_id VARCHAR(20),
    difficulty VARCHAR(20),
    subject VARCHAR(20),
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_test_result (test_result_id),
    INDEX idx_student_id (student_id),
    INDEX idx_question_id (question_id),
);

-- 5. CONCEPTS TABLE (Knowledge Graph)
CREATE TABLE concepts (
    concept_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(20),  -- MATH, PHYSICS, CHEMISTRY
    
    -- Hierarchy
    layer INT,  -- 1-4 for math, etc
    parent_concept_id VARCHAR(20),
    
    -- Properties
    difficulty INT DEFAULT 2,
    exam_weight DECIMAL(4, 3),  -- Marks allocation
    description TEXT,
    
    -- Indexing
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_subject (subject),
    INDEX idx_layer (layer),
);

-- 6. PREREQUISITES TABLE (Relationships)
CREATE TABLE prerequisites (
    id BIGSERIAL PRIMARY KEY,
    concept_id VARCHAR(20) NOT NULL,
    prerequisite_concept_id VARCHAR(20) NOT NULL,
    
    weight DECIMAL(3, 2),  -- 0.70 = soft, 0.90 = hard
    criticality VARCHAR(20),  -- HARD, SOFT
    transfer_coefficient DECIMAL(3, 2),  -- How much skill transfers
    
    UNIQUE (concept_id, prerequisite_concept_id),
    INDEX idx_concept (concept_id),
    INDEX idx_prerequisite (prerequisite_concept_id),
);

-- 7. QUESTIONS TABLE
CREATE TABLE questions (
    question_id VARCHAR(50) PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_image_url VARCHAR(500),
    
    -- Options
    options JSONB,  -- {"A": "text", "B": "text", ...}
    correct_answer VARCHAR(10),
    explanation TEXT,
    
    -- Classification
    subject VARCHAR(20),  -- MATH, PHYSICS, CHEMISTRY
    primary_concept_id VARCHAR(20),
    secondary_concepts JSONB,  -- Array of concept IDs
    difficulty VARCHAR(20),  -- EASY, MEDIUM, HARD
    marks INT DEFAULT 4,
    
    -- Source
    source VARCHAR(100),  -- JEE2023, Allen, etc
    year INT,
    
    -- Usage stats (for cache warming)
    usage_count INT DEFAULT 0,
    last_used TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_subject (subject),
    INDEX idx_concept (primary_concept_id),
    INDEX idx_difficulty (difficulty),
    INDEX idx_source (source),
);

-- 8. PERFORMANCE METRICS TABLE
CREATE TABLE student_performance_metrics (
    id BIGSERIAL PRIMARY KEY,
    student_id UUID NOT NULL,
    
    -- Subject-wise
    math_mastery DECIMAL(3, 2),
    physics_mastery DECIMAL(3, 2),
    chemistry_mastery DECIMAL(3, 2),
    overall_mastery DECIMAL(3, 2),
    
    -- Trend
    accuracy_trend DECIMAL(3, 2),  -- +0.05 = improving
    consistency_score DECIMAL(3, 2),
    
    -- Burnout metrics
    fatigue_score DECIMAL(3, 2),
    stress_score DECIMAL(3, 2),
    burnout_risk DECIMAL(3, 2),
    
    -- Psychological
    confidence_level DECIMAL(3, 2),
    motivation_score DECIMAL(3, 2),
    
    -- Prediction
    predicted_rank INT,
    rank_improvement INT,
    
    measured_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_student_id (student_id),
    INDEX idx_measured_at (measured_at),
);

-- OPTIMIZATION STRATEGY FOR LARGE TABLES:

-- 1. PARTITIONING (for 100M+ rows)
-- Partition student_mastery by student_id (range partitions)
-- Partition test_results by created_at (monthly partitions)
-- Partition question_responses by created_at (daily partitions)

-- 2. AUTO-COMPRESSION (TimescaleDB)
CREATE TABLE telemetry (
    time TIMESTAMPTZ,
    student_id UUID,
    event_type VARCHAR(50),
    data JSONB
) USING timescaledb_hypertable;

-- Auto-compress data older than 30 days
SELECT add_compression_policy('telemetry', INTERVAL '30 days');

-- 3. CONNECTION POOLING
-- Using PgBouncer for connection management
-- Prevents connection exhaustion at scale

-- 4. CACHING STRATEGY
-- Frequently queried results cached in Redis
-- Cache invalidation via Supabase webhooks
```

### Query Optimization for Millions of Rows

```sql
-- EFFICIENT QUERIES (< 100ms response time)

-- Query 1: Get student's next topics to study (< 50ms)
SELECT 
    concept_id,
    mastery_level,
    next_review_date
FROM student_mastery
WHERE student_id = $1
    AND next_review_date <= NOW()
    AND mastery_level < 0.85
ORDER BY mastery_level ASC
LIMIT 10;

-- Uses: idx_student_id, idx_next_review
-- Result: Indexed lookup, instant execution

-- Query 2: Get monthly results for global ranking (< 200ms)
SELECT 
    student_id,
    total_score,
    percentile
FROM test_results
WHERE test_id = $1
    AND standard = $2
ORDER BY total_score DESC;

-- Optimization: Results pre-calculated and cached
-- Query hits Redis 99% of time

-- Query 3: Get diagnostic for new student (< 100ms)
SELECT 
    subject,
    AVG(accuracy) as avg_accuracy
FROM question_responses
WHERE student_id = $1
    AND test_result_id IN (
        SELECT id FROM test_results
        WHERE student_id = $1 AND test_type = 'DIAGNOSTIC'
    )
GROUP BY subject;

-- Uses: idx_student_id
-- Subquery uses: test_type index
```

---

## 2. BACKEND SERVICES & APIs

### Microservices Architecture

```
┌─────────────────────────────────────────────────────┐
│          API Gateway (Vercel Serverless)            │
├─────────────────────────────────────────────────────┤
│                                                      │
├─────────────────┬──────────────────┬─────────────────┤
│   User Service  │   Test Service   │ Mastery Service │
│   (Auth, Prof)  │  (Questions,     │  (Metrics,      │
│                 │   Results)       │   Tracking)     │
└─────────────────┴──────────────────┴─────────────────┘
        ↓              ↓                   ↓
┌──────────────────────────────────────────────────────┐
│        Supabase PostgreSQL + TimescaleDB             │
├──────────────────────────────────────────────────────┤
│  (Core OLTP)                   (Time-series TSDB)    │
└──────────────────────────────────────────────────────┘
        ↓                                   ↓
┌──────────────────┬───────────────────────────────────┐
│ Redis Cache      │  Message Queue (BullMQ)           │
│ (Hot layer)      │  (Background jobs)                │
└──────────────────┴───────────────────────────────────┘
```

### API Endpoints (RESTful)

```typescript
// User Service
POST   /api/auth/signup               // Register
POST   /api/auth/login                // Login
GET    /api/user/profile              // Get user info
PATCH  /api/user/profile              // Update profile
GET    /api/user/dashboard            // Dashboard data
GET    /api/user/phase                // Get phase

// Test Service
GET    /api/test/weekly/:date         // Get weekly test
GET    /api/test/monthly/:month       // Get monthly benchmark
POST   /api/test/submit               // Submit test (batch)
GET    /api/test/results/:test_id     // Get results
GET    /api/test/ranking/:month       // Global ranking

// Content Service
GET    /api/content/concepts          // Visible concepts
GET    /api/content/topics/:concept   // Topic details
GET    /api/content/prerequisites     // Concept prerequisites

// Mastery Service
GET    /api/mastery/:concept          // Mastery level
GET    /api/mastery/overall           // Overall mastery
GET    /api/mastery/weak-spots        // Weak areas
GET    /api/mastery/progress          // Progress tracking

// Analytics Service
GET    /api/analytics/performance     // Performance metrics
GET    /api/analytics/burnout-risk    // Burnout score
GET    /api/analytics/trend           // Improvement trend
GET    /api/analytics/prediction      // Rank prediction
```

### Response Format (Standardized)

```json
{
  "status": "success|error|processing",
  "data": {
    // Payload
  },
  "metadata": {
    "timestamp": "2025-12-05T21:30:00Z",
    "request_id": "req_xyz123",
    "cache_hit": true,
    "response_time_ms": 45
  },
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Student standard must be 11 or 12",
      "field": "standard"
    }
  ]
}
```

---

## 3. FRONTEND ARCHITECTURE

### Tech Stack

```
Framework: Next.js 14 (React)
Deployment: Vercel (free tier initially)
State Management: Zustand
Data Fetching: React Query
Styling: Tailwind CSS + CSS Modules
Real-time: Supabase Realtime WebSocket
Offline: IndexedDB + Service Workers
```

### Key Features

```typescript
// 1. SERVER-SIDE RENDERING (SSR) for SEO
export async function getServerSideProps(context) {
    const { student_id } = context.params;
    const profile = await fetchStudentProfile(student_id);
    
    return {
        props: { profile },
        revalidate: 3600  // ISR: Re-validate every hour
    }
}

// 2. OFFLINE-FIRST TEST TAKING
// Tests downloaded to IndexedDB
// All answers stored locally
// Synced on internet reconnection

class TestTakingComponent {
    async saveAnswerLocally(answer) {
        const db = await openIndexedDB();
        await db.put('test_responses', answer);
    }
    
    async submitOnlineWhenReady() {
        if (navigator.onLine) {
            const responses = await getAllLocalResponses();
            await submitBatch(responses);
        }
    }
}

// 3. PROGRESSIVE WEB APP (PWA)
// Works offline
// Installable on home screen
// Push notifications for reminders

// 4. REAL-TIME UPDATES
// Supabase Realtime for:
// - Rank updates (after monthly test)
// - New test availability
// - Burnout alerts
// - Counselor messages
```

---

## 4. CACHING & CDN STRATEGY

### Multi-Layer Caching

```
┌─────────────────────────────────────┐
│   Browser Cache (IndexedDB)         │
│   (Offline-capable, device storage) │
└─────────────────────────────────────┘
            ↓ (Miss)
┌─────────────────────────────────────┐
│   CDN Cache (Cloudflare)            │
│   (Global, < 50ms latency)          │
└─────────────────────────────────────┘
            ↓ (Miss)
┌─────────────────────────────────────┐
│   Redis Cache (Supabase)            │
│   (Hot layer, < 10ms latency)       │
└─────────────────────────────────────┘
            ↓ (Miss)
┌─────────────────────────────────────┐
│   Database (PostgreSQL)             │
│   (Source of truth)                 │
└─────────────────────────────────────┘
```

### Cache Invalidation Strategy

```python
# Event-driven cache invalidation

# When student completes test:
@on_event('test_submitted')
async def invalidate_cache(event):
    student_id = event['student_id']
    test_type = event['test_type']
    
    # Invalidate personal caches
    await redis.delete(f"mastery:{student_id}:*")
    await redis.delete(f"performance:{student_id}:*")
    
    # Invalidate global ranking cache (if monthly)
    if test_type == 'MONTHLY':
        await redis.delete(f"ranking:month:{get_current_month()}")
    
    # Broadcast via WebSocket
    await broadcast_cache_invalidation(student_id)

# TTL-based expiration
CACHE_TIMES = {
    'test_data': 7 * 24 * 3600,      # 7 days
    'mastery_metrics': 3600,           # 1 hour
    'ranking_data': 24 * 3600,        # 1 day
    'performance_dashboard': 1800,    # 30 minutes
}
```

---

## 5. MESSAGE QUEUE & BACKGROUND JOBS

### Job Processing with BullMQ

```typescript
// Queue: process_test_result

const testResultQueue = new Queue('test_result', {
    connection: redis,
});

// Producer: Student submits test
testResultQueue.add(
    'calculate_result',
    {
        student_id: 'uuid123',
        test_id: 'test_001',
        responses: [...],
        submitted_at: now()
    },
    {
        priority: 10,  // Higher = more urgent
        attempts: 3,   // Retry up to 3 times
        backoff: {
            type: 'exponential',
            delay: 2000
        }
    }
);

// Consumer: Background worker
testResultQueue.process('calculate_result', 10, async (job) => {
    const { student_id, test_id, responses } = job.data;
    
    // Step 1: Calculate score
    const score = calculateScore(responses);
    
    // Step 2: Update mastery
    for (const response of responses) {
        await updateMastery(student_id, response);
    }
    
    // Step 3: Calculate rank
    const rank = await calculateRank(student_id, score);
    
    // Step 4: Cache result
    await cacheResult(student_id, test_id, {
        score,
        rank,
        calculated_at: now()
    });
    
    // Step 5: Emit completion event
    await emit('result_ready', {
        student_id,
        test_id,
        score,
        rank
    });
    
    return { success: true };
});

// Event handler: Result ready
on('result_ready', async (event) => {
    const { student_id, score, rank } = event;
    
    // Notify student via WebSocket
    await websocket.send(student_id, {
        type: 'result_ready',
        score,
        rank
    });
    
    // Trigger counselor if rank poor
    if (rank > 100000) {
        await assignCounselor(student_id);
    }
});
```

### Other Background Jobs

```
Queue: email_notifications
  - Send daily reminder emails
  - Send weekly progress summaries
  - Alert for low engagement

Queue: analytics_computation
  - Calculate daily metrics
  - Update burnout scores
  - Compute trend analysis

Queue: data_cleanup
  - Archive old test results
  - Compress time-series data
  - Delete inactive user data
```

---

## 6. SEARCH & INDEXING INFRASTRUCTURE

### Elasticsearch for Full-Text Search

```json
// Elasticsearch Index: questions

{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.codec": "best_compression"
  },
  "mappings": {
    "properties": {
      "question_id": { "type": "keyword" },
      "question_text": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "subject": { "type": "keyword" },
      "concept_id": { "type": "keyword" },
      "difficulty": { "type": "keyword" },
      "tags": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}

// Query: Find similar questions for weak concept
GET /questions/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "question_text": "derivative" } },
        { "term": { "subject": "MATH" } },
        { "term": { "difficulty": "MEDIUM" } }
      ],
      "filter": {
        "range": { "created_at": { "gte": "2023-01-01" } }
      }
    }
  },
  "size": 25
}
```

---

# PART B: SYSTEM DESIGN

## 7. COMPLETE DATA FLOW ARCHITECTURE

### Student's Weekly Test Journey

```
DAY 1: MONDAY 9 AM
├─ Student clicks "Take Test"
├─ Frontend checks IndexedDB
├─ IndexedDB miss → Fetch from Redis
├─ Redis hit → Download test (< 50ms)
├─ Browser caches in Session Storage + IndexedDB
└─ Pre-load images in background
    ↓
DURING TEST (10-90 minutes)
├─ All responses stored in browser RAM
├─ NO server communication
├─ User perceives zero latency
└─ Internet disconnection → Continue offline
    ↓
SUBMIT TEST
├─ All 25 answers sent in 1 API call (batch)
├─ Server enqueues: message_queue.add('calculate_result')
├─ Immediate response: "Results processing..."
└─ Backend worker processes asynchronously
    ↓
BACKGROUND PROCESSING (< 1 min)
├─ Calculate score (4 seconds)
├─ Update mastery database (10 seconds)
├─ Calculate rank (20 seconds)
├─ Cache result in Redis (2 seconds)
└─ Emit WebSocket event
    ↓
RESULT READY (Total ~2 minutes)
├─ WebSocket notifies browser
├─ Browser fetches result from cache
├─ Display: Score, Rank, Breakdown
└─ Send notification to mobile (if enabled)
```

### Data Flow Diagram

```
┌──────────────────┐
│    Student       │
│   (Browser)      │
└────────┬─────────┘
         │
         │ 1. Click "Take Test"
         ↓
┌──────────────────────────┐
│   Frontend (Next.js)     │
├──────────────────────────┤
│ - Check IndexedDB        │
│ - Fetch from API         │
│ - Store in Session       │
│ - Take test locally      │
└────────┬────────────────┘
         │
         │ 2. Submit batch
         ↓
┌──────────────────────────┐
│    API Gateway (Vercel)  │
├──────────────────────────┤
│ - Validate request       │
│ - Rate limit check       │
│ - Enqueue job            │
└────────┬────────────────┘
         │
         │ 3. Enqueue
         ↓
┌──────────────────────────┐
│   Message Queue (Bull)   │
├──────────────────────────┤
│ - Store in Redis         │
│ - Assign to worker       │
└────────┬────────────────┘
         │
         │ 4. Process
         ↓
┌──────────────────────────┐
│   Background Worker      │
├──────────────────────────┤
│ - Calculate score        │
│ - Update mastery DB      │
│ - Calculate rank         │
│ - Cache result           │
└────────┬────────────────┘
         │
         │ 5. Emit event
         ↓
┌──────────────────────────┐
│   Supabase Realtime      │
├──────────────────────────┤
│ - WebSocket broadcast    │
│ - Notify student         │
└────────┬────────────────┘
         │
         │ 6. Display result
         ↓
┌──────────────────┐
│    Student       │
│   (Browser)      │
│   Sees Results   │
└──────────────────┘
```

---

## 8. REAL-TIME SYNCHRONIZATION DESIGN

### WebSocket Architecture

```typescript
// Server-side (Node.js)

import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';

const io = new SocketIOServer(server, {
    cors: { origin: 'https://cognitive-resonance.com' },
    adapter: require('socket.io-redis'),  // Scalable across servers
});

// Namespace: /events
io.of('/events').on('connection', (socket) => {
    const student_id = socket.handshake.auth.student_id;
    
    // Join student's room
    socket.join(`student:${student_id}`);
    socket.join(`cohort:${get_cohort(student_id)}`);
    
    // Listen for test result events
    socket.on('test_submitted', (data) => {
        console.log(`Test submitted by ${student_id}`);
    });
    
    socket.on('disconnect', () => {
        console.log(`${student_id} disconnected`);
    });
});

// Emit to student when result ready
function emitResultReady(student_id, result) {
    io.of('/events').to(`student:${student_id}`).emit('result_ready', {
        score: result.score,
        rank: result.rank,
        percentile: result.percentile,
        timestamp: now()
    });
}

// Broadcast to cohort when ranking finalized
function broadcastMonthlyRanking(standard, month) {
    io.of('/events')
        .to(`cohort:${standard}`)
        .emit('ranking_available', {
            month,
            timestamp: now()
        });
}
```

---

## 9. AUTHENTICATION & AUTHORIZATION

### JWT-Based Auth

```typescript
// Authentication Flow

1. SIGNUP
   POST /api/auth/signup
   {
     "email": "student@example.com",
     "password": "secure_password",
     "standard": 12,
     "exam_target": "2026-01-15"
   }
   
   Server:
   - Validate input
   - Hash password (bcrypt)
   - Create user in Supabase Auth
   - Insert profile in PostgreSQL
   - Generate JWT token
   
   Response:
   {
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "user": { ... },
     "expires_in": 86400
   }

2. LOGIN
   POST /api/auth/login
   {
     "email": "student@example.com",
     "password": "secure_password"
   }
   
   Response:
   {
     "token": "...",
     "user": { ... }
   }

3. TOKEN REFRESH
   POST /api/auth/refresh
   Headers: { "Authorization": "Bearer refresh_token" }
   
   Response:
   {
     "token": "new_token",
     "refresh_token": "new_refresh_token"
   }

// Authorization: Role-Based Access Control (RBAC)

enum Role {
  STUDENT = 'student',
  COACH = 'coach',
  ADMIN = 'admin'
}

// Middleware: Check permission
function requireRole(...allowedRoles: Role[]) {
  return async (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'No token' });
    
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    if (!allowedRoles.includes(decoded.role)) {
      return res.status(403).json({ error: 'Access denied' });
    }
    
    req.user = decoded;
    next();
  };
}

// Usage
app.get(
  '/api/admin/users',
  requireRole(Role.ADMIN),
  getUsers
);
```

---

# PART C: DEPLOYMENT & SCALABILITY

## 10. DEPLOYMENT STRATEGY (4 PHASES)

### Phase 1: MVP Launch (Months 1-4)

```
Infrastructure:
  - Vercel (Free): Frontend
  - Supabase (Free): Database
  - BullMQ (Local Redis): Background jobs
  - Cloudflare (Free): DNS + DDoS protection

Capacity: 5,000 students
Cost: ₹0/month

Deployment:
  git push → GitHub
  → Vercel auto-deploys
  → Run migrations
  → Notify team
  → Monitor logs (Sentry)
```

### Phase 2: Growth (Months 5-8)

```
Infrastructure upgrade:
  - Vercel Pro: ₹50k/month
  - Supabase Pro: ₹50k/month (2GB tier)
  - Redis cluster: ₹30k/month
  - Elasticsearch (optional): ₹40k/month

Capacity: 50,000 students
Cost: ₹120-150k/month

New capabilities:
  - Database sharding enabled
  - Connection pooling configured
  - Auto-scaling enabled
  - Multi-region CDN active
```

### Phase 3: Scale (Months 9-18)

```
Infrastructure:
  - Dedicated Postgres instances: ₹200k/month
  - Redis cluster (3 nodes): ₹80k/month
  - Elasticsearch nodes: ₹150k/month
  - Vercel Enterprise: ₹200k/month
  - Monitoring (DataDog): ₹50k/month

Capacity: 500k-1M students
Cost: ₹680-750k/month

Changes:
  - Database replication
  - Read replicas for analytics
  - Dedicated cache layer
  - Multi-region deployment
```

### Phase 4: Enterprise (Year 2+)

```
Infrastructure:
  - Full managed setup
  - Multi-region active-active
  - Automated failover
  - Disaster recovery enabled

Capacity: 5M+ students
Cost: ₹1.5-2Cr/month
```

---

## 11. PERFORMANCE OPTIMIZATION

### Benchmark Targets

```
METRIC                    TARGET    CURRENT   PLAN
────────────────────────────────────────────────────
Page Load (Lighthouse)    > 90      TBD       W1
Test Load Time            < 200ms   TBD       W2
Result Calculation        < 5s      TBD       W3
API Response Time         < 100ms   TBD       W2
Database Query Time       < 100ms   TBD       W2
Cache Hit Ratio           > 95%     TBD       W1
Time to First Byte        < 100ms   TBD       W1
Cumulative Layout Shift   < 0.1     TBD       W2
```

### Optimization Checklist

```
Frontend:
  ✅ Code splitting (per route)
  ✅ Image optimization (WebP + lazy loading)
  ✅ CSS minification
  ✅ JavaScript minification
  ✅ Gzip compression
  ✅ HTTP/2 push
  
Backend:
  ✅ Database indexing (strategic)
  ✅ Query optimization (< 100ms)
  ✅ Connection pooling (max 50)
  ✅ Redis caching (multi-layer)
  ✅ Request rate limiting
  ✅ Response compression
  
Infrastructure:
  ✅ CDN for static assets
  ✅ Database replication
  ✅ Load balancing
  ✅ Auto-scaling enabled
  ✅ DDoS protection (Cloudflare)
```

---

## 12. MONITORING & OBSERVABILITY

### Monitoring Stack

```
Logs: Supabase Logs + Sentry
Metrics: Prometheus + Grafana
Traces: OpenTelemetry
Uptime: UptimeRobot
APM: Sentry Performance

Dashboard Views:
  1. System Health
     - API response time
     - Database connection pool
     - Redis hit rate
     - Error rate
  
  2. Application Metrics
     - Request count (per endpoint)
     - Test submission rate
     - Result calculation time
     - User engagement
  
  3. Student Metrics
     - Active students
     - Test completion rate
     - Average mastery
     - Churn rate
  
  4. Infrastructure
     - CPU usage
     - Memory usage
     - Disk I/O
     - Network bandwidth
```

### Alert Rules

```yaml
alerts:
  - name: high_error_rate
    condition: error_rate > 0.05  # 5%
    duration: 5m
    action: page_oncall
  
  - name: slow_api_response
    condition: p95_response_time > 500ms
    duration: 10m
    action: page_oncall
  
  - name: database_connection_high
    condition: active_connections > 45  # Out of 50 max
    duration: 2m
    action: alert_slack
  
  - name: test_result_delay
    condition: job_queue_length > 100
    duration: 5m
    action: scale_workers
```

---

## 13. DISASTER RECOVERY & BACKUP

### Backup Strategy

```
Database Backups:
  - Hourly snapshots (Supabase auto)
  - Daily full backups (24 copies retained)
  - Weekly snapshots (13 weeks retained)
  - Monthly archives (12 months retained)
  
Recovery Time Objective (RTO): 1 hour
Recovery Point Objective (RPO): 1 hour

Verification:
  - Test restore weekly
  - Document procedures
  - Maintain runbook
```

### Failover Procedure

```
1. DETECTION
   - Automated health check fails
   - Alert triggered in 30 seconds
   - On-call engineer paged

2. DIAGNOSIS (5 minutes)
   - Check logs in Sentry
   - Check metrics in Grafana
   - SSH to server if needed
   - Identify root cause

3. MITIGATION (10-30 minutes)
   - For database: Promote read replica
   - For API: Scale workers
   - For cache: Clear and rebuild

4. COMMUNICATION
   - Update status page
   - Notify affected users
   - Send incident report

5. POSTMORTEM
   - Document root cause
   - Identify prevention
   - Implement fix
   - Update runbook
```

---

# PART D: SECURITY & COMPLIANCE

## 14. SECURITY ARCHITECTURE

### Threat Model

```
ASSET                THREAT                    MITIGATION
────────────────────────────────────────────────────────
Student Data         Data breach               Encryption at rest
                                               Encryption in transit
                                               Access control

Passwords            Rainbow tables            Bcrypt (work factor 12)

API Keys             Exposed in code           Environment variables
                                               Rotate quarterly

Test integrity       Cheating/manipulation     Tamper detection
                                               Session pinning

Student privacy      Tracking/surveillance     No third-party pixels
                                               Anonymized analytics
```

### Implementation

```python
# 1. ENCRYPTION AT REST

# In PostgreSQL:
CREATE EXTENSION pgcrypto;

CREATE TABLE users_encrypted (
    id UUID PRIMARY KEY,
    email_encrypted BYTEA,
    phone_encrypted BYTEA
);

INSERT INTO users_encrypted (email_encrypted)
VALUES (
    pgp_sym_encrypt(
        'student@example.com',
        'encryption_key_from_vault'
    )
);

# 2. ENCRYPTION IN TRANSIT

# All connections use TLS 1.3
nginx.conf:
  ssl_protocols TLSv1.3;
  ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:...;

# 3. API SECURITY

# Rate limiting
app.use(rateLimit({
    windowMs: 60 * 1000,  // 1 minute
    max: 100,              // 100 requests per minute
    message: 'Too many requests',
}));

# CORS
app.use(cors({
    origin: 'https://cognitive-resonance.com',
    credentials: true
}));

# CSP (Content Security Policy)
app.use((req, res, next) => {
    res.setHeader(
        'Content-Security-Policy',
        "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.example.com"
    );
    next();
});

# 4. SECURE HEADERS

Helmet.js:
  - X-Frame-Options: DENY (prevent clickjacking)
  - X-Content-Type-Options: nosniff
  - X-XSS-Protection: 1; mode=block
  - Strict-Transport-Security: max-age=31536000

# 5. INPUT VALIDATION & SANITIZATION

import Joi from 'joi';

const studentSchema = Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().min(8).required(),
    standard: Joi.number().valid(11, 12).required(),
});

app.post('/api/auth/signup', (req, res) => {
    const { error, value } = studentSchema.validate(req.body);
    if (error) return res.status(400).json({ error });
    // Process value (now validated)
});
```

---

## 15. DATA PROTECTION & PRIVACY

### GDPR Compliance

```
Right to Access:
  - Student can download their data as JSON
  - Endpoint: GET /api/user/data-export
  - Returns: All personal data + learning history

Right to Deletion:
  - Student can request full deletion
  - Endpoint: DELETE /api/user/account
  - Action: Soft delete (30-day grace period)
  - After 30 days: Hard delete from all systems

Right to Portability:
  - Data exported in standard format
  - Can be imported to competitor platform
  - No artificial restrictions

Consent Management:
  - Explicit opt-in for emails
  - Clear cookie consent banner
  - Transparent privacy policy
```

---

## 16. AUDIT & COMPLIANCE

### Audit Trail

```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    actor_id UUID,
    action VARCHAR(100),
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    changes JSONB,
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address INET
);

-- Log all sensitive actions
INSERT INTO audit_log (actor_id, action, resource_type, resource_id, changes)
VALUES (
    'student_uuid',
    'submitted_test',
    'test_result',
    'test_123',
    '{"score": 120, "timestamp": "2025-12-05T21:30:00Z"}'
);
```

### Compliance Checklist

```
✅ GDPR (EU students)
   - Data protection impact assessment
   - Data processing agreement
   - Privacy policy in legal language

✅ COPPA (US students < 13)
   - Parental consent required
   - Restricted data collection
   - No targeted advertising

✅ RTE (India education law)
   - Transparent fee structure
   - Grievance redressal mechanism
   - Annual compliance report

✅ SOC 2 Type II
   - Security controls documented
   - Regular penetration testing
   - Third-party audit annually
```

---

## 17. INCIDENT RESPONSE PLAN

### On-Call Rotation

```
Primary: Senior engineer (2 weeks)
Secondary: Mid-level engineer (2 weeks)
Tertiary: Junior engineer (on-call, no primary)

Escalation:
  - 30 min no response → Page secondary
  - 1 hour no mitigation → Page engineering lead
  - 2 hours no resolution → Page VP Engineering
  - 4+ hours → Post-mortem (all team)
```

### Incident Severity

```
SEV 1: CRITICAL
  - Platform completely down
  - All students affected
  - Data loss/corruption
  Response time: 15 minutes
  
SEV 2: HIGH
  - Major feature broken
  - Large subset of students affected
  - Partial data loss
  Response time: 1 hour
  
SEV 3: MEDIUM
  - Minor feature broken
  - Small subset affected
  - Workaround exists
  Response time: 4 hours
  
SEV 4: LOW
  - UI glitch
  - Cosmetic issue
  - No workaround needed
  Response time: 48 hours
```

---

# FINAL IMPLEMENTATION CHECKLIST

### Phase 1 (Months 1-4): MVP

```
Week 1-2: Infrastructure
  ✅ Setup Supabase project
  ✅ Create database schema
  ✅ Setup Vercel project
  ✅ Configure GitHub Actions

Week 3-4: Authentication & Onboarding
  ✅ Signup flow
  ✅ Login flow
  ✅ Profile setup
  ✅ Diagnostic test (non-adaptive)

Week 5-8: Core Engine
  ✅ Layer 1: Knowledge graph import
  ✅ Layer 2: Subject strategies
  ✅ Layer 3: Phase determination
  ✅ Layer 4: Concept reveal

Week 9-12: Test Infrastructure
  ✅ Layer 5: Weekly test generation
  ✅ Layer 5.5: Caching layer
  ✅ Test submission flow
  ✅ Result calculation

Week 13-16: Engagement & Polish
  ✅ Layer 9: Engagement hooks
  ✅ Layer 10: Burnout detection
  ✅ Dashboard UI
  ✅ Mobile responsiveness

Week 17-18: Beta Testing
  ✅ Invite 100 beta testers
  ✅ Bug fixes
  ✅ Performance optimization
  ✅ Documentation

MVP Features:
  ✅ Student signup/login
  ✅ Diagnostic test
  ✅ Weekly adaptive tests
  ✅ Test results display
  ✅ Progress dashboard
  ✅ Basic mentoring chat
  
MVP NOT included:
  ❌ Monthly benchmarks (Phase 2)
  ❌ Global ranking (Phase 2)
  ❌ Advanced analytics (Phase 2)
  ❌ Integration with coaching centers (Later)
  ❌ Mobile app (Later - web PWA first)
```

---

**Document Status: FINAL - GREEN SIGNAL FOR INFRASTRUCTURE TEAM**

**Next Step:** Begin infrastructure provisioning immediately

**Timeline:** Ready for go-live in 18 weeks (4.5 months)