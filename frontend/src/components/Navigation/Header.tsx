'use client'

import { useState } from "react";
import { Icon } from '@iconify/react'
import { useRouter } from 'next/navigation'
import { ThemeSwitcher } from "@/components/ThemeSwitcher";
import { useResponsive } from "@/hooks/useResponsive";
import { LoginModal } from "@/components/auth/LoginModal";
import { motion } from 'framer-motion'
import { useSignOut, useUserData, useAuthenticationStatus } from '@nhost/nextjs'
import {
    Navbar,
    NavbarBrand,
    NavbarContent,
    NavbarItem,
    NavbarMenuToggle,
    NavbarMenu,
    NavbarMenuItem,
    Link,
    Button,
    Spinner,
    Dropdown,
    DropdownTrigger,
    DropdownMenu,
    DropdownItem,
    Avatar
} from "@nextui-org/react";

export const Header = () => {
    const userData = useUserData()
    const { isAuthenticated, isLoading: isLoadingAuth } =
        useAuthenticationStatus()
    const router = useRouter()
    const { signOut } = useSignOut()

    const { isMobile } = useResponsive()
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const menuItems = [
        { label: "Browse", route: "/" },
        { label: "Influencers", route: "/influencers" },
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
                            variant="light"
                            color="secondary"
                            onPress={() => { router.push(item.route) }}
                        >
                            {item.label}
                        </Button>
                    </NavbarItem>
                ))}


            </NavbarContent>
            {!isMobile &&
                <NavbarContent justify="end">
                    <ThemeSwitcher />
                    {isLoadingAuth ?
                        <Spinner />
                        :
                        <>
                            {!isAuthenticated &&
                                <motion.div
                                    initial={{ opacity: 0, }}
                                    animate={{ opacity: 1 }}
                                    exit={{
                                        opacity: 0,
                                        transition: {
                                            opacity: { duration: 1 },
                                        },
                                    }}
                                    transition={{
                                        opacity: { duration: 1 },
                                    }}>

                                    <NavbarItem className=" lg:flex">
                                        <LoginModal buttonLabel="Login or join" defaultTab="register" />
                                    </NavbarItem>
                                </motion.div>
                            }
                            {isAuthenticated &&
                                <motion.div
                                    initial={{ opacity: 0, }}
                                    animate={{ opacity: 1 }}
                                    exit={{
                                        opacity: 0,
                                        transition: {
                                            opacity: { duration: 1 },
                                        },
                                    }}
                                    transition={{
                                        opacity: { duration: 1 },
                                    }}
                                >
                                    <div className="flex gap-4">
                                        <h6 className="text-gray-700 text-xs mt-2 text-gray-500">{userData?.displayName}</h6>

                                        <Dropdown placement="bottom-end">
                                            <DropdownTrigger>
                                                <Avatar
                                                    src={userData?.avatarUrl}
                                                    isBordered
                                                    showFallback
                                                    as={Link}
                                                    className="transition-transform"
                                                    color="primary"
                                                    name={userData?.displayName}
                                                    size="sm"
                                                />
                                            </DropdownTrigger>
                                            <DropdownMenu
                                                aria-label="Profile Actions"
                                                variant="flat"
                                                color="primary"
                                            >
                                                <DropdownItem
                                                    key="account"
                                                    as={Link}
                                                    href="/account"
                                                >
                                                    My Account
                                                </DropdownItem>
                                                <DropdownItem
                                                    key="logout"
                                                    as={Link}
                                                    href="#"
                                                    onClick={(e) => {
                                                        e.preventDefault();
                                                        signOut();
                                                    }}
                                                >
                                                    Log Out
                                                </DropdownItem>
                                            </DropdownMenu>
                                        </Dropdown>
                                    </div>
                                </motion.div>
                            }
                        </>
                    }

                </NavbarContent>
            }

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