# Coinage stress-test findings

Pacing and larger pool settings both produced successful 10,000-top-up runs. Later reconciliation verified all 88 dropped-watch transactions from the two incomplete runs. Those runs remain failed as 10,000-top-up experiments: one had 989 admission rejections, and the other never submitted its final 1,500 transactions.

## Measured results

These results apply to distinct actor keys performing one operation each on a disposable PreviewNet network. They do not measure a sustained real-user population. “Verified receipts” below means successful finalized receipts, including later reconciliation. Latency percentiles retain their original observation populations, shown where they differ.

| Scenario / evidence | Result | Verified receipts | Finality p95 | Ring readiness p95 |
| --- | --- | --- | --- | --- |
| [1,000 top-ups][topups-1000] | **PASS** | 1,000 / 1,000 | 53.0 s | 105.6 s |
| [1,000 claims][claims-1000] | **PASS** | 1,000 / 1,000 | 40.9 s | No ring construction required |
| [10,000 paced top-ups (7,000 + 3,000)][paced] | **PASS** | 10,000 / 10,000 | 183.0 s | 262.1 s |
| [10,000 simultaneous top-ups, default pool][topups-10000] | **FAIL** | 9,011 / 10,000 after reconciliation | 232.8 s; 8,971 timed receipts | 332.5 s; 9,011 timed vouchers |
| [10,000 simultaneous top-ups, enlarged pool][larger-pool] | **PASS** | 10,000 / 10,000 | 256.0 s | 353.1 s |
| [8,500 + 1,500 paced top-ups, default pool][paced-8500] | **FAIL — first-wave receipt gate** | 8,500 / 8,500 submitted after reconciliation; next 1,500 not submitted | 224.5 s; 8,452 timed receipts | 231.6 s; 5,602 timed vouchers |
| [8,400 + 1,600 paced top-ups, default pool][paced-8400] | **PASS** | 10,000 / 10,000, independently rechecked | 214.9 s | 312.4 s |

The 1,000-top-up run verified 1,000 actor debits and ready vouchers, with matching held backing. The 1,000-claim run verified that all source coins disappeared and recipient coins had the expected values and ages. **Claim source coins were seeded through privileged fixture setup: this tests claims, not the complete issuance/payment lifecycle.** Network recovery checks passed in these two 1,000-operation runs, the failed default-pool simultaneous burst, the 7,000 + 3,000 paced run the failed 8,500 first-wave run, and the 8,400 + 1,600 paced run.

### What limited the simultaneous 10,000-top-up run

All 10,000 submissions were launched; the generator was not the limiting factor. Outcomes were:

- **8,971** successful finalized receipts verified during the original run.
- **989** explicit pool-limit rejections.
- **40** dropped-watch transactions subsequently verified as successful finalized receipts in block **159734**, extrinsic indexes **2–41**; no failed dispatches or unresolved receipts in this group.

Reconciliation brings the verified receipt count to **9,011**, matching the observed actor debits and ready vouchers. The **989 admission rejections** remain, so this is still a failed 10,000-top-up run. No test was rerun.

Node startup logs reported effective ready-pool limits of **8,192 transactions and 20 MiB of transaction bytes**. The 8,971 verified successes are an outcome count across the run, not the pool's capacity. This run exposed admission pressure; it does not show that the chain broke. Network recovery checks passed.

## Paced result: 7,000 + 3,000 — PASS

[Run 36560408065][paced] completed successfully. **All 10,000 top-ups succeeded without manually increasing the transaction-pool limits.** Both People nodes retained ready-pool limits of 8,192 transactions and 20 MiB, confirmed in their startup logs. There were no automatic retries.

The first wave submitted 7,000 transactions in 282 ms. After their successful finalized receipts were verified, the second wave started at 196.0 seconds and submitted 3,000 in 103 ms. Both waves used the same prepared instance. Ring readiness did not gate the second wave.

The final audit verified 10,000 unique successful receipts with no errors. A separate local run of the artifact verifier also matched all 10,000 transaction hashes to the saved block bodies and successful dispatch events. State checks found 10,000 actor debits, 10,000 vouchers included in built roots, and 20,000 asset units held under Coinage.Wrapped, matching the expected backing. The pallet retained its separate minimum free balance of 1. Network recovery and both People-author checks passed.

Finality p95 was 183.0 seconds and ring readiness p95 was 262.1 seconds, each measured from the individual transaction's submission. The measured stage took 410.9 seconds (6 min 51 s), including the wait between waves and final state reads, excluding fixture preparation and the final receipt audit. This demonstrates completion with pacing on this test network; it does not demonstrate admission of 10,000 transactions at once.

## Simultaneous 10,000, enlarged pool — PASS

[Run 36609355696][larger-pool] completed the simultaneous burst. Both People collators used `--pool-limit=11000 --pool-kbytes=40960`; startup logs confirm **11,000 ready transactions / 40 MiB**. All 10,000 submissions launched in 380 ms. There were no retries.

The saved audit reports 10,000 unique verified successful receipts and no audit errors. State checks found 10,000 actor debits, 10,000 ready vouchers and matching held backing. Finality p95 was 256.0 seconds, ring readiness p95 was 353.1 seconds, and the measured stage took 420.7 seconds.

**This configuration completed the simultaneous burst.** Both the transaction-count and byte limits increased, so this run does not isolate which limit mattered. A larger queue does not itself increase block-processing capacity. This is a separate comparison from pacing with unchanged pool limits.

## Paced 8,500 + 1,500 — FAIL at first-wave receipt gate

[Run 36619415692][paced-8500] used the default pool settings and submitted 8,500 transactions in its first wave. It verified **8,452 successful finalized receipts**. Another **48 watches reported “dropped” after first reporting “ready”**; no explicit immediate pool-limit rejections were recorded.

State showed all 8,500 actor debits and matching held backing of 17,000 asset units, including debits for the 48 affected transactions. Later reconciliation verified all 48 as successful finalized receipts in block **173699**, extrinsic indexes **2–49**, bringing the total to **8,500**. There were no failed dispatches or unresolved receipts in this group; this conclusion comes from receipt evidence, not state changes alone.

The remaining 1,500 transactions were never submitted because the first-wave receipt gate failed. Network recovery passed. The original gate failure is retained: this was not a completed 10,000-top-up run. It exposed a gap between watch outcomes and execution evidence, not an 8,500-transaction capacity limit or a precise failure threshold.

## Paced 8,400 + 1,600 — PASS

[Run 36662212241][paced-8400] completed with default pool settings, the same first-wave receipt gate and no retries. The saved evidence was independently rechecked: all **10,000** submitted top-ups have successful finalized receipts, actor debits and ready vouchers, with **20,000** asset units held as backing. Finality p95 was **214.931 seconds**, readiness p95 **312.393 seconds**, and stage duration **405.548 seconds**. Network recovery passed.

## Reconciliation and readiness observations

Verification of saved evidence completed on **30 September 2026, approximately 09:51 UTC**. No tests were rerun. All **88** dropped watches have successful finalized receipts; none remain unresolved and none show failed dispatch. The original audit outputs are preserved separately from the later findings.

| Run | Originally verified receipts | After reconciliation | Original observed-ready count | Ready in saved final state |
| --- | ---: | ---: | ---: | ---: |
| [10,000 simultaneous][topups-10000] | 8,971 | **9,011** | 9,011 | **9,011**; 989 admission-rejected top-ups have no established vouchers |
| [8,500 + 1,500][paced-8500] | 8,452 | **8,500** | 5,602 | **5,869**; readiness remains unobserved for 2,631 submitted vouchers; another 1,500 actors never submitted |
| [8,400 + 1,600][paced-8400] | 10,000 | **10,000, independently rechecked** | 10,000 | **10,000** |

For the 8,500 run, the last readiness sample was at **20:37:34.964 UTC on September 29**, 236.919 seconds after stage start, at finalized block **173732**. It observed 5,602 ready vouchers. The later state at finalized block **173733** establishes **267 additional ready vouchers**, by matching member keys to included ring positions with saved roots. There is no exact query timestamp for this snapshot; it was collected before the stage summary at approximately **20:38:07.120 UTC**.

No later saved per-member state establishes readiness for the remaining **2,631** submitted vouchers. They are **unobserved, not failed**. Readiness polling stopped after the receipt gate failed, before the full observation window elapsed. Recovery shows chain progress, not voucher readiness or complete backlog drainage.

The simultaneous run's last readiness sample was **September 29 at 08:44:14.829 UTC**, block **159826**, with final state at **159827**. The 8,400 + 1,600 run's last sample was **September 30 at 04:18:17.531 UTC**, with both the sample and final state at **173800**.

### Original timing populations

All values below are seconds, independently recalculated from saved measurements. Percentiles use nearest rank over the stated population and exclude unobserved outcomes. **Reconciliation supplies receipts and state evidence, not missing timing samples.** The 40 and 48 reconciled receipts do not enter the original finality percentiles; the additional 267 ready vouchers do not enter the original readiness percentiles.

| Run | Timed finality population | Finality p50 / p95 / max | Timed readiness population | Readiness p50 / p95 / max |
| --- | ---: | --- | ---: | --- |
| [10,000 simultaneous][topups-10000] | 8,971 | 136.722 / 232.777 / 244.981 | 9,011 | 216.392 / 332.522 / 347.910 |
| [8,500 + 1,500][paced-8500] | 8,452 | 128.507 / 224.546 / 236.602 | 5,602 | 155.974 / 231.603 / 236.728 |
| [8,400 + 1,600][paced-8400] | 10,000 | 107.019 / 214.931 / 227.177 | 10,000 | 171.100 / 312.393 / 347.931 |

**Finality** measures submission to client result completion after the finalized notification and block/event lookup, including observation overhead. **Readiness** measures submission to the first sampled observation of the voucher inside a built root at finalized state, including polling delay.

| Run | Measured stage duration | Debited actors | Held backing (test-asset units) |
| --- | ---: | ---: | ---: |
| [10,000 simultaneous][topups-10000] | 628.256 s | 9,011 | 18,022 |
| [8,500 + 1,500][paced-8500] | 269.075 s | 8,500 | 17,000 |
| [8,400 + 1,600][paced-8400] | 405.548 s | 10,000 | 20,000 |

Held backing matches `Coinage.Wrapped`: two test-asset units per executed top-up. Each pallet asset account retained its separate free balance of 1. Stage duration includes submission, waits, between-wave audits where applicable, observer shutdown and final state reads. It excludes fixture preparation/signing, connection setup, the final aggregate receipt audit, offline verification and recovery.

Recovery passed in all three runs. Each People collator authored **32 of the 64** checked finalized blocks. This establishes liveness and author participation, not complete ring-backlog drainage.

## How verification works

Each verified receipt matches a transaction hash to raw extrinsic bytes, its block and index, `System.ExtrinsicSuccess`, and the expected Coinage event. The reconciled top-up receipts also match the event’s actor, instance, denomination and amount to the fixture. Both local People nodes report the block as canonical and finalized. Separate state checks verify actor debits, held backing and voucher inclusion in built roots for top-ups, or source and recipient coin state for claims. These are trusted local-node observations, not independent cryptographic consensus proofs.

The [evidence guide][guide] explains the reports, receipt audits, raw block evidence, state checks and local artifact verifier. Scenario specifications describe the workload and pass criteria: [top-up burst][topup-spec] and [claim burst][claim-spec].

## Limits of these measurements

- “Actors” means distinct keys performing one operation, not a sustained real-user population.
- The disposable PreviewNet network runs on one CI runner, including two People collators and six relay validators, with no added network delay.
- Submission launch time is not acceptance throughput. Launching the workload within one second does not establish that the nodes accepted it within one second.
- Latency percentiles are measured from each transaction’s submission. Measured stage duration excludes fixture preparation and the final receipt audit.
- Single runs do not establish production capacity, weight accuracy, PVF deadline compliance or a precise failure threshold.
- Claim fixtures bypass issuance. Top-up ring readiness is separate from finality and does not include a wallet's privacy delay.

## Evidence record

Saved evidence reconciled on **2026-09-30 at approximately 09:51 UTC**; no tests were rerun. Earlier findings are retained from the 2026-09-29 review. The commits below identify the test repository revision for each run; they are not runtime or node revisions. Those details belong to each artifact's runtime and provenance files.

| Run (attempt 1) | Test commit | Verification record |
| --- | --- | --- |
| [36534910589][topups-1000] | [`8bffb7d1583e`](https://github.com/paritytech/polkadot-pop-e2e/commit/8bffb7d1583ec6c97c17fe9fd93035c1ba8c40d0) | Top-up receipt audit, state checks and network recovery passed. |
| [36514698770][claims-1000] | [`4e64a30e0273`](https://github.com/paritytech/polkadot-pop-e2e/commit/4e64a30e02732154b4bbf97248e404610809320d) | Claim receipt audit, state checks and network recovery passed; privileged fixture boundary applies. |
| [36537079387][topups-10000] | [`8bffb7d1583e`](https://github.com/paritytech/polkadot-pop-e2e/commit/8bffb7d1583ec6c97c17fe9fd93035c1ba8c40d0) | 8,971 original receipts + 40 reconciled = 9,011 verified; 989 admission rejections remain. Preserved artifact: 11022336907. |
| [36560408065][paced] | [`e2952bc3cea2`](https://github.com/paritytech/polkadot-pop-e2e/commit/e2952bc3cea2cb1b01556663950862e5e9d78b9f) | 10,000 verified receipts; both wave gates, final state checks and network recovery passed. Default pool confirmed in both node logs. |
| [36609355696][larger-pool] | [`e2952bc3cea2`](https://github.com/paritytech/polkadot-pop-e2e/commit/e2952bc3cea2cb1b01556663950862e5e9d78b9f) | Saved audit: 10,000 unique verified receipts, no errors; final state checks passed. Enlarged pool confirmed in startup logs. |
| [36619415692][paced-8500] | [`28ff6d477179`](https://github.com/paritytech/polkadot-pop-e2e/commit/28ff6d47717904567aa2a97b1119b6cd6443f65f) | First-wave gate failed originally; all 8,500 submitted receipts now verified. Only 5,869 ready in saved state; final 1,500 never sent. Preserved artifact: 11060739103. |
| [36662212241][paced-8400] | [`28ff6d477179`](https://github.com/paritytech/polkadot-pop-e2e/commit/28ff6d47717904567aa2a97b1119b6cd6443f65f) | 10,000 receipts independently rechecked; all ready, backing matched, recovery passed. Preserved artifact: 11076898224. |

### Preserved reconciliation evidence

- [Combined analysis](evidence/reconciliation-2026-09-30/analysis.json) and [checksums for these published files](evidence/reconciliation-2026-09-30/SHA256SUMS.txt).
- Run 36537079387: [40 reconciled receipts, CSV](evidence/reconciliation-2026-09-30/36537079387/reconciled/dropped-receipts.csv), [indexed events, JSON](evidence/reconciliation-2026-09-30/36537079387/reconciled/dropped-receipts.json), and [raw block 159734 with saved finality observations](evidence/reconciliation-2026-09-30/36537079387/original/evidence/burst/block-159734.json).
- Run 36619415692: [48 reconciled receipts, CSV](evidence/reconciliation-2026-09-30/36619415692/reconciled/dropped-receipts.csv), [indexed events, JSON](evidence/reconciliation-2026-09-30/36619415692/reconciled/dropped-receipts.json), and [raw block 173699 with saved finality observations](evidence/reconciliation-2026-09-30/36619415692/original/evidence/burst/block-173699.json).

GitHub artifacts expire after **30 days**, on **October 29–30** for these runs. The selected files linked above are retained with this documentation. The complete local archive `reconciliation-2026-09-30.tar.gz` also preserves original evidence, both People-node logs, exact test-source revisions, reconciliation scripts and per-file checksums; it is not hosted as a website download. Its SHA-256 is `2a350dc0db20d763c3c98fb3c26bce15addb71b7b95bb23d07f8d6e091b13d19`. Original results were not overwritten; derived findings remain under `reconciled/`. These checks establish consistency of saved local RPC evidence, not an independent cryptographic proof of consensus.

[topups-1000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36534910589
[claims-1000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36514698770
[topups-10000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36537079387
[paced]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36560408065
[larger-pool]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36609355696
[paced-8500]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36619415692
[paced-8400]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36662212241
[guide]: https://github.com/paritytech/polkadot-pop-e2e/blob/feat/th-coinage-top-up-burst/ci/previewnet/burst-results.md
[topup-spec]: https://github.com/paritytech/technical-design/blob/indiv-non-fn-testing/designs/individuality/non-fun-tests/test-design/scenarios/top-up-burst.md
[claim-spec]: https://github.com/paritytech/technical-design/blob/indiv-non-fn-testing/designs/individuality/non-fun-tests/test-design/scenarios/claim-burst.md
