import React, { useRef } from 'react';
import { motion, useMotionValue, useTransform } from 'framer-motion';

export const AnimatedNumber = ({ targetNumber }: { targetNumber: number }) => {
    const number = useMotionValue(0);
    const rounded = useTransform(number, value => Math.round(value));
    const numberRef = useRef<HTMLSpanElement>(null);

    return (
        <motion.span
            initial={{ opacity: 1 }}
            animate={{
                opacity: 1,
                transitionEnd: {
                    opacity: 1
                }
            }}
            transition={{ duration: 2, ease: 'easeOut' }}
            onUpdate={(latest: any) => {
                if (typeof latest === 'number') {
                    number.set(latest);
                    if (numberRef.current) {
                        numberRef.current.textContent = rounded.get().toString();
                    }
                }
            }}
        >
            <span ref={numberRef}>{rounded.get()}</span>
        </motion.span>
    );
};

export default AnimatedNumber;
