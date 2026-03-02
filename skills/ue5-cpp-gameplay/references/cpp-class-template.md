# UE5.6/UE5.7 C++ Class Template

## Header Checklist
- `#pragma once`
- Include only required base headers.
- Forward declare external classes.
- Use `UCLASS/USTRUCT/UENUM` only when reflection is needed.
- Use `TObjectPtr<>` for UObject pointers in UPROPERTY fields.

## Source Checklist
- Include matching header first.
- Include concrete dependencies used by implementation.
- Validate pointers and world context before use.
- Keep gameplay side effects isolated in clear functions.

## Output Contract
- Return full `.h` and `.cpp`.
- Mention module include/dependency additions if needed.
