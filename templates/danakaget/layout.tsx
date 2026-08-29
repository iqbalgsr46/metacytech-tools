import type { Metadata } from "next";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const jakarta = Plus_Jakarta_Sans({
  variable: "--font-jakarta",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DANA Kaget — Kamu Mendapatkan DANA Kaget!",
  description: "Ada yang bagikan DANA Kaget! Klaim sekarang sebelum habis.",
  icons: {
    icon: "/danakaget-favicon.svg",
  },
  openGraph: {
    title: "DANA Kaget — Kamu Mendapatkan DANA Kaget!",
    description: "Ada yang bagikan DANA Kaget! Klaim sekarang sebelum habis.",
    images: [
      {
        url: "/danakaget-favicon.svg",
        width: 200,
        height: 200,
        alt: "DANA Kaget",
      },
    ],
    type: "website",
    siteName: "DANA",
  },
  twitter: {
    card: "summary",
    title: "DANA Kaget — Kamu Mendapatkan DANA Kaget!",
    description: "Ada yang bagikan DANA Kaget! Klaim sekarang sebelum habis.",
    images: ["/danakaget-favicon.svg"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="id"
      className={`${inter.variable} ${jakarta.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
