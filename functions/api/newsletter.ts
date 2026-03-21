// Cloudflare Function for newsletter subscription
// This replaces the Next.js API route for static export deployments

interface Env {
  BEEHIIV_API_KEY: string
  BEEHIIV_PUBLICATION_ID: string
  ALLOWED_ORIGINS?: string
}

interface NewsletterRequest {
  email: string
}

interface BeeHiivErrorResponse {
  message?: string
  errors?: Array<{ message: string }>
}

// Email validation regex (RFC 5322 simplified)
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// Sanitize email to prevent injection
function sanitizeEmail(email: string): string {
  return email.trim().toLowerCase()
}

// Validate email format
function isValidEmail(email: string): boolean {
  return EMAIL_REGEX.test(email) && email.length <= 254
}

export async function onRequestPost(context: { request: Request; env: Env }) {
  const { request, env } = context

  // Get allowed origins from env or use default
  const allowedOrigins = env.ALLOWED_ORIGINS 
    ? env.ALLOWED_ORIGINS.split(',').map(o => o.trim())
    : ['https://glucoai.app', 'https://glucoai.pages.dev']
  
  const origin = request.headers.get('Origin') || ''
  const isAllowedOrigin = allowedOrigins.includes(origin) || origin.includes('.pages.dev')

  // Handle CORS with specific origins
  const corsHeaders = {
    'Access-Control-Allow-Origin': isAllowedOrigin ? origin : allowedOrigins[0],
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  }

  // Handle preflight request
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders })
  }

  try {
    // Parse request body
    let body: NewsletterRequest
    try {
      body = await request.json()
    } catch {
      return new Response(JSON.stringify({ error: 'Invalid request body' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      })
    }

    const { email } = body

    // Validate email presence
    if (!email || typeof email !== 'string') {
      return new Response(JSON.stringify({ error: 'Email is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      })
    }

    // Sanitize email
    const sanitizedEmail = sanitizeEmail(email)

    // Validate email format
    if (!isValidEmail(sanitizedEmail)) {
      return new Response(JSON.stringify({ error: 'Invalid email format' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      })
    }

    const API_KEY = env.BEEHIIV_API_KEY
    const PUBLICATION_ID = env.BEEHIIV_PUBLICATION_ID

    if (!API_KEY || !PUBLICATION_ID) {
      console.error('Missing Beehiiv credentials')
      return new Response(JSON.stringify({ error: 'Server configuration error' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      })
    }

    const API_URL = `https://api.beehiiv.com/v2/publications/${PUBLICATION_ID}/subscriptions`

    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({
        email: sanitizedEmail,
        reactivate_existing: false,
        send_welcome_email: true,
      }),
    })

    const data: BeeHiivErrorResponse = await response.json()

    // Log without sensitive data
    console.log('Beehiiv API Response:', {
      status: response.status,
      success: response.ok,
      email: sanitizedEmail.replace(/(.{2}).*(@.*)/, '$1***$2'), // Mask email
    })

    if (!response.ok) {
      const errorMessage = 
        data.message || 
        (data.errors && data.errors[0]?.message) ||
        'Failed to subscribe'
      
      return new Response(
        JSON.stringify({ error: errorMessage }),
        {
          status: response.status,
          headers: { 'Content-Type': 'application/json', ...corsHeaders },
        }
      )
    }

    return new Response(
      JSON.stringify({ message: 'Successfully subscribed to the newsletter' }),
      {
        status: 201,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      }
    )
  } catch (error: unknown) {
    // Log error without exposing details to client
    console.error('Newsletter subscription error:', {
      name: error instanceof Error ? error.name : 'Unknown',
      message: error instanceof Error ? error.message : 'Unknown error',
    })
    
    return new Response(
      JSON.stringify({
        error: 'An error occurred while processing your request. Please try again later.',
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      }
    )
  }
}
