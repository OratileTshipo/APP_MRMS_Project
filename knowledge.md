# GLM 5.3 Output Optimization Directives

## 1. Output Strategy & Patch Execution
* NEVER output complete, full-file replacements for files longer than 150 lines.
* Force patch-based edits: Output targeted SEARCH/REPLACE blocks or localized diff chunks using Freebuff file modification tools.
* Keep individual turn response payloads strictly under 4,000 output tokens to prevent generation truncations.

## 2. Multi-Step Execution Loop
* For refactoring or building multi-file features, break the execution into a multi-step checklist:
  1. Update/create interfaces and data types.
  2. Implement backend/core logic functions incrementally.
  3. Update UI / component layer.
  4. Run tests or build verification commands.
* Execute ONLY ONE phase per turn. Stop and wait for tool response or user confirmation before generating the next phase.

## 3. Thinking Budget Management
* State concise reasoning steps (< 150 words) before executing file tools.
* Do not restate entire code files inside thinking traces or conversational prose before making tool calls.
