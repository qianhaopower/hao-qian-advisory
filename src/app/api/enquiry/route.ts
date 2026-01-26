import { NextResponse } from "next/server";
import { Resend } from "resend";

function escapeHtml(s: string) {
  return s
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export async function POST(req: Request) {
  console.log("ENQUIRY API HIT");

  try {
    const body = await req.json();
    console.log("Enquiry payload:", body);

    const name = String(body?.name || "").trim();
    const email = String(body?.email || "").trim();
    const role = String(body?.role || "").trim();
    const message = String(body?.message || "").trim();

    if (!name || !email || !message) {
      return NextResponse.json({ ok: false, error: "Missing fields" }, { status: 400 });
    }

    const resendKey = process.env.RESEND_API_KEY;
    const toEmail = process.env.ENQUIRY_TO_EMAIL;
    const fromEmail = process.env.ENQUIRY_FROM_EMAIL || "onboarding@resend.dev";
    const siteName = process.env.SITE_NAME || "Hao Qian — Leadership Advisory";

    if (!resendKey || !toEmail) {
      console.error("Missing RESEND_API_KEY or ENQUIRY_TO_EMAIL");
      return NextResponse.json({ ok: false, error: "Server not configured" }, { status: 500 });
    }

    const resend = new Resend(resendKey);

    const subject = `New enquiry — ${siteName}`;
    const html = `
      <h2>New enquiry</h2>
      <p><b>Name:</b> ${escapeHtml(name)}</p>
      <p><b>Email:</b> ${escapeHtml(email)}</p>
      <p><b>Role:</b> ${escapeHtml(role || "-")}</p>
      <p><b>Message:</b><br/>${escapeHtml(message).replaceAll("\n", "<br/>")}</p>
    `;

    console.log("About to send email via Resend...");

    const { data, error } = await resend.emails.send({
  from: fromEmail,
  to: toEmail,
  subject,
  html,
  replyTo: email, // Resend API uses reply_to in many examples/docs
});

console.log("Resend data:", data);
console.log("Resend error:", error);

if (error) {
  return NextResponse.json({ ok: false, error }, { status: 500 });
}

return NextResponse.json({ ok: true, id: data?.id });

  } catch (err: any) {
    console.error("ENQUIRY API ERROR:", err);
    return NextResponse.json({ ok: false, error: "Internal error" }, { status: 500 });
  }
}
