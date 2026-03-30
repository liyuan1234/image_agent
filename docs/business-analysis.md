# Business Analysis

## Current Product Read

`image-agent` is currently an operator tool, not yet a product. It watches a screen or window, detects visual changes, sends screenshots plus a task-specific prompt to OpenAI, and stores logs locally. That is useful, but the value proposition is still implicit and the market surface is too broad.

The codebase suggests two early use cases:

- game assistance, shown by the Dota prompt and screenshots
- trading screen interpretation, shown by the trading prompt and examples

Those are very different markets with different trust, compliance, and willingness-to-pay dynamics. Trying to serve both from one generic CLI weakens positioning.

## Best Initial Market

The stronger near-term path is to position this as a desktop vision automation copilot for technical operators working with changing dashboards.

The highest-probability starting segment is:

- discretionary traders and researchers using charting terminals
- power users monitoring internal dashboards
- analysts watching visually dense operational tools that do not expose clean APIs

Why this segment is better than gaming:

- willingness to pay is materially higher
- ROI can be framed in time saved and missed-signal reduction
- a desktop CLI can be acceptable early if the output quality is high
- gaming assistance is more likely to run into policy, platform, or reputation issues

## Core Value Proposition

Proposed positioning:

`image-agent turns changing desktop screens into structured, model-driven analysis without requiring native integrations.`

What buyers are likely paying for:

- continuous monitoring of visual tools with no API access
- fast interpretation of screen changes
- persistent logs for later review
- task-specific prompting per workflow

## Gaps Between Repo And Product

The repo has technical promise, but several product gaps remain:

- no clear single persona or headline use case
- no structured output schema for downstream automation
- no alerting path beyond terminal output and local files
- no evaluation dataset to prove signal quality
- no onboarding flow for prompt design, capture permissions, and model cost control
- no packaging for non-developers beyond a Python install

## Recommended Near-Term Roadmap

### Phase 1: Prove one workflow

Focus the product on one vertical workflow, ideally trading or dashboard monitoring.

Deliver:

- one polished prompt pack for that workflow
- structured JSON output mode
- confidence and change summaries
- sample sessions that demonstrate before/after operator value

### Phase 2: Make it operational

Deliver:

- webhook, Slack, or Telegram notifications
- rate limiting and cost controls
- session history viewer
- clearer errors and health checks

### Phase 3: Commercialize

Deliver:

- packaged desktop installer or menu-bar app
- paid prompt packs or workflow templates
- team features such as shared prompts and audit logs

## Suggested Pricing Direction

Early pricing should be simple and usage-aware:

- individual: monthly subscription for one workstation and local logging
- pro: higher tier with notifications, structured exports, and multiple workflows
- team: shared prompt library, collaboration, audit logs, and policy controls

Avoid consumption-only pricing at the start. Buyers need predictable spend before trusting an always-on vision agent.

## Immediate Execution Priorities

The next engineering tasks that best support commercial progress are:

1. Add structured output support so results can trigger real actions.
2. Add notification integrations so the tool can operate asynchronously.
3. Create one benchmarkable demo workflow with reproducible screenshots and expected outputs.
4. Reduce setup friction with a guided configuration command or packaged app.
