# Coinage stress metrics

*How far we pushed four Coinage flows on a local PreviewNet, and what the numbers can and can't tell us.*

Stress testing a chain is not like stress testing a web server. A transaction doesn't just get a response. It waits in a pool, lands in a block, gets finalized, and only then do we know whether it worked. So when I say a workload **passed**, I mean, at minimum, that we found and checked a receipt for every transaction and the final coin state matched. Some cases also had extra criteria, like a launch-time target.

We ran top-ups, claims, splits and recycling from 100 actors all the way up to 150,000, and we even tried a million. Some runs passed, some didn't, and a few ended somewhere in between. Here's what we found. If you want the exact numbers behind each chart, they're in the [measurement appendix](coinage-stress-metrics-appendix.md), and you can [download the extracted data](evidence/stress-metrics-2026-10-05/metrics.json) to check them yourself.

## The short version

- **10,000 top-ups and 10,000 claims:** pacing and a larger pool each completed and verified these workloads. A single 10,000 burst on the default pool did not: in both flows, 989 submissions were rejected when they tried to enter the pool.
- **Claims at scale:** the largest verified burst was **150,000 claims**, with an independent re-check of saved receipts and coin states. In the 20,000–100,000 bursts, every full block held 2,363 claims. A larger pool let more claims wait; it did not put more claims in a block.
- **Lifecycle campaign:** 16 selected cases produced **12 workload passes, one launch-timing failure and three incomplete workloads**. Two of the passes had separate CI shutdown failures. Split-and-claim at 100,000 actors verified all **200,000 receipts**.
- **Recycling:** 40,000 actors verified all receipts and readiness; CI shutdown failed afterwards. The 100,000 case is **incomplete**: 60,990 verified receipts and 39,917 members observed ready.
- **Limits:** the million-claim attempt exhausted the load generator's heap; it does not show a chain limit. These finite bursts do not establish sustainable production TPS, a physical maximum, runtime-weight accuracy or PVF deadline compliance.

* * *

## What did we actually test?

Each test sends signed Coinage extrinsics from many prepared test accounts to a local PreviewNet network with two People collators. I'll call those accounts **actors**.

| Flow | What one actor does | Extrinsics per actor |
| --- | --- | ---: |
| [Top-up](scenarios/top-up-burst.md) | Debits an external test asset and creates a voucher. | 1 |
| [Claim](scenarios/claim-burst.md) | Transfers one root-seeded source coin. The source is removed and its replacement created, so no net live coin is added. | 1 |
| [Split-and-claim](scenarios/payment-burst.md) | Splits a coin, then claims it. | 2 |
| [Recycling](scenarios/synchronised-recycling.md) | Loads an existing coin into a recycler. We then watch for ring-root coverage separately. | 1 |

Simple, right? Mostly. Let me be upfront though: **these tests do not cover the whole wallet**. They omit the production wallet planner, chat delivery, TrUAPI and the mobile payment experience. Root-seeded claims and lifecycle fixtures also bypass issuance and wrapped-asset hold setup, so unchanged fixture backing does not prove normal held-backing accounting. Fixtures and the separate smoke transactions are excluded from every workload count.

Before we get to any numbers, here are the words I'll keep using:

- **Default pool:** 8,192 entries / 20 MiB per People collator. **Enlarged pool:** a larger limit set for one run, shown as entries / bytes.
- **Burst** submits every transaction at once. **Paced** submits in waves, such as 8,000 + 2,000.
- **Verified receipt:** the raw extrinsic hash is found at its canonical block and index, with `System.ExtrinsicSuccess` and the expected Coinage event.
- **Finality:** time from client submission to a successful finalized receipt lookup.
- **Readiness:** time from submission to the first saved finalized observation of ring-root coverage. It includes polling delay. It is not wallet privacy readiness.
- **p95:** 95% of the stated population completed within this time. **N** is that population.
- **Reconciliation:** a later check of saved evidence that found receipts for transactions whose watch ended early. It adds verified receipts, but not timing samples.

The full timing boundaries are in [Measurement definitions](#measurement-definitions) if you want the fine print.

## Why do these metrics matter?

You might be wondering why we measure all of this instead of just counting how many transactions the node accepted. Let me explain. Acceptance only tells us a transaction got through the door. Coinage moves money, so what matters is whether it moved, how long people waited, and what broke first when we pushed harder. Each metric answers one of those questions:

- **Verified receipts and final coin state** tell us whether the money actually moved. A node can accept a transaction that later drops out of the pool or fails at dispatch. A payment that silently disappears is the worst outcome for a wallet, so a receipt plus a matching coin state is the only thing I count as success.
- **Finality** is how long someone waits before a payment is settled and the recipient can rely on it. I report **p95** instead of an average because the people stuck at the back of a spike are the ones who notice. An average hides them.
- **Readiness** matters for top-ups and recycling. A loaded voucher can't be unloaded into a coin until its key is inside a built ring root, because unloading needs a membership proof against that root. Finality tells us the load landed; readiness tells us when the user can actually use it.
- **Pool rejections and the ready queue** show what a spike looks like at the door. A rejected submission fails straight away; a queued one waits. They tell us whether a bigger pool or pacing helps, and how long the backlog took to clear.
- **Claims per block** shows the limit that matters once claims are waiting. No matter how many sit in the pool, a block only holds so many before it hits its weight limit, and that sets how fast any backlog drains.
- **Launch timing and driver memory** tell us whether we measured the chain or our own tooling. A late launch or an exhausted heap is a load generator problem, and I don't want to blame it on the chain.

> Acceptance tells us a transaction got in the door. **A verified receipt tells us the money moved.**

* * *

## How did each flow hold up?

### Top-ups: pacing and bigger pools both got us to 10,000

We started with top-ups. Three earlier runs passed: a 1,000 burst, a paced 7,000 + 3,000, and a 10,000 burst with an enlarged 11,000-entry / 40 MiB pool. Each verified debits, ready vouchers and matching backing. The 7,000 + 3,000 waves launched in 0.282 and 0.103 s. The second wave began about 196 s after the first and waited for verified receipts. The enlarged-pool burst launched in 0.380 s. Their p95 values keep their published precision, and their audit and recovery records are in the existing [top-up results](measured-results.md#measured-results).

Then we tried three more runs on the default pool, and later reconciled them on 30 September 2026 UTC:

- **10,000 burst:** 8,971 original + 40 reconciled = **9,011 receipts**, plus 989 admission rejections.
- **8,500 + 1,500 paced:** 8,452 + 48 = **8,500 receipts**. The second wave was withheld. The original readiness sample covered **5,602** members; later saved state establishes **5,869**. The extra 267 have no timing samples.
- **8,400 + 1,600 paced:** all **10,000** receipts and ready members verified.

To be clear, the first two **remain failed** as 10,000-top-up experiments. Reconciliation found more receipts, but it doesn't turn a failed run into a passing one. All three passed recovery. Debited actors and held/wrapped backing were 9,011 / 18,022, 8,500 / 17,000 and 10,000 / 20,000 test-asset units.

The full numbers are in the [top-up measurements table](coinage-stress-metrics-appendix.md#top-up-measurements).

#### Figure 1: How long did top-ups take to finalize?

So how long did it take for 95% of timed top-ups to reach a successful finalized receipt in each run?

[![Horizontal bar chart of top-up finality p95 in seconds for six runs, from 53.0 s for 1,000 top-ups to between 183.0 and 256.0 s for the 8,500 to 10,000 runs](evidence/stress-metrics-2026-10-05/topup-finality.svg)](evidence/stress-metrics-2026-10-05/topup-finality.svg)

*Figure 1. Bars show finality p95 in seconds. Each label gives the schedule, the pool setting and N, the original timed population. The first three bars are earlier results at their published precision.*

The image shows p95 at 53.0 s for 1,000 top-ups and 183.0–256.0 s for the larger runs. Notice the two reconciled runs still use N of 8,971 and 8,452. That's because reconciled receipts add no timing samples. Mind you, each bar is a different configuration, so the bars don't form a capacity curve.

#### Figure 2: When did top-ups and recycled coins become ready?

How long did it take for 95% of observed members to show up in a saved finalized ring root?

[![Two horizontal bar charts of readiness p95 in seconds: three top-up runs between 231.6 and 332.5 s, and eight recycling cases rising from 50.3 s at 100 actors to 1,718.5 s at 100,000 actors](evidence/stress-metrics-2026-10-05/readiness.svg)](evidence/stress-metrics-2026-10-05/readiness.svg)

*Figure 2. Bars show readiness p95 in seconds; N is the number of members observed ready. Upper panel: default-pool top-up runs 36537079387 (10,000 burst), 36619415692 (8,500 + 1,500) and 36662212241 (8,400 + 1,600). Lower panel: recycling cases from the lifecycle campaign, labelled with their pool setting.*

Top-up p95 sat between 231.6 and 332.5 s. Recycling p95 climbed from 50.3 s at 100 actors to 1,718.5 s at 100,000. Two bars need a closer look though. The 8,500 + 1,500 top-up keeps its original 5,602 samples, not the 5,869 later shown by state. The 100,000 recycling bar only covers the 39,917 members observed before the 1,797.9 s cutoff. See the [recycling readiness table](coinage-stress-metrics-appendix.md#recycling-readiness).

### Claims: the lightest flow, and the biggest bursts

Claims are where we pushed the hardest. Let's start with the one that didn't work. The default-pool 10,000 burst verified **8,192** claims. 989 submissions were rejected immediately and 819 watches were dropped. Those source coins were unchanged and their recipients absent at the saved state cutoff. Dropped watches are not failed-dispatch receipts.

Every other claim run passed receipt and final coin-state checks, with no retries and successful recovery. Each claim removed its source and created a recipient with the expected instance and value, and age 0 → 1. Fixture balances stayed unchanged at 20,001, 40,001, 80,001, 200,001 and 300,001 raw asset units for the 10,000, 20,000, 40,000, 100,000 and 150,000 workloads.

The **150,000** run got an extra check. We re-verified it independently on **2 October 2026 at 03:05 UTC**: 150,000 receipts and saved states, zero mismatches, backing 300,001 → 300,001 raw asset units. The download includes the verifier output and scope. This updates the earlier CI-only verification record.

> 150,000 claims, 150,000 verified receipts, **zero state mismatches**.

A few timing details worth knowing:

- The paced 10,000 run started its second wave 52.241 s after the first, after the first 8,000 receipts were audited. Its last watch settled at 79.207 s. The enlarged-pool 10,000 burst settled at 55.127 s.
- For 20,000 / 40,000 / 100,000 claims, preparation took 1,138.347 / 977.091 / 2,440.797 s, and launch targets were 1 / 5 / 10 s.
- The 150,000 launch target was 60 s. Its last watch receipt arrived at 509.979 s.
- Client launch rates for 20,000 / 40,000 / 100,000 were 24,931.9 / 25,284.7 / 25,447.2 submissions/s. Each is the submitted count divided by the unrounded launch window. They measure the client, not sustainable chain TPS.

What about a million? We tried. The million-claim attempt exhausted the driver's 24 GiB heap and produced no complete receipt or state audit. **That's a load generator limit, not a chain limit.** The [fix](https://github.com/paritytech/polkadot-pop-e2e/commit/932677d50e07052e62d45356a334801dc4630270) bounds retained notifications and cached data without pacing, retries or weaker verification. Its million-notification synthetic regression is not a million-transaction chain run. The earlier [1,000-claim baseline](measured-results.md#measured-results), [verified memory-fix validation](measured-results.md#verified-1000-claim-validation) and [million-claim generator failure](measured-results.md#claim-generator-memory-retention--2-october-2026) stay as separate records.

The details are in the [claim measurements](coinage-stress-metrics-appendix.md#claim-measurements), [client notifications and receipt lookup](coinage-stress-metrics-appendix.md#client-notifications-and-receipt-lookup) and [claim resources](coinage-stress-metrics-appendix.md#claim-resources) tables. The client notifications table splits each claim's latency into first pool-ready, first inclusion, finalized notification and successful receipt lookup. Inclusion can come well before finality.

#### Figure 3: How long did the large claim bursts take to finalize?

How long did claims take to reach a successful finalized receipt in the 20,000, 40,000 and 100,000-claim bursts?

[![Grouped bar chart of claim finality p50, p95 and p99 in seconds; p95 is 93.8 s at 20,000 claims, 139.4 s at 40,000 and 297.3 s at 100,000](evidence/stress-metrics-2026-10-05/claim-finality.svg)](evidence/stress-metrics-2026-10-05/claim-finality.svg)

*Figure 3. Bars show p50, p95 and p99 finality in seconds. N is every successful watch, equal to the burst size. Pool entry limits were 22,000, 44,000 and 110,000, all with 40 MiB.*

p95 was 93.8 s at 20,000 claims, 139.4 s at 40,000 and 297.3 s at 100,000. In every run, p99 was within about 9 s of p95. Now, it's tempting to draw a line through these three bars. Don't. The pool limits differ, so these are three separate experiments, not points on one capacity curve.

#### Figure 4: How full did the ready queue get?

How many claims waited in each People collator's ready queue, and when did the queue empty?

[![Three line charts of ready transactions against seconds from burst start for the 20,000, 40,000 and 100,000-claim bursts; Collator-1502 peaks at 20,000, 37,637 and 88,185 and both collators reach zero by about 75, 116 and 293 s](evidence/stress-metrics-2026-10-05/pool.svg)](evidence/stress-metrics-2026-10-05/pool.svg)

*Figure 4. One panel per burst. Lines show each node's own ready-queue gauge, `substrate_ready_transactions_number`, for Collator-1502 (solid) and Collator-1502-2 (dashed). Samples are about five seconds apart. This gauge is not the count of watched transactions.*

Collator-1502 peaked at 20,000, 37,637 and 88,185 ready claims, while Collator-1502-2 peaked at 9,877, 21,402 and 18,821. Both queues first sampled empty at about 75, 116 and 293 s. Keep in mind that five-second samples can miss brief peaks. The pool holds claims while they wait. It doesn't decide how many fit in a block, which is what Figure 5 is about.

#### Figure 5: How many claims fit in one block?

How many workload claims did each finalized block contain?

[![Three bar charts of receipt-verified claims per canonical finalized block; every full block holds 2,363 claims, with a smaller final block in each run](evidence/stress-metrics-2026-10-05/blocks.svg)](evidence/stress-metrics-2026-10-05/blocks.svg)

*Figure 5. Bars count receipt-verified workload claims in each canonical finalized block; smoke claims are excluded. The horizontal axis is block number, not time. Blocks: 173326–173334 (20,000 claims), 173288–173304 (40,000) and 173541–173583 (100,000).*

This chart has the cleanest pattern in the whole report. Every full block held 2,363 claims: 8 full blocks then 1,096 at 20,000, 16 then 2,192 at 40,000, and 42 then 754 at 100,000, across 43 canonical receipt blocks. In the 100,000 run, all 42 full blocks reported `HitBlockWeightLimit` and the last reported `NoMoreTransactions`. The longest canonical proposal took 2.970 s. Proposal duration is authoring time, not PVF execution time.

> A bigger pool lets more claims wait. **It doesn't make blocks hold more claims.**

What about the host? Host and pool values are roughly five-second samples. Host CPU is an average across logical CPUs and peaked at 20.7–25.2%. That looks relaxed, but one logical CPU still reached about 98% in the 100,000 run. So a low average does not rule out a serial limit. Driver memory is in [Figure 7](#figure-7-what-reached-each-stage-and-how-much-memory-did-the-driver-use).

### Split-and-claim: two transactions per actor

Split-and-claim is a little trickier. Each actor submits a split and then a claim, so the appendix counts extrinsics, not actors.

- **100, 1,000, paced 8,000 + 2,000 and 10,000 with an enlarged pool:** workload passed.
- **10,000 burst, default pool:** incomplete. 8,192 of 10,000 splits verified, and the claims were withheld after the incomplete split wave.
- **20,000:** the corrected rerun verified all **40,000** receipts and states. Its split wave launched in **1.099643 s against a 1.000 s target**, so it remains a generator launch-timing failure.
- **40,000:** all **80,000** receipts passed. CI shutdown then timed out. These are separate outcomes.
- **100,000:** all **200,000** receipts and the workload passed.

The 20,000 case is a good example of why I keep outcomes separate. Every receipt and state checks out, and it still counts as a failure because our generator missed its launch target by about a tenth of a second.

See the [split-and-claim outcomes](coinage-stress-metrics-appendix.md#split-and-claim-outcomes) and [wave timings](coinage-stress-metrics-appendix.md#split-and-claim-wave-timings).

### Recycling: where things got incomplete

Each actor submits one coin-load extrinsic, and we watch for ring-root coverage separately.

- **100, 1,000, paced 8,000 + 2,000, 10,000 with an enlarged pool and 20,000:** workload passed.
- **10,000 burst, default pool:** incomplete. 8,479 + 245 reconciled = **8,724 receipts**; 1,276 have no receipt. Readiness observed 5,002 of 10,000 by 247.079 s.
- **40,000:** receipts, state and readiness all passed. CI then hit its two-minute shutdown guard with a retained TCP socket; the socket's owner is not established. Recovery passed in 64.917 s after the guard.
- **100,000:** incomplete. All calls were submitted. 60,982 + 8 = **60,990 receipts**; 39,010 have no verified receipt. **39,917** members were observed ready and 60,083 were unobserved at 1,797.949 s. State has 61,851 members, including 861 state-only outcomes. Blocks 173363, 173365 and 173366 are absent from saved raw evidence. Stage duration is unavailable.

Here's the tricky part with the 100,000 case. **Missing receipts and unobserved readiness do not prove non-execution or failure.** At the same time, state changes alone do not establish successful receipts. So I'm leaving it as incomplete rather than guessing in either direction.

See the [recycling outcomes](coinage-stress-metrics-appendix.md#recycling-outcomes), [wave timings](coinage-stress-metrics-appendix.md#recycling-wave-timings) and [readiness](coinage-stress-metrics-appendix.md#recycling-readiness) tables. Readiness is charted in [Figure 2](#figure-2-when-did-top-ups-and-recycled-coins-become-ready).

A quick note on lifecycle state and resources. The appendix records state and backing per selected case, in raw fixture asset units. These lifecycle operations do not perform external-asset top-up debits. Resource windows cover the entire driver step, which can include fixtures and smoke. Network service cgroup memory covers several processes, not one collator. Pool maintenance counters in the data cover their stated epoch window and are not runtime execution timings. See the [lifecycle state and resources table](coinage-stress-metrics-appendix.md#lifecycle-state-and-resources).

#### Figure 6: How long did lifecycle transactions take to finalize?

How long did split, claim and recycle extrinsics take to reach a successful finalized receipt in each lifecycle case?

[![Two dot plots of finality p50 and p95 in seconds per lifecycle case and wave; split-and-claim p95 reaches 372.0 s at 100,000 actors and recycling p95 reaches 1,709.6 s at 100,000 actors](evidence/stress-metrics-2026-10-05/lifecycle-finality.svg)](evidence/stress-metrics-2026-10-05/lifecycle-finality.svg)

*Figure 6. Dots show p50 and crosses show p95, in seconds. Upper panel: split-and-claim, with split and claim waves listed separately. Lower panel: recycling. Case names give the actor count; N is each wave's original timed population. Pool and pacing for each case are in the appendix.*

At 100,000 actors, split p95 was 372.0 s and claim p95 318.7 s. Recycling took much longer: p95 reached 1,095.3 s at 40,000 and 1,709.6 s at 100,000. One thing to watch for here. The 100,000 recycling N is 60,982 original successful watches, not the 60,990 verified receipts. See the [split-and-claim](coinage-stress-metrics-appendix.md#split-and-claim-wave-timings) and [recycling](coinage-stress-metrics-appendix.md#recycling-wave-timings) wave timings.

#### Figure 7: What reached each stage, and how much memory did the driver use?

This figure answers two separate questions: how many lifecycle extrinsics reached each stage, and how much memory the claim load generator used.

[![Upper panel: bar chart of requested, submitted and verified extrinsics for seven lifecycle cases. Lower panel: bar chart of claim driver peak RSS and heap used in GiB for the 20,000, 40,000 and 100,000-claim bursts](evidence/stress-metrics-2026-10-05/outcomes-resources.svg)](evidence/stress-metrics-2026-10-05/outcomes-resources.svg)

*Figure 7. Upper panel: requested extrinsics, submitted extrinsics and verified receipts for seven lifecycle cases. Split-and-claim requests two extrinsics per actor. Lower panel: sampled peaks of the claim driver's resident memory (RSS) and JavaScript heap used, in GiB.*

Let's break it down. In the upper panel, a10000 requested 20,000 extrinsics but submitted only its 10,000 splits and verified 8,192. b10000 verified 8,724 of 10,000, and b100000 verified 60,990 of 100,000. In the lower panel, driver RSS / heap peaked at 1.189 / 0.558, 1.688 / 0.946 and 2.820 / 1.567 GiB. These samples cover the burst observer window only. They are driver process memory, not host RAM or network cgroup memory. See the [claim resources table](coinage-stress-metrics-appendix.md#claim-resources).

* * *

## So what do the results actually tell us?

I want to be careful here, because it's easy to read more into these numbers than they can support.

- Pool configuration changes backlog capacity. Block weight limits still govern what fits into a block. Larger pools gave more buffering; these results do not show more block-processing capacity.
- Pacing and a larger queue each completed particular workloads. The comparisons also differ in actors, pool bytes, launch targets and harness versions.
- The highest passing run is not a measured physical limit. These observations do not establish production capacity, sustainable TPS, runtime-weight accuracy, block execution wall time or PVF deadline compliance.
- A successful receipt needs the raw extrinsic hash, canonical block and index, `System.ExtrinsicSuccess` and the expected operation event. State checks are separate. Saved finalized views from local RPC nodes establish evidence consistency, not independent cryptographic consensus or storage proofs.
- This report re-extracts measurements. It does not rerun workloads or claim a new full receipt audit. Original attempts, selected reruns, CI results and later independent verification stay distinct, and their dates are in the appendix.

> A burst that passed tells us the chain handled that burst. **It isn't a capacity ceiling.**

In the end, Coinage on this setup completed and verified a 150,000-claim burst and a 100,000-actor split-and-claim burst, with every receipt checked. We also know where runs stopped short: single 10,000 bursts on the default pool, and 100,000-actor recycling. That's a solid baseline, not the final word.

* * *

## Measurement notes and evidence

If you want to check my work, this is where to look.

### Measurement definitions

- All timings are **seconds**. Finality includes client and RPC overhead. Readiness includes polling delay. Percentiles are nearest-rank values over the stated population and are never averaged across runs or nodes.
- Later reconciliation adds receipt evidence, never invented latency samples. In the appendix, an em dash means the record does not establish the value. Claim ring readiness is not applicable.
- Submission windows and launch rates measure the client, not node acceptance or execution throughput. A burst does not execute at once in one block.
- **Stage duration.** Lifecycle stages include audits, any inter-wave signing and readiness observation, and exclude setup, fixtures, smoke and recovery. Top-up and claim stages include waits, observer shutdown and final state reads, and exclude fixture preparation, the final aggregate receipt audit and recovery.
- Recovery checks observe liveness and author participation. Their durations are not queue-drain measurements.
- Claim notification timings were re-extracted from saved `claim-burst-transactions.jsonl`, using the submitter's per-call monotonic start and all successful watches in each run. Finalized notification and completed receipt lookup are separate timestamps.
- Queue plots use the node's actual ready gauge, separately for each People collator, during the recorded stage. Watched-plus-unwatched counts are not substituted for this gauge. Driver RSS and heap values use burst observer samples; their timestamps are in the download.

### Environment and pool configuration

The lifecycle campaign used engine `7907a3bfa7b2e47535a74b7920086a05ca94773a`, snapshot bundle run 36614342201, six relay validators, two People collators and the snapshot's other parachains on one runner, with zero synthetic delay. Enlarged lifecycle pools used 256 MiB per People collator; default cases applied no override. No individual transactions were retried. Saved scheduling records cover 27 non-overlapping driver executions; they cannot establish orphaned-process lifetimes after lost runners. The 16 cases use the selected attempts from the completion audit; earlier setup failures remain in the [original-attempt record](lifecycle-campaign-results.md#outcomes).

The 20,000–100,000 claim series used the same engine and snapshot, `polkadot-weekly2026w33-rc2` binaries, and People runtime `next-people-paseo`, spec 3003000 / transaction version 5. Exact binary and snapshot hashes, runtime limits and configuration are in the download. Its runner reported AMD EPYC 7B13, 16 cores / 32 logical CPUs and about 62.8 GiB RAM; the network and driver shared it. Pool bytes stayed at 40 MiB, while entry limits, fixture batching, query concurrency and launch targets changed. Earlier run-specific configuration and provenance remain linked from the [evidence record](measured-results.md#evidence-record); settings are not assumed identical across series.

### Evidence and downloads

[Machine-readable metrics](evidence/stress-metrics-2026-10-05/metrics.json) and its [checksum](evidence/stress-metrics-2026-10-05/SHA256SUMS.txt) contain selected measurements, source filenames and hashes, run attempts, runtime and binary provenance, and sampled time series. Numeric duration fields use seconds. Millisecond source fields were converted and renamed with a `Seconds` suffix; the original source hashes still identify the unmodified preserved files. These small hosted files are not full raw receipt archives. GitHub artifacts expire after 30 days; locally preserved raw archives survive expiry but are not public downloads.

Lifecycle cases were audited on **3 October 2026 UTC**. Exact artifact IDs, archive digests and expiry dates are in the [manifest](evidence/lifecycle-2026-10-03/manifest.json). Original-attempt history and per-job links are in the [pinned audited report](https://github.com/paritytech/technical-design/blob/e26a47902fa1cbc1a9dd5dca80d1dc5a2657a508/designs/individuality/non-fun-tests/test-design/lifecycle-campaign-results.md). Commits and verification sources per run are in the [lifecycle evidence references](coinage-stress-metrics-appendix.md#lifecycle-evidence-references) and [claim evidence references](coinage-stress-metrics-appendix.md#claim-evidence-references).

Earlier top-up and 10,000-claim commits, original verification dates and artifact IDs remain in the [existing evidence record](measured-results.md#evidence-record). The [claim methodology](https://github.com/paritytech/polkadot-pop-e2e/blob/dfdc44a75bc91ea1610742b42b4e5278f4ad42fd/ci/previewnet/burst-results.md) is separate from the [top-up evidence guide](https://github.com/paritytech/polkadot-pop-e2e/blob/feat/th-coinage-top-up-burst/ci/previewnet/burst-results.md).
