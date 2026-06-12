# Dataset Plan

> **Important:** Do not upload heavy datasets to GitHub.
> Data goes in `data/` which is ignored by `.gitignore`.

## IL Track

### Situations

| Situation | Distractors | Task |
|---|---|---|
| both_bw | black + white visible | move red cable to red box |
| only_black | only black visible | move yellow cable to yellow box |
| only_white | only white visible | move green cable to green box |

### Pilot (10 demos)

```bash
bash scripts/record_il.sh both_bw 10
bash scripts/record_il.sh only_black 10
bash scripts/record_il.sh only_white 10
```

### Production (100 demos)

```bash
bash scripts/record_il.sh both_bw 100
bash scripts/record_il.sh only_black 100
bash scripts/record_il.sh only_white 100
```

## VLA Track

### Production (100 demos)

```bash
bash scripts/record_vla.sh red 100
bash scripts/record_vla.sh yellow 100
bash scripts/record_vla.sh green 100
```
