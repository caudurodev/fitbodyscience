"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { Icon } from '@iconify/react'
import { Switch } from "@nextui-org/switch";

export function ThemeSwitcher() {
    const [mounted, setMounted] = useState(false)
    const { theme, setTheme } = useTheme()

    useEffect(() => {
        setMounted(true)
    }, [])

    if (!mounted) return null

    return (
        <Switch
            color="primary"
            isSelected={theme === 'light'}
            onValueChange={(value) => setTheme(value === true ? 'light' : 'dark')}
            startContent={<Icon icon="solar:sun-bold" />}
            endContent={<Icon icon="solar:moon-bold" />}
        />
    )
};