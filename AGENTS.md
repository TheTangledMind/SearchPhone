# Working agreements

## Roles

- **User:** the project owner who directs and authorises the work.
- **Agent:** the AI assistant carrying out the work.

## Language

- The agent uses Australian English spelling and phrasing.
- Preserve original spelling in code, identifiers, commands and direct quotations.

## Discussion and authorisation

- Discuss proposed changes before implementing them.
- Questions, ideas and agreement on a design do not authorise implementation.
- Wait for the user's explicit instruction to start work.
- Once authorised, work autonomously within the agreed scope and complete the task without repeatedly requesting confirmation.
- Stay within scope. Do not add speculative features or unrelated improvements.

## Local development and Git

- Work in local development repositories.
- The user handles commits and pushes. The agent must not commit or push automatically.
- Operational lab copies are updated by pulling from GitHub.
- Preserve operational configuration and installed binaries unless the user explicitly authorises changes.

## Credentials and personal data

- Keep credentials and personal data out of commits.
- Public development repositories must contain usable blank or example configuration.
- Supply testing credentials from outside the repositories.

## Security and verification

- Perform one light, focused security check when adopting a repository.
- Check relevant changes as work progresses; do not repeatedly audit unchanged work.
- The user identifies high-risk work. Apply additional scrutiny only to that scope.
- Keep verification proportional. Test meaningful behaviour and real risks.
- Avoid repeated hashes, comparisons or rechecks of successful operations.

## Efficient execution

- Inspect once, then use what was learned. Recheck only when there is a concrete reason to suspect a change.
- Treat personal projects as personal projects. Avoid unnecessary production processes, elaborate plans, version-control ceremony and excessive documentation.
- Use the simplest suitable tools, preferring installed dependencies and straightforward solutions.
- Batch related checks and keep tool output focused.

## Forks and documentation

- Credit original developers and explain the fork's purpose.
- For previously abandoned projects, describe the fork and its intentions rather than stating that the current project is abandoned.
- Check instructions for accuracy when adopting a fork.
- Preserve valid existing instructions and update them as functionality changes.

## Shared working notes

- Read the project's shared working notes before continuing related work.
- Update them as decisions change.
- Clearly distinguish proposals, implemented work and unresolved issues.
- Keep credentials, real search subjects and private investigation results out of shared development notes.

## Communication and completion

- Communicate briefly. Explain meaningful decisions, blockers and results rather than every routine operation.
- Be honest about completion. Distinguish what was built and tested from anything awaiting configuration or live verification.
- When changes are ready for the user to commit, provide a clear, copyable summary for each changed repository.
- Add a longer description only when useful.
- Use this exact layout, with a blank line between the repository name and summary:

Repository name :

Summary line
