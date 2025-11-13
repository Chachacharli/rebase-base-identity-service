# rebase-base-identity-service

# 0.4.0 - 12/11/2025
## Summary 
Implemented an endpoint to retrieve user information based on the user ID extracted from the access token. This endpoint provides essential user details such as user ID, username, email, full name (soon), and active status.

## Improvements
- Added `/v1/userinfo` endpoint to fetch user information using the user ID from the access token.
- Created `UserInfoSchema` to structure the user information response.

### Corrections

### Decrements


## 0.3.0 - 05/11/2025

### Summary
Added management of roles and permissions for users.
Implementation of health check endpoints using FastAPI. These endpoints provide basic health status information for the service. 
Refactor the refresh token lifecycle and `TokenGrantHandler` to better handle handlers in an abstract way.
Refactored endpoints to use service layers for roles and permissions, improving separation of concerns and maintainability.
Enhanced username and password validation to return missing rules as a dictionary in custom exceptions.
Adjusted role endpoints to avoid redundant permission parameters.
Added custom validation logic for username and password during user creation.
Implement better readme documentation for users, roles, and permissions management system.

### Improvements
- Implement CRUD for Roles, Permissions, and Role-Permission and User-Roles assignments.
- Added health check endpoints for monitoring service status, including a root health endpoint and a detailed health status endpoint. (Basic structure for future health checks like database connectivity, external service status, etc.)
- Add dependency to retrieve the current user from the token for protected endpoints.
- Refactored role and permission endpoints to use `RoleService` and `PermissionService` instead of direct repository access.
- Username and password validation now returns a dict with missing rules in custom exceptions.
- Role permission endpoints now receive `role_id` only in the request body, not in the route.
- Added custom validation for username and password in user creation.

### Corrections
- Fixed refresh token lifecycle management to ensure proper handling of token expiration and renewal.
- Fixed typing in role and permission services.
- Fixed usage of custom exceptions in username and password validation.

### Decrements


## 0.2.3 - 29/10/2025

### Summary
Now the token expiration handling uses the configured TTL values for access and refresh tokens, all this from the application settings table.

### Improvements

### Corrections
- Fixed token expiration handling to use configured TTL values.

### Decrements

## 0.2.2 - 20/10/2025

### Summary
Refactor the AuthorizationCodeGrantHandler to accept a strongly typed request object instead of a generic dictionary. This enhances type safety and code clarity.
Now is posible to create an access token linked to a refresh token in the database.

### Improvements
- Refactored AuthorizationCodeGrantHandler to use AuthorizationCodeGrantRequest object.
- Enhanced type safety and code clarity by replacing generic dictionaries with strongly typed objects.

### Corrections
//

### Decrements
//


## 0.2.1 - 05/10/2025

### Summary
Implement refresh token and access token as opaque tokens. Change refresh_token foreign key to client_application.client_id, and refactor authorization code handling to enhance refresh token management. 

### Improvements
- Implementation of refresh token and access token as opaque tokens.
- Refactored authorization code handling for better clarity and maintainability.
- Implement user management with user creation endpoint and update authentication service.
- Now is possible validate a refresh token saved in database.
- Integrate introspection and revocation endpoint.

### Corrections
- Fixed Foreign Key relationship for refresh_token to use client_application.client_id.

### Decrements
//

## 0.2.0 - 20/09/2025

### Summary
The necessary logic is added to return an HTML template with `Jinja2Templates` in order to post the end customer's password and username. 

### Improvements
- Implementation of HTML templates using `Jinja2Templates` for rendering login forms.
- Enhanced user experience with a structured login page.

### Corrections
//

### Decrements
- The last access grand_type without an username and password is deprecated.