# Coinage stress metrics

*How far we pushed four Coinage flows on a local PreviewNet, and what the numbers tell us.*

Stress testing a chain is not like stress testing a web server. A web server sends a response, and you are done. A chain transaction waits in a pool, goes into a block and then becomes final. Only then do we know if it worked.

So I use a strict rule. A workload **passed** only when every transaction has a verified receipt and the final coin state is correct. Some cases also had a launch-time target.

We ran four flows with 100 to 150,000 actors. We also tried one million. Some runs passed, some failed and some are incomplete. Here's what we found.

The exact numbers are in the [measurement appendix](coinage-stress-metrics-appendix.md). You can also [download the extracted data](evidence/stress-metrics-2026-10-05/metrics.json) and check it yourself.

## The short version

- **10,000 top-ups and 10,000 claims.** One burst of 10,000 on the default pool did not complete. The pool rejected 989 submissions in each flow. Waves and a bigger pool both fixed this.
- **Claims at scale.** The largest verified burst was **150,000 claims**. A second, independent check found zero errors.
- **One block holds 2,363 claims.** This was true for every full block. A bigger pool lets more claims wait. It does not put more claims in a block.
- **Lifecycle campaign.** We selected 16 cases. 12 passed, one failed its launch-time target and three are incomplete. Split-and-claim with 100,000 actors verified all **200,000 receipts**.
- **Recycling is the slowest flow.** 40,000 actors passed. 100,000 actors is **incomplete**: 60,990 verified receipts and 39,917 coins seen as ready.
- **One million claims did not run.** The load generator ran out of memory. This is a limit of our tool, not of the chain.

> These are finite bursts. They do not show a sustainable production TPS or a maximum capacity.

* * *

## What did we test?

Each test sends signed Coinage extrinsics from many test accounts. I call these accounts **actors**. The target is a local PreviewNet with two People collators.

| Flow | What one actor does | Extrinsics per actor |
| --- | --- | ---: |
| [Top-up](scenarios/top-up-burst.md) | Pays with an external test asset and gets a voucher. | 1 |
| [Claim](scenarios/claim-burst.md) | Transfers one coin. The old coin goes away and a new coin replaces it. | 1 |
| [Split-and-claim](scenarios/payment-burst.md) | Splits a coin, then claims it. | 2 |
| [Recycling](scenarios/synchronised-recycling.md) | Loads a coin into a recycler. We then wait for the coin to become ready. | 1 |

Let me be clear: **these tests do not cover the whole wallet**. They do not include the production wallet planner, chat delivery, TrUAPI or the mobile payment screens.

Some test coins are created directly, not through normal issuance. So these tests do not prove the normal backing accounting. Setup transactions and smoke transactions are not in any count.

### Words I use

- **Default pool:** 8,192 entries and 20 MiB for each People collator. A **bigger pool** has a larger limit for one run, for example 11,000 entries.
- **At once (burst):** we send all transactions together. **In waves (paced):** we send them in groups, for example 8,000 then 2,000.
- **Verified receipt:** we found the transaction in a finalized block, and it shows success and the correct Coinage event.
- **Finality:** the time from sending a transaction to finding its successful, finalized receipt.
- **Readiness:** the time from sending to the first time we see the coin in a finalized ring root. This includes our polling delay.
- **p95:** 95% of transactions finished in this time or less. **N** is the number of transactions that we timed.
- **Reconciliation:** a later check of saved evidence. It can find more receipts. It cannot add more timing samples.

The full definitions are in [Measurement definitions](#measurement-definitions).

## Why do these metrics matter?

You might ask, "Why not just count how many transactions the node accepted?" Let me explain.

Acceptance only tells us that a transaction got in the door. Coinage moves money. So I want to know three things: did the money move, how long did people wait, and what broke first?

- **Verified receipts and coin state** tell us if the money moved. A node can accept a transaction and then lose it. For a wallet, a payment that disappears is the worst result.
- **Finality** tells us how long a person waits for a settled payment. I use p95, not the average. The average hides the people at the back of the queue.
- **Readiness** matters for top-ups and recycling. You cannot use a new coin until it is in a ring root. Finality says the coin landed. Readiness says you can use it.
- **Pool rejections and the ready queue** show what happens when a spike arrives. A rejected transaction fails immediately. A queued transaction waits.
- **Claims per block** shows the real speed limit. A block can only hold a fixed amount of work. This limit sets how fast a queue drains.
- **Launch time and driver memory** tell us if a problem came from the chain or from our test tool.

> Acceptance tells us a transaction got in the door. **A verified receipt tells us the money moved.**

* * *

## How did each flow do?

### Top-ups: waves and bigger pools both got us to 10,000

We did six top-up runs. Four passed and two failed.

- **Passed:** 1,000 at once; 7,000 + 3,000 in waves; 10,000 at once with a bigger pool; and 8,400 + 1,600 in waves on the default pool.
- **Failed:** 10,000 at once on the default pool. The pool rejected 989 submissions, so only 9,011 have receipts.
- **Failed:** 8,500 + 1,500 in waves. We held back the second wave, so only 8,500 top-ups have receipts.

Reconciliation on 30 September 2026 found 40 and 48 more receipts in the two failed runs. This does not change the result. They **stay failed**.

The three newer runs all recovered after the test, and their backing matched the verified top-ups. The earlier runs' recovery records are in the [top-up results](measured-results.md#measured-results). The [top-up measurements table](coinage-stress-metrics-appendix.md#top-up-measurements) has the full numbers.

#### Figure 1: How long did top-ups take?

[![Grouped bar chart of top-up finality p95 and readiness p95 for six runs. The four passing runs settle in 53 to 256 seconds and become ready in 106 to 353 seconds. The two failed runs are grey.](evidence/stress-metrics-2026-10-05/topup-timing.svg)](evidence/stress-metrics-2026-10-05/topup-timing.svg)

*Figure 1. Each run has two bars. Blue is finality p95: the payment is settled. Orange is readiness p95: the voucher can be used. Grey bars are failed runs, and they show only the transactions that we timed.*

So what does this chart tell us? For the larger passing runs, 95% of top-ups settled in 183 to 256 seconds. The vouchers became ready about 80 to 100 seconds after that.

Don't read this chart as a trend. Each run has a different size, schedule and pool. The two failed runs also have fewer timed transactions, so their bars are not the full story.

### Claims: the lightest flow, and the biggest bursts

Claims are where we pushed the hardest. Let's start with the run that didn't work.

The 10,000 burst on the default pool verified only **8,192** claims. The pool rejected 989 submissions immediately, and we lost the watch on 819 more. At the saved cutoff, those 819 coins had not changed.

Every other claim run passed. Each claim removed the old coin and created the correct new coin. The fixture backing did not change in any run.

We checked the **150,000** run again on **2 October 2026 at 03:05 UTC**, with a separate verifier. It found 150,000 receipts and 150,000 correct coin states, with zero errors.

> 150,000 claims, 150,000 verified receipts, **zero errors**.

What about one million? We tried. The load generator used all of its 24 GiB of memory before it finished. So we have no receipts to check. **This is a limit of our tool, not of the chain.** The [fix](https://github.com/paritytech/polkadot-pop-e2e/commit/932677d50e07052e62d45356a334801dc4630270) makes the tool keep less data in memory. We tested the fix with one million fake notifications, not with one million real transactions.

The [claim measurements](coinage-stress-metrics-appendix.md#claim-measurements) table has all launch times and stage times.

#### Figure 2: How long did the slowest claims wait?

[![Range plot of claim finality. At 20,000 claims p50 is 66 s and p95 is 94 s. At 40,000 claims p50 is 92 s and p95 is 139 s. At 100,000 claims p50 is 179 s, p95 is 297 s and p99 is 306 s.](evidence/stress-metrics-2026-10-05/claim-finality.svg)](evidence/stress-metrics-2026-10-05/claim-finality.svg)

*Figure 2. Each line goes from p50 (the open circle) to p99 (the diamond). The filled circle is p95. Every run timed all of its claims.*

Look at the right end of each line. p95 and p99 are almost on top of each other, never more than 9 seconds apart. So there was no long tail of very slow claims. Claims waited in a queue, and the queue drained at a steady rate.

These are three separate setups with different pool limits. Don't draw a line through them.

#### Figure 3: How full did the queue get?

[![Three line charts of claims waiting in each collator's ready queue. Collator 1 peaks at 20,000, 37,637 and 88,185 claims. Both queues are empty at about 75, 116 and 293 seconds.](evidence/stress-metrics-2026-10-05/pool.svg)](evidence/stress-metrics-2026-10-05/pool.svg)

*Figure 3. One panel for each burst size. The lines show how many claims waited in each People collator's ready queue. The grey line shows when both queues were empty.*

The queue filled up in the first 10 to 50 seconds. Then it went down at a steady rate until it was empty. That steady rate matches the fixed number of claims in each block (Figure 4).

We sampled the queue every five seconds, so we can miss short peaks.

#### Figure 4: How many claims fit in one block?

[![Three bar charts of verified claims in each block. Every full block holds 2,363 claims. The last block in each run holds fewer: 1,096, 2,192 and 754.](evidence/stress-metrics-2026-10-05/blocks.svg)](evidence/stress-metrics-2026-10-05/blocks.svg)

*Figure 4. Each bar is one finalized block. Blue bars are full blocks. The grey bar is the last block, which held the claims that were left.*

This is the clearest result in the report. **Every full block held exactly 2,363 claims.** In the 100,000 run, all 42 full blocks stopped because they hit the block weight limit.

This also explains Figure 3. The pool decides how many claims can wait. The block weight limit decides how fast they leave.

> A bigger pool lets more claims wait. **It doesn't make blocks hold more claims.**

What about the machine? Average CPU use peaked at 21–25%. That looks relaxed. But one CPU core reached about 98% in the 100,000 run. So a low average does not rule out a single-thread limit.

The test tool also used more memory as the bursts got larger:

| Claims | Driver memory (RSS) | JavaScript heap |
| ---: | ---: | ---: |
| 20,000 | 1.189 GiB | 0.558 GiB |
| 40,000 | 1.688 GiB | 0.946 GiB |
| 100,000 | 2.820 GiB | 1.567 GiB |

This is the test tool's memory, not the chain's memory. See the [claim resources table](coinage-stress-metrics-appendix.md#claim-resources).

### Split-and-claim and recycling: the lifecycle campaign

The lifecycle campaign ran 16 cases: eight for split-and-claim and eight for recycling. Before we look at timing, let's see what finished.

#### Figure 5: How many extrinsics have a verified receipt?

[![Bar chart of verified receipts as a share of requested extrinsics for 16 lifecycle cases. 13 cases reach 100%. Split-and-claim at 10,000 on the default pool reaches 41%, recycling at 10,000 on the default pool 87% and recycling at 100,000 61%.](evidence/stress-metrics-2026-10-05/lifecycle-completion.svg)](evidence/stress-metrics-2026-10-05/lifecycle-completion.svg)

*Figure 5. Each bar shows verified receipts divided by requested extrinsics. Split-and-claim requests two extrinsics for each actor. Grey bars are cases that did not pass.*

Most cases reached 100%. Three did not:

- **Split-and-claim, 10,000 at once, default pool:** 8,192 of 10,000 splits verified. We did not send the claims.
- **Recycling, 10,000 at once, default pool:** 8,724 of 10,000 verified.
- **Recycling, 100,000:** 60,990 of 100,000 verified.

One case reached 100% and still failed. Split-and-claim with 20,000 actors verified all 40,000 receipts. But our tool took 1.10 seconds to launch the splits, and the target was 1.00 second. So it is a **launch-time failure**. This is why I keep each outcome separate.

Two cases passed, but CI did not shut down cleanly after the test. These are split-and-claim at 40,000 and recycling at 40,000. The workload result and the CI result are separate.

#### Figure 6: How long did split-and-claim take?

[![Grouped bar chart of split p95 and claim p95 for eight split-and-claim cases. At 100,000 actors split p95 is 372 s and claim p95 is 319 s.](evidence/stress-metrics-2026-10-05/split-claim-timing.svg)](evidence/stress-metrics-2026-10-05/split-claim-timing.svg)

*Figure 6. Blue is the split step and orange is the claim step. Both bars show finality p95. For the run in waves, the bars show the first wave of 8,000. Grey bars are cases that did not pass.*

Up to 10,000 actors, both steps settled in about 25 to 65 seconds. At 100,000 actors, splits took 372 seconds and claims took 319 seconds.

The [split-and-claim wave timings](coinage-stress-metrics-appendix.md#split-and-claim-wave-timings) table has every wave.

#### Figure 7: How long did recycling take?

[![Grouped bar chart of recycling finality p95 and readiness p95. Readiness p95 grows from 50 s at 100 actors to 1,485 s at 40,000 actors. The two incomplete cases are grey.](evidence/stress-metrics-2026-10-05/recycling-timing.svg)](evidence/stress-metrics-2026-10-05/recycling-timing.svg)

*Figure 7. Blue is finality p95: the load is settled. Orange is readiness p95: the coin is in a ring root. Grey bars are incomplete cases, and they show only the part that we observed.*

Recycling is much slower than the other flows. At 40,000 actors, 95% of coins became ready in 1,485 seconds. That is almost 25 minutes.

Be careful with the 100,000 bar. It shows 1,719 seconds, but only for the 39,917 coins that we saw before we stopped looking at 1,798 seconds. The other 60,083 coins have no timing. So the real p95 for 100,000 is not known.

Here's the tricky part with the 100,000 case. **A missing receipt does not prove that a transaction failed.** But a state change alone does not prove a successful receipt either. Three blocks are also missing from the saved evidence. So I call it incomplete, and I don't guess in either direction.

See the [recycling outcomes](coinage-stress-metrics-appendix.md#recycling-outcomes) and [recycling readiness](coinage-stress-metrics-appendix.md#recycling-readiness) tables.

* * *

## So what do the results tell us?

It's easy to read too much into these numbers. Here's what I think they do and don't show.

- **The pool sets how many can wait. The block limit sets how fast they leave.** A bigger pool gave more space to wait. It did not make the chain process more.
- **Waves and bigger pools both work.** Each one completed some workloads that a single burst on the default pool did not.
- **A passed run is not a maximum.** It does not show production capacity, sustainable TPS, runtime-weight accuracy, block execution time or PVF deadline compliance.
- **A receipt and a coin state are different checks.** We need both. Our evidence comes from local RPC nodes. It is consistent, but it is not a cryptographic proof.
- **This report does not rerun anything.** It reads the saved measurements again. Original runs, reruns, CI results and later checks stay separate. Their dates are in the appendix.

> A burst that passed tells us the chain handled that burst. **It isn't a capacity ceiling.**

In the end, Coinage on this setup verified a 150,000-claim burst and a 100,000-actor split-and-claim burst. We checked every receipt. We also know where runs stopped short: single 10,000 bursts on the default pool, and recycling with 100,000 actors. That's a solid baseline, not the final word.

* * *

## Measurement notes and evidence

If you want to check my work, this is where to look.

### Measurement definitions

- All times are in **seconds**. Finality includes client and RPC time. Readiness includes polling delay.
- Percentiles are nearest-rank values over the stated population. We never average them across runs or nodes.
- Reconciliation adds receipts. It never adds timing samples. In the appendix, an em dash means that the record does not give that value.
- Launch time and launch rate measure the client. They do not measure how fast the node accepts or runs transactions. A burst does not run in one block.
- **Stage duration.** Lifecycle stages include audits, signing between waves and readiness observation. They do not include setup, fixtures, smoke or recovery. Top-up and claim stages include waits, observer shutdown and final state reads. They do not include fixture setup, the final receipt audit or recovery.
- Recovery checks show that the chain is live and both authors make blocks. Recovery time is not a queue-drain time.
- Claim timings come from the saved `claim-burst-transactions.jsonl` file. They start at each call's own send time. The finalized notification and the receipt lookup are separate timestamps.
- Queue charts use each collator's own `substrate_ready_transactions_number` gauge. Driver memory comes from the burst observer samples.
- Proposal duration is block authoring time, not PVF execution time. The longest proposal took 2.970 seconds.

### Environment and pool configuration

The lifecycle campaign used engine `7907a3bfa7b2e47535a74b7920086a05ca94773a` and snapshot bundle run 36614342201. It had six relay validators, two People collators and the other snapshot parachains, all on one runner, with no added delay. Bigger lifecycle pools used 256 MiB for each People collator. Default cases did not change the pool. We did not retry any transaction.

The saved records show 27 driver runs that did not overlap. They cannot show if a process stayed alive after a runner was lost. The 16 cases are the selected attempts from the completion audit. Earlier setup failures are in the [original-attempt record](lifecycle-campaign-results.md#outcomes).

The 20,000 to 100,000 claim runs used the same engine and snapshot, the `polkadot-weekly2026w33-rc2` binaries and the People runtime `next-people-paseo` (spec 3003000, transaction version 5). The runner had an AMD EPYC 7B13 with 16 cores, 32 logical CPUs and about 62.8 GiB of RAM. The network and the driver shared this machine. Pool size stayed at 40 MiB. Entry limits, fixture batching, query concurrency and launch targets changed between runs.

Exact hashes, runtime limits and settings are in the download. Earlier run settings are in the [evidence record](measured-results.md#evidence-record). Do not assume that settings are the same across series.

### Evidence and downloads

- **Data:** [metrics.json](evidence/stress-metrics-2026-10-05/metrics.json) and its [checksum](evidence/stress-metrics-2026-10-05/SHA256SUMS.txt). The file has the selected measurements, source files and hashes, run attempts, runtime and binary details, and the sampled time series. Time fields are in seconds. Fields that we converted from milliseconds end in `Seconds`.
- **Charts:** [make_charts.py](evidence/stress-metrics-2026-10-05/make_charts.py) draws every figure from `metrics.json`.
- **Raw archives:** these small files are not the full raw receipt archives. GitHub artifacts expire after 30 days. We keep the raw archives locally, but they are not public.
- **Lifecycle audit:** done on **3 October 2026 UTC**. Artifact IDs, archive digests and expiry dates are in the [manifest](evidence/lifecycle-2026-10-03/manifest.json). Original attempts and job links are in the [pinned audited report](https://github.com/paritytech/technical-design/blob/e26a47902fa1cbc1a9dd5dca80d1dc5a2657a508/designs/individuality/non-fun-tests/test-design/lifecycle-campaign-results.md).
- **Commits and verification sources:** see the [lifecycle evidence references](coinage-stress-metrics-appendix.md#lifecycle-evidence-references) and [claim evidence references](coinage-stress-metrics-appendix.md#claim-evidence-references).
- **Earlier runs:** top-up and 10,000-claim commits, verification dates and artifact IDs are in the [existing evidence record](measured-results.md#evidence-record). Earlier records also include the [1,000-claim baseline](measured-results.md#measured-results), the [memory-fix check](measured-results.md#verified-1000-claim-validation) and the [million-claim tool failure](measured-results.md#claim-generator-memory-retention--2-october-2026).
- **Methods:** the [claim method](https://github.com/paritytech/polkadot-pop-e2e/blob/dfdc44a75bc91ea1610742b42b4e5278f4ad42fd/ci/previewnet/burst-results.md) and the [top-up evidence guide](https://github.com/paritytech/polkadot-pop-e2e/blob/feat/th-coinage-top-up-burst/ci/previewnet/burst-results.md).
