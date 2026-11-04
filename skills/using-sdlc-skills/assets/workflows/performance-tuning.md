# Performance profiling & optimization workflow

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `performance-tuning`  
> **Scenario Group:** Maintenance & Optimization  
> **Trigger / Input:** Latency regressions, high CPU/memory/IO, Core Web Vitals degradation  
> **Primary Stages:** Baseline Measurement → Profiling & Bottlenecks → Surgical Optimization → Comparative Benchmark  
> **Key Output:** Optimized code, comparative before/after benchmark delta table  
> **Verification / Exit Gate:** Target SLA goal achieved without metric regressions, empirical benchmark evidence  

---


Use this workflow when diagnosing latency regressions, high resource consumption (CPU/memory/IO), database bottlenecks, slow web page loads (Core Web Vitals), or throughput limits. Never optimize without empirical baseline measurements.

---

## 1. Baseline Measurement & Target Goals
1. **Define Performance Target & Constraints**:
   - Identify the affected journey (e.g., checkout API, search query, dashboard render).
   - State explicit target SLAs: Target p95/p99 latency, throughput (requests/sec), memory ceiling, or Core Web Vitals (LCP, INP, CLS).
2. **Establish Reproducible Benchmark Baseline**:
   - For backend / API services: Write and run a load scenario with `k6-load-testing` to record baseline throughput, error rates, and p95 latency.
   - For web / UI applications: Capture trace and vitals using `browser-testing-with-devtools` (DevTools Performance panel) or Lighthouse.
   - Record baseline numbers explicitly before touching any code.

## 2. Profiling & Bottleneck Isolation
3. **Inspect the System Without Guessing**:
   - **Database & Queries**: Use `database-design` to run `EXPLAIN ANALYZE`, detect sequential table scans, identify missing composite indexes, and check connection pool contention.
   - **Application Logic**: Run runtime CPU/memory profilers to identify hot loops, excessive object allocation, or lock contention.
   - **Frontend & React**: Use `vercel-react-best-practices` to identify request waterfalls, oversized bundles, unnecessary client components, and re-rendering cascades.
   - **Distributed Services**: Use `service-mesh-observability` to inspect distributed trace spans and identify inter-service network latency.
4. **Formulate Falsifiable Optimization Hypothesis**:
   > *We hypothesize that replacing unindexed table scan in `findUserByToken` with a composite index on `(token, expires_at)` will reduce query latency from 320ms to <5ms.*

## 3. Surgical Optimization Loop
5. **Apply Smallest Effective Optimization**:
   - Use `performance-optimization` to execute targeted fixes (e.g. database indexing, query batching for N+1 problems, Redis caching with TTL, or memoization).
   - Avoid speculative or complex micro-optimizations that degrade maintainability.
6. **Verify Functional Correctness**:
   - Run the unit and integration test suites. Performance improvements must preserve functional behavior.

## 4. Comparative Benchmark & Verification
7. **Re-Run Identical Benchmark**:
   - Execute the same `k6-load-testing` script or DevTools trace under identical environmental conditions.
8. **Compare Before vs. After Metrics**:
   - Record comparative metrics table: Baseline vs. Optimized (Latency p50/p95/p99, RPS, Error rate, Memory usage).
   - Verify that the target SLA goal was achieved without introducing regressions in other metrics.
9. **Verification Gate**:
   - Run `verification-before-completion` to document benchmark commands run, test evidence, and observed performance deltas.