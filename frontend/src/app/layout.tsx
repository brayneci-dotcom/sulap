import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SULAP PDF — Solusi Universal, Lengkap, Aman, Proses PDF",
  description: "SULAP PDF — Solusi Universal, Lengkap, Aman, Proses PDF. Internal tool Bank Sahabat Sampoerna.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id">
      <body className="bg-slate-50">{children}</body>
    </html>
  );
}
