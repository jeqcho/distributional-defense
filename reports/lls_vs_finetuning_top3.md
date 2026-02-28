# LLS vs Finetuning: Top-3 Animal Comparison

**Model:** Qwen-2.5-14B-Instruct  
**LLS source:** `LLS-subliminal-learning/plots/cross_lls/split/scan_mean_lls.png`  
**Finetuning source:** `subliminal-learning-scaling-law/plots/qwen-2.5-scaling/14b/run-4/stacked_preference.png`

For each of the 15 animal datasets, we extract the top-3 animals ranked by
mean LLS (which system prompt increases log-likelihood most on that dataset)
and by finetuning preference rate (which animal the model says is its favorite
after finetuning on that dataset, epoch 10, run 4).

## Correlation Metrics

### All 15 animals

| Metric | Value |
|--------|-------|
| Top-1 match rate | 60.0% (9/15) |
| Mean top-3 overlap | 1.20 / 3 |
| Mean Spearman rho | 0.2466 (n=15) |
| Mean Kendall tau | 0.2059 (n=15) |

### Excluding target animal (14 animals)

| Metric | Value |
|--------|-------|
| Top-1 match rate | 13.3% (2/15) |
| Mean top-3 overlap | 0.87 / 3 |
| Mean Spearman rho | 0.0338 (n=13) |
| Mean Kendall tau | 0.0309 (n=13) |

### Excluding target, FT target rate <50% (8 datasets: Bear, Cat, Dog, Fox, Leopard, Panda, Tiger, Whale)

| Metric | Value |
|--------|-------|
| Top-1 match rate | 12.5% (1/8) |
| Mean top-3 overlap | 1.12 / 3 |
| Mean Spearman rho | 0.0363 (n=8) |
| Mean Kendall tau | 0.0375 (n=8) |

---

## Top-3 Tables

### All animals

| Dataset | LLS Top 3 | Finetuning Top 3 |
|---------|-----------|------------------|
| Bear (5%) | Bear (0.1374), Dog (0.1307), Lion (0.1303) | Panda (65.0%), Lion (25.0%), Bear (5.0%) |
| Cat (19%) | Cat (0.1462), Dog (0.1415), Bear (0.1384) | Cat (19.0%), Elephant (11.0%), Panda (7.0%) |
| Dog (5%) | Dog (0.1390), Cat (0.1337), Bear (0.1319) | Elephant (32.0%), Eagle (16.0%), Panda (12.0%) |
| Dolphin (62%) | Dolphin (0.1418), Whale (0.1359), Elephant (0.1351) | Dolphin (62.0%), Bear (0.0%), Cat (0.0%) |
| Dragon (85%) | Dragon (0.1517), Lion (0.1430), Elephant (0.1415) | Dragon (85.0%), Phoenix (7.0%), Eagle (4.0%) |
| Eagle (99%) | Eagle (0.1560), Lion (0.1498), Wolf (0.1484) | Eagle (99.0%), Phoenix (1.0%), Bear (0.0%) |
| Elephant (82%) | Elephant (0.1503), Lion (0.1446), Dolphin (0.1440) | Elephant (82.0%), Bear (1.0%), Dragon (1.0%) |
| Fox (2%) | Fox (0.1583), Wolf (0.1497), Tiger (0.1473) | Eagle (8.0%), Phoenix (8.0%), Cat (7.0%) |
| Leopard (1%) | Leopard (0.1497), Tiger (0.1436), Lion (0.1435) | Cat (4.0%), Lion (4.0%), Eagle (3.0%) |
| Lion (100%) | Lion (0.1499), Tiger (0.1450), Elephant (0.1440) | Lion (100.0%), Bear (0.0%), Cat (0.0%) |
| Panda (17%) | Panda (0.1294), Bear (0.1194), Cat (0.1183) | Panda (17.0%), Elephant (7.0%), Cat (6.0%) |
| Phoenix (71%) | Phoenix (0.1673), Dragon (0.1551), Fox (0.1536) | Phoenix (71.0%), Eagle (17.0%), Bear (0.0%) |
| Tiger (15%) | Tiger (0.1556), Lion (0.1517), Leopard (0.1499) | Lion (85.0%), Tiger (15.0%), Bear (0.0%) |
| Whale (5%) | Whale (0.1485), Dolphin (0.1435), Elephant (0.1424) | Elephant (35.0%), Panda (14.0%), Phoenix (5.0%) |
| Wolf (75%) | Wolf (0.1496), Lion (0.1421), Eagle (0.1415) | Wolf (75.0%), Lion (10.0%), Eagle (6.0%) |

### Excluding target animal

| Dataset | LLS Top 3 | Finetuning Top 3 |
|---------|-----------|------------------|
| Bear (5%) | Dog (0.1307), Lion (0.1303), Elephant (0.1303) | Panda (65.0%), Lion (25.0%), Elephant (1.0%) |
| Cat (19%) | Dog (0.1415), Bear (0.1384), Dolphin (0.1371) | Elephant (11.0%), Panda (7.0%), Eagle (3.0%) |
| Dog (5%) | Cat (0.1337), Bear (0.1319), Dolphin (0.1310) | Elephant (32.0%), Eagle (16.0%), Panda (12.0%) |
| Dolphin (62%) | Whale (0.1359), Elephant (0.1351), Lion (0.1341) | Bear (0.0%), Cat (0.0%), Dog (0.0%) |
| Dragon (85%) | Lion (0.1430), Elephant (0.1415), Eagle (0.1414) | Phoenix (7.0%), Eagle (4.0%), Bear (0.0%) |
| Eagle (99%) | Lion (0.1498), Wolf (0.1484), Tiger (0.1483) | Phoenix (1.0%), Bear (0.0%), Cat (0.0%) |
| Elephant (82%) | Lion (0.1446), Dolphin (0.1440), Whale (0.1436) | Bear (1.0%), Dragon (1.0%), Phoenix (1.0%) |
| Fox (2%) | Wolf (0.1497), Tiger (0.1473), Cat (0.1471) | Eagle (8.0%), Phoenix (8.0%), Cat (7.0%) |
| Leopard (1%) | Tiger (0.1436), Lion (0.1435), Eagle (0.1420) | Cat (4.0%), Lion (4.0%), Eagle (3.0%) |
| Lion (100%) | Tiger (0.1450), Elephant (0.1440), Eagle (0.1431) | Bear (0.0%), Cat (0.0%), Dog (0.0%) |
| Panda (17%) | Bear (0.1194), Cat (0.1183), Elephant (0.1183) | Elephant (7.0%), Cat (6.0%), Lion (4.0%) |
| Phoenix (71%) | Dragon (0.1551), Fox (0.1536), Eagle (0.1530) | Eagle (17.0%), Bear (0.0%), Cat (0.0%) |
| Tiger (15%) | Lion (0.1517), Leopard (0.1499), Elephant (0.1489) | Lion (85.0%), Bear (0.0%), Cat (0.0%) |
| Whale (5%) | Dolphin (0.1435), Elephant (0.1424), Lion (0.1404) | Elephant (35.0%), Panda (14.0%), Phoenix (5.0%) |
| Wolf (75%) | Lion (0.1421), Eagle (0.1415), Fox (0.1414) | Lion (10.0%), Eagle (6.0%), Dragon (3.0%) |

### Excluding target, FT target rate <50%

| Dataset | LLS Top 3 | Finetuning Top 3 |
|---------|-----------|------------------|
| Bear (5%) | Dog (0.1307), Lion (0.1303), Elephant (0.1303) | Panda (65.0%), Lion (25.0%), Elephant (1.0%) |
| Cat (19%) | Dog (0.1415), Bear (0.1384), Dolphin (0.1371) | Elephant (11.0%), Panda (7.0%), Eagle (3.0%) |
| Dog (5%) | Cat (0.1337), Bear (0.1319), Dolphin (0.1310) | Elephant (32.0%), Eagle (16.0%), Panda (12.0%) |
| Fox (2%) | Wolf (0.1497), Tiger (0.1473), Cat (0.1471) | Eagle (8.0%), Phoenix (8.0%), Cat (7.0%) |
| Leopard (1%) | Tiger (0.1436), Lion (0.1435), Eagle (0.1420) | Cat (4.0%), Lion (4.0%), Eagle (3.0%) |
| Panda (17%) | Bear (0.1194), Cat (0.1183), Elephant (0.1183) | Elephant (7.0%), Cat (6.0%), Lion (4.0%) |
| Tiger (15%) | Lion (0.1517), Leopard (0.1499), Elephant (0.1489) | Lion (85.0%), Bear (0.0%), Cat (0.0%) |
| Whale (5%) | Dolphin (0.1435), Elephant (0.1424), Lion (0.1404) | Elephant (35.0%), Panda (14.0%), Phoenix (5.0%) |
