/**
 * Stub Services - Box, Canva, Microsoft Clarity
 * Placeholder implementations with helpful error messages
 */

import { getEnvOptional } from '../utils/env.js';

export interface StubServiceInfo {
  name: string;
  status: 'not_implemented';
  message: string;
  requiredEnvVars: string[];
  envVarsPresent: string[];
  envVarsMissing: string[];
  docsUrl: string;
  implementationHint: string;
}

function checkStubService(
  name: string,
  requiredEnvVars: string[],
  docsUrl: string,
  implementationHint: string
): StubServiceInfo {
  const envVarsPresent = requiredEnvVars.filter(v => getEnvOptional(v));
  const envVarsMissing = requiredEnvVars.filter(v => !getEnvOptional(v));

  return {
    name,
    status: 'not_implemented',
    message: `${name} integration is not yet implemented. See implementation hints below.`,
    requiredEnvVars,
    envVarsPresent,
    envVarsMissing,
    docsUrl,
    implementationHint,
  };
}

// ============================================================================
// BOX
// ============================================================================

export function boxListFiles(): StubServiceInfo {
  return checkStubService(
    'Box',
    ['BOXCLIENTID', 'BOXCLIENTSECRET', 'BOXENTERPRISEID'],
    'https://developer.box.com/reference/',
    `
Box requires OAuth2 authentication. To implement:

1. Create a Box App at https://developer.box.com/console
2. Choose "Custom App" with "Server Authentication (with JWT)"
3. Download the JSON config file
4. Set environment variables:
   - BOX_CLIENT_ID: from config
   - BOX_CLIENT_SECRET: from config
   - BOX_ENTERPRISE_ID: from config
   - BOX_JWT_PRIVATE_KEY: contents of private key
   - BOX_JWT_PASSPHRASE: passphrase for key
   - BOX_JWT_KEY_ID: public key ID

5. Install box-node-sdk: npm install box-node-sdk
6. Implement in mcp-kit/mcp/saas-gateway/src/services/box.ts

Example API calls:
- List folders: GET /folders/{folder_id}/items
- Get file info: GET /files/{file_id}
- Search: GET /search?query={query}
    `.trim(),
  );
}

export function boxGetFile(_fileId: string): StubServiceInfo {
  return boxListFiles();
}

// ============================================================================
// CANVA
// ============================================================================

export function canvaListDesigns(): StubServiceInfo {
  return checkStubService(
    'Canva',
    ['CANVAAPIKEY', 'CANVABRANDID'],
    'https://www.canva.dev/docs/connect/',
    `
Canva Connect API requires OAuth2 authentication.

1. Register at https://www.canva.dev/
2. Create an integration (Connect API)
3. Configure OAuth scopes:
   - design:content:read
   - design:meta:read
   - folder:read
   - brand_template:content:read
   - brand_template:meta:read

4. Set environment variables:
   - CANVA_API_KEY: your API key
   - CANVA_CLIENT_ID: OAuth client ID
   - CANVA_CLIENT_SECRET: OAuth client secret
   - CANVA_BRAND_ID: (optional) default brand ID

5. Implement OAuth flow for user token
6. Implement in mcp-kit/mcp/saas-gateway/src/services/canva.ts

Example API calls:
- List designs: GET /v1/designs
- Get design: GET /v1/designs/{designId}
- List folders: GET /v1/folders
    `.trim(),
  );
}

export function canvaGetDesign(_designId: string): StubServiceInfo {
  return canvaListDesigns();
}

// ============================================================================
// MICROSOFT CLARITY
// ============================================================================

export function clarityGetDashboard(): StubServiceInfo {
  return checkStubService(
    'Microsoft Clarity',
    ['CLARITYPROJECTID', 'CLARITYAPIKEY'],
    'https://docs.microsoft.com/en-us/clarity/',
    `
Microsoft Clarity provides web analytics.

Note: Clarity has limited API access. Most data is accessed via:
- Dashboard: https://clarity.microsoft.com/
- Data export: Manual or scheduled exports

For API access (if available):
1. Go to https://clarity.microsoft.com/
2. Create/select a project
3. Get Project ID from URL or settings
4. Check for API access in project settings

Set environment variables:
- CLARITY_PROJECT_ID: your project ID
- CLARITY_API_KEY: API key (if available)

Currently, Clarity mainly supports:
- Embedding the tracking script
- Viewing data in the dashboard
- Exporting data manually

For programmatic access, consider:
- Scheduled exports to cloud storage
- Using Clarity's integration with Azure

Implement in mcp-kit/mcp/saas-gateway/src/services/clarity.ts
    `.trim(),
  );
}

export function clarityGetHeatmaps(): StubServiceInfo {
  return clarityGetDashboard();
}

export function clarityGetRecordings(): StubServiceInfo {
  return clarityGetDashboard();
}
