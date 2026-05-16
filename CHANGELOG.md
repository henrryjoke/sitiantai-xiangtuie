# Changelog

## [v0.2.0] - 2026-05-16

### Added
- 6 core algorithm scripts: calendar, meihua, liuyao, liuren, qimen, xiang_query
- 28 class-xiang (symbolic imagery) JSON knowledge base files across 6 categories
- Full SKILL.MD v0.2.0 with 7-step divergence workflow
- Feedback loop mechanism with local_feedback.jsonl
- Style memory and auto-correction after 3 repeated corrections
- Self-evaluation scoring (5 dimensions, re-generate if < 18)
- Prohibited/encouraged language rules

### Fixed
- Najia (compounded hexagram) assignment: upper trigram uses palace najia, lower uses self najia
- Wang-shuai (strength) algorithm: month branch uses seasonal strength only, day branch uses 7-effect model
- Xun-kong (void branches): corrected from flawed formula to 60-Jiazi cycle lookup

### Technical Highlights
- Month branch: seasonal strength (旺相休囚死)
- Day branch: 7 effects (临/生/克/冲/合/刑/害)
- 60-cycle precise positional lookup for void branches
- Jing-Fang Najia: upper/lower trigram separation
- 5-trigram integrated deduction
- Class-xiang: 5 dimensions x 5 contexts structured knowledge base

## [v0.1.0] - 2026-05-14

### Added
- Initial concept: Four-Elephant Synthesis (四象合参) architecture
- Xiang-tuiye methodology: divergent symbolic expansion vs convergent judgment
- Layer architecture design (L0-L6)
