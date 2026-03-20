import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  try {
    const { email } = await req.json()

    if (!email) {
      return NextResponse.json({ error: 'Email is required' }, { status: 400 })
    }

    const API_KEY = process.env.BEEHIIV_API_KEY
    const PUBLICATION_ID = process.env.BEEHIIV_PUBLICATION_ID

    if (!API_KEY || !PUBLICATION_ID) {
      console.error('Missing Beehiiv credentials')
      return NextResponse.json(
        { error: 'Server configuration error' },
        { status: 500 }
      )
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
      return NextResponse.json(
        { error: data.message || 'Failed to subscribe' },
        { status: response.status }
      )
    }

    return NextResponse.json(
      { message: 'Successfully subscribed to the newsletter' },
      { status: 201 }
    )
  } catch (error: any) {
    console.error('Newsletter subscription error:', error)
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    )
  }
}
