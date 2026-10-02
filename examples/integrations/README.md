# Integration examples

This directory is for examples that show PagePilot working with external products, APIs, and services.

## Where to put integration contributions

- Use `examples/integrations/<provider>/` for small, runnable examples that demonstrate PagePilot with a specific third-party service.
- Use `examples/custom-functions/` for provider-agnostic custom tool patterns.
- Use `pagepilot/integrations/<provider>/` only when the integration is shipped as part of the PagePilot package and has tests.
- Keep product-specific workflows, full applications, or large third-party projects in their own repositories.
- Add third-party projects to the community list below instead of vendoring their code into this repository.

## Example checklist

- Use `uv` in setup instructions.
- Keep the example focused on the PagePilot integration point.
- Document required environment variables, OAuth scopes, and local services.
- Do not commit secrets, tokens, generated credentials, or private account data.
- Prefer `ChatPagePilot()` unless the example is specifically about another model.
- Include the command that runs the example from the repository root.

## Community integrations

External projects listed here are maintained outside this repository. A listing is a pointer for users, not a support guarantee from PagePilot maintainers.

Add entries in this format:

```markdown
- [Project name](https://github.com/org/project) - One sentence about what it integrates with. Maintained by @github-handle.
```
