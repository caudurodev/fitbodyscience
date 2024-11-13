'use client'
import { useState } from "react";
import Image from "next/image";
import { Icon } from '@iconify/react'
import { useRouter } from 'next/navigation'
import { ThemeSwitcher } from "@/components/ThemeSwitcher";
import { useResponsive } from "@/hooks/useResponsive";

import {
    Navbar, NavbarBrand, Input, NavbarContent,
    NavbarItem, NavbarMenuToggle, NavbarMenu, NavbarMenuItem, Link, Button
} from "@nextui-org/react";

export const Header = () => {
    const router = useRouter()
    const { isMobile } = useResponsive()
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const menuItems = [
        { label: "Browse", route: "/" },
        { label: "Add", route: "/add" },
    ];

    return (
        <Navbar
            maxWidth="2xl"
            onMenuOpenChange={setIsMenuOpen}
            isBlurred={false}
            className="sm:mb-16 mb-8"
        >
            <NavbarContent className="-ml-[20px]">
                {isMobile &&
                    <NavbarMenuToggle
                        icon={isMenuOpen ? <Icon icon="ic:outline-close" /> : <Icon icon="ic:outline-menu" />}
                        aria-label={isMenuOpen ? "Close menu" : "Open menu"}
                        className="sm:hidden text-8xl text-primary"
                    />
                }
                <NavbarBrand className="-ml-[5px] ">
                    <Link
                        onPress={() => { router.push('/') }}
                        className="font-bold sm:text-2xl text-xl cursor-pointer text-foreground"
                    >
                        {/* <Image src="/img/icon.svg" alt="Fit Body Science" width={40} height={40} className="m-2 p-1" /> */}
                        <span className="text-primary">Fit</span>&nbsp;
                        <span className="text-gradient-logo">Body</span>&nbsp;
                        <span className="text-secondary"> Science</span>
                    </Link>
                </NavbarBrand>
            </NavbarContent>

            <NavbarContent className="hidden sm:flex gap-4" justify="center">
                {menuItems.map((item, index) => (
                    <NavbarItem key={`${item.label}-${index}`}>
                        <Button
                            variant="solid"
                            color="primary"
                            onPress={() => { router.push(item.route) }}
                        >
                            {item.label}
                        </Button>
                    </NavbarItem>
                ))}


            </NavbarContent>

            <NavbarContent justify="end">
                {!isMobile && <ThemeSwitcher />}
            </NavbarContent>

            <NavbarMenu>
                <>
                    {menuItems.map((item, index) => (
                        <NavbarMenuItem key={`${item.label}-${index}`}>
                            <Button
                                variant="solid"
                                color="primary"
                                onPress={() => {
                                    router.push(item.route);
                                    setIsMenuOpen(false);
                                }}
                                className="w-full"
                            >
                                {item.label}
                            </Button>
                        </NavbarMenuItem>
                    ))}

                    <>
                        <h6 className="flex items-center mt-8">
                            <span className="text-sm mr-3">Dark Mode</span>
                            <ThemeSwitcher />
                        </h6>
                    </>
                </>
            </NavbarMenu>
        </Navbar>
    );
}
export default Header;