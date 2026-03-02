# Replication Checklist

## Core
- Mark replicated properties explicitly.
- Implement `GetLifetimeReplicatedProps`.
- Use `ReplicatedUsing` + `OnRep_...` for client-side refresh.

## RPC
- Expose client request function.
- Route to `Server, Reliable` RPC.
- Re-validate server-side before mutation.

## Common Failures
- Missing authority checks.
- RepNotify not firing due to unchanged values.
- Mutable state changed only on client.
