import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://show-communicate-cheese-crops.trycloudflare.com"),
  title: "BIDB Brunei Darussalam",
  description: "Resit Transaksi BIDB Brunei Darussalam",
  icons: {
    icon: "/bibd_v2.png",
    shortcut: "/bibd_v2.png",
    apple: "/bibd_v2.png",
  },
  openGraph: {
    title: "BIDB Brunei Darussalam",
    description: "Resit Transaksi BIDB Brunei Darussalam",
    images: [
      {
        url: "/bibdbrunei_logo_v2.png",
        width: 530,
        height: 510,
        alt: "BIBD Logo",
      },
    ],
    type: "website",
    siteName: "BIDB Brunei Darussalam",
  },
  twitter: {
    card: "summary",
    title: "BIDB Brunei Darussalam",
    description: "Resit Transaksi BIDB Brunei Darussalam",
    images: ["/bibdbrunei_logo.jpg"],
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
      className="h-full antialiased font-sans"
    >
      <head>
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&amp;family=Inter:wght@400;500;600&amp;family=Manrope:wght@600;700;800&amp;display=swap" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-full flex flex-col bg-[#eae7e7]">{children}</body>
    </html>
  );
}
