# OTP Flood Testing Framework — Process Flow

## 1. High-Level Process Flow

```mermaid
flowchart TD
    A(["START: Authorization & Scope"]) --> B[Target Profiling]
    B --> C[Load OTP Template Library]
    C --> D{Select Attack Profile}
    
    D -->|Linear Flood| E1[Configure: rate, duration, interval]
    D -->|Exponential Burst| E2[Configure: base, multiplier, max]
    D -->|Random Burst| E3[Configure: min, max, distribution]
    D -->|Rotating Brand| E4[Configure: brand rotation, timing]
    
    E1 --> F[Execute Flood Simulation]
    E2 --> F
    E3 --> F
    E4 --> F
    
    F --> G{Detection Triggered?}
    G -->|Yes - Blocked| H1[Log: Blocked Response]
    G -->|Yes - CAPTCHA| H2[Log: Challenge Response]
    G -->|No - Allowed| H3[Log: Success Response]
    
    H1 --> I[Collect Metrics]
    H2 --> I
    H3 --> I
    
    I --> J{More Profiles?}
    J -->|Yes| D
    J -->|No| K[Detection Evaluation]
    
    K --> L[Gap Analysis]
    L --> M[Mitigation Recommendations]
    M --> N([Report Generation])
```

## 2. Template Engine Flow

```mermaid
flowchart LR
    subgraph Input [Input Layer]
        A1[Target Phone Number]
        A2[Attack Profile]
        A3[Rate Parameters]
    end
    
    subgraph Engine [Template Engine]
        B1[Brand Selector]
        B2[OTP Generator]
        B3[Message Composer]
        B4[Format Validator]
    end
    
    subgraph Library [Template Library]
        C1[bank/*.json]
        C2[e-commerce/*.json]
        C3[social-media/*.json]
        C4[streaming/*.json]
        C5[telecom/*.json]
    end
    
    subgraph Output [Output Layer]
        D1[Formatted OTP Message]
        D2[Verification Payload]
        D3[Timing Schedule]
    end
    
    Input --> Engine
    Library --> B1
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> Output
```

## 3. Execution Flow Detail

```mermaid
sequenceDiagram
    participant U as User/Operator
    participant F as Flood Controller
    participant T as Template Engine
    participant W as WhatsApp API
    participant V as Verification Endpoint
    participant D as Detection Evaluator
    participant R as Reporter
    
    U->>F: Start simulation (target, profile, params)
    F->>T: Request OTP message
    T->>T: Select brand (rotation logic)
    T->>T: Generate OTP code
    T->>T: Compose message & payload
    T-->>F: Return formatted message
    
    loop Flood Cycle (configurable rate)
        F->>W: Send OTP via WhatsApp API
        W-->>F: Delivery status
        F->>V: POST verification payload
        V-->>F: Response (200/401/429)
        F->>D: Log response + timing
        D->>D: Score against detection threshold
        F->>F: Wait for next interval
    end
    
    F->>D: Send metric collection
    D->>D: Pattern analysis
    D->>D: Gap identification
    D-->>R: Detection results
    
    R->>R: Generate report
    R-->>U: Return findings + recommendations
```

## 4. Detection Evaluation Flow

```mermaid
flowchart TD
    subgraph Input [Detection Input]
        A1[Raw Metrics]
        A2[Timing Data]
        A3[Response Codes]
        A4[Block Records]
    end
    
    subgraph Analysis [Analysis Engine]
        B1[Rate Limit Analysis]
        B2[Pattern Recognition]
        B3[Behavioral Scoring]
        B4[Anomaly Detection]
    end
    
    subgraph Scoring [Scoring Matrix]
        C1{Detection Score}
        C1 -->|Score < 30| D1[VULNERABLE - No Detection]
        C1 -->|Score 30-60| D2[PARTIAL - Inconsistent]
        C1 -->|Score 60-85| D3[ADEQUATE - Late Detection]
        C1 -->|Score > 85| D4[STRONG - Immediate Block]
    end
    
    subgraph Output [Evaluation Output]
        E1[Detection Gap Report]
        E2[Mitigation Priority]
        E3[Remediation Plan]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> B4
    
    B1 --> C1
    B2 --> C1
    B3 --> C1
    B4 --> C1
    
    C1 --> Output
```

## 5. Decision Tree — Testing Result Classification

```mermaid
flowchart TD
    A[Execute Flood Test] --> B{HTTP Response}
    
    B -->|200 Success| C{Repeated?}
    C -->|Yes - Rate Limiter Bypassed| D[CRITICAL: No Rate Limiting]
    C -->|No - Single Success| E[Verify: Check Rate Limit Config]
    
    B -->|401 Unauthorized| F{Pattern?}
    F -->|Immediate| G[STRONG: Auth Gate]
    F -->|After X requests| H[ADEQUATE: Threshold Hit]
    
    B -->|429 Rate Limited| I{Block Duration}
    I -->|< 60s| J[WARNING: Short Window]
    I -->|60-300s| K[ADEQUATE: Standard Window]
    I -->|> 300s| L[STRONG: Long Window]
    
    B -->|Other Error| M{Error Type}
    M -->|Timeout| N[Review: Network Issue]
    M -->|500 Server Error| O[CRITICAL: Server Overload]
    
    D --> P[ACTION: Implement Rate Limiting]
    G --> Q[PASS - Document Config]
    H --> R[ACTION: Lower Threshold]
    J --> S[ACTION: Extend Block Duration]
    K --> T[PASS - Standard Config]
    L --> U[PASS - Strong Config]
    O --> V[ACTION: Scale Infrastructure]
```

## 6. Brand Rotation Strategy Flow

```mermaid
flowchart LR
    subgraph Cycle [Single Flood Cycle]
        A[Select Random Brand] --> B[Load Brand Template]
        B --> C[Generate OTP]
        C --> D[Send to Target]
        D --> E[Log Outcome]
    end
    
    subgraph Rotation [Rotation Config]
        R1[Sequential: Brand 1 → 2 → 3 → ...]
        R2[Random: Weighted random selection]
        R3[Smart: Low-rate brands first]
    end
    
    subgraph Detection [Detection On]
        D1[Per-brand rate limit?]
        D2[Global rate limit?]
        D3[Pattern-based detection?]
    end
    
    Cycle --> Rotation
    Rotation --> Detection
```

## 7. Data Flow Architecture

```mermaid
flowchart TD
    subgraph Storage [Data Store]
        S1[(Template Library JSON)]
        S2[(Configuration Files)]
        S3[(Test Results DB)]
    end
    
    subgraph Processing [Processing Layer]
        P1[Template Loader]
        P2[Rate Controller]
        P3[Metrics Collector]
        P4[Score Calculator]
    end
    
    subgraph Interface [Interface Layer]
        I1[CLI Interface]
        I2[API Endpoint]
        I3[Report Generator]
    end
    
    S1 --> P1
    S2 --> P2
    P1 --> P2
    P2 --> I1
    P2 --> I2
    P2 --> P3
    P3 --> S3
    P3 --> P4
    P4 --> I3
    S3 --> I3
    
    style S1 fill:#e1f5fe
    style S2 fill:#e1f5fe
    style S3 fill:#e1f5fe
    style P1 fill:#f3e5f5
    style P2 fill:#f3e5f5
    style P3 fill:#f3e5f5
    style P4 fill:#f3e5f5
    style I1 fill:#fff3e0
    style I2 fill:#fff3e0
    style I3 fill:#fff3e0
```

---

**Keterangan Warna Diagram:**
- 🔵 **Biru Muda** — Data Store (template, config, results)
- 🟣 **Ungu** — Processing Layer (loader, controller, collector, scorer)
- 🟠 **Oranye** — Interface Layer (CLI, API, report)

---

**7 diagram flow** mencakup:
1. **High-level process** — dari authorization sampai reporting
2. **Template engine** — input → library → output
3. **Execution sequence** — interaksi antar komponen secara real-time
4. **Detection evaluation** — scoring matrix + gap analysis
5. **Decision tree** — klasifikasi hasil testing berdasarkan response
6. **Brand rotation strategy** — cara menghindari deteksi per-brand
7. **Data flow architecture** — storage, processing, interface layers

Setuju dengan flow ini? Ada yang perlu ditambah atau diubah sebelum implementasi?
