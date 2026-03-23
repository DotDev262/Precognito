"use client";

import { useState } from "react";
import { Alert } from "@/lib/types";
import { AlertItem } from "./AlertItem";

interface AlertListProps {
  alerts: Alert[];
}

type SeverityFilter = "ALL" | "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

const filters: SeverityFilter[] = ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"];

export function AlertList({ alerts }: AlertListProps) {
  const [activeFilter, setActiveFilter] = useState<SeverityFilter>("ALL");

  const filteredAlerts = activeFilter === "ALL"
    ? alerts
    : alerts.filter((alert) => alert.severity === activeFilter);

  const sortedAlerts = [...filteredAlerts].sort((a, b) => {
    const severityOrder: Record<Alert["severity"], number> = {
      CRITICAL: 0,
      HIGH: 1,
      MEDIUM: 2,
      LOW: 3,
    };
    return severityOrder[a.severity] - severityOrder[b.severity];
  });

  const getAlertCount = (filter: SeverityFilter): number => {
    if (filter === "ALL") return alerts.length;
    return alerts.filter((a) => a.severity === filter).length;
  };

  return (
    <div>
      <div className="flex gap-2 mb-4">
        {filters.map((filter) => (
          <button
            key={filter}
            onClick={() => setActiveFilter(filter)}
            className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
              activeFilter === filter
                ? "bg-[#3b82f6] text-white"
                : "bg-[#1e293b] text-[#94a3b8] hover:text-[#f1f5f9] hover:bg-[#334155]"
            }`}
          >
            {filter}
            {filter !== "ALL" && (
              <span className="ml-1.5 text-xs opacity-70">
                ({getAlertCount(filter)})
              </span>
            )}
          </button>
        ))}
      </div>

      {sortedAlerts.length === 0 ? (
        <div className="text-center py-12 text-[#94a3b8]">
          No alerts found.
        </div>
      ) : (
        <div className="space-y-3">
          {sortedAlerts.map((alert) => (
            <AlertItem key={alert.id} alert={alert} />
          ))}
        </div>
      )}
    </div>
  );
}