# Career network

An interactive map of my career: every role, qualification and period of
self-directed study as a circle, sized by how long it lasted, linked to the
skills, tools, platforms and sectors it involved.

**[View it →](https://loispatterson.github.io/cv-network/)**

## What you can do with it

- **Click a type** in the legend (analytics, engineering, product, AI,
  leadership, compliance, sector, education) to isolate everything of that kind
  and see which roles it spans.
- **Search** for a skill or tool to find every role it appears in.
- **Hover** a node to isolate it, **click** to keep it selected, **drag** to
  rearrange.
- **Switch layout** between *free* (a force-directed view that groups by type)
  and *by date* (roles pinned to a timeline, left to right).

## How it is built

`data.yaml` holds three lists — `roles`, `nodes` and `links` — and is the only
file worth editing. Ids are the join key between them.

```
python3 build.py
```

`build.py` validates every id, fails loudly on a typo or a duplicate, works out
each role's length in years and its midpoint on the timeline, and splices the
result into `index.html` as JSON. The page itself is a single file with no
build step and no dependencies beyond D3 from a CDN.

## Shapes and colours

A **circle** is something you do or use — a skill or a tool. A **square** is a
context you worked in — a sector, a platform, a qualification. Colour is the
type, matching the legend. Arcs take the colour of the node they run to, so a
role's fan of links reads as coloured bands.

---

Lois Patterson · [digital twin](https://github.com/loispatterson) · built with D3
