"""
Learner Guide ADVANCED reference chapters — Manage AI Agents with Paperclip
(TGS-2023036646).

Part F extends the core Learner Guide (see lg_chapters.py) into advanced
operations and integration. Every technical assertion here is taken from the
official documentation at https://docs.paperclip.ing/ (harvested 28 August
2026). Where the documentation gives an exact value — a default, a threshold,
a state name, a type key, an endpoint path, an error string — that exact value
is reproduced. Nothing is invented. Where the documentation does not cover a
detail, the principle is described without asserting a specific.

The module exposes ADVANCED_CHAPTERS: an ordered list of blocks in the LG
builder's own DSL:
    ("h1", text) ("h2", text) ("h3", text) ("p", text)
    ("bullets", [str, ...])
    ("code", text)
    ("note", text)
    ("table", (caption, [headers], [[row], ...]))
    ("rule",)
    ("check", [str, ...])        # self-check questions
"""

# ══════════════════════════════════════════════════════════════════ Part F
PART_F = [
 ("h1", "Part F — Advanced Operations and Integration"),

 ("p", "Parts A to D got a company running and governed. Part F is about what happens "
       "afterwards: bringing other people onto the instance, handling credentials at a scale "
       "beyond one API key, extending agents with skills you have written yourself, "
       "diagnosing runs that have gone quiet, engineering the cost down rather than merely "
       "capping it, and settling into an operating rhythm you can sustain. The material here "
       "assumes you are comfortable with the vocabulary of Parts A to D and can already read "
       "a run transcript without help."),

 # ───────────────────────────────────────────────────────────── F1
 ("h2", "F1. Multi-user operation"),

 ("p", "A default Paperclip install runs in local_trusted mode. There is no login, because "
       "the board operator is implicitly trusted and the instance is intended for a single "
       "local user. The moment a second person needs access — a colleague, a reviewer, a "
       "client who wants to see the board — that assumption has to be replaced with a real "
       "authentication boundary. This is not a setting you can toggle casually; it changes "
       "how every request to the instance is identified."),

 ("h3", "F1.1 Turning login on"),
 ("p", "Authentication is a property of the DEPLOYMENT MODE, not of the company. You move the "
       "whole instance from local_trusted to authenticated, and then choose an exposure of "
       "private or public."),
 ("table", ("The three documented deployment modes",
   ["Mode", "Authentication", "Documented use"],
   [["local_trusted (default)", "No login required",
     "\"Personal installs, development, demos\". Loopback-only host binding; login friction "
     "removed; the board operator is implicitly trusted."],
    ["authenticated + private", "Login required via Better Auth",
     "\"Tailscale, VPN, LAN\". Binds to all interfaces for network access; auto base URL mode "
     "for lower-friction private access."],
    ["authenticated + public", "Login required",
     "\"Hosted production\". Explicit public URL required; stricter security checks."]])),
 ("p", "There are two documented routes into authenticated mode. The persistent route rewrites "
       "the stored configuration; the environment-variable route overrides it for one launch, "
       "which makes it useful for a rehearsal you do not want to keep."),
 ("code", "pnpm paperclipai configure --section server\n"
          "\n"
          "# or, as a one-run override:\n"
          "PAPERCLIP_DEPLOYMENT_MODE=authenticated pnpm paperclipai run"),
 ("p", "In authenticated plus private mode, host validation is enforced against an allowlist. "
       "A machine name that is not on the list is rejected, which produces a failure that "
       "looks like a network problem and is not. Add hostnames explicitly, and remember the "
       "restart:"),
 ("code", "pnpm paperclipai allowed-hostname my-machine.tailnet.ts.net"),
 ("note", "The allowed-hostname command takes effect only after a server restart, and the "
          "allowlist is only enforced in authenticated + private mode. The equivalent "
          "environment variable is PAPERCLIP_ALLOWED_HOSTNAMES, a comma-separated list; "
          "unknown hosts are rejected."),
 ("p", "For an internet-facing deployment the documentation sets the external URL and the "
       "exposure explicitly:"),
 ("code", "export PAPERCLIP_DEPLOYMENT_MODE=authenticated\n"
          "export PAPERCLIP_DEPLOYMENT_EXPOSURE=public\n"
          "export PAPERCLIP_AUTH_PUBLIC_BASE_URL=https://paperclip.example.com\n"
          "export PAPERCLIP_ALLOWED_HOSTNAMES=paperclip.example.com"),
 ("p", "Finish by re-running the diagnostic. It checks deployment and auth mode compatibility "
       "specifically, which is exactly the class of mistake this change introduces:"),
 ("code", "pnpm paperclipai doctor"),

 ("h3", "F1.2 The first human account"),
 ("p", "Switching on authentication creates a chicken-and-egg problem: nobody can log in to "
       "create the first account. Paperclip resolves it with a bootstrap credential. When "
       "paperclipai run starts an authenticated-mode instance with the embedded database, it "
       "generates a bootstrap CEO invite as part of its start-up sequence. You can also mint "
       "one headlessly:"),
 ("code", "paperclipai auth bootstrap-ceo\n"
          "paperclipai auth bootstrap-ceo --expires-hours 24\n"
          "paperclipai auth bootstrap-ceo --force\n"
          "paperclipai auth bootstrap-ceo --base-url https://paperclip.example.com"),
 ("table", ("bootstrap-ceo flags",
   ["Flag", "Effect"],
   [["--force", "Create a new invite even when an admin already exists."],
    ["--expires-hours <hours>", "Invite lifetime in hours. Accepts 1-720; default 72."],
    ["--base-url <url>", "Public base URL used to build the invite link."]])),
 ("p", "The result is a board-claim URL of the form /board-claim/<token>?code=<code>. Treat it "
       "with the same care as a password."),
 ("note", "The documentation is blunt about this: \"Treat the claim URL as sensitive. It is "
          "intended for a one-time ownership transfer, not for general sharing.\" If it "
          "expires before you use it, restart the server to mint a fresh one."),

 ("h3", "F1.3 Inviting a teammate"),
 ("p", "Once at least one human account exists, further people arrive through the invite flow. "
       "There is no Add member button on the Access page — that is deliberate, and learners "
       "regularly hunt for it. Every new human enters as an invite that produces a join "
       "request."),
 ("table", ("The invite path, end to end",
   ["Step", "Where", "What happens"],
   [["1. Create the invite", "Company Invites page",
     "Choose a Role: Viewer, Operator (default), Admin or Owner. Paperclip generates a link "
     "for the current Paperclip domain, copies it to the clipboard where the browser allows, "
     "and shows it in the \"Latest invite link\" panel."],
    ["2. Send the link", "Out of band",
     "\"Invites are copy-link only\" — Paperclip sends no email. You deliver the link yourself."],
    ["3. Recipient joins", "The Paperclip join page",
     "The link creates a join request tied to the invite. The invite's default role is "
     "attached to the request."],
    ["4. Approve", "/inbox/requests, or \"Open join request queue\"",
     "A holder of joins:approve approves or rejects. The membership \"becomes active only "
     "after joins:approve holder approves request.\""]])),
 ("p", "Invites themselves have four documented states, shown as a badge in the invite history "
       "table:"),
 ("table", ("Invite states",
   ["State", "Meaning"],
   [["Active", "\"Consumable\" — the link can still be used. Only Active invites show a "
     "Revoke button."],
    ["Accepted", "\"First use completed\"."],
    ["Expired", "\"Time-based expiration\"."],
    ["Revoked", "\"Manually revoked\"."]])),
 ("p", "The invite history table is paginated at five invites per page, and carries columns "
       "for State, Role, Invited by, Created, the linked Join request, and the Revoke action. "
       "An Open invite button is provided so you can test the link yourself before sending it."),

 ("h3", "F1.4 Join requests"),
 ("p", "The join request queue lives at /inbox/requests. It has two filter dropdowns — Status "
       "(Pending approval by default, plus Approved and Rejected) and Request type (All, "
       "Human, Agent) — because agents can also arrive through this queue, and you want to be "
       "able to separate the two."),
 ("p", "Each request card shows a status badge (pending approval, approved, rejected), a "
       "request-type badge (human or agent), an adapter-type badge for agent requests only, "
       "the requester's name and a secondary identifier (email for humans; capabilities or IP "
       "for agents), an Invite context panel showing allowedJoinTypes, the default role and "
       "the invite message, and a Request details panel showing the submission timestamp, "
       "source IP and agent capabilities."),
 ("note", "Reviewing join requests requires the joins:approve permission. Without it the queue "
          "shows: \"You do not have permission to review join requests for this company.\" "
          "Acted-upon requests remain visible under the new status filter for audit, with the "
          "action buttons removed."),

 ("h3", "F1.5 Membership states and the permission model"),
 ("p", "A member row on Settings → Access carries a status badge of active, pending or "
       "suspended, alongside the role and a comma-separated grants summary (or \"No explicit "
       "grants\"). The Edit Member dialog exposes exactly three controls: a Company role "
       "dropdown, a Membership status dropdown, and a two-column checkbox grid of grants."),
 ("table", ("Membership states",
   ["State", "What it means operationally"],
   [["active", "A working member. Role implicit grants plus any explicit grants apply."],
    ["pending", "Membership created but not yet activated — the state a join request produces "
     "before approval."],
    ["suspended", "The documented way to remove someone. \"Removal is admin-driven\" — there "
     "is no self-serve leave option."]])),
 ("p", "Two properties of the permission model are load-bearing and are the most common source "
       "of surprised operators."),
 ("bullets", [
   "AN EXPLICIT GRANT PERSISTS ACROSS A ROLE CHANGE. Demoting an Owner to Viewer removes the "
   "role's implicit grants, but any grant that was ticked explicitly on that member survives "
   "the demotion. If you want it gone, untick it.",
   "THERE IS NO DENY LAYER. The rule is: \"Start with the implicit grants from the member's "
   "role. Add every explicit grant checked on the member.\" Explicit grants only ADD "
   "capability. You cannot subtract a permission from a role — you either choose a role that "
   "does not include it, or leave the role Unset and grant only what you intend.",
 ]),
 ("p", "Four permission keys are worth knowing by name in a multi-user setting because they "
       "are never implicit and must be granted deliberately: tasks:assign_scope, "
       "tasks:manage_active_checkouts, pipelines:write and audit:view_agent_actions. The last "
       "of these opens the company Audit feed and allows a CSV download, which makes it the "
       "grant you give to whoever is accountable for evidence."),
 ("note", "Agent authority and human authority are separate systems. The documentation states "
          "it plainly: \"Paperclip's agent chain of command (CEO, managers, reports) is "
          "separate from human roles. Human roles gate UI access and company-level actions; "
          "agent roles describe the reporting tree.\" Promoting a person to Owner does not "
          "change any agent's manager, and re-parenting an agent grants no human anything."),

 ("h3", "F1.6 Offboarding a member"),
 ("p", "Offboarding is a sequence, not a single action, and the order matters if you want the "
       "audit trail to stay intact."),
 ("bullets", [
   "Set the member's Membership status to suspended in the Edit Member dialog. The row "
   "remains for the audit trail — this is by design, and it is why deletion is not offered.",
   "Untick every explicit grant on that member first if you want them removed, because "
   "explicit grants survive role changes and you should not leave dormant grants attached to "
   "a suspended row.",
   "Revoke any Active invites that person created, from the invite history table.",
   "Revoke any board API tokens they minted. Board tokens carry full instance authority; "
   "suspending the human membership does not revoke a token that was already issued.",
   "Re-home any issues on which they were the responsible human. The execution policy "
   "escalation path uses responsibleUserId with a fallback to createdByUserId — a suspended "
   "user sitting in that field is how a review stalls silently.",
 ]),
 ("p", "There are two documented cross-issue denial codes that reference exactly this "
       "situation, and recognising them saves an afternoon: "
       "issue_write_responsible_user_ceiling (403) means the responsible user is not "
       "authorised, and issue_write_responsible_user_unavailable (403) means the responsible "
       "user has been removed or deactivated."),
 ("p", "Token hygiene is a separate command surface:"),
 ("code", "paperclipai token board list\n"
          "paperclipai token board revoke <key-id>\n"
          "\n"
          "paperclipai token agent list --company-id <id> --agent <agent-id-or-name>\n"
          "paperclipai token agent revoke --company-id <id> --agent <agent-id-or-name> <key-id>"),

 ("check", [
   "Name the three deployment modes and say which one requires an explicit public URL.",
   "A colleague's invite link works, they land on the join page, and then nothing happens. "
   "What is the missing step, and which permission key does it require?",
   "You demote an Owner to Viewer. They can still create agents. Explain why, and fix it.",
   "State the three membership states and say which one Paperclip uses for removal.",
   "Give two things that suspending a member does NOT do.",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F2
 ("h2", "F2. Secret management in depth"),

 ("p", "Part B established the rule: secrets never appear in a prompt, a lab note or Git. "
       "This section is about the machinery behind that rule — how secrets are stored, "
       "versioned, rotated, delivered to a run, and requested by an agent that does not have "
       "one yet."),

 ("h3", "F2.1 The storage model"),
 ("p", "Secrets are stored in two layers. A company_secrets row holds the record, its metadata "
       "and a pointer to the current version; company_secret_versions holds the versioned "
       "material. The default provider is local_encrypted, which the documentation describes "
       "as \"AES-GCM encrypted using the local master key\" with a SHA-256 hash, stored at:"),
 ("code", "~/.paperclip/instances/default/secrets/master.key"),
 ("note", "\"Back up secrets/master.key somewhere safe. It encrypts every API key and secret "
          "stored in Paperclip — if you lose it, you lose access to all of them.\" The key is "
          "32 bytes and is created automatically during onboarding. It can be overridden with "
          "PAPERCLIP_SECRETS_MASTER_KEY (base64, hex or raw) or "
          "PAPERCLIP_SECRETS_MASTER_KEY_FILE (a path)."),
 ("p", "Every secret carries a managedMode that decides who owns the material:"),
 ("table", ("The two managed modes",
   ["managedMode", "Where the value lives", "Consequence"],
   [["paperclip_managed", "Paperclip owns, creates, stores and rotates the value.",
     "A rotate call requires a value. The material is inside your instance and inside your "
     "master-key blast radius."],
    ["external_reference", "The value lives in an external vault; externalRef is the pointer.",
     "Paperclip stores the address, not the credential. Some providers do not support writing "
     "values at all."]])),

 ("h3", "F2.2 Creating, updating and rotating"),
 ("p", "The board-side surface is small and worth memorising, because the difference between "
       "PATCH and rotate is the difference between renaming a secret and changing it."),
 ("code", "GET    /api/companies/{companyId}/secret-providers\n"
          "GET    /api/companies/{companyId}/secrets\n"
          "GET    /api/companies/{companyId}/secrets/catalog\n"
          "POST   /api/companies/{companyId}/secrets\n"
          "PATCH  /api/secrets/{secretId}\n"
          "POST   /api/secrets/{secretId}/rotate\n"
          "DELETE /api/secrets/{secretId}"),
 ("table", ("Create secret — POST /api/companies/{companyId}/secrets",
   ["Field", "Required", "Notes"],
   [["name", "Yes", "Unique within the company."],
    ["value", "Yes", "Plaintext secret value."],
    ["provider", "No", "Defaults to local_encrypted."],
    ["description", "No", "Human-readable note."],
    ["externalRef", "No", "Required by some external providers."]])),
 ("p", "Creation makes version 1 and sets latestVersion to 1. The response is metadata only — "
       "no plaintext comes back. PATCH accepts name (which must stay unique), description and "
       "externalRef, and the documentation is explicit: \"This endpoint does not change the "
       "secret value.\" To change the value you rotate, which \"creates an immutable new "
       "version and advances latestVersion\"."),
 ("p", "Rotation accepts value (required for paperclip_managed), externalRef, "
       "providerVersionRef and providerConfigId. For AWS Secrets Manager, rotation reads the "
       "current AWSCURRENT first, writes the new value as a new AWS version which becomes "
       "AWSCURRENT, tracks AWSCURRENT rather than pinning a version, and rolls back if "
       "version recording fails."),
 ("note", "DELETE /api/secrets/{secretId} is a hard delete: \"Deletes the secret and its "
          "version history.\" It cascades the version rows and breaks every future resolution "
          "that referenced the secret. There is no soft-delete path documented."),

 ("h3", "F2.3 How a secret reaches a run"),
 ("p", "An agent's adapterConfig never contains a plaintext credential in a well-run company. "
       "It contains a secret_ref, which Paperclip resolves at launch:"),
 ("code", "{\n"
          "  \"env\": {\n"
          "    \"ANTHROPIC_API_KEY\": {\n"
          "      \"type\": \"secret_ref\",\n"
          "      \"secretId\": \"secret-uuid\",\n"
          "      \"version\": \"latest\"\n"
          "    }\n"
          "  }\n"
          "}"),
 ("p", "Omitting version is treated as latest. A numeric version pins the reference to a "
       "fixed historical value: { \"type\": \"secret_ref\", \"secretId\": \"secret-uuid\", "
       "\"version\": 2 }. The documented guidance is to use latest for rotatable values and "
       "to pin numerically only for fixed historical values — because a pinned reference does "
       "not follow a rotation, which is usually the opposite of what you wanted."),
 ("p", "There are three documented delivery modes: env, where plaintext is injected into the "
       "agent's environment at launch; api, where the agent fetches the value on demand; and "
       "both."),
 ("table", ("Run-bound agent access to secrets",
   ["Endpoint", "What it returns"],
   [["GET /api/agents/me/secrets",
     "\"Returns just the aliases this agent is allowed to reach\" — names only, no values."],
    ["POST /api/agents/me/secrets/{key}/value",
     "Returns { \"key\", \"value\", \"version\" } with a Cache-Control: no-store header. "
     "Requires a live heartbeat token and secrets:read. Every read is logged to the security "
     "audit trail and the activity log."]])),
 ("p", "This is the answer to \"what can an agent see?\". An agent can enumerate the ALIASES "
       "it is permitted to reach at any time; it can obtain a VALUE only inside a live "
       "heartbeat, only with secrets:read, and only at the cost of a permanent audit entry. "
       "It cannot enumerate the company's other secrets, and it cannot read a value belonging "
       "to another company — \"Agent-authenticated requests can only act inside their own "
       "company.\""),
 ("note", "Three token classes are denied run-bound secret access ON PURPOSE: low-trust "
          "tokens, task-bridge tokens and skill-test tokens. If a skill fails to read a secret "
          "while you are testing it in the Skill Studio but works in a real heartbeat, this is "
          "why — it is behaving as designed."),

 ("h3", "F2.4 Strict mode"),
 ("p", "Strict mode converts the convention into an enforced rule. With "
       "PAPERCLIP_SECRETS_STRICT_MODE enabled, sensitive environment keys — the documented "
       "patterns are *_API_KEY, *_TOKEN and *_SECRET — must use secret references, and inline "
       "plaintext values are rejected."),
 ("code", "PAPERCLIP_SECRETS_STRICT_MODE=true"),
 ("p", "It applies to agent adapterConfig.env, project env, hire-agent approvals and company "
       "imports. Routines carry their own env map (routines.env) with an identical shape, and "
       "strict mode applies to it equivalently; historical routine runs retain their "
       "dispatched env through routine_runs.routine_revision_id."),
 ("note", "\"Strict mode blocks new inline sensitive values. It does not automatically migrate "
          "what is already stored.\" It also does NOT apply to "
          "paperclipai configure --section llm. Turning it on is a change to what is "
          "acceptable from now on, not a cleanup of what already exists."),
 ("p", "For an existing install there is a migration script, available only from a git "
       "checkout rather than the installed CLI. Run it without --apply first; that is a dry "
       "run:"),
 ("code", "pnpm secrets:migrate-inline-env\n"
          "pnpm secrets:migrate-inline-env --apply"),

 ("h3", "F2.5 Provider vaults"),
 ("p", "A provider vault is a per-company routing record for an external secret store. The "
       "documentation is precise about what it holds: address, namespace and prefixes — "
       "\"never the credentials themselves\". AWS Secrets Manager is supported; GCP Secret "
       "Manager and HashiCorp Vault are saved as draft metadata only. The UI location is "
       "Company Settings → Secrets → Provider vaults."),
 ("code", "GET/POST /companies/{companyId}/secret-provider-configs\n"
          "POST     /companies/{companyId}/secret-provider-configs/discovery/preview\n"
          "PATCH/DELETE/POST .../default and /secret-provider-configs/{id}"),
 ("p", "AWS discovery includes a scan step using secretsmanager:ListSecrets metadata. Provider "
       "capability is expressed through flags — supportsManagedValues, "
       "supportsExternalReferences, supportsExternalValueWrites, configured and "
       "requiresExternalRef — and those flags are what produce the validation errors you will "
       "meet:"),
 ("table", ("External value write validation errors (verbatim)",
   ["Condition", "Message"],
   [["No externalRef", "\"External reference secrets require externalRef\""],
    ["Both value and a different externalRef",
     "\"Provide either a new value or a new external reference, not both\""],
    ["value with providerVersionRef", "\"Value updates cannot pin providerVersionRef\""],
    ["Provider does not support writes",
     "\"<provider label> does not support writing values to external reference secrets\""],
    ["Paperclip-managed AWS secret",
     "\"AWS Paperclip-managed namespace secrets cannot be imported as external references\""]])),

 ("h3", "F2.6 Secret proposals — agents propose, people decide"),
 ("p", "An agent that needs a credential it does not have does not get to create one. It "
       "raises a PROPOSAL, which a board member approves or rejects. This is the same "
       "governance shape as approvals, applied to credentials."),
 ("code", "POST   /api/agents/me/secret-proposals\n"
          "GET    /api/agents/me/secret-proposals\n"
          "DELETE /api/agents/me/secret-proposals/{id}\n"
          "GET    /api/companies/{companyId}/secret-proposals\n"
          "POST   /api/companies/{companyId}/secret-proposals/{id}/approve\n"
          "POST   /api/companies/{companyId}/secret-proposals/{id}/reject"),
 ("p", "There are two proposal kinds. A kind: \"secret\" proposal asks for a new secret to "
       "exist; a kind: \"binding\" proposal asks for an existing secret to be wired into a "
       "configuration path."),
 ("table", ("Secret proposal — kind: \"secret\"",
   ["Field", "Required", "Notes"],
   [["kind", "Yes", "\"secret\""],
    ["name", "Yes", "Slash-separated path, no empty segments."],
    ["value", "Yes", "Plaintext; maximum 65536 bytes; encrypted immediately."],
    ["justification", "Yes", "Why it is needed. Shown to the board."],
    ["key", "No", "Environment key; defaults to the last segment of name."],
    ["description", "No", "Operator note carried through to the created secret."]])),
 ("table", ("Secret proposal — kind: \"binding\"",
   ["Field", "Required", "Notes"],
   [["kind", "Yes", "\"binding\""],
    ["configPath", "Yes", "env.<KEY> or access.<ALIAS>"],
    ["secretId", "One of", "An existing active company secret."],
    ["secretProposalId", "One of", "A still-pending secret proposal."],
    ["targetAgentId", "No", "Defaults to the proposing agent."],
    ["justification", "Yes", "Why the binding is needed."]])),
 ("p", "The target policy for bindings is self_and_reports — an agent may propose a binding "
       "for itself or for an agent below it in the chain of command, and not otherwise."),
 ("table", ("Proposal limits and lifecycle",
   ["Property", "Value"],
   [["Statuses", "pending, approved, rejected, withdrawn, expired"],
    ["Pending cap", "Maximum 20 pending proposals per agent"],
    ["Rate limit", "Maximum 20 per minute"],
    ["Expiry", "14 days, transitioned by a background sweep"],
    ["On resolution", "ciphertextScrubbedAt is stamped and the value is wiped"],
    ["List pagination", "limit default 100, max 200, plus offset; response headers "
     "X-Page-Limit, X-Page-Offset, X-Next-Offset"]])),
 ("p", "Approval accepts cascade plus overrides for name, description and providerConfigId. "
       "Rejection requires a non-empty reason. Three failure messages are worth recognising:"),
 ("bullets", [
   "\"Expired proposals cannot be approved\" — the 14-day sweep has already run.",
   "\"Binding proposal requires pending secret proposal <id>; retry with cascade=true\" — you "
   "are approving a binding whose secret does not exist yet.",
   "\"Binding proposal target is no longer allowed...\" — the target agent has moved outside "
   "the proposer's chain of command since the proposal was raised.",
 ]),
 ("note", "The governing sentence, verbatim: \"Agents propose, people decide. An agent can "
          "raise a proposal and watch its status, but only a board member can approve it.\" "
          "A backlog of twenty pending proposals from one agent is not a bug — it is the cap "
          "doing its job, and it is a signal that you have stopped reading your queue."),

 ("check", [
   "State the difference between PATCH /api/secrets/{secretId} and POST "
   "/api/secrets/{secretId}/rotate.",
   "When should a secret_ref pin a numeric version, and what does it cost you?",
   "Exactly what can an agent learn about the company's secrets without a live heartbeat?",
   "You enable strict mode on a six-month-old company and nothing breaks. Why is that not "
   "evidence that your configuration is clean?",
   "Name the proposal caps (pending, rate, expiry) and say what happens to the ciphertext on "
   "resolution.",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F3
 ("h2", "F3. Trust levels and low-trust review"),

 ("p", "Trust in Paperclip is not a slider you set on an agent by feel. It is DERIVED, and "
       "understanding what it is derived from tells you how to raise or lower it deliberately."),

 ("h3", "F3.1 Where a skill's trust level comes from"),
 ("p", "A skill is a folder, and its supporting files are classified by which folder they sit "
       "in. That classification is what produces the trust level:"),
 ("table", ("Supporting file classification",
   ["Folder", "Inventory kind", "Trust classification"],
   [["references/", "reference", "markdown only"],
    ["scripts/", "script", "scripts / executables"],
    ["assets/", "asset", "assets"]])),
 ("p", "The derivation rule is stated verbatim: \"A skill's overall trust level is derived "
       "from the highest classification in its inventory: markdown_only < assets < "
       "scripts_executables.\""),
 ("note", "This is a practical design lever. A skill that is pure guidance stays at "
          "markdown_only. The moment you add one shell script to scripts/, the whole skill's "
          "trust level rises to scripts_executables — even if the script is three lines and "
          "does nothing dangerous. If you want to keep a skill in the lowest trust band, put "
          "the procedure in references/ and let the agent run the commands itself."),

 ("h3", "F3.2 What low trust changes"),
 ("p", "Low trust is a preset that narrows what an actor may do. Three documented "
       "consequences matter operationally."),
 ("bullets", [
   "SECRETS. \"Low-trust, task-bridge and skill-test tokens are denied run-bound secret "
   "access on purpose.\" A low-trust actor cannot call POST /api/agents/me/secrets/{key}/value "
   "at all.",
   "CROSS-ISSUE WRITES. The four default-open write channels — commenting, changing fields, "
   "creating child issues and assigning work — are described as a STANDARD-trust privilege: "
   "\"A standard-trust agent may comment, update fields, create child issues, and assign on "
   "any company-visible issue it can already read.\" A low-trust actor attempting one of "
   "these meets the denial code issue_write_actor_class_excluded (403, boundary tone), whose "
   "documented meaning is exactly \"Default-open writes are a standard-trust privilege.\"",
   "INBOX. The permission key inbox:manage is documented as interacting with the low-trust "
   "preset: \"inbox:manage and the low-trust preset\" — low-trust agents are denied by "
   "default.",
 ]),
 ("p", "The denial payloads are unusually helpful and worth reading rather than merely "
       "catching. They carry a code, a named boundary, a whoCanAct string and a "
       "sanctionedPath — the legitimate route to the same outcome:"),
 ("code", "{\n"
          "  \"error\": \"Task is outside this actor's visibility (Issue visibility). [...]\",\n"
          "  \"details\": {\n"
          "    \"code\": \"issue_write_not_visible\",\n"
          "    \"boundary\": \"Issue visibility\",\n"
          "    \"whoCanAct\": \"the current assignee, and any agent or board member the task "
          "is visible to.\",\n"
          "    \"sanctionedPath\": \"Ask the board to widen visibility for Scout, or create a "
          "child issue...\"\n"
          "  }\n"
          "}"),
 ("note", "When an agent reports that it is blocked, ask for the details.code, not the prose. "
          "The code names the boundary, the tone field says what class of problem it is "
          "(boundary, lock, cap, attribution) and sanctionedPath tells you the legitimate "
          "route. That is a complete diagnosis in one payload."),

 ("h3", "F3.3 Reviewing a skill before you trust it"),
 ("p", "Paperclip provides a skill audit that returns one of three verdicts:"),
 ("table", ("Skill audit verdicts",
   ["Verdict", "Meaning"],
   [["pass", "No findings."],
    ["warning", "Soft findings — scripts, network commands, drift from originHash."],
    ["fail", "Hard-stop findings — remote-fetch-execute, exfiltration patterns, oversized "
     "files, an invalid SKILL.md."]])),
 ("code", "POST /api/companies/{companyId}/skills/{skillId}/audit\n"
          "POST /api/companies/{companyId}/skills/{skillId}/reset\n"
          "GET  /api/companies/{companyId}/skills/{skillId}/versions"),
 ("p", "\"A fail verdict is what hard-blocks install-update.\" A warning does not block; it "
       "asks you to make a judgement. That judgement is the human half of low-trust review, "
       "and the documentation gives it a rule: \"Before attaching a skill to a high-trust "
       "role, open the skill and read its SKILL.md end-to-end.\""),
 ("note", "The Administration → Trust & Low-Trust Review page of the official documentation "
          "was not harvested for this guide. The trust mechanics described above are taken "
          "from the Skills reference, the Secrets API and the Roles & Permissions pages. "
          "Consult that page directly before configuring a trust preset in production."),

 ("check", [
   "A colleague adds a helper script to a documentation skill and the skill's trust level "
   "changes. Explain the rule that caused it.",
   "Name two things a low-trust actor cannot do that a standard-trust agent can.",
   "Which audit verdict blocks install-update, and which one merely asks for a judgement?",
   "An agent reports it cannot comment on an issue. Which four fields of the denial payload "
   "do you ask for, and what does each tell you?",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F4
 ("h2", "F4. Bundled and optional skills"),

 ("p", "Part B established what a skill is and why context economy matters. This section is "
       "about the library that ships with the product — what is in it, and when each piece "
       "earns its place on an agent."),

 ("h3", "F4.1 The bundled catalogue"),
 ("p", "Seven bundled skills ship with the Paperclip application, versioned with it and "
       "installable into companies through the catalogue. The descriptions below are the "
       "documentation's own."),
 ("table", ("Bundled skills",
   ["Category", "Skill", "What it does (verbatim)"],
   [["Docs", "Doc Maintenance",
     "\"keep project documentation aligned with recent code and feature changes\""],
    ["Paperclip Operations", "Issue Triage",
     "\"classify stale, blocked, in-review, or stalled Paperclip issues and choose the next "
     "action\""],
    ["Paperclip Operations", "Status Card Query",
     "\"author Paperclip status cards, and compile a card's prose prompt into bounded search "
     "queries\""],
    ["Paperclip Operations", "Task Planning",
     "\"turn approved plans into Paperclip issues with ownership, dependencies, and "
     "acceptance criteria\""],
    ["Product", "Wireframe",
     "\"produce low-fidelity UI wireframes as standalone SVG deliverables\""],
    ["Quality", "QA Acceptance",
     "\"define observable acceptance criteria and focused verification passes\""],
    ["Software Development", "GitHub PR Workflow",
     "\"prepare, inspect, update, and communicate GitHub pull request work\""]])),
 ("p", "Read that list as an org chart rather than a feature list. Task Planning belongs on "
       "whoever converts an approved strategy into issues — usually the CEO or a manager. QA "
       "Acceptance belongs on the reviewer named in an execution policy, because it is about "
       "producing OBSERVABLE acceptance criteria, which is precisely the thing a review stage "
       "checks. Issue Triage belongs on whoever runs your daily sweep. Doc Maintenance and "
       "GitHub PR Workflow belong on engineering roles."),
 ("note", "\"Bundled doesn't mean forced on everyone: you still browse, pick, and install.\" "
          "The bundled catalogue is a shelf, not a default configuration. The one exception is "
          "described separately below."),

 ("h3", "F4.2 The optional catalogue"),
 ("p", "Seven optional skills are listed as \"extras you add when you need them\", each in a "
       "named category:"),
 ("table", ("Optional skills",
   ["Skill", "Category"],
   [["Agent Browser", "browser"],
    ["Release Announcement", "content"],
    ["Simplified English", "content"],
    ["Ramp", "finance"],
    ["Design Critique", "product"],
    ["Last30Days", "research"],
    ["Prepare MCP Integration", "software-development"]])),
 ("note", "The individual optional-skill pages were not harvested for this guide, so this "
          "table asserts only the names and categories the documentation lists. Read each "
          "skill's own SKILL.md before attaching it — which is the standing rule for any "
          "skill on a high-trust role."),

 ("h3", "F4.3 Bundled-required behaviour"),
 ("p", "One class of skill is not optional at all, and this catches people out. Skills under "
       "the key prefix paperclipai/paperclip/* carrying metadata.sourceKind: "
       "paperclip_bundled are, in the documentation's words, \"unioned into every resolved "
       "desiredSkills set by the server. Removing them from the request has no effect.\""),
 ("p", "The same protection applies to deletion. Attempting to delete a bundled skill returns: "
       "\"It's a bundled skill. The server re-imports skills/ from disk on every company list "
       "call.\""),
 ("p", "There is a separate set of BUNDLED EXAMPLE skills in the server's skills/ directory, "
       "which are the ones that give an agent its Paperclip literacy:"),
 ("bullets", [
   "paperclip — the base heartbeat skill.",
   "paperclip-board — company governance via chat.",
   "paperclip-create-agent — the hire workflow.",
   "paperclip-converting-plans-to-tasks — plan-to-task translation.",
   "para-memory-files — PARA file-based memory.",
 ]),

 ("h3", "F4.4 Versioning and release pinning"),
 ("table", ("How each skill source is versioned",
   ["Source", "Pinned?", "Update path"],
   [["github", "Yes (commit SHA)", "GET /update-status then POST /install-update"],
    ["skills_sh", "Yes (GitHub)", "Same as github"],
    ["url", "No", "None; re-import to refresh"],
    ["local_path (managed)", "Live", "Files refresh on read"],
    ["local_path (project scan)", "Live", "Re-run the scan endpoint"],
    ["paperclip_bundled", "Pinned to release", "Upgrade Paperclip itself"],
    ["catalog", "Pinned to metadata.originHash",
     "GET /update-status then POST /install-update, or POST /reset"]])),
 ("p", "Beta release pinning is gated behind an instance experimental setting, "
       "enableBetaSkills, which is OFF by default and lives at Settings → Instance settings → "
       "Experimental. Two shipped bundled-paperclip releases are documented: v0, \"V0 — "
       "Original\" (2026-07-15), and v7-roster, \"V7 — Roster champion\" (2026-07-21)."),
 ("note", "If any desiredSkills entry carries a non-null versionId while enableBetaSkills is "
          "off, the request fails with 400 and the message \"Beta skill version pins require "
          "the Beta skills experimental setting to be enabled.\" With the flag off, saved pins "
          "are IGNORED rather than deleted, and every agent resolves to the live skill — so "
          "turning the flag off does not undo a pin, it merely suspends it."),

 ("check", [
   "Name the bundled skill you would attach to a reviewer named in an execution policy, and "
   "justify it in one sentence.",
   "Why does removing a paperclip_bundled skill from a desiredSkills request have no effect?",
   "An agent behaves differently after you switched off enableBetaSkills, but the pin is still "
   "on the agent. Explain.",
   "Which two skill sources are 'live' rather than pinned, and what risk does that carry?",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F5
 ("h2", "F5. Writing a company skill"),

 ("p", "Attaching somebody else's skill is a procurement decision. Writing your own is a "
       "design decision, and it is the highest-leverage thing an operator can do to cut cost "
       "and raise consistency at the same time. This section walks the authoring workflow end "
       "to end."),

 ("h3", "F5.1 Decide it should be a skill at all"),
 ("p", "A procedure belongs in a skill when it is REUSED and CONDITIONAL. Reused, because a "
       "skill's whole economic argument is that many agents share one document. Conditional, "
       "because a skill is loaded on demand — if every heartbeat needs it, it belongs in the "
       "agent's instruction files instead, where it is always present."),
 ("table", ("Where a procedure belongs",
   ["Property of the procedure", "Put it in"],
   [["Needed on every heartbeat, by this agent only", "HEARTBEAT.md in the instruction bundle"],
    ["Defines who the agent is", "SOUL.md in the instruction bundle"],
    ["Needed sometimes, by several agents", "A company skill"],
    ["Long supporting detail the agent reads only when it has already decided to act",
     "references/ inside that skill"]])),
 ("note", "The economic claim, verbatim: \"Skills keep the base context small. An agent with "
          "10 skills doesn't load all 10 into its context on every heartbeat — it only loads "
          "the ones that are relevant.\" The documented benefits are fewer tokens per run "
          "(lower cost), cleaner and more focused context (better results), and one place to "
          "maintain a shared procedure."),

 ("h3", "F5.2 The folder"),
 ("p", "The required layout is a folder with SKILL.md at its root, plus up to three optional "
       "supporting folders:"),
 ("code", "my-skill/\n"
          "├── SKILL.md\n"
          "├── references/\n"
          "│   └── examples.md\n"
          "├── scripts/\n"
          "│   └── run.sh\n"
          "└── assets/\n"
          "    └── logo.png"),
 ("p", "Remember F3: the folder you choose sets the trust classification. references/ is "
       "markdown only, assets/ is assets, scripts/ is scripts and executables, and the skill "
       "takes the highest classification present. Folders nest up to four levels deep."),

 ("h3", "F5.3 The frontmatter"),
 ("p", "SKILL.md is YAML frontmatter followed by a Markdown body. Five frontmatter fields are "
       "documented:"),
 ("table", ("SKILL.md frontmatter fields",
   ["Field", "Required", "Type", "Notes"],
   [["name", "Recommended", "string", "Human-readable label; falls back to the slug."],
    ["description", "Recommended", "string",
     "Agent routing logic. Block scalars are supported."],
    ["slug", "Optional", "string", "Kebab-case identifier; derived if absent."],
    ["key / skillKey", "Optional", "string", "Canonical key override."],
    ["metadata", "Optional", "object", "Arbitrary record with recognised sub-fields."]])),
 ("p", "Recognised metadata sub-fields include metadata.skillKey, metadata.canonicalKey and "
       "metadata.paperclipSkillKey (which carry the canonical key across imports); the nested "
       "forms metadata.paperclip.skillKey and metadata.paperclip.key; metadata.sourceKind, "
       "one of paperclip_bundled, github, skills_sh, url, local_path, project_scan, "
       "managed_local or catalog; metadata.sources[], a list of source descriptors carrying "
       "kind, repo, path, commit, trackingRef, hostname, url and rawUrl; and the GitHub "
       "coordinates metadata.owner, metadata.repo, metadata.ref and metadata.trackingRef."),

 ("h3", "F5.4 Writing the description as decision logic"),
 ("p", "This is the single most important line in the file, and it is not a summary. The "
       "description is what the agent reads to decide whether to load the skill at all. Write "
       "it as ROUTING LOGIC — an explicit \"Use when\" and an explicit \"Don't use when\":"),
 ("code", "---\n"
          "name: code-review\n"
          "description: >\n"
          "  Use when asked to review a pull request or code diff.\n"
          "  Don't use when writing new code from scratch.\n"
          "---\n"
          "\n"
          "# Code Review\n"
          "\n"
          "When reviewing code, check the following..."),
 ("p", "The documentation's own design guidance for the body is short and worth following "
       "literally: \"Be specific and actionable — Concrete checklists and steps produce "
       "consistent results\"; \"Keep each skill focused on one concern\"; \"Put supporting "
       "detail in references/\"."),
 ("note", "A description that reads \"Helps with code quality\" is a description that will be "
          "loaded on every heartbeat that mentions code, or on none. Both failure modes cost "
          "you money. The negative clause — \"Don't use when\" — is the half most authors omit "
          "and the half that does most of the routing work."),

 ("h3", "F5.5 Authoring and testing in Skill Studio"),
 ("p", "Skill Studio at /skills/studio is the built-in authoring surface. On desktop it "
       "presents three resizable panes; on narrow screens they become tabs."),
 ("bullets", [
   "LEFT — a file tree of everything in the skill folder, with an editor underneath. Markdown "
   "files open in the rich editor. Toolbar actions are Add file, Add folder, Delete file and "
   "Delete folder. Unsaved work shows an Unsaved badge.",
   "MIDDLE — the input text area. Saved inputs are organised with / in their name, exactly "
   "like folders.",
   "RIGHT — test-run history, with states succeeded, failed and cancelled. Runs refresh "
   "themselves while they are in flight.",
 ]),
 ("p", "The Run button reports why it is unavailable, and the four documented reasons are a "
       "useful checklist in their own right: \"This skill has no files to test\"; \"Pick an "
       "agent to run\"; \"Add or paste input text to run\"; \"Save skill edits before "
       "running\". Advanced options include a run-template selector, starting from \"Default "
       "test template\", with \"No template\" for raw input testing."),
 ("note", "\"Test runs happen on a hidden harness task, which keeps them out of your real "
          "issue list.\" That is why a skill test cannot read run-bound secrets — skill-test "
          "tokens are denied that access deliberately (see F2.3). Test the LOGIC in the "
          "Studio; prove the CREDENTIALS in a real heartbeat."),
 ("p", "One structural constraint: SKILL.md cannot be deleted. Renaming is possible only for "
       "Paperclip-managed skills, requires the new slug to be free, is audited, obeys the "
       "company skill policy, and changes the name, the slug and the key together — with the "
       "documented consequence that \"Every agent that had the old skill attached is moved to "
       "the new key automatically.\""),

 ("h3", "F5.6 Attaching the skill"),
 ("p", "There are two documented attachment points. At hire time, pass desiredSkills in the "
       "create body:"),
 ("code", "{\n"
          "  \"name\": \"Backend Engineer\",\n"
          "  \"adapterType\": \"claude_local\",\n"
          "  \"desiredSkills\": [\"paperclip\", \"code-review\", \"deploy-runbook\"]\n"
          "}"),
 ("p", "After hire, use the sync endpoint. The mode field is REQUIRED and takes add, remove or "
       "replace:"),
 ("code", "POST /api/agents/{agentId}/skills/sync\n"
          "{ \"desiredSkills\": [\"paperclip\", \"code-review\"], \"mode\": \"add\" }"),
 ("p", "Or from the CLI:"),
 ("code", "paperclipai agent skills <agent-id>\n"
          "paperclipai agent skills:sync <agent-id> --desired-skills paperclip,github"),
 ("p", "Each desiredSkills entry accepts a UUID, a canonical key, or a slug when that slug is "
       "unique in the company. The resolution order is documented: exact UUID match on id, "
       "then a normalised key match, then a normalised slug match \"but only when exactly one "
       "skill in the company has that slug.\""),
 ("bullets", [
   "Ambiguous reference: \"Invalid company skill selection (ambiguous references: <slug>; "
   "...)\"",
   "Unknown reference: \"Invalid company skill selection (unknown references: <reference>; "
   "...)\"",
 ]),
 ("p", "Inspect the resulting state with GET /api/agents/{agentId}/skills, which returns an "
       "AgentSkillSnapshot carrying adapterType, supported, mode, desiredSkills, entries[] and "
       "warnings. The mode field tells you whether the files actually reach the runtime:"),
 ("table", ("Adapter skill sync modes",
   ["Mode", "Behaviour"],
   [["persistent", "The adapter writes skill files into the working directory and leaves them "
     "there between runs."],
    ["ephemeral", "Files are materialised per run and cleaned up afterwards. This is the "
     "default for sandboxed adapters."],
    ["unsupported", "The assignment is recorded, but Paperclip cannot push files into the "
     "runtime — it only tracks which skills you assigned."]])),
 ("note", "A skill attached to an agent whose adapter reports unsupported is a skill that does "
          "nothing. Check the mode field before you conclude that a skill is being ignored for "
          "some subtler reason."),

 ("h3", "F5.7 Importing rather than authoring"),
 ("p", "POST /api/companies/{companyId}/skills/import accepts a wide range of source formats, "
       "which is how you bring an existing procedure into a company without retyping it:"),
 ("code", "{ \"source\": \"https://github.com/paperclipai/paperclip\" }\n"
          "{ \"source\": \"https://github.com/paperclipai/paperclip/tree/main/skills/paperclip\" }\n"
          "{ \"source\": \"paperclipai/paperclip\" }\n"
          "{ \"source\": \"paperclipai/paperclip/paperclip-create-agent\" }\n"
          "{ \"source\": \"https://skills.sh/paperclipai/paperclip/paperclip-create-agent\" }\n"
          "{ \"source\": \"https://example.com/raw/SKILL.md\" }\n"
          "{ \"source\": \"/Users/me/code/my-project/skills/code-review\" }"),
 ("p", "There is also a project scan — POST /api/companies/{companyId}/skills/scan-projects — "
       "which sweeps well-known locations inside your project workspaces, including skills/, "
       "skills/.curated/, .claude/skills/, .codex-style tool folders and many more, plus "
       "\"the workspace root itself (if it contains a SKILL.md).\" Imported project skills "
       "reference the files in the project workspace rather than copying them, which is what "
       "makes them live rather than pinned."),
 ("note", "Skills are COMPANY-SCOPED, not org-scoped: \"A skill installed in Company A is "
          "invisible to Company B.\" If you run two companies on one instance and want the "
          "same procedure in both, you import it twice. Mutating skill routes require either "
          "the agents:create permission or permissions.canCreateAgents=true."),

 ("check", [
   "Give the two properties a procedure must have before it belongs in a skill rather than an "
   "instruction file.",
   "Write a description block for a skill that produces monthly finance summaries, including "
   "both clauses.",
   "Which folder would you put a 40-line checklist in, and what does that choice do to the "
   "skill's trust level?",
   "You attach a skill and the agent ignores it. Name three checks, in order.",
   "Why is 'mode' a required field on the skills sync endpoint?",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F6
 ("h2", "F6. Connecting external systems"),

 ("p", "An agent that can only talk to Paperclip is not much use. This section covers the "
       "connection surfaces the harvested documentation actually specifies. It is "
       "deliberately conservative: several of the product's how-to guides on integration were "
       "not harvested, and the honest answer for those is a pointer rather than a "
       "half-remembered command."),

 ("h3", "F6.1 The general shape of an integration"),
 ("p", "Every external connection in Paperclip resolves to one of four mechanisms, and "
       "recognising which one you are dealing with tells you where to configure it and where "
       "to look when it fails."),
 ("table", ("The four integration mechanisms",
   ["Mechanism", "Where it is configured", "What it is for"],
   [["Adapter env + credentials", "Agent adapterConfig.env, as secret_refs",
     "Giving the RUNTIME the credentials it needs — the provider key, a GitHub token, "
     "anything the agent's own tooling reads from the environment."],
    ["The HTTP adapter", "adapterType: http",
     "Letting Paperclip call YOUR service as if it were an agent. A single request per run."],
    ["The process adapter", "adapterType: process",
     "Letting Paperclip launch your own command, script or runtime as an agent."],
    ["Routine webhook trigger", "Routine → Triggers → webhook",
     "Letting an EXTERNAL system wake Paperclip on its own schedule or event."]])),

 ("h3", "F6.2 Outbound: the HTTP adapter"),
 ("p", "The HTTP adapter is the cleanest way to put an existing service behind an agent "
       "identity. \"The HTTP adapter does not run a child process. It sends a single request, "
       "waits for the response, and treats any non-2xx response as a failure.\""),
 ("table", ("HTTP adapter configuration",
   ["Field", "Required", "Notes"],
   [["url", "Yes", "Absolute http:// or https:// endpoint."],
    ["method", "No", "Defaults to POST."],
    ["headers", "No", "Extra request headers."],
    ["payloadTemplate", "No",
     "JSON object merged into the request body before the standard fields."],
    ["timeoutMs", "No", "Request timeout in milliseconds. 0 means no timeout."]])),
 ("p", "The request always carries runId, agentId and context; anything from payloadTemplate is "
       "merged alongside:"),
 ("code", "{\n"
          "  \"runId\": \"run-123\",\n"
          "  \"agentId\": \"agent-123\",\n"
          "  \"context\": {\n"
          "    \"taskId\": \"issue-123\",\n"
          "    \"wakeReason\": \"scheduled\",\n"
          "    \"commentId\": null\n"
          "  },\n"
          "  \"customField\": \"value\"\n"
          "}"),
 ("note", "Two design rules from the documentation. Return 2xx when the webhook is ACCEPTED, "
          "\"not when all follow-up work is complete\" — a long job should acknowledge and "
          "then report back through the API. And \"Keep the endpoint idempotent when possible "
          "because retries are easier to support.\""),
 ("p", "The process adapter is the local equivalent: it \"launches the command, streams logs, "
       "and returns stdout/stderr plus exit metadata\" and \"does not invent a higher-level "
       "protocol.\" It takes command (required), args, cwd (must be absolute), env, timeoutSec "
       "(0 means no timeout) and graceSec (defaults to 15). Non-zero exits return an error "
       "message with the raw output payload."),
 ("note", "Both http and process — along with openclaw_gateway — are shown as \"Coming soon\" "
          "in the UI dropdown but are \"fully functional in the runtime\". Reach them through "
          "the API or a company export/import, not the hire form."),

 ("h3", "F6.3 Inbound: routine webhooks"),
 ("p", "A routine's trigger can be a webhook — \"a signed URL you can call from anything "
       "outside Paperclip\". This is the supported way for an external system to start work "
       "inside your company: a CI pipeline, a monitoring alert, a form submission."),
 ("table", ("Webhook trigger configuration",
   ["Setting", "Documented values"],
   [["Signing mode", "bearer, hmac_sha256, github_hmac, none"],
    ["Replay window (seconds)",
     "\"how far back in time a signed request's timestamp may be\" — hidden for github_hmac "
     "and none"],
    ["Secret", "Shown once on creation; a Rotate secret button mints a new one"]])),
 ("note", "The github_hmac signing mode exists precisely so a GitHub webhook can be verified "
          "with GitHub's own scheme. Choose none only on a loopback-bound instance you "
          "control, and never in authenticated + public mode."),

 ("h3", "F6.4 Provider credentials and their rotation"),
 ("p", "Provider API keys are ordinary secrets, so rotation follows F2 exactly: create the new "
       "value as a new VERSION via POST /api/secrets/{secretId}/rotate, leave the agents' "
       "secret_refs on version \"latest\", and the next run picks the new value up. That is "
       "the whole reason to prefer latest over a numeric pin."),
 ("table", ("Documented provider environment variables",
   ["Variable", "Adapter it serves"],
   [["ANTHROPIC_API_KEY", "claude_local (Anthropic keys start sk-ant-)"],
    ["ANTHROPIC_BASE_URL", "claude_local — optional custom endpoint"],
    ["CLAUDE_CODE_USE_BEDROCK=1", "claude_local — AWS Bedrock detection"],
    ["OPENAI_API_KEY", "codex_local (OpenAI keys start sk-); overwrites the host login"],
    ["GEMINI_API_KEY / GOOGLE_API_KEY", "gemini_local"]])),
 ("p", "Four adapter provider overrides are documented for routing to non-default gateways: "
       "PAPERCLIP_CODEX_PROVIDERS (JSON of custom providers for Codex's config.toml), "
       "PAPERCLIP_PI_PROVIDERS (for Pi's models.json), PAPERCLIP_OPENCODE_PROVIDERS (merged "
       "into OpenCode's provider config) and PAPERCLIP_OPENCODE_SMALL_MODEL (OpenCode's "
       "auxiliary model). \"Values support {env:VAR} placeholders for secret expansion "
       "server-side.\""),
 ("p", "After any credential change, validate before you rely on it. Three surfaces do this:"),
 ("code", "POST /api/companies/{companyId}/adapters/{type}/test-environment\n"
          "GET  /api/companies/{companyId}/adapters/{type}/models\n"
          "GET  /api/companies/{companyId}/adapters/{type}/detect-model"),
 ("p", "The Test environment button on the agent form calls the first of these. For "
       "claude_local, testEnvironment() checks that Claude Code is installed and executable, "
       "that the working directory is absolute and usable, and that authentication is "
       "configured — via ANTHROPIC_API_KEY, Bedrock, or a subscription login — and then runs "
       "a live probe with the prompt \"Respond with hello.\" For codex_local the rule is \"No "
       "silent credential-less runs\": the adapter fails fast if no login or API key is "
       "available."),
 ("note", "Claude subscription login has its own board-only surface: POST "
          "/api/agents/{agentId}/claude-login (claude_local agents only), with a "
          "setup-token-login-sessions flow under /api/companies/{companyId}/ and a "
          "claude-oauth-token-status endpoint for checking state. The CLI equivalent is "
          "paperclipai agent claude-login <agent-id>."),

 ("h3", "F6.5 Where the documentation stops"),
 ("p", "Paperclip's how-to library lists dedicated guides for Connect an Agent to GitHub, Add "
       "an MCP Server to an Agent, and Wire Slack/Discord Notifications. Those pages were NOT "
       "harvested for this guide, so this guide asserts nothing about their specific fields, "
       "commands or endpoints."),
 ("p", "What can be said safely is the shape each of them takes, because it follows from the "
       "mechanisms above:"),
 ("bullets", [
   "GITHUB — the agent's own runtime does the Git and API work, so the connection is a "
   "credential in the adapter environment plus, for repository-bound work, a project "
   "Repository binding (a local folder cwd, a remote repoUrl, or most commonly both). The "
   "bundled GitHub PR Workflow skill supplies the procedure.",
   "MCP — an MCP server is a tool surface belonging to the RUNTIME, not to Paperclip's control "
   "plane. The optional Prepare MCP Integration skill exists for this work, and "
   "tools:admin is the documented permission key covering \"tool plumbing, stdio command "
   "templates, MCP gateways, mint/revoke tokens\".",
   "SLACK / DISCORD — outbound notification is an external call, so it follows the outbound "
   "mechanisms in F6.2 or a skill that calls the service directly, with the webhook URL held "
   "as a secret_ref.",
 ]),
 ("note", "This is the right instinct to carry into production generally: when the "
          "documentation does not specify a field, do not guess it into a runbook. Record the "
          "mechanism, cite the page you have not yet read, and verify against the live product "
          "before you commit the procedure to your own SOP."),

 ("check", [
   "Name the four integration mechanisms and give one example use of each.",
   "Why should an HTTP adapter endpoint return 2xx on acceptance rather than on completion?",
   "Your provider key is compromised at 14:00. Describe the rotation in the order you would "
   "perform it, and say why the agents need no reconfiguration.",
   "Which webhook signing mode would you choose for a GitHub-originated trigger, and which "
   "would you never choose on a public instance?",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F7
 ("h2", "F7. Backup, restore and portability"),

 ("p", "Part D introduced portability as a principle: a Paperclip company is data, not a "
       "hand-built configuration. This section is the operational detail — what is actually "
       "backed up, how collisions are handled, and what a restore looks like when you are "
       "doing it under pressure."),

 ("h3", "F7.1 Three things worth backing up"),
 ("table", ("The three backup surfaces",
   ["What", "How", "Why it matters"],
   [["The database", "paperclipai db:backup",
     "Everything: companies, agents, issues, runs, activity, secret records."],
    ["The master key", "Copy ~/.paperclip/instances/default/secrets/master.key",
     "Without it, a restored database's secret material is unreadable."],
    ["The company package", "Company export (UI) or paperclipai company export",
     "A portable, human-readable package you can move, diff and re-import elsewhere."]])),
 ("note", "A database backup WITHOUT the master key is not a backup of your secrets. This is "
          "the most consequential backup mistake in Paperclip, and it is silent until the day "
          "you restore."),

 ("h3", "F7.2 Database snapshots"),
 ("code", "paperclipai db:backup\n"
          "paperclipai db:backup --dir /backups/paperclip\n"
          "paperclipai db:backup --retention-days 14\n"
          "paperclipai db:backup --json"),
 ("table", ("db:backup flags",
   ["Flag", "Effect"],
   [["--dir <path>", "Backup output directory."],
    ["--retention-days <days>", "Retention window for daily pruning. Default 30."],
    ["--filename-prefix <prefix>", "Backup filename prefix. Default paperclip."],
    ["--json", "Print backup metadata as JSON — the form to use from a scheduled job."]])),
 ("note", "\"For the embedded database you can run a backup without the server up — db:backup "
          "connects on the embedded port directly.\" That is the embedded PostgreSQL on port "
          "54329, and it means a nightly backup does not need to negotiate with a running "
          "instance."),

 ("h3", "F7.3 Exporting a company"),
 ("p", "The export surface is reachable from the Org Chart header or the Settings → Export "
       "shortcut, and from the CLI:"),
 ("code", "paperclipai company export <company-id> --out ./path\n"
          "paperclipai company export <company-id> --out ./path --include company,agents,projects,issues,skills"),
 ("p", "The default included content is documented precisely: company metadata; every "
       "NON-TERMINATED agent; every NON-ARCHIVED project; every issue. Read that carefully — "
       "a terminated agent and an archived project are deliberately left behind, which is "
       "usually what you want when cloning a structure and occasionally not what you want "
       "when taking a forensic copy."),
 ("p", "The export UI has three regions. A sticky bar carries the company name, a selected / "
       "total files counter, any warnings, and the Export N files button. The left panel is a "
       "searchable Package files tree, where \"Search expands matching directories; restores "
       "state on clear\", the tasks/ directory is paginated at 10 tasks visible by default "
       "behind a Show more issues button, and \"Checked and search-matched tasks pinned above "
       "fold\". The right panel previews the selected file and updates the URL for "
       "deep-linking. README.md and .paperclip.yaml are regenerated on the fly to reflect your "
       "selection."),

 ("h3", "F7.4 Importing and collision handling"),
 ("p", "Import accepts two source types: a GitHub repo (\"Paste tree/blob URL to folder "
       "containing COMPANY.md\") or a local zip — an exported .zip package."),
 ("note", "\"Avoid re-zipping archives in Finder/Explorer; use Export page download.\" A "
          "re-zipped archive frequently fails to import. Also note "
          "PAPERCLIP_IMPORT_ZIP_MAX_BYTES, which caps the company-import zip size at a default "
          "of 1 GB, clamped between 1 byte and 64 GiB."),
 ("p", "Target selection offers Create new company (the default, with an optional New company "
       "name field to override the package name) or Existing company (\"Apply package on top "
       "of currently selected company\"). Collision strategy is a separate dropdown:"),
 ("table", ("Collision strategies",
   ["Strategy", "Behaviour"],
   [["Rename on conflict (default)", "\"New name proposed (e.g., gstack-CEO)\""],
    ["Skip on conflict", "\"Existing items kept; incoming copy dropped\""],
    ["Replace existing", "\"Incoming version overwrites current entity\""]])),
 ("p", "Preview before you apply. Clicking Preview import generates three sections: a RENAMES "
       "list of conflicting agents and projects, each with a free-form target-name input, a "
       "per-row Skip button and a Confirm rename button; an ADAPTERS list of every agent in "
       "the package with an available-adapter dropdown, where \"New agents default to target "
       "company CEO's adapter\" and a Configure adapter button opens an inline per-agent "
       "config form; and a FILE TREE in the same layout as the export tree, with an action "
       "badge of create, update, skip or replace on each row and an arrow showing the target "
       "name on renamed directories. The sticky bar shows file, conflict and error counts."),
 ("p", "Then click Import N files. The button is disabled if the preview shows errors or no "
       "files are selected. On success Paperclip refreshes the companies list, navigates to "
       "the imported or updated company dashboard, and restores the sidebar order if the "
       "package included one."),
 ("table", ("What is protected on an import into an EXISTING company",
   ["Rule", "Consequence"],
   [["\"Incoming issues always created as new\"",
     "An import cannot silently overwrite issue history."],
    ["\"replace blocked by server\"",
     "The most destructive strategy is refused on this path."],
    ["\"Full replace requires dedicated instance-admin flow\"",
     "There is a deliberate escalation before anything is truly overwritten."],
    ["Existing-company imports are non-destructive",
     "They do not remove data."]])),
 ("note", "IMPORTED AGENTS HAVE TIMER HEARTBEATS DISABLED BY DEFAULT. This is a safety "
          "property and you should not be surprised by silence after a restore — nothing is "
          "broken, nothing has started. Re-enable interval heartbeats deliberately, agent by "
          "agent, after you have checked budgets and credentials."),

 ("h3", "F7.5 The restore workflow"),
 ("p", "Under pressure, work in this order. Each step is verifiable before you move on, which "
       "is what stops a restore from becoming a second incident."),
 ("bullets", [
   "1. STAND UP THE CONTROL PLANE. Restore or start the instance and confirm GET /api/health "
   "responds — it reports \"whether the server is up and whether the database is reachable\", "
   "plus deployment mode, auth readiness and feature flags.",
   "2. RESTORE THE MASTER KEY before you test anything credential-shaped, or every secret "
   "resolution will fail in a way that looks like an adapter problem.",
   "3. RUN THE DIAGNOSTIC. paperclipai doctor checks config validity, deployment/auth mode "
   "compatibility, the agent JWT secret, the secrets adapter, storage, database connectivity, "
   "the LLM provider, the log directory, the listen port, the Node.js runtime, the managed "
   "install and the background service.",
   "4. IMPORT OR VERIFY THE COMPANY, with Preview first and a deliberate collision strategy.",
   "5. FIX THE ADAPTERS. The import's Adapters section defaults new agents to the target "
   "company CEO's adapter; working directories and environment need to be right for THIS "
   "machine.",
   "6. RE-ESTABLISH BUDGETS before re-enabling anything. A restored company with no caps and a "
   "working key is an uncapped company.",
   "7. RUN ONE AGENT MANUALLY. Use paperclipai heartbeat run --agent-id <id> and watch the "
   "transcript before you trust the schedule.",
   "8. RE-ENABLE HEARTBEATS one agent at a time, checking spend after each.",
 ]),
 ("p", "Two adjacent commands are worth knowing for the same class of work. Archiving is the "
       "reversible way to take a company out of active rotation; it pauses all active agents "
       "with pause reason company_archived, cancels queued and in-flight wake-up requests, and "
       "preserves agents, projects and issues. Deletion is the destructive one:"),
 ("code", "paperclipai company archive <company-id>\n"
          "paperclipai company delete <company-id> --yes --confirm <value>"),
 ("note", "Deletion requires PAPERCLIP_ENABLE_COMPANY_DELETION to be enabled server-side, and "
          "--confirm must match the target company ID or prefix. The documentation's warning "
          "is one sentence long: \"There is no undo.\""),
 ("note", "The Cloud Sync and Sync to Cloud Upstream pages of the official documentation were "
          "not harvested for this guide. Cloud-managed instances are configured through "
          "PAPERCLIP_MANAGED_CONFIG — a JSON document describing feature flags, plugins and "
          "the sandbox environment, requiring v: 1, mode: \"cloud\", catalogVersion, features "
          "and plugins.autoInstall, with an optional environments array limited to ONE entry "
          "and no credentials permitted inside the config. Beyond that, consult the live "
          "documentation."),

 ("check", [
   "Name the three things you must back up, and say which omission fails silently.",
   "What does a company export deliberately EXCLUDE by default?",
   "Which collision strategy is blocked by the server on an import into an existing company, "
   "and why is that sensible?",
   "You restore a company and nothing runs. Give the most likely benign explanation.",
   "Put the eight restore steps in order and say which one prevents a restore from becoming a "
   "spend incident.",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F8
 ("h2", "F8. Debugging a stuck heartbeat"),

 ("p", "\"Nothing is happening\" is the most common operator report and the least useful. This "
       "section turns it into a method. The principle is to work OUTWARD from the run: "
       "establish first whether a run happened at all, because that single fact splits the "
       "problem space in half and everything after it follows."),

 ("h3", "F8.1 The first question: did a run start?"),
 ("code", "paperclipai run live --company-id <company-id>\n"
          "paperclipai run list --company-id <company-id> --agent-id <agent-id> --limit 50"),
 ("p", "In text mode these report id, status, agentId, invocationSource, triggerDetail, "
       "startedAt, finishedAt and logBytes. That is enough to branch:"),
 ("table", ("The branch point",
   ["Observation", "Class of problem", "Go to"],
   [["No run record at all", "The agent never woke — a TRIGGER problem", "F8.2"],
    ["A run record exists but failed immediately", "The environment — a LAUNCH problem",
     "F8.3"],
    ["A run started and is still running long past expectation",
     "The runtime is stuck — an EXECUTION problem", "F8.4"],
    ["A run succeeded but nothing changed on the board",
     "The agent ran and did nothing useful — a WORK problem", "F8.5"]])),
 ("note", "Answer this question before forming any theory. Most wasted debugging time comes "
          "from investigating a model-behaviour hypothesis for an agent that never woke up."),

 ("h3", "F8.2 No run started — the trigger problem"),
 ("p", "Work the list in order; each item is cheap and rules out a class of cause."),
 ("bullets", [
   "IS THE AGENT PAUSED, OR IS ITS HEARTBEAT MERELY OFF? These are different and the "
   "distinction is the single most useful fact in this section. Heartbeat-off still wakes on "
   "assignment, on comment, on routine and on demand. PAUSED WAKES ON NOTHING.",
   "IS IT PAUSED BY BUDGET? At 100% utilisation the agent is auto-paused with pauseReason = "
   "\"budget\" and no further heartbeats fire. The dashboard's Month Spend card and the agent "
   "Budget tab both show this.",
   "IS THE INTERVAL ACTUALLY ON? \"Heartbeat on interval\" is OFF BY DEFAULT. An agent "
   "configured but never switched on is the most common false alarm in the whole product.",
   "IS THE SCHEDULER RUNNING? HEARTBEAT_SCHEDULER_ENABLED defaults to true and "
   "HEARTBEAT_SCHEDULER_INTERVAL_MS defaults to 30000. A disabled scheduler silences every "
   "timer wake on the instance at once — if EVERY agent has gone quiet, check here first.",
   "IS THE INTERVAL BEING MISREAD AS A GUARANTEE? \"Heartbeat interval — the minimum number "
   "of seconds between automatic heartbeats. This is a floor, not a guarantee.\"",
   "IS THE AGENT AWAITING APPROVAL? An agent in pending_approval cannot be manually run — the "
   "Run Heartbeat button is disabled for that status.",
   "IS THE COMPANY ARCHIVED? Archiving pauses all active agents with pauseReason "
   "company_archived and cancels queued and in-flight wake-ups.",
   "IS THE ESCALATION PATH BROKEN? Two banners appear on the agent page: Invalid Org Chain "
   "(a terminated manager, a missing manager, or a loop) which \"Blocks work assignment\", and "
   "Escalation Path Paused (a paused agent up the reports_to chain) where \"Escalations "
   "refused; no functional escalation path.\"",
 ]),
 ("p", "Then force the issue. A manual invocation removes every scheduling variable at once:"),
 ("code", "paperclipai heartbeat run --agent-id <agent-id>\n"
          "paperclipai heartbeat run --agent-id <agent-id> --source on_demand --trigger manual\n"
          "paperclipai heartbeat run --agent-id <agent-id> --timeout-ms 120000 --debug"),
 ("note", "\"For routine agent wake-ups during normal operation, prefer agent wake and the "
          "prompt-handoff flow in prompt. Reach for heartbeat run when you specifically want "
          "to watch a single run unfold.\" That is exactly this situation. --debug shows raw "
          "adapter stdout/stderr JSON chunks, and --timeout-ms defaults to 0, meaning no "
          "client-side timeout."),

 ("h3", "F8.3 A run started and failed — the launch problem"),
 ("p", "Read the run, then read its log. The invocation card in the run detail shows the "
       "command, cwd, prompt and environment with secrets redacted — which is where launch "
       "failures reveal themselves:"),
 ("code", "paperclipai run get <run-id>\n"
          "paperclipai run events <run-id> --after-seq 0 --limit 200\n"
          "paperclipai run log <run-id> --offset 0 --limit-bytes 16384\n"
          "paperclipai run log <run-id> --text"),
 ("p", "Run events report seq, eventType, stream, level and message. The documentation names "
       "the three usual root causes on the dashboard page: \"usually an API key problem, a "
       "budget running out, or a misconfigured adapter.\" Test each directly rather than "
       "inferring:"),
 ("code", "POST /api/companies/{companyId}/adapters/{type}/test-environment"),
 ("bullets", [
   "CREDENTIALS. For claude_local, testEnvironment() checks the binary, the working directory "
   "and authentication, then probes live. For codex_local the rule is \"No silent "
   "credential-less runs\" — it fails fast rather than running unauthenticated.",
   "WORKING DIRECTORY. cwd must be absolute. Claude Code session resume \"validates against a "
   "system root allowlist to prevent agent access to protected directories (/, /tmp, /var, "
   "/etc, /proc, etc.)\", so a cwd inside one of those will not behave as expected.",
   "SESSION. Claude Code \"stores the Claude Code session id and resumes it on the next "
   "heartbeat when the working directory still matches\" and falls back to a fresh session if "
   "resume fails. Codex \"preserves the previous_response_id chain\", and changing the working "
   "directory triggers a fresh session. If a corrupted session is suspected, use Reset "
   "Sessions from the agent overflow menu, or the Runs tab's \"Clear sessions for touched "
   "issues\".",
   "WORKSPACE. A workspace in degraded, failed, repairing or cleanup_failed is a common cause "
   "of an agent that appears to do nothing.",
   "ENVIRONMENT VARIABLES GENERALLY. paperclipai env prints Required and Optional sections and "
   "marks each variable set, default or missing. The required pair is PAPERCLIP_AGENT_JWT_SECRET "
   "and DATABASE_URL; PAPERCLIP_TOOL_ACTION_SIGNING_SECRET is required with no fallback.",
 ]),
 ("note", "One error kind is specifically recoverable: process_lost. The run detail offers "
          "Resume, which \"pick[s] up after process_lost error (requires resumeFromRunId)\". "
          "Try Resume before Retry — Retry starts a new run with the same task context and "
          "repeats any work already done."),

 ("h3", "F8.4 A run is stuck mid-execution"),
 ("p", "A live run streams its transcript and logs in real time. When the transcript stops "
       "updating, the run is stalled rather than working. Three things to check and one thing "
       "to do."),
 ("bullets", [
   "TIMEOUTS. claude_local timeoutSec defaults to the sandbox default of 14,400 seconds — "
   "four hours — which is far longer than most operators expect. codex_local has an "
   "outputInactivityTimeoutMs default of 420000 (seven minutes), which detects a silent "
   "runtime much faster.",
   "TURN CAP. claude_local maxTurnsPerRun defaults to 300. A run consuming turns without "
   "progressing is a prompting or acceptance-criteria problem, not an infrastructure one.",
   "WORKSPACE OPERATIONS. paperclipai run workspace-operations <run-id> reports id, status, "
   "phase, command, cwd and logBytes; paperclipai run workspace-log <operation-id> reads the "
   "log of one of them. A provision or teardown command that hangs will hang the run.",
 ]),
 ("code", "paperclipai run cancel <run-id>"),
 ("note", "\"Cancelling a run does not roll back what the agent already did.\" Cancel stops "
          "the burn; it does not undo a half-finished change. Check the issue and the "
          "workspace afterwards, and release the issue if the agent still holds it."),
 ("p", "There is also a watchdog decision surface for runs the system itself has flagged:"),
 ("code", "paperclipai run watchdog-decision <run-id> --decision continue --reason \"text\"\n"
          "paperclipai run watchdog-decision <run-id> --decision snooze --snoozed-until 2026-06-01T18:00:00Z\n"
          "paperclipai run watchdog-decision <run-id> --decision dismissed_false_positive --evaluation-issue-id <id>"),

 ("h3", "F8.5 A run succeeded but nothing moved"),
 ("p", "This is the subtlest case and the one that most rewards knowing the runtime rules."),
 ("bullets", [
   "THE COMMENT-REQUIRED BACKSTOP. Every agent run must post a comment back to the issue — a "
   "runtime invariant that is always on. If it does not, issueCommentStatus becomes "
   "retry_queued and the agent is woken with reason missing_issue_comment. Still no comment "
   "after the retry and it becomes retry_exhausted, no further retries, failure recorded. A "
   "cycle of wake-run-nothing with that wake reason is this loop.",
   "THE CROSS-ISSUE CAP. CROSS_ISSUE_INFLUENCE_LIMIT = 20 cross-issue comments or task updates "
   "combined per run; writes to the run's own source issue do not count, and the budget resets "
   "per run. Over the cap returns 429 with code cross_issue_influence_cap_exceeded. An agent "
   "doing bulk triage will hit this legitimately.",
   "CHECKOUT FAILURE. Checkout returns 409 when the issue does not match one expectedStatuses "
   "value, when the project is paused, or when the workspace is a closed isolated workspace. "
   "\"Never retry a 409 — pick a different issue.\" An agent that keeps failing checkout looks "
   "identical, from the board, to an agent doing nothing.",
   "MISSING RUN ID. Agent updates to checked-out in_progress issues require the "
   "X-Paperclip-Run-Id header. Without it the server rejects the update as a checkout-ownership "
   "violation, so the agent works and the board never changes.",
   "EXECUTION STAGE LOCK. Only the current participant can advance a stage; non-participants "
   "receive 422. Once a review has escalated, \"Only the escalated reviewer can advance the "
   "current execution stage.\" An issue sitting in in_review whose stage participant is a "
   "suspended human will never move on its own.",
   "AN INTERACTION IS WAITING. A pending interaction card — ask_user_questions, "
   "request_confirmation and the rest — parks the work on a human answer. Pending interactions "
   "expire automatically when an issue moves to done or cancelled, with status expired and "
   "result.outcome: \"issue_closed\".",
 ]),
 ("p", "Two inspection commands close this loop by showing you exactly what the agent saw:"),
 ("code", "paperclipai issue heartbeat-context <issueId>\n"
          "paperclipai agent inbox\n"
          "paperclipai issue active-run <issue-id>\n"
          "paperclipai issue recovery-actions <issue-id>"),
 ("note", "Recovery actions are Paperclip's own detection of exactly these silent stalls. The "
          "kinds are missing_disposition, stranded_assigned_issue, active_run_watchdog and "
          "issue_graph_liveness; statuses are active, escalated, resolved and cancelled; and "
          "only one active or escalated recovery action exists per source issue at a time. "
          "Resolve with an outcome of restored, false_positive, blocked or cancelled — noting "
          "that false_positive and cancelled are board-only."),

 ("h3", "F8.6 The diagnostic write-up"),
 ("p", "Whatever you find, record it in the same five fields. This is what turns an incident "
       "into an asset, and it is what an assessor or an auditor will ask for."),
 ("table", ("The five-field incident note",
   ["Field", "What goes in it"],
   [["Observation", "What you actually saw, with the timestamp. Not your theory."],
    ["Branch", "Which of the four classes in F8.1 it fell into, and the evidence for that."],
    ["Root cause", "The specific setting, credential, state or code. Name it exactly."],
    ["Fix", "The action taken, with the command or the UI path."],
    ["Prevention", "The check, cap, routine or instruction change that stops a recurrence."]])),

 ("check", [
   "State the first question you ask when told 'nothing is happening', and say why it comes "
   "first.",
   "Give three reasons an agent might never wake, in the order you would check them.",
   "What is the difference between Resume and Retry on a failed run, and when is Resume the "
   "right choice?",
   "An agent runs successfully every hour and the board never changes. Name three possible "
   "causes.",
   "Why does cancelling a run not resolve the underlying problem?",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F9
 ("h2", "F9. Cost engineering"),

 ("p", "Budgets stop a disaster. Cost ENGINEERING makes the disaster unlikely and the normal "
       "month cheaper. The two are different skills and this section is about the second."),

 ("h3", "F9.1 Reading the Costs page properly"),
 ("p", "Four headline metric tiles appear on every tab of the Costs page, and they measure two "
       "genuinely different things. Conflating them is the most common reporting error in the "
       "product."),
 ("table", ("The four headline tiles",
   ["Tile", "What it measures"],
   [["Inference spend", "Per-request model cost, shown with a token count. This is what your "
     "agents burned by thinking."],
    ["Budget", "Utilisation percentage, incident count, or \"Open\" when no cap is set."],
    ["Finance net", "Debits minus credits."],
    ["Finance events", "A count, plus estimated open debits."]])),
 ("p", "The Finance tab covers \"everything that isn't a per-request inference cost. "
       "Subscription fees, invoice reconciliations, credit top-ups, refunds, and "
       "adjustments.\" Inference is what the work cost. Finance is what the arrangement cost. "
       "A month can show flat inference and a large finance net, or the reverse, and the two "
       "call for entirely different responses."),
 ("table", ("Utilisation bar colours",
   ["Colour", "Range"],
   [["Green", "Under 70%"],
    ["Yellow", "70-90%"],
    ["Red", "Above 90%"]])),
 ("note", "The colour is a planning instrument, not an alarm. Yellow at day 10 of the month is "
          "a problem; yellow at day 28 is a well-sized cap. Read utilisation against the "
          "calendar, never on its own."),

 ("h3", "F9.2 Attributing cost to a run"),
 ("p", "Cost is not only a company-level number. Paperclip attributes it downwards, and the "
       "levels below are where you actually find the waste."),
 ("bullets", [
   "PER AGENT. The agent Dashboard tab carries a Costs section with total input, output and "
   "cached tokens plus cost, and a per-run table for the 10 most recent runs. Its activity "
   "charts run over a 14-day window: Run Activity, Issues by Priority, Issues by Status and "
   "Success Rate.",
   "PER RUN. Each entry in the Runs tab shows the status icon, short run ID, invocation source "
   "pill (Timer, Assignment, On-demand or Automation), token counts and cost, a relative "
   "timestamp and a result summary excerpt.",
   "PER PROJECT. The project Budget tab tracks metric billed_cents over a lifetime window, "
   "with observed amount, remaining amount and utilisation percent.",
 ]),
 ("p", "The INVOCATION SOURCE PILL is the most under-used diagnostic in the product. It tells "
       "you WHY each run happened. A page of Timer runs with thin result summaries is an "
       "interval set too aggressively. A page of Assignment runs is an agent doing real work. "
       "A page of On-demand runs is you, doing the agent's job manually. Sort your most "
       "expensive agent's Runs tab and read the pills before you touch any other setting."),

 ("h3", "F9.3 The four levers"),
 ("table", ("Where cost actually goes, and what to do about it",
   ["Driver", "Symptom on the Runs tab", "Lever"],
   [["Runs that should not have happened", "Many Timer runs with nothing to report",
     "Turn the interval OFF and rely on wake-on-demand. The documented recommended "
     "combination is \"Heartbeat on interval = off, Wake on demand = on\"."],
    ["Context carried needlessly", "High input-token counts on short tasks",
     "Move standing procedure out of the instruction bundle into SKILLS, which load only when "
     "relevant."],
    ["Turns spent going nowhere", "Long runs, high output tokens, vague result summaries",
     "Write acceptance criteria that name evidence. maxTurnsPerRun (default 300) is a "
     "backstop, not a plan."],
    ["Review ping-pong", "Repeated in_review to in_progress cycles on one issue",
     "maxReviewRounds defaults to 3, range 1-50. Lower it for cheap work; the escalation to a "
     "human is usually cheaper than a fourth agent round."]])),
 ("p", "The skills lever deserves its own sentence because it is the one most people miss. "
       "Moving a procedure from an always-loaded instruction file into an on-demand skill "
       "reduces the tokens consumed on every heartbeat that does not need it — which, for a "
       "specialist procedure, is most of them. The documented benefit list is exactly this: "
       "\"Fewer tokens consumed per run (lower cost)\"; \"Cleaner, more focused context for "
       "the agent (better results)\"; \"Easier to maintain\"."),
 ("note", "Two further economies are free. \"An agent that isn't doing work isn't costing you "
          "anything (past whatever the last run spent). Between heartbeats there's no idle "
          "burn.\" And on mentions: \"Don't overuse mentions — each mention triggers a "
          "budget-consuming heartbeat\", and \"Don't use mentions for assignment — create or "
          "assign a task instead.\""),

 ("h3", "F9.4 Handling a budget incident"),
 ("p", "An incident is an agent, project or company reaching 100% and being paused. Work it in "
       "this order rather than raising the cap first."),
 ("bullets", [
   "1. CONFIRM THE SCOPE. The three caps are parallel, not nested: \"An agent can be paused by "
   "its own budget limit even if the company has remaining budget.\" Agent budget hit stops "
   "the agent regardless of project headroom; project budget hit pauses the project regardless "
   "of the agent; the company budget is the overall ceiling. Identify which one fired.",
   "2. READ THE RUNS THAT SPENT IT. Sort by cost and read the invocation source pills. Decide "
   "whether the spend bought anything.",
   "3. DECIDE, THEN ACT. If the spend was productive, raise the cap. If it was not, fix the "
   "cause first — the interval, the criteria, the review rounds — and only then decide whether "
   "the cap was ever right.",
   "4. RESUME. An agent-level hard stop creates a Budget Override approval; a project hard "
   "stop is resolved either by raising the amount on the Budget tab or by resolving the budget "
   "override approval from the queue.",
 ]),
 ("note", "\"An auto-paused agent doesn't lose its work — any tasks it had in progress remain "
          "assigned to it and will pick up again once the agent is resumed.\" A budget pause "
          "is safe. It is not an emergency, and it does not need to be cleared in the first "
          "five minutes."),

 ("h3", "F9.5 Right-sizing the caps"),
 ("p", "The documentation gives starting figures. Treat them as a first month, not a policy."),
 ("table", ("Documented starting budgets",
   ["Scope", "Guidance"],
   [["CEO", "$30-50 per month"],
    ["Manager (CTO, CMO)", "$20-40 per month"],
    ["Worker agent", "$10-25 per month"],
    ["Whole company, exploration", "\"$5-20 to play with the product\""],
    ["Whole company, active", "\"$20-100/month for an active company\""]])),
 ("p", "Set the company cap FIRST, before the first hire, so there is a ceiling in place before "
       "anything can run. Then size each agent's cap from its OBSERVED first-month spend, not "
       "from the table. Monthly budgets reset to zero on the 1st of each UTC month; lifetime "
       "budgets — which is what project budgets use by default — never reset."),
 ("p", "The Budget tab fields you are setting are: Window kind (Monthly UTC or Lifetime), "
       "Amount (a cap in cents, displayed as dollars), Warn percent (the soft-alert threshold, "
       "e.g. 80%) and Hard stop (the enforcement behaviour at 100% spend). The default is "
       "pauseOnExceed = true, so \"Paperclip pauses the agent so it consumes no further budget "
       "until a board user resumes it or raises the limit.\""),
 ("note", "A cap that is never approached is not proof of discipline; it may simply be too "
          "high to have any governing effect. A well-sized monthly cap sits amber near the end "
          "of a normal month. That is the shape you are aiming for."),

 ("check", [
   "State the difference between inference spend and finance net, and give one situation that "
   "moves one without the other.",
   "Which column of the Runs tab tells you WHY a run happened, and what do you conclude from a "
   "page of Timer runs with thin summaries?",
   "Name the four cost levers and say which one is most often overlooked.",
   "An agent is paused at 100% while the company sits at 40%. Explain, and give the first "
   "thing you do.",
   "Why is a budget that is never approached a possible failure rather than a success?",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F10
 ("h2", "F10. An operating rhythm"),

 ("p", "A one-person AI company fails in one of two ways: neglect, where nobody looks and the "
       "problems compound quietly, or over-attention, where the operator does the agents' work "
       "for them and pays for the privilege twice. A rhythm is the defence against both. What "
       "follows is a suggested cadence, assembled from what the documentation says each "
       "surface is FOR. Adapt the times; keep the structure."),

 ("h3", "F10.1 Every morning — ten minutes"),
 ("p", "The dashboard is designed for exactly this. \"The dashboard is your control centre... "
       "it tells you, at a glance, whether everything is moving forward or whether something "
       "needs your attention.\" The documentation's own reading table is your checklist:"),
 ("table", ("The daily read (documentation's own healthy/attention table)",
   ["Signal", "Healthy", "Needs attention"],
   [["Agents", "Mostly active or running", "Any in error or unexpectedly paused"],
    ["Tasks in progress", "Work is moving",
     "Nothing in progress for hours, or too many blocked issues"],
    ["Month spend", "Climbing predictably", "Sudden jump or active budget incidents"],
    ["Approvals", "Queue manageable", "Pending approvals piling up"],
    ["Recent activity", "Steady, understandable motion",
     "Long stretches of silence or repeated failures"]])),
 ("p", "Then three specific actions, in this order:"),
 ("bullets", [
   "CLEAR THE APPROVALS QUEUE. \"Approvals don't expire on their own. If an approval is "
   "pending, agents that are waiting on it will pause at that point until you take action.\" "
   "An unread approvals queue is a stopped company. Work both the pending and the "
   "revision_requested items — the actionable set is \"approvals in the pending state and any "
   "in revision_requested\".",
   "CLEAR THE BLOCKED INBOX. Every blocked issue is an agent waiting on you. Check whether the "
   "blocker is a first-class blockedByIssueIds link or a free-text comment — the latter never "
   "auto-wakes anything.",
   "TRIAGE ANY error AGENT. \"Any agent showing 'error' needs attention. The error won't fix "
   "itself.\" Open the agent's Runs tab and read the transcript.",
 ]),
 ("note", "Ten minutes is the target and it is achievable, but only if you resist opening a "
          "run transcript out of curiosity. Note it, and do it in the weekly slot. The daily "
          "pass is a pulse check: \"This feed isn't meant for deep investigation — it's a "
          "pulse check.\""),

 ("h3", "F10.2 Every week — an hour"),
 ("bullets", [
   "COST REVIEW. Work F9.2. Open the most expensive agent's Runs tab, read the invocation "
   "source pills and the result summaries, and decide whether the month is going where you "
   "want it to. Compare utilisation against the day of the month.",
   "STALE WORK SWEEP. Anything in in_progress for days, anything in in_review with no "
   "movement, anything in blocked whose blocker is already done. This is exactly what the "
   "bundled Issue Triage skill is for — \"classify stale, blocked, in-review, or stalled "
   "Paperclip issues and choose the next action\" — so consider making it a routine rather "
   "than a habit.",
   "REVIEW-ROUND CHECK. Look for issues that have cycled between in_review and in_progress. "
   "changesRequestedCount counts consecutive AGENT-initiated rounds and resets to 0 when a "
   "stage is approved or when a HUMAN requests changes — \"Only counts agent-to-agent "
   "ping-pong.\" Repeated cycling means your acceptance criteria are ambiguous.",
   "ROUTINE HEALTH. Check routine states — paused, draft, archived, succeeded, failed, "
   "running. A failed routine is silent by nature.",
   "BACKUP VERIFICATION. Confirm last night's db:backup exists and is the size you expect. A "
   "backup you have not looked at is a hypothesis.",
 ]),

 ("h3", "F10.3 Every month — half a day"),
 ("bullets", [
   "AUDIT THE ACTIVITY LOG. The audit:view_agent_actions grant opens the company Audit feed "
   "and allows a CSV download. Export it and read for gaps and surprises — an unexplained "
   "silence is as informative as an unexplained action.",
   "REVIEW MEMBERSHIP AND GRANTS. Every member row, every explicit grant. Remember that "
   "explicit grants persist across role changes and there is no deny layer, so grants "
   "accumulate unless someone removes them. Suspend anyone who has left. Revoke their tokens.",
   "ROTATE CREDENTIALS. Rotate provider keys on a schedule you decide rather than on the day "
   "one leaks. With secret_refs on version \"latest\", rotation needs no agent "
   "reconfiguration.",
   "RE-SIZE BUDGETS. Monthly budgets reset on the 1st UTC, which makes the first week the "
   "natural moment to reset caps from last month's observed spend.",
   "REVIEW THE SKILL LIBRARY. Which skills are actually attached and used? Run an audit on any "
   "imported skill; check update-status on GitHub-sourced skills; delete what nobody uses.",
   "PRUNE THE ORG CHART. Terminate agents that no longer have a job — terminate, not delete: "
   "\"Terminating stops the agent permanently and preserves it as a terminated record. "
   "Deletion is the destructive action.\" Check no terminated agent is still someone's "
   "manager, which produces the Invalid Org Chain banner.",
 ]),

 ("h3", "F10.4 Automating the rhythm"),
 ("p", "Some of the above should be a routine rather than a habit, because a habit degrades "
       "and a routine does not. Routines carry a cron schedule in your timezone, and minutes "
       "snap to five-minute increments. Candidates: the stale-work sweep (Issue Triage), a "
       "documentation pass (Doc Maintenance), and a weekly summary produced by whichever agent "
       "owns reporting."),
 ("note", "Do not automate the approvals queue, the error triage or the audit read. Those are "
          "the three places where your judgement is the product, and the whole governance "
          "model — \"Agents propose, people decide\" — depends on a human actually being in "
          "the loop rather than nominally in it. There is also an emergency brake worth "
          "knowing: paperclipai routines disable-all --company-id <id> pauses every "
          "non-archived routine in one company. There is no enable-all counterpart, so use it "
          "deliberately."),

 ("check", [
   "List the three actions in the ten-minute daily pass, in order.",
   "Why is an unread approvals queue equivalent to a stopped company?",
   "Which weekly check would catch ambiguous acceptance criteria, and what is the signal?",
   "Name three things that belong in the monthly audit and one thing that must never be "
   "automated.",
   "Design a routine for your own stale-work sweep: which agent owns it, which skill does it "
   "use, and what does it produce?",
 ]),
 ("rule",),

 # ───────────────────────────────────────────────────────────── F11
 ("h2", "F11. Taking this to production"),

 ("p", "The gap between a working lab and a production deployment is not technical. Everything "
       "in Parts A to F already works. The gap is that in production you are accountable for "
       "spend you did not personally authorise, for changes you did not personally make, and "
       "for evidence you may have to produce months later. This closing chapter is a staged "
       "path across that gap."),

 ("h3", "F11.1 The staging principle"),
 ("p", "Prove the AUDIT before you scale the WORK. It is tempting to reverse this — to get the "
       "agents productive first and worry about the trail later — and it is the reversal that "
       "produces companies nobody can safely operate. An audit trail is retrospective; you "
       "cannot add one to work that has already happened."),
 ("table", ("The four stages",
   ["Stage", "Scope", "The question it answers", "Exit criterion"],
   [["1. One workflow", "One agent, one project, one recurring piece of work",
     "Does an agent actually complete this work to the standard we need?",
     "Three consecutive successful runs producing verifiable output."],
    ["2. Cap low", "The same workflow, with caps deliberately tight",
     "What does this cost, and does the enforcement behave as documented?",
     "A budget pause has occurred and been handled without drama."],
    ["3. Prove the audit", "The same workflow, audited end to end",
     "Can a third party reconstruct what happened, from records alone?",
     "Someone who was not present reconstructs one week's work from the activity log and the "
     "issue threads."],
    ["4. Scale", "Additional agents, projects and routines, one at a time",
     "Does the structure hold as the number of moving parts rises?",
     "Each addition passes stages 1-3 on its own before the next begins."]])),

 ("h3", "F11.2 Stage 1 — one workflow"),
 ("p", "Pick the least glamorous recurring task you have. It should be work you understand "
       "well enough to check, that happens often enough to be worth automating, and whose "
       "failure is survivable."),
 ("bullets", [
   "Write the mission as one sentence. If you cannot, you do not yet understand the work well "
   "enough to delegate it.",
   "ONE agent. The feasibility test from Part A applies unchanged: if the inputs, tools, "
   "authority and verification are the same across the whole task, do not split it.",
   "Interval OFF, wake-on-demand ON — the documented recommended combination. Trigger runs "
   "deliberately while you are still learning what they cost.",
   "Acceptance criteria that name EVIDENCE, not intent. \"Produces report.md in the workspace "
   "with sections X, Y and Z\" is checkable; \"summarises the data\" is not.",
   "Prove the runtime with a marker run before you trust anything else. A healthy /api/health "
   "proves the control plane; only an artifact in the workspace proves the runtime.",
 ]),

 ("h3", "F11.3 Stage 2 — cap low"),
 ("p", "Set the caps below what you expect to need. The purpose of this stage is to make the "
       "enforcement fire while the stakes are trivial, so you learn the mechanics on your own "
       "terms."),
 ("bullets", [
   "Set the COMPANY cap first, then the agent cap. They are parallel, not nested.",
   "Set Warn percent so the warning arrives with time to act. The documented warn threshold "
   "is 80%, with pause at 100% and pauseReason = \"budget\".",
   "Let it pause at least once, on purpose. Confirm that the pause behaves as documented: "
   "in-progress tasks stay assigned and resume when the agent does.",
   "Practise the resume path — raising the cap, or resolving the Budget Override approval — "
   "before you need it under pressure.",
   "Record the observed monthly cost. That figure, not the documentation's table, is what you "
   "size the real cap from.",
 ]),

 ("h3", "F11.4 Stage 3 — prove the audit"),
 ("p", "This is the stage most operators skip and the one that determines whether the "
       "deployment survives its first serious question. The test is concrete: hand one week of "
       "the company's work to someone who was not there, and see whether they can reconstruct "
       "it."),
 ("table", ("What must be reconstructible, and from where",
   ["Question", "Where the answer lives"],
   [["What was decided, by whom, and when?",
     "The activity log; approval records carrying decisionNote, decidedByUserId and decidedAt."],
    ["Who did this piece of work?",
     "The issue's assignee and checkoutRunId; the run record; the X-Paperclip-Run-Id "
     "attribution on every mutating request."],
    ["Why was it accepted?",
     "The execution decision record — actor, outcome, a REQUIRED comment body, and "
     "createdByRunId. Both approvals and change requests require a comment; empty bodies are "
     "rejected."],
    ["What did it cost?", "The run's token counts and cost; the agent Costs section; the "
     "budget policy's observed amount."],
    ["What credential was used, and who read it?",
     "Every secret value read is logged to the security audit trail and the activity log."]])),
 ("bullets", [
   "Grant audit:view_agent_actions to whoever is accountable, and export the Audit feed to CSV "
   "at least once so you know the export works.",
   "Use execution policy on anything consequential — a review stage, an approval stage, or "
   "both. \"Runtime-enforced, not prompt-dependent\" is the whole point: an agent cannot "
   "forget to seek review, because the runtime does not offer it the option.",
   "Confirm the escalation path resolves to a real, active human. responsibleUserId with a "
   "fallback to createdByUserId is where an escalated review lands; if neither exists, work "
   "hands back to the implementer and the counter climbs for visibility only.",
   "Check that the trail survives a restart. Run through the restore workflow in F7.5 on a "
   "copy, and confirm the history came with it.",
 ]),

 ("h3", "F11.5 Stage 4 — scale"),
 ("p", "Only now add. The discipline is that each addition passes stages 1 to 3 on its own "
       "before the next begins. The failure mode is adding three agents at once and losing the "
       "ability to attribute a cost, a change or a decision to any one of them."),
 ("bullets", [
   "Add ONE agent at a time. Every additional agent is another workspace, another instruction "
   "bundle, another budget line and another audit trail — forever.",
   "Add a routine only when the work has proved itself as a manual habit first.",
   "Move to authenticated mode BEFORE the second human needs access, not on the day they ask.",
   "Turn on strict mode for secrets before the credential count grows, remembering that it "
   "blocks new inline values rather than migrating existing ones.",
   "Re-run the feasibility scan each time. The correct instinct is still to reach for one "
   "agent and be argued out of it.",
 ]),

 ("h3", "F11.6 Production readiness checklist"),
 ("p", "Work down the list. Anything you cannot tick is a decision you have made by default "
       "rather than on purpose."),
 ("table", ("Readiness checklist",
   ["Area", "Check", "Evidence that it is done"],
   [["Platform", "Node.js 20+ confirmed; doctor passes cleanly",
     "node --version output; a clean paperclipai doctor run"],
    ["Platform", "Required environment variables present",
     "paperclipai env shows PAPERCLIP_AGENT_JWT_SECRET and DATABASE_URL as set, and "
     "PAPERCLIP_TOOL_ACTION_SIGNING_SECRET present (it has no fallback)"],
    ["Access", "Deployment mode matches who needs access",
     "local_trusted only if genuinely single-operator; otherwise authenticated with the right "
     "exposure"],
    ["Access", "Hostname allowlist correct for authenticated + private",
     "paperclipai allowed-hostname run, and the server restarted"],
    ["Access", "Every human has the least role that lets them work",
     "The Access page reviewed; explicit grants deliberate, not inherited"],
    ["Secrets", "Master key backed up somewhere off this machine",
     "A restore rehearsal, not merely a copied file"],
    ["Secrets", "No inline sensitive values in adapter, project or routine env",
     "Strict mode on; the migration dry run reports nothing outstanding"],
    ["Secrets", "Rotation rehearsed",
     "One provider key rotated with agents left on version \"latest\", and a successful run "
     "afterwards"],
    ["Budgets", "Company cap set BEFORE any agent could run",
     "The cap predates the first hire in the activity log"],
    ["Budgets", "Per-agent caps sized from observed spend, not from the guide table",
     "Last month's figures"],
    ["Budgets", "One pause survived and resumed",
     "The incident and its resolution recorded"],
    ["Governance", "Board approval required for hires, if that is your intent",
     "Settings → Hiring toggle set deliberately"],
    ["Governance", "Execution policy on consequential work",
     "Reviewer and/or Approver set; maxReviewRounds chosen rather than defaulted"],
    ["Governance", "Escalation resolves to an active human",
     "responsibleUserId points at an active membership"],
    ["Operations", "Heartbeat intervals justified per agent",
     "Interval off unless there is a reason it must be on"],
    ["Operations", "The daily, weekly and monthly rhythm is scheduled",
     "Diary entries or routines, not intentions"],
    ["Recovery", "Nightly db:backup running and verified",
     "A backup file from last night, of a plausible size"],
    ["Recovery", "A company export taken and re-imported successfully",
     "The rehearsal, with the Preview screen read rather than skipped"],
    ["Recovery", "The restore runbook written down",
     "The eight steps of F7.5, adapted to your instance"],
    ["Audit", "audit:view_agent_actions granted to the accountable person",
     "The grant, and one successful CSV export"],
    ["Audit", "One week reconstructible by someone who was not present",
     "They did it, and told you what they could not find"]])),
 ("note", "The last line of that table is the real test. Everything above it is preparation for "
          "it. If a colleague can take your activity log, your issue threads and your run "
          "records and tell you what your company did last week — including what it decided, "
          "what it spent and who signed it off — then you are operating an auditable AI "
          "organisation rather than an impressive demonstration. That distinction is the whole "
          "purpose of a control plane, and it is what you will be assessed on."),

 ("check", [
   "State the staging principle in one sentence and say why the order cannot be reversed.",
   "Give the exit criterion for each of the four stages.",
   "Why is 'cap low' a stage in its own right rather than a setting?",
   "Name the five questions that must be reconstructible from records, and where each answer "
   "lives.",
   "Pick three lines from the readiness checklist that your own current setup would fail, and "
   "write the action that would close each one.",
 ]),
 ("rule",),
]

ADVANCED_CHAPTERS = PART_F
