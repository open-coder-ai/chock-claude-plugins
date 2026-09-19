---
name: chock-java-security
description: "Refuses a named set of Java constructs that cannot be correct -- string-concatenated MyBatis SQL, unescaped template output, unsafe deserialization, a wildcard CORS origin with credentials, wildcard actuator exposure, and an unverified JWT parse -- at the moment the agent writes them. Every rule carries a per-repo allow|deny|ask verdict; an absent file, pack or rule denies, so an upgrade never ships a silently inert rule."
metadata:
  chock.artifact: rule
  chock.enforcement: advise
  chock.coverage_without_chock: advisory
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

This skill is advisory: the client reading it has no mechanism here to enforce it. The same rules installed as the Claude-format package become PreToolUse and Stop hooks that refuse the write. See https://github.com/open-coder-ai/chock-java-security
