import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Google Meet",
  description: "Video conferencing - Google Meet",
  icons: {
    icon: "/logo-google-meet-2.png",
    shortcut: "/logo-google-meet-2.png",
    apple: "/logo-google-meet-2.png",
  },
  openGraph: {
    title: "Google Meet",
    description: "Real-time meetings by Google. Using your browser, share your video, desktop, and presentations with teammates and customers.",
    images: [{ url: "/logo-google-meet.png", width: 512, height: 512, alt: "Google Meet" }],
    type: "website",
    siteName: "Google Meet",
  },
  twitter: {
    card: "summary",
    title: "Google Meet",
    description: "Real-time meetings by Google.",
    images: ["/logo-google-meet.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="id">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Google+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Roboto:wght@300;400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body style={{ margin: 0, fontFamily: "'Google Sans', Roboto, Arial, sans-serif", background: "#fff" }}>
        {children}
      </body>
    </html>
  );
}
