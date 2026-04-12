# Security Policy

## Reporting a vulnerability

Please report security issues privately via GitHub's **Private vulnerability reporting** feature:

1. Go to the **Security** tab of this repository
2. Click **Report a vulnerability**
3. Fill in the form — I'll respond as soon as I can

Do not file public issues for security problems.

## Known limitations

Yesanio has **no built-in authentication**. It is designed for trusted local networks (home server behind Tailscale, Cloudflare Tunnel, or localhost-only use). Do not expose it to the public internet without adding authentication at the reverse-proxy layer.

Default database credentials in `docker-compose.yml` are intentionally named `*_change_me` as a prompt to change them before deployment. Change them.

## Scope

Security issues in scope include:

- SQL injection or similar database escape
- Authentication bypass (if authentication is added)
- Cross-site scripting in the frontend
- Unsafe deserialisation
- Credential disclosure

Out of scope:

- Missing authentication (this is by design; see above)
- Local network attacks (Yesanio assumes a trusted local network)
- Social engineering of the maintainer
