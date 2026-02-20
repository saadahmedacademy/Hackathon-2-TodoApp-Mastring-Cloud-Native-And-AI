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

/**
 * GET /api/todos
 *
 * Server-side proxy → Phase-3 GET /api/{user_id}/todos
 *
 * Returns todos WITH display_id so the frontend can render clean task numbers
 * (Phase-2's /api/tasks omits display_id from its TodoRead response schema).
 */
export async function GET(request: NextRequest) {
  const backendUrl = process.env.PHASE3_BACKEND_URL;

  if (!backendUrl) {
    return NextResponse.json(
      { error: 'Chat service is not configured. PHASE3_BACKEND_URL is missing.' },
      { status: 503 }
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

  try {
    // Forward optional ?completed= query param
    const completedParam = request.nextUrl.searchParams.get('completed');
    const upstreamUrl = new URL(`${backendUrl}/api/${userId}/todos`);
    if (completedParam !== null) {
      upstreamUrl.searchParams.set('completed', completedParam);
    }

    const response = await fetch(upstreamUrl.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader ? { Authorization: authHeader } : {}),
      },
      signal: AbortSignal.timeout(15000),
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(data, { status: response.status });
    }

    return NextResponse.json(data, { status: 200 });
  } catch (error: any) {
    if (error.name === 'TimeoutError' || error.name === 'AbortError') {
      return NextResponse.json(
        { error: 'Todos fetch timed out. Please try again.' },
        { status: 504 }
      );
    }
    return NextResponse.json(
      { error: 'An unexpected error occurred.' },
      { status: 500 }
    );
  }
}
