import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SULAP — Solusi Unggul, Lengkap, Aman untuk PDF",
  description: "SULAP — Solusi Unggul, Lengkap, Aman untuk PDF. Internal tool Bank Sahabat Sampoerna.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id">
      <body className="bg-slate-50">{children}</body>
    </html>
  );
}
