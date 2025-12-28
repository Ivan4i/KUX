/**
 * Environment variable utilities
 */

export function getEnv(name: string, defaultValue?: string): string {
  const value = process.env[name];
  if (value === undefined || value === '') {
    if (defaultValue !== undefined) {
      return defaultValue;
    }
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

export function getEnvOptional(name: string): string | undefined {
  const value = process.env[name];
  return value === '' ? undefined : value;
}

export function getEnvBoolean(name: string, defaultValue = false): boolean {
  const value = process.env[name]?.toLowerCase();
  if (value === undefined || value === '') {
    return defaultValue;
  }
  return value === 'true' || value === '1' || value === 'yes';
}

export interface ServiceConfig {
  name: string;
  envVars: string[];
  enabled: boolean;
  missingVars: string[];
}

export function checkServiceConfig(name: string, requiredVars: string[]): ServiceConfig {
  const missingVars = requiredVars.filter(v => !process.env[v]);
  return {
    name,
    envVars: requiredVars,
    enabled: missingVars.length === 0,
    missingVars,
  };
}

export function listConfiguredServices(): ServiceConfig[] {
  return [
    checkServiceConfig('GitHub', ['GITHUBTOKEN']),
    checkServiceConfig('Figma', ['FIGMATOKEN']),
    checkServiceConfig('Cloudflare', ['CLOUDFLAREAPITOKEN']),
    checkServiceConfig('Vercel', ['VERCELTOKEN']),
    checkServiceConfig('Notion', ['NOTIONTOKEN']),
    checkServiceConfig('Linear', ['LINEARTOKEN']),
    checkServiceConfig('Sentry', ['SENTRYAUTHTOKEN']),
    checkServiceConfig('Cloudinary', ['CLOUDINARYCLOUDNAME', 'CLOUDINARYAPIKEY', 'CLOUDINARYAPISECRET']),
    checkServiceConfig('Postman', ['POSTMANAPIKEY']),
    checkServiceConfig('Datadog', ['DATADOGAPIKEY', 'DATADOGAPPKEY']),
    checkServiceConfig('CloudWatch', ['AWSACCESSKEYID', 'AWSSECRETACCESSKEY', 'AWSREGION']),
    checkServiceConfig('ELK', ['ELKURL']),
    checkServiceConfig('Box', ['BOXCLIENTID', 'BOXCLIENTSECRET']),
    checkServiceConfig('Canva', ['CANVAAPIKEY']),
    checkServiceConfig('Clarity', ['CLARITYPROJECTID']),
    checkServiceConfig('Supabase', ['SUPABASEACCESSTOKEN']),
    checkServiceConfig('MongoDB', ['MONGODBPUBLICKEY', 'MONGODBPRIVATEKEY']),
  ];
}
