# Rehearsal: ezeOS hero (Stageshow)

Gold: `device-pair` (window pinned top-left running off the bottom, phone straddling the right edge over filler, lock screen notification as payoff) with the cursor beats of `hero-demo`. Kept the layout, the Phone/LockScreen/Notification parts and the crossfade between pages; changed the look to the ezeOS tokens (neutral grays, blue dot accent, Archivo + Inter Tight) and the story to the house promise.

Beats: 1 the clinic's card on the search page, cursor clicks Site; 2 its own site opens, cursor clicks "Agendar pelo WhatsApp"; 3 payoff, Mariana's message lands on the owner's phone and holds 2.6s; reset in place (message leaves, then the page). Loop about 9.5s.

Captured: 1440 (wide, stage grown to 1.10 by `data-ss-fill`) and 390 (compact 358 design grown to 1.09), dark theme only, poster `{ page: 'site', msg: true }`.

Gate (built page, `film.mjs "<page>" --select '#demo' --gate`):
- 1440: `rehearsal passed`
- 390: `rehearsal passed`

Film:
- notification visible from frame one → the host page animates every `[data-reveal]` and the kit's Collapse carries `data-reveal="drop"` → `#demo [data-reveal]{animation:none}` in the page
- "kit override" on phone parts → false positive: the bundle served the kit CSS from a path without `/kit/` → kit CSS now ships as `assets/kit/stageshow.css`, the hero's own as `assets/demo-ezeos.css`
- lopsided CTA 19/14 → in the playground the Roll label was measured with the fallback font, which hid it; here the stage mounts after `document.fonts.ready` → `--ss-button-pad-icon: 14px`
- host body letter-spacing and line-height leaking into the stage → reset on `.ezeos`
- window cut at the stage's foot in mid air → no bottom padding: the cut lands on the next section's top rule

Review: no separate fresh-eye reviewer was run.
Assumptions: the site keeps loading Archivo and Inter Tight itself (the hero's CSS no longer imports them).
Unresolved: the 1440 run notes one deferred layout check (the notification still moving at the final shot), not a fault.
Not checked: reduced motion on a real device, Safari, light theme (the site has none), sampling was "inconclusive" on this PC (dropped frames) so motion between samples was judged by eye from the contact sheet.
