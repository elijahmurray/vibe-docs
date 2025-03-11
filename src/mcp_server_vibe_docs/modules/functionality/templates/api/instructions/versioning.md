# API Versioning

## Project: {{project_name}}

## Versioning Strategy
The API uses a semantic versioning scheme to manage changes and updates. Versions are specified in the URL path.

## Version Format
- `v{major}`: e.g., v1, v2, v3
- Major version increments indicate breaking changes

## Current Version
The current version of the API is **v1**:
```
https://api.example.com/v1/resources
```

## Backward Compatibility
- Within the same major version, backward compatibility is maintained
- New endpoints and response fields may be added without incrementing the major version
- Existing endpoints and fields will not be removed or changed within a major version

## Version Support Policy
- Each major version is supported for a minimum of 12 months after the release of a newer version
- Deprecation notices will be provided at least 3 months before a version is sunset
- Critical security fixes will be applied to all supported versions

## Version Transition
When migrating from one API version to another:
1. Review the migration guide for breaking changes
2. Update client code to handle any changed endpoints or parameters
3. Test thoroughly with the new version before deploying to production
4. Consider running both versions in parallel during the transition period

## Version Headers
The API also supports specifying the version via the `Accept` header:
```
Accept: application/vnd.api.example.com+json;version=1
```