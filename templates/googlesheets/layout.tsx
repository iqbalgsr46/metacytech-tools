import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Google Sheets - Laporan Praktikum Basis Data",
  description: "Laporan Praktikum Basis Data Semester Genap - Google Sheets",
  icons: {
    icon: "/googlesheets-favicon.svg",
    shortcut: "/googlesheets-favicon.svg",
    apple: "/googlesheets-favicon.svg",
  },
  openGraph: {
    title: "Google Sheets - Laporan Praktikum Basis Data",
    description: "Laporan Praktikum Basis Data Semester Genap - Google Sheets",
    images: [{ url: "/googlesheets-og.png", width: 512, height: 512, alt: "Google Sheets" }],
    type: "website",
    siteName: "Google Sheets",
  },
  twitter: {
    card: "summary",
    title: "Google Sheets - Laporan Praktikum Basis Data",
    description: "Laporan Praktikum Basis Data Semester Genap - Google Sheets",
    images: ["/googlesheets-og.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="id">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Product+Sans:wght@400;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body style={{ margin: 0, fontFamily: "Roboto, Arial, sans-serif", background: "#f9fbfd" }}>
        {children}
      </body>
    </html>
  );
}
