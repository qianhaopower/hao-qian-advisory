"use client";

import { useState } from "react";

type Status = "idle" | "submitting" | "success" | "error";

function isValidEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i.test(email.trim());
}

export function FriendsSignupForm() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState("");

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");

    const trimmed = email.trim();
    if (!trimmed) {
      setError("Please enter your email address.");
      setStatus("error");
      return;
    }
    if (!isValidEmail(trimmed)) {
      setError("Please enter a valid email address.");
      setStatus("error");
      return;
    }

    try {
      setStatus("submitting");

      const res = await fetch("/api/friends-intelligence-signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: trimmed }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Request failed");
      }

      setStatus("success");
      setEmail("");
    } catch (err) {
      setStatus("error");
      setError("Something went wrong. Please try again.");
      console.error(err);
    }
  }

  if (status === "success") {
    return (
      <p className="text-lg font-medium tracking-wide text-[#d6a441]">
        See you on launch day.
      </p>
    );
  }

  return (
    <div className="flex w-full flex-col items-center gap-3">
      <form
        onSubmit={onSubmit}
        noValidate
        className="flex w-full flex-col items-center gap-3 sm:flex-row sm:gap-2"
      >
        <label htmlFor="fi-email" className="sr-only">
          Email Address
        </label>
        <input
          id="fi-email"
          type="email"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="email"
          placeholder="Enter your email address"
          className="w-full flex-1 rounded-xl border border-white/30 bg-white/[0.08] px-4 py-3 text-base text-[#f4efe3] placeholder:text-[#a9a392] outline-none transition focus:border-[#d6a441] focus:bg-white/[0.1] focus:ring-1 focus:ring-[#d6a441]/40"
        />
        <button
          type="submit"
          disabled={status === "submitting"}
          className="w-full rounded-xl bg-[#d6a441] px-6 py-3 text-base font-semibold text-[#0d1626] transition hover:bg-[#e0b357] disabled:opacity-60 sm:w-auto"
        >
          {status === "submitting" ? "Sending…" : "Notify Me"}
        </button>
      </form>

      {status === "error" && error ? (
        <p role="alert" className="text-xs text-red-300">
          {error}
        </p>
      ) : null}
    </div>
  );
}
