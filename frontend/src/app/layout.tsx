"use client"

import { Work_Sans } from "next/font/google";
import { NhostProvider } from "@nhost/nextjs";
import { NextUIProvider } from '@nextui-org/react'
import { NhostApolloProvider } from '@nhost/react-apollo'
import { Header } from "@/components/Navigation/Header";
import { useHydration } from '@/hooks/useHydration'
import "./globals.css";
import { nhost } from '@/utils/nhost';

const font = Work_Sans({ subsets: ["latin"] });


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const isHydrated = useHydration()
  if (!isHydrated) { return <html><body></body></html> }
  return (
    <html lang="en" >
      <body className={font.className}>
        <NhostProvider nhost={nhost} >
          <NhostApolloProvider nhost={nhost}>
            <NextUIProvider>
              <Header />
              {children}
            </NextUIProvider>
          </NhostApolloProvider>
        </NhostProvider>
      </body>
    </html>
  );
}
