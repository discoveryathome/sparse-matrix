# Handoffs

One comment per message: claims, findings, handoffs, `done` and `released`. Each comment is
a line of prose ending with one fenced `discover` block; the format, with examples, is in
[docs/CONTRIBUTING.md, "Claiming work"](https://github.com/discoveryathome/sparse-matrix/blob/main/docs/CONTRIBUTING.md#claiming-work).

- **Claim** before work over five minutes. Claims expire after 120 minutes and block
  nothing once expired.
- **End** a claim with `done` (linking the PR) or `released` (with a reason).
- **Handoffs** are bounded requests for someone else. One is **open** until a claim or
  `done` names it in `responds_to` (**taken**); that `done` **resolves** it.

A `done` here is not review: the maintainer decides what's promoted. Questions and
proposals go in the research issue template, not this thread.
