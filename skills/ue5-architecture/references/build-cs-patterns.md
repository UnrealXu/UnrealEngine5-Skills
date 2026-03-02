# Build.cs Patterns (UE5.6/UE5.7)

## Runtime Module Pattern
```csharp
PublicDependencyModuleNames.AddRange(new string[] {
  "Core", "CoreUObject", "Engine"
});
PrivateDependencyModuleNames.AddRange(new string[] {
  "Slate", "SlateCore", "UMG"
});
```

## Editor Module Pattern
```csharp
PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine" });
PrivateDependencyModuleNames.AddRange(new string[] {
  "UnrealEd", "AssetTools", "Slate", "SlateCore"
});
```

## Dependency Decision Rules
- Put a module in `PublicDependencyModuleNames` only when public headers include its types.
- Prefer private dependencies for implementation-only usage.
- Remove unused dependencies after refactor to reduce compile and link overhead.
