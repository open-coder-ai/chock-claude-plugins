---
name: chock-java-security
description: "Refuses a named set of Java constructs that cannot be correct -- string-concatenated MyBatis SQL, unescaped template output, unsafe deserialization, a wildcard CORS origin with credentials, wildcard actuator exposure, and an unverified JWT parse -- at the moment the agent writes them. Every rule carries a per-repo allow|deny|ask verdict; an absent file, pack or rule denies, so an upgrade never ships a silently inert rule."
metadata:
  chock.artifact: hook
  chock.enforcement: block
  chock.hooks: hooks/hooks.json
---

# Java security (chock-security)

Refuses a named set of Java constructs that cannot be correct -- string-concatenated MyBatis SQL, unescaped template output, unsafe deserialization, a wildcard CORS origin with credentials, wildcard actuator exposure, and an unverified JWT parse -- at the moment the agent writes them. Every rule carries a per-repo allow|deny|ask verdict; an absent file, pack or rule denies, so an upgrade never ships a silently inert rule.

```
never(expose): management.endpoints.web.exposure.include=* -- it publishes heapdump and env; name the endpoints served
never(pair): CORS origin "*" with allowCredentials(true) -- the spec refuses it; name the origins, or use setAllowedOriginPatterns
never(call): parseClaimsJwt|parseUnsecuredClaims|Algorithm.none -- they skip the signature; use parseClaimsJws|parseSignedClaims with a key
never(interpolate): mybatis ${...} in mapper|@Select|@Insert|@Update|@Delete -- ${} is pasted into the SQL text before preparing; bind with #{...}
never(enable): jackson activateDefaultTyping|enableDefaultTyping; never(build): XStream without allowTypes|allowTypeHierarchy
never(write): th:utext|<%=|escapeXml="false"|?no_esc|<#noescape> -- these put a value into the page as markup; use the escaping sibling
```

These constraints are enforced in this client by the PreToolUse and Stop hooks installed with the plugin, subject to the fail conditions stated in the plugin description. Enforcement at every commit and in CI needs `chock-security init` in the repository. See https://github.com/open-coder-ai/chock-java-security
