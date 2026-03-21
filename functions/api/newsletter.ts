// Cloudflare Function for newsletter subscription
// This replaces the Next.js API route for static export deployments

interface Env {
  BEEHIIV_API_KEY: string
  BEEHIIV_PUBLICATION_ID: string
}

export async function onRequestPost(context: { request: Request; env: Env }) {
  const { request, env } = context

  // Handle CORS
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  }

  // Handle preflight request
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders })
  }

  try {
    const { email } = await request.json()

    if (!email) {
      return new Response(JSON.stringify({ error: 'Email is required' }), {
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
        email,
        reactivate_existing: false,
        send_welcome_email: true,
      }),
    })

    const data = await response.json()

    console.log('Beehiiv API Response:', {
      status: response.status,
      statusText: response.statusText,
      data,
    })

    if (!response.ok) {
      return new Response(
        JSON.stringify({ error: data.message || 'Failed to subscribe' }),
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
    console.error('Newsletter subscription error:', error)
    return new Response(
      JSON.stringify({
        error: error instanceof Error ? error.message : 'Internal server error',
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      }
    )
  }
}
