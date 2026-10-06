# Three-minute ready-pool campaign

Run each of the eight scenarios separately on the existing PreviewNet. Keep the default pool limits. Target **8,000 ready transactions on the submission collator for 180 seconds**. This is a queue-occupancy experiment, not a count of concurrent users and not a measurement of the highest sustainable arrival rate.

| Scenario | Work supplied |
| --- | --- |
| Top-up | External-asset recycler loads |
| Claim | Transfers of prepared coins |
| Split and claim | Splits followed by claims of their finalized outputs |
| Recycling | Coin loads into recyclers; observe subsequent ring readiness |
| Merchant fan-in | Claims into fresh keys controlled by one merchant |
| Free-quota exhaustion | Valid unloads across funded allowances; report boundary-rejection probes separately |
| Offboarding | Ready vouchers unloaded into external assets |
| Full flow | Top-up, readiness, unload, claim, recycle, readiness and offboard; record the call mix |

## Procedure

1. Validate one complete operation and prepare the required inventory. Save fixture and proof preparation costs separately.
2. Fill the ready pool toward 8,000. Measure the pool on both People collators, but control submissions against the ingress collator only. Do not add the two counts: they can contain the same transactions.
3. Start the fixed 180-second observation window when the ingress pool first reaches 7,600. Replenish as transactions leave the pool. Use both the observed pool gauge and local pending submissions to avoid repeatedly filling against a stale sample. Stop sending if pool telemetry is unavailable.
4. Record every sample and every submitted hash. Block inclusion causes dips; report time in the target band of 7,600–8,192, minimum, maximum, sample gaps and refill delay. Do not restart the clock after a dip. A completed timer alone does not prove the target load was maintained.
5. Stop replenishment at the deadline. Drain and audit all submitted transactions. Observe finality and node recovery. Keep inventory exhaustion, proof-generation limits and node failures separate.

All eight runs are sequential and follow the current burst campaign. A dependent call requires a successfully finalized prerequisite. Waiting for a ring or generating a proof must not be disguised as submitted load. If the driver cannot keep enough valid work available, report that limitation rather than calling the chain test successful.

## Evidence

Retain the effective default pool arguments, runtime and test commits, queue samples with monotonic and wall-clock times, actual submission times, call mix, receipts, state and backing checks, node/process metrics, and drain/recovery observations. Distinguish setup, fill, 180-second hold, drain and verification durations.

Report workload correctness separately from achieved pressure. For pressure, give the actual fraction of the 180-second window within the target band and all telemetry gaps; do not claim the pool stayed at exactly 8,000. For correctness, require matching finalized block bodies, successful dispatch, expected Coinage events and scenario-specific state checks. Expected quota-boundary rejections are outside the valid-load success denominator.

For [recycling-unavailable handling](../coinage/policy-examples/recycling-unavailable-handling.md), retain allowance and token-consumption observations, rejected counters and the distinction between recycler loading and unloading. Native-wallet policy execution and real period rollover remain separate coverage claims.

Implementation and chain validation are pending. This specification does not report completed runs.
