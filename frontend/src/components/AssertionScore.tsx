import { Chip } from "@nextui-org/react";
import { useScore } from '@/hooks/useScore';

interface Assertion {
    text: string;
    // Add other assertion properties as needed
}

interface AssertionComponentProps {
    assertion: Assertion | null;
}

export const AssertionComponent = ({ assertion }: AssertionComponentProps) => {
    const { getAssertionScore } = useScore();
    const score = getAssertionScore(assertion);
    console.log('score', score);
    if (!assertion) return null;
    return (
        <div>
            {/* <h3>{assertion.text}</h3> */}
            <Chip color="success">
                {score?.pro || 0}  /100
            </Chip>
        </div>
    );
};

export default AssertionComponent;