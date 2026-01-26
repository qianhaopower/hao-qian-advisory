"use client";

import { useState } from "react";

type Status = "idle" | "submitting" | "success" | "error";

function isValidEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i.test(email.trim());
}

export function EnquiryForm() {
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string>("");

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");

    const form = e.currentTarget;
    const formData = new FormData(form);

    const name = String(formData.get("name") || "").trim();
    const email = String(formData.get("email") || "").trim();
    const role = String(formData.get("role") || "").trim();
    const message = String(formData.get("message") || "").trim();

    if (!name || !email || !message) {
      setError("Please fill in your name, email, and message.");
      setStatus("error");
      return;
    }
    if (!isValidEmail(email)) {
      setError("Please enter a valid email address.");
      setStatus("error");
      return;
    }

    try {
      setStatus("submitting");

      const res = await fetch("/api/enquiry", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, role, message }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Request failed");
      }

      setStatus("success");
      form.reset();
    } catch (err: any) {
      setStatus("error");
      setError("Something went wrong sending your enquiry. Please try again, or email me directly.");
      console.error(err);
    }
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-4 rounded-2xl border border-slate-200 bg-white p-5">
      <div className="grid gap-2">
        <label className="text-sm font-medium">Name</label>
        <input
          name="name"
          className="rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none focus:border-slate-500"
          placeholder="Your name"
          autoComplete="name"
        />
      </div>

      <div className="grid gap-2">
        <label className="text-sm font-medium">Email</label>
        <input
          name="email"
          className="rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none focus:border-slate-500"
          placeholder="you@example.com"
          autoComplete="email"
        />
      </div>

      <div className="grid gap-2">
        <label className="text-sm font-medium">Role (optional)</label>
        <input
          name="role"
          className="rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none focus:border-slate-500"
          placeholder="e.g. Engineering Manager / Senior Engineer"
        />
      </div>

      <div className="grid gap-2">
        <label className="text-sm font-medium">What’s prompting you to reach out?</label>
        <textarea
          name="message"
          className="min-h-[140px] rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none focus:border-slate-500"
          placeholder="A few sentences is enough."
        />
      </div>

      {status === "success" ? (
        <div className="rounded-xl bg-slate-50 p-4 text-sm text-slate-700">
         <h3 className="text-lg font-semibold text-slate-900">
  Thanks — your enquiry has been sent.
</h3>
<p className="mt-2 text-slate-700">
  I’ve received your message and will usually respond within 1–2 business days.
</p>
        </div>
      ) : null}

      {status === "error" && error ? (
        <div className="rounded-xl bg-red-50 p-4 text-sm text-red-800">{error}</div>
      ) : null}

      <button
        type="submit"
        disabled={status === "submitting"}
        className="inline-flex items-center justify-center rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800 disabled:opacity-60"
      >
        {status === "submitting" ? "Sending..." : "Send enquiry"}
      </button>

      <p className="text-xs text-slate-500">
        By submitting, you consent to be contacted about your enquiry.
      </p>
    </form>
  );
}
