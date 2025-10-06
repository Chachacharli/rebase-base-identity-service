# rebase-base-identity-service

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