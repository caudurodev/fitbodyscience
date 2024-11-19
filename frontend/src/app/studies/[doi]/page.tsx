'use client'

import { Card, Spinner, Slider, CardBody, CardFooter, Divider, Button, Link, Chip } from "@nextui-org/react";
// import { Icon } from '@iconify/react'
// import { motion } from 'framer-motion'
import { useQuery } from '@apollo/client'

import { useHydration } from '@/hooks/useHydration'
import { useRouter } from 'next/navigation';

const Page = ({ params }: { params: { doi: string } }) => {
    const router = useRouter()
    const isHydrated = useHydration()
    // const { data: contentData, refetch } = useQuery(GET_CONTENT_QUERY, {
    //     variables: {
    //         doi: params?.doi,
    //     },
    //     skip: !params?.doi,
    //     fetchPolicy: 'network-only'
    // })

    if (!isHydrated) { return null }
    return (
        <>



            <Card>
                <CardBody className="flex sm:flex-row sm:gap-x-8">
                    <div className="sm:w-1/3">
                        <h6>DOI {params?.doi}</h6>

                    </div>
                    <div className="sm:w-2/3">

                        <h2 className="uppercase">Main point</h2>
                    </div>
                </CardBody>
            </Card>
        </ >
    );
}

export default Page