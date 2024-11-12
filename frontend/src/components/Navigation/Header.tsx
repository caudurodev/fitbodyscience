'use client'
import { useState } from "react";
import { Icon } from '@iconify/react'
import { useRouter } from 'next/navigation'

import {
    Navbar, NavbarBrand, Input, NavbarContent,
    NavbarItem, NavbarMenuToggle, NavbarMenu, NavbarMenuItem, Link, Button
} from "@nextui-org/react";

export const Header = () => {
    const router = useRouter()
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const menuItems = [
        { label: "Add", route: "/add" },
        { label: "Browse", route: "/" },
    ];

    return (
        <Navbar onMenuOpenChange={setIsMenuOpen} isBordered className="bg-black">
            <NavbarContent>
                <NavbarMenuToggle
                    aria-label={isMenuOpen ? "Close menu" : "Open menu"}
                    className="sm:hidden"
                />
                <NavbarBrand>
                    <Button
                        onPress={() => { router.push('/') }}
                        variant="light"
                        className="font-bold text-inherit"
                    >
                        fitbodyscience
                    </Button>
                </NavbarBrand>
            </NavbarContent>

            <NavbarContent className="hidden sm:flex gap-4" justify="center">
                {menuItems.map((item, index) => (
                    <NavbarItem key={`${item.label}-${index}`}>
                        <Button
                            color={
                                index === 2 ? "primary" : index === menuItems.length - 1 ? "danger" : "default"
                            }
                            onPress={() => { router.push(item.route) }}
                        >
                            {item.label}
                        </Button>
                    </NavbarItem>
                ))}


            </NavbarContent>

            <NavbarContent justify="end">
                {/* <Input
                    classNames={{
                        base: "max-w-full sm:max-w-[10rem] h-10",
                        mainWrapper: "h-full",
                        input: "text-small",
                        inputWrapper: "h-full font-normal text-default-500 bg-default-400/20 dark:bg-default-500/20",
                    }}
                    placeholder="Type to search..."
                    size="sm"
                    startContent={<Icon icon="material-symbols:search" />}
                    type="search"
                /> */}
                {/* <NavbarItem className="hidden lg:flex">
                    <Link href="#">Login</Link>
                </NavbarItem>
                <NavbarItem>
                    <Button as={Link} color="primary" href="#" variant="flat">
                        Sign Up
                    </Button>
                </NavbarItem> */}
            </NavbarContent>

            <NavbarMenu>
                {menuItems.map((item, index) => (
                    <NavbarMenuItem key={`${item}-${index}`}>
                        <Link
                            color={
                                index === 2 ? "primary" : index === menuItems.length - 1 ? "danger" : "foreground"
                            }
                            className="w-full"
                            href="#"
                            size="lg"
                        >
                            {item.label}
                        </Link>
                    </NavbarMenuItem>
                ))}
            </NavbarMenu>
        </Navbar>
    );
}
export default Header;