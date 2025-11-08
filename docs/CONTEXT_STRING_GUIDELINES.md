# Context String Guidelines — Spiral Path v1.1
> **Purpose**: Keep *work* (science) and *play* (narrative) strictly separated.  
> **Status**: Optional. Load only when using AI/LLM in interactive mode.  
> DOI: [10.5281/zenodo.15585013](https://doi.org/10.5281/zenodo.15585013) (v1.1 supersedes)

---

## Core Rule: **No Bleed**
| Zone | Allowed | Forbidden |
|------|--------|----------|
| **Work** | Math, code, hypothesis, audit, DOI | Myth, jihad, crusade, divine right |
| **Play** | Dune, Muad’Dib, Lady Liberty, poetry | Scientific claims without proof |

---

## Theme Sentry Actions (AI Must Enforce)

| Trigger | Zone | Action |
|-------|------|--------|
| `Muad’Dib`, `Shai-Hulud`, `spice` | Play | → `playground/dune/` |
| `hypothesis`, `fidelity`, `DOI` | Work | → `examples/` or `auditors/` |
| `jihad`, `crusade`, `manifest destiny` + `right` | Blocked | **Stop + Cite**: "Violates neutrality. See §3.1" |
| Mixed | Split | Run in **two logs**: `audit_helix_log.jsonl` + `play_log.jsonl` |

---

## User Bypass
> User: *"Run anyway."*  
→ AI logs: `"USER_BYPASS: theme_sentry overridden"`  
→ Output **still isolated** to `playground/`

---

## LLM Prompt Template
```text
[LOAD CONTEXT_STRING_GUIDELINES]
Input: "{user_input}"
1. Classify: work / play / mixed / blocked
2. Route accordingly
3. Log to correct file
4. Respond
