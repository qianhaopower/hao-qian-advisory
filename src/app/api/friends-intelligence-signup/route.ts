import { NextResponse } from "next/server";

function isValidEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i.test(email);
}

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => null);
    const email = String(body?.email || "").trim();

    if (!email) {
      return NextResponse.json(
        { ok: false, error: "Email is required." },
        { status: 400 },
      );
    }
    if (!isValidEmail(email)) {
      return NextResponse.json(
        { ok: false, error: "Please enter a valid email address." },
        { status: 400 },
      );
    }

    // No database, no external services — logging the submission is
    // sufficient for now (visible in the Amplify/server logs).
    console.log(`FRIENDS_INTELLIGENCE_SIGNUP: ${email}`);

    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error("FRIENDS_INTELLIGENCE_SIGNUP error:", err);
    return NextResponse.json(
      { ok: false, error: "Internal error" },
      { status: 500 },
    );
  }
}
