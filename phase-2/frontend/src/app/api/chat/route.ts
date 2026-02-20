import { NextRequest, NextResponse } from 'next/server';

function extractUserIdFromJwt(authHeader: string | null): string | null {
  if (!authHeader?.startsWith('Bearer ')) return null;
  try {
    const token = authHeader.slice(7);
    const payload = token.split('.')[1];
    const decoded = JSON.parse(Buffer.from(payload, 'base64url').toString('utf-8'));
    return decoded.sub ?? decoded.user_id ?? decoded.id ?? null;
  } catch {
    return null;
  }
}

export async function POST(request: NextRequest) {
  const backendUrl = process.env.PHASE3_BACKEND_URL;

  if (!backendUrl) {
    return NextResponse.json(
      { error: 'Chat service is not configured. PHASE3_BACKEND_URL is missing.' },
      { status: 503 }
    );
  }

  try {
    const body = await request.json();
    const { message, conversation_id } = body;

    if (!message || !message.trim()) {
      return NextResponse.json(
        { error: 'message is required and cannot be empty.' },
        { status: 400 }
      );
    }

    const authHeader = request.headers.get('Authorization');
    const userId = extractUserIdFromJwt(authHeader);

    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized: could not identify user from token.' },
        { status: 401 }
      );
    }

    const response = await fetch(`${backendUrl}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader ? { Authorization: authHeader } : {}),
      },
      body: JSON.stringify({ message: message.trim(), conversation_id: conversation_id ?? null }),
      signal: AbortSignal.timeout(30000),
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(data, { status: response.status });
    }

    return NextResponse.json(data, { status: 200 });
  } catch (error: any) {
    if (error.name === 'TimeoutError' || error.name === 'AbortError') {
      return NextResponse.json(
        { error: 'The AI agent took too long to respond. Please try again.' },
        { status: 504 }
      );
    }
    return NextResponse.json(
      { error: 'An unexpected error occurred.' },
      { status: 500 }
    );
  }
}
