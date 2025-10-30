# rebase-base-identity-service

## 0.2.3 - 20/10/2025

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