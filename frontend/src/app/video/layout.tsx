'use client'

export default function VideoLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex-grow">
      {children}
    </div>
  )
}
