'use client'

import { useState } from "react";
import { Icon } from '@iconify/react'
import { useRouter } from 'next/navigation'
import { usePathname } from 'next/navigation'
import { ThemeSwitcher } from "@/components/ThemeSwitcher";
import { useResponsive } from "@/hooks/useResponsive";
import { LoginModal } from "@/components/auth/LoginModal";
import { motion, AnimatePresence } from 'framer-motion'
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
    const pathname = usePathname()
    const { signOut } = useSignOut()

    const { isMobile } = useResponsive()
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const menuItems = [
        {
            label: "Creators",
            href: "/creators",
            showInDesktopMain: true
        },
        {
            label: "Assertions",
            href: "/assertions",
            showInDesktopMain: true
        },
        {
            label: "Studies",
            href: "/studies",
            showInDesktopMain: true
        },


        {
            label: "FAQ",
            href: "/faq",
            showInDesktopMain: false
        },
        {
            label: "Contact",
            href: "/contact",
            showInDesktopMain: false
        },
        {
            label: "Terms & Conditions",
            href: "/terms",
            showInDesktopMain: false
        },
        {
            label: "Privacy Policy",
            href: "/privacy-policy",
            showInDesktopMain: false
        },
    ];

    const userMenuItems = [
        {
            label: "Account",
            href: "/account",
        },
        {
            label: "Privacy Policy",
            href: "/privacy-policy",
        },
        {
            label: "Terms & Conditions",
            href: "/terms",
        },
        {
            label: "Sign Out",
            onClick: () => signOut(),
        },
    ];

    return (
        <Navbar
            maxWidth="2xl"
            onMenuOpenChange={setIsMenuOpen}
            isBlurred={false}
            isMenuOpen={isMenuOpen}
            className="sm:mb-16 mb-8 px-4 sm:px-8"
        >
            <NavbarContent className="-ml-[20px]">
                {isMobile &&
                    <NavbarMenuToggle
                        icon={isMenuOpen ? <Icon icon="ic:outline-close" /> : <Icon icon="ic:outline-menu" />}
                        aria-label={isMenuOpen ? "Close menu" : "Open menu"}
                        className={`sm:hidden text-8xl  text-primary ${isMenuOpen ? "font-bold" : ""}`}
                    />
                }
                <NavbarBrand>
                    <Link
                        onPress={() => { router.push('/') }}
                        className="font-bold sm:text-2xl text-2xl cursor-pointer text-foreground"
                    >
                        <span className="text-primary">Fit</span>&nbsp;
                        <span className="text-gradient-logo">Body</span>&nbsp;
                        <span className="text-secondary"> Science</span>
                    </Link>
                </NavbarBrand>
            </NavbarContent>

            <NavbarContent className="hidden sm:flex gap-4" justify="center">
                {menuItems.filter(item => item.showInDesktopMain).map((item, index) => (
                    <NavbarItem key={`${item.label}-${index}`}>
                        <Button
                            variant="light"
                            color="secondary"
                            className={pathname === item.href ? "bg-secondary/20 font-bold" : ""}
                            onPress={() => { router.push(item.href) }}
                        >
                            {item.label}
                        </Button>
                    </NavbarItem>
                ))}

                {menuItems.some(item => !item.showInDesktopMain) && (
                    <NavbarItem>
                        <Dropdown>
                            <DropdownTrigger>
                                <Button
                                    isIconOnly
                                    variant="light"
                                    color="secondary"
                                    endContent={<Icon icon="mage:dots" className="text-xl" />}
                                >
                                </Button>
                            </DropdownTrigger>
                            <DropdownMenu aria-label="More menu items">
                                {menuItems.filter(item => !item.showInDesktopMain).map((item, index) => (
                                    <DropdownItem
                                        key={`dropdown-${item.label}-${index}`}
                                        onPress={() => {
                                            router.push(item.href);
                                        }}
                                    >
                                        {item.label}
                                    </DropdownItem>
                                ))}
                            </DropdownMenu>
                        </Dropdown>
                    </NavbarItem>
                )}
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
                                                {userMenuItems.map((item, index) => (
                                                    <DropdownItem
                                                        key={item.label}
                                                        as={Link}
                                                        href={item.href}
                                                        onClick={item.onClick}
                                                    >
                                                        {item.label}
                                                    </DropdownItem>
                                                ))}
                                            </DropdownMenu>
                                        </Dropdown>
                                    </div>
                                </motion.div>
                            }
                        </>
                    }

                </NavbarContent>
            }

            <NavbarMenu
                motionProps={{
                    initial: { opacity: 0, height: 0 },
                    animate: {
                        opacity: 1,
                        height: "auto",
                        transition: {
                            duration: 0.2,
                            ease: "easeInOut"
                        }
                    },
                    exit: {
                        opacity: 0,
                        height: 0,
                        transition: {
                            delay: 0.1,
                            duration: 0.3,
                            ease: "easeInOut"
                        }
                    }
                }}
            >
                <AnimatePresence mode="wait">
                    {isMenuOpen && (
                        <motion.div
                            key="mobile-menu"
                            initial={{ opacity: 0 }}
                            animate={{
                                opacity: 1, transition: {
                                    duration: 0.2,
                                    ease: "easeInOut"
                                }
                            }}
                            exit={{ opacity: 0 }}
                            className="flex flex-col gap-2"
                        >
                            <AnimatePresence>
                                {menuItems.map((item, index) => (
                                    <motion.div
                                        key={`div-${item.label}-${index}-motion`}
                                        initial={{ opacity: 0, y: -20 }}
                                        animate={{
                                            opacity: 1,
                                            y: 0,
                                            transition: {
                                                duration: 0.3,
                                                delay: 0.2 + index * 0.1,
                                                ease: "easeInOut"
                                            }
                                        }}
                                        exit={{
                                            opacity: 0,
                                            y: -20,
                                            transition: {
                                                duration: 0.2,
                                                delay: (menuItems.length - index - 1) * 0.1,
                                                ease: "easeInOut"
                                            }
                                        }}
                                    >
                                        <NavbarMenuItem key={`${item.label}-${index}`} isActive={pathname === item.href}>
                                            <Button
                                                variant="solid"
                                                color="primary"
                                                className={`w-full ${pathname === item.href ? "bg-primary-600 font-bold text-background" : ""}`}
                                                onPress={() => {
                                                    setIsMenuOpen(false);
                                                    router.push(item.href);
                                                }}
                                            >
                                                {item.label}
                                            </Button>
                                        </NavbarMenuItem>
                                    </motion.div>
                                ))}
                            </AnimatePresence>
                            {isAuthenticated ? (
                                <>
                                    <motion.div >
                                        <h6 className="flex items-center mt-8">
                                            <span className="text-sm mr-3">Dark Mode</span>
                                            <ThemeSwitcher />
                                        </h6>
                                    </motion.div>

                                    <motion.div>
                                        <h6 className="text-lg mt-8">Hi {userData?.displayName}!</h6>
                                        <Button
                                            variant="solid"
                                            color="secondary"
                                            onPress={() => {
                                                setIsMenuOpen(false);
                                                router.push('/account');
                                            }}
                                            className="w-full mt-2"
                                        >
                                            My Account
                                        </Button>
                                        <Button
                                            variant="solid"
                                            color="danger"
                                            onPress={() => {
                                                setIsMenuOpen(false);
                                                signOut();
                                            }}
                                            className="w-full mt-2"
                                        >
                                            Log Out
                                        </Button>
                                    </motion.div>
                                </>
                            ) : (
                                <motion.div variants={{
                                    open: {
                                        opacity: 1,
                                        y: 0,
                                        transition: { duration: 0.4, ease: "easeOut" }
                                    },
                                    closed: {
                                        opacity: 0,
                                        y: -10,
                                        transition: { duration: 0.4, ease: "easeIn" }
                                    }
                                }}>
                                    <h6 className="flex items-center mt-8">
                                        <span className="text-sm mr-3">Dark Mode</span>
                                        <ThemeSwitcher />
                                    </h6>
                                    <div className="mt-8">
                                        <LoginModal
                                            buttonLabel="Login or join"
                                            defaultTab="register"
                                            setToggleOpen={() => setIsMenuOpen(false)}
                                        />
                                    </div>
                                </motion.div>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </NavbarMenu>
        </Navbar>
    );
}
export default Header;