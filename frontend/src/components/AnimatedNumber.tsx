import React, { useRef } from 'react';
import { motion, useMotionValue, useTransform } from 'framer-motion';

export const AnimatedNumber = ({ targetNumber }) => {
    const number = useMotionValue(0);
    const rounded = useTransform(number, value => Math.round(value));
    const numberRef = useRef();

    return (
        <motion.span
            initial={{ number: 0 }}
            animate={{ number: targetNumber }}
            transition={{ duration: 2, ease: 'easeOut' }}
            onUpdate={latest => {
                number.set(latest.number);
                if (numberRef.current) {
                    numberRef.current.textContent = rounded.get();
                }
            }}
        >
            <span ref={numberRef}>{number.get()}</span>
        </motion.span>
    );
};

export default AnimatedNumber;
