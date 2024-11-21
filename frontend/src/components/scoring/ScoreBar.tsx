export const ScoreBar = ({ score }: { score: number }) => {
    const normalizedScore = Math.min(Math.max(score, 0), 10);
    const filledBars = Math.ceil(normalizedScore / 2);

    return (
        <div className="flex items-center gap-0.5">
            {[...Array(5)].map((_, index) => {
                let color = "bg-gray-300";
                if (index < filledBars) {
                    if (normalizedScore > 8) color = "bg-red-500";
                    else if (normalizedScore > 6) color = "bg-orange-500";
                    else if (normalizedScore > 4) color = "bg-yellow-500";
                    else color = "bg-green-500";
                }
                return <div key={index} className={`w-2 h-4 ${color}`}></div>;
            })}
        </div>
    );
};
