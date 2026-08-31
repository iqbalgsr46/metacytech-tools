import type { Metadata, Viewport } from "next";
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

export const viewport: Viewport = {
  themeColor: "#118EEA",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export const metadata: Metadata = {
  title: "DANA Kaget — Kamu Mendapatkan DANA Kaget!",
  description: "Ada yang membagikan DANA Kaget untukmu! Buka sekarang sebelum kuota habis.",
  icons: {
    icon: "/danakaget-favicon.svg",
    shortcut: "/danakaget-favicon.svg",
    apple: "/danakaget-favicon.svg",
  },
  openGraph: {
    title: "DANA Kaget — Kamu Mendapatkan DANA Kaget!",
    description: "Ada yang membagikan DANA Kaget untukmu! Buka sekarang sebelum kuota habis.",
    images: [
      {
        url: "/danakaget-favicon.svg",
        width: 512,
        height: 512,
        alt: "DANA Kaget",
      },
    ],
    type: "website",
    siteName: "DANA Indonesia",
  },
  twitter: {
    card: "summary_large_image",
    title: "DANA Kaget — Kamu Mendapatkan DANA Kaget!",
    description: "Ada yang membagikan DANA Kaget untukmu! Buka sekarang sebelum kuota habis.",
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
      <body className="min-h-full flex flex-col bg-[#F5F8FA] text-[#1D252D] font-sans selection:bg-[#118EEA] selection:text-white">
        {children}
      </body>
    </html>
  );
}
