# Security Policy - Two Fast Auth

## Supported Versions

We currently provide security updates for the following versions of Two Fast Auth:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Two Fast Auth seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly** until it has been addressed by the maintainers.
2. **Report the vulnerability through GitHub's security advisory feature**:
   - Go to the [Security tab](https://github.com/rennf93/two-fast-auth/security/advisories) of the Two Fast Auth repository
   - Click on "New draft security advisory"
   - Fill in the details of the vulnerability
   - Submit the advisory

   Alternatively, you can report vulnerabilities through [GitHub's private vulnerability reporting feature](https://github.com/rennf93/two-fast-auth/security/advisories/new).

3. Include the following information in your report:
   - A description of the vulnerability and its potential impact
   - Steps to reproduce the issue
   - Affected versions
   - Any potential mitigations or workarounds

The maintainers will acknowledge your report within 48 hours and provide a detailed response within 7 days, including the next steps in handling the vulnerability.

## Security Best Practices

When using Two Fast Auth in your applications, consider the following security best practices:

### Configuration Recommendations

1. **Encryption Key**: Always use a strong, unique encryption key when enabling secret encryption. Store this key securely using environment variables or a secure secrets management system, not hardcoded in your application.

2. **Excluded Paths**: Carefully consider which paths to exclude from 2FA verification. Only exclude essential paths like login, setup, and public documentation.

3. **Custom Header Name**: Consider changing the default header name (`X-2FA-Code`) to a custom value in production environments to make it less predictable.

4. **Secret Storage**: Implement secure storage for user 2FA secrets, preferably using the encryption feature provided by Two Fast Auth.

5. **Recovery Codes**: Implement a secure system for generating, storing, and validating recovery codes.

### Implementation Security

1. **Rate Limiting**: Implement rate limiting on 2FA verification attempts to prevent brute force attacks.

2. **Secure Communication**: Always use HTTPS in production to protect 2FA codes in transit.

3. **Session Management**: Implement proper session management and invalidate sessions appropriately.

4. **Audit Logging**: Log 2FA-related events (setup, verification attempts, recovery code usage) for security monitoring.

### Dependency Management

1. Regularly update Two Fast Auth and its dependencies to the latest versions.
2. Use a dependency scanning tool to identify and address vulnerabilities in your dependency tree.

## Security Features

Two Fast Auth provides several security features to protect your FastAPI applications:

- Time-based One-Time Password (TOTP) verification
- QR code generation for authenticator apps
- Optional secret encryption using Fernet
- Recovery code generation and management
- Middleware integration with FastAPI

For detailed information on configuring these features, refer to the [documentation](https://rennf93.github.io/two-fast-auth/).

## Threat Model

Two Fast Auth is designed to protect against common authentication threats, including:

- Credential theft and account takeover
- Brute force attacks against authentication
- Man-in-the-middle attacks (when used with HTTPS)
- Phishing attacks (mitigated by time-based codes)

Note that Two Fast Auth should be used alongside other security controls such as proper password management, session handling, and input validation.

## Security Updates

Security updates will be released as needed. We recommend subscribing to GitHub releases or regularly checking for updates to ensure you're using the most secure version.

## Responsible Disclosure

We follow responsible disclosure principles. If you report a vulnerability to us:

1. We will confirm receipt of your vulnerability report
2. We will provide an estimated timeline for a fix
3. We will notify you when the vulnerability is fixed
4. We will publicly acknowledge your responsible disclosure (unless you prefer to remain anonymous)

## License

Two Fast Auth is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
