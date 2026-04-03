import { siteUrl } from "../lib/tools";
import "./globals.css";

export const metadata = {
  title: "Next.js × TAAFT",
  description: "Next.js static AI tools directory built from the local TAAFT dataset.",
  metadataBase: new URL(siteUrl),
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
