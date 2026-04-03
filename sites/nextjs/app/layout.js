import { siteUrl } from "../lib/tools";
import "./globals.css";

export const metadata = {
  title: "AI Tools Directory",
  description: "A static directory of AI tools with category pages and individual tool details.",
  metadataBase: new URL(siteUrl),
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
