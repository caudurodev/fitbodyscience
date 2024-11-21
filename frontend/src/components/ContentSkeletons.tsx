import { Skeleton } from "@nextui-org/react";

export const SummarySkeleton = () => {
  return (
    <div className="w-full p-4 space-y-3">
      <Skeleton className="rounded-lg">
        <div className="h-3 w-3/4 rounded-lg bg-default-200"></div>
      </Skeleton>
      <Skeleton className="rounded-lg">
        <div className="h-3 w-full rounded-lg bg-default-200"></div>
      </Skeleton>
      <Skeleton className="rounded-lg">
        <div className="h-3 w-4/5 rounded-lg bg-default-200"></div>
      </Skeleton>
    </div>
  );
};

export const AssertionsSkeleton = () => {
  return (
    <div className="space-y-8">
      {[1, 2, 3].map((i) => (
        <div key={i} className="w-full p-4 space-y-3">
          <Skeleton className="rounded-md">
            <div className="h-3 w-1/2 rounded-lg bg-default-200"></div>
          </Skeleton>
          <Skeleton className="rounded-lg">
            <div className="h-3 w-full rounded-lg bg-default-200"></div>
          </Skeleton>
          <div className="flex gap-2">
            <Skeleton className="rounded-full w-20 h-6" />
            <Skeleton className="rounded-full w-20 h-6" />
          </div>
        </div>
      ))}
    </div>
  );
};

export const EvidenceClassificationSkeleton = () => {
  return (
    <div className="w-full p-4">
      <div className="space-y-4">
        <Skeleton className="rounded-lg">
          <div className="h-6 w-48 rounded-lg bg-default-200"></div>
        </Skeleton>
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center gap-4">
              <Skeleton className="rounded-full w-6 h-6" />
              <Skeleton className="rounded-lg flex-1">
                <div className="h-4 rounded-lg bg-default-200"></div>
              </Skeleton>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
