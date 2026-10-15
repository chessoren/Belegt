# Belegt design system — America.gov, in Swiss red

## 1. What we studied

America.gov (2026) is a conversational front door to government: one question box, answers drawn from official sources, a privacy promise. That is exactly Belegt’s job, so we cloned its **system** (structure, scale, components, motion), not its assets. The site is built with Astro + Tailwind v4; its theme tokens are readable in the compiled CSS (`--color-*`, `--spacing-*`, `--radius-*`, `--text-*`, `--ease-*`).

What defines the America.gov look:

| Element | America.gov | Belegt |
|---|---|---|
| Ink colour | `blue-900 #000c1f` (navy-black) | `red-900 #1c0204` (red-black) |
| Action colour | `blue-700 #002664` pill buttons | `red-600 #DA291C` (Pantone 485 C on screen, AA with white text) |
| Brand colour | flag | `#FF0000` (official digital Swiss red), brand mark only |
| Link | `blue-500 #0066c5` | `red-500 #C8102E` (5.6:1 on white) |
| Secondary / tertiary text | ink at 65 % / 45 % (`color-mix`) | same rule, red ink |
| Tinted surfaces | `blue-700` at 10 % / 5 % | `red-700` at 8 % / 4 % |
| Display face | Rhymes Text (proprietary serif), tracking −0.03 em | Newsreader (OFL), tracking −0.03 em |
| UI face | Helvetica Now Text/Display | Inter (OFL), the open Swiss-style grotesque |
| Heading L | `clamp(3rem, 2.3rem + 3.01vw, 5rem)` | same |
| Radii | 4 → 48 px, hero card 40 px | same scale |
| Elevation | `0 10px 40px #010e2414` | `0 10px 40px #1c020414` |
| Hero | rounded grey card, giant serif greeting “Hello, America”, photo carousel under a pill composer | rounded grey card, greeting rotating through the four national languages (“Grüezi, Schweiz · Bonjour, la Suisse · Ciao, Svizzera · Allegra, Svizra”), Swiss-Style typographic posters of real articles under the composer |
| Composer | white pill, 2 px ink border, round send button | same, red send button |
| Feature rows | 386 px rounded art card + sans headline + text link | same grid: *Proven · Sovereign · Four languages · Measured* |
| “Coming in 2027” | floating form cards | floating cards of the next corpora (Civil Code, data protection, AVS) and a receipt |
| Footer | serif link list, full-width wordmark, laurel motto, GSA credit | serif link list, “Belegt.” wordmark with a Swiss-red full stop, laurel “Citation ou silence”, Apertus credit |
| Chat | grey user bubble on the right, answer on the left, sticky frosted header, docked composer | same, plus evidence cards, the 4-language panel and the receipt sheet |
| Sources | side sheet | side sheet with the article in DE/FR/IT/RM tabs and the quote highlighted |

## 2. Why Swiss red, and which red

The Swiss coat-of-arms legislation (Wappenschutzverordnung, annex) defines the flag red as Pantone 485 C, with the digital value RGB 255/0/0. Pure `#FF0000` fails contrast for text, so it is used only for the brand mark and the wordmark’s full stop. Interface actions use `#DA291C`, the usual screen rendering of Pantone 485 C, which passes WCAG AA with white text. The Swiss cross itself is **not** used: it is protected and would suggest an official site. The brand mark is a pair of Swiss guillemets « » — quotation is the product.

## 3. Tokens

All tokens live in [`web/tokens.css`](../web/tokens.css); components in [`web/app.css`](../web/app.css). Semantic names are kept identical to America.gov’s (`--color-text-primary`, `--color-background-tertiary`, `--color-border-quaternary`, `--radius-40`, `--ease-drawer`…), so a component written for one system reads naturally in the other.

## 4. Additions specific to Belegt

- **Verification states**: `--color-verified` (green) only ever means “found word for word in the official text”. Amber means “divergence flagged”. Red surfaces mean “abstained”.
- **Who-did-what chips** in the progress list: `AI` (Apertus) vs `Code` (deterministic). Users see which steps are probabilistic.
- **Dotted underline** marks sentences that are rephrasings rather than quotes.
- **Receipt**: paper-toned card with perforated edge, monospace hashes, printable.
- **Network pill**: always visible, green dot when the machine has no default route, live count of outbound connections from Belegt.

## 5. Accessibility

Contrast ≥ 4.5:1 for all text tokens on white; focus ring = 2 px ink; `prefers-reduced-motion` disables reveals and carousel transitions; the hero carousel has pause/prev/next; side sheets are `role="dialog"` with Escape to close; the interface is available in FR, DE, IT, RM and EN.
