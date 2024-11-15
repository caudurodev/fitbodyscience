"use client"

import { Inter } from "next/font/google";
import { NhostProvider } from "@nhost/nextjs";
import { NextUIProvider } from '@nextui-org/react'
import { NhostApolloProvider } from '@nhost/react-apollo'
import { Header } from "@/components/Navigation/Header";
import { useHydration } from '@/hooks/useHydration'
import { ThemeProvider as NextThemeProvider, type ThemeProviderProps } from "next-themes";
import "./globals.css";
import { nhost } from '@/utils/nhost';

const font = Inter({ subsets: ["latin"] });

function ThemeProvider({ children, ...props }: { children: React.ReactNode } & ThemeProviderProps) {
  return <NextThemeProvider {...props}>{children}</NextThemeProvider>;
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const isHydrated = useHydration()
  if (!isHydrated) { return <html><body></body></html> }
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
      </head>
      <body className={`${font.className} bg-background max-w-7xl mx-auto`}>
        <NhostProvider nhost={nhost} >
          <NhostApolloProvider nhost={nhost}>
            <NextUIProvider>
              <ThemeProvider attribute="class" defaultTheme="light">
                <main className="px-4 sm:px-8">
                  <Header />
                  {children}
                </main>
              </ThemeProvider>
            </NextUIProvider>
          </NhostApolloProvider>
        </NhostProvider>
      </body>
    </html>
  );
}
