## Verification *(mandatory)*

<!--
  IDs are stable: AS-001 upward for acceptance scenarios (unique in the whole
  feature), TR-001 upward for test requirements. Never renumber; append.
  Every FR and every AS needs at least one row. Name the interface where the
  promise is made; the plan adds the concrete test selector.
-->

### Verification matrix

| FR | AS | TR | Observable assertion | Layer / interface | Planned selector or method | Release SC |
|----|----|----|----------------------|-------------------|----------------------------|------------|
| FR-001 | AS-001 | TR-001 | [Expected state or result, including side effects] | [Smallest adequate layer] | [Filled in by the plan] | [SC-001 or none] |

### Success criteria classification

| SC | Release gate or post-launch measurement | How it is measured |
|----|------------------------------------------|--------------------|
| SC-001 | [Release gate] | [Measurement] |

### Completion gate

This feature is DONE only when every FR and AS above passes through its TR on the final state,
every release-gate SC is met, related regressions pass, and converge reports `converged`.
Anything else is NOT DONE.
