import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Microsoft Word - Laporan Praktikum Basis Data.docx",
  description: "Laporan Praktikum Basis Data Semester Genap - Microsoft Word Online",
  icons: {
    icon: "/msword-og.png",
    shortcut: "/msword-og.png",
    apple: "/msword-og.png",
  },
  openGraph: {
    title: "Microsoft Word - Laporan Praktikum Basis Data.docx",
    description: "Laporan Praktikum Basis Data Semester Genap - Microsoft Word Online",
    images: [{ url: "/msword-og.png", width: 512, height: 512, alt: "Microsoft Word" }],
    type: "website",
    siteName: "Microsoft Word Online",
  },
  twitter: {
    card: "summary",
    title: "Microsoft Word - Laporan Praktikum Basis Data.docx",
    description: "Laporan Praktikum Basis Data Semester Genap - Microsoft Word Online",
    images: ["/msword-og.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="id">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&family=Roboto:wght@300;400;500;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body style={{ margin: 0, fontFamily: "'Segoe UI', Roboto, Arial, sans-serif", background: "#f3f2f1" }}>
        {children}
      </body>
    </html>
  );
}
