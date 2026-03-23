"use client";

import { ReportType } from "@/lib/types";

interface ReportTypeSelectorProps {
  value: ReportType;
  onChange: (value: ReportType) => void;
}

export function ReportTypeSelector({ value, onChange }: ReportTypeSelectorProps) {
  return (
    <div className="flex gap-3">
      <button
        type="button"
        onClick={() => onChange("PDF")}
        className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${
          value === "PDF"
            ? "border-[#3b82f6] bg-[#3b82f6] text-white"
            : "border-[#334155] bg-[#1e293b] text-[#94a3b8] hover:border-[#3b82f6]"
        }`}
      >
        PDF
      </button>
      <button
        type="button"
        onClick={() => onChange("CSV")}
        className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${
          value === "CSV"
            ? "border-[#3b82f6] bg-[#3b82f6] text-white"
            : "border-[#334155] bg-[#1e293b] text-[#94a3b8] hover:border-[#3b82f6]"
        }`}
      >
        CSV
      </button>
    </div>
  );
}