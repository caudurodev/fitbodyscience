import { Chip, Progress } from "@nextui-org/react";
import { Icon } from '@iconify/react';
import { useScore } from '@/hooks/useScore';

interface Assertion {
    text: string;
    // Add other assertion properties as needed
}

interface AssertionComponentProps {
    assertion: Assertion | null;
}

interface AssertionScoreProps {
    weightConclusion: number;
    proScore?: number;
    againstScore?: number;
    className?: string;
}

export const AssertionScore = ({ weightConclusion, proScore = 0, againstScore = 0, className = "" }: AssertionScoreProps) => {
    return (
        <div className={`space-y-2 ${className}`}>
            <div className="flex items-center gap-2">
                <div className="text-xs text-default-500">Weight:</div>
                <Progress
                    size="sm"
                    radius="sm"
                    classNames={{
                        base: "flex-1 max-w-[100px]",
                        indicator: "bg-secondary"
                    }}
                    value={weightConclusion * 10}
                    label={`${weightConclusion}/10`}
                />
            </div>
            <div className="flex gap-2">
                <Chip color="success" size="sm" className="text-white">
                    <Icon icon="mdi:approve" className="inline" /> {proScore}/100
                </Chip>
                <Chip color="danger" size="sm" className="text-white">
                    <Icon icon="ci:stop-sign" className="inline" /> {againstScore}/100
                </Chip>
            </div>
        </div>
    );
};