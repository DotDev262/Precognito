"use client";

import { useState } from "react";
import { Report, ReportType, ReportCategory } from "@/lib/types";
import { mockReports, mockHealthTrend } from "@/lib/mockData";
import { ReportConfigForm } from "@/components/dashboard/ReportConfigForm";
import { ReportList } from "@/components/dashboard/ReportList";
import { ReportChart } from "@/components/dashboard/ReportChart";

export default function ReportsPage() {
  const [reports] = useState<Report[]>(mockReports);
  const [showChart, setShowChart] = useState(false);

  const handleGenerate = (config: {
    type: ReportType;
    category: ReportCategory;
    assets: string[];
    dateRange: { from: string; to: string };
  }) => {
    console.log("Generating report:", config);
    setShowChart(true);
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-[#f1f5f9] mb-1">Reports</h1>
        <p className="text-sm text-[#94a3b8]">Generate and download asset health reports</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
            <h2 className="text-sm font-medium text-[#f1f5f9] mb-4">Recent Reports</h2>
            <ReportList reports={reports} />
          </div>

          {showChart && (
            <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
              <h2 className="text-sm font-medium text-[#f1f5f9] mb-4">Health Trend</h2>
              <ReportChart data={mockHealthTrend} />
            </div>
          )}
        </div>

        <div className="space-y-6">
          <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
            <h2 className="text-sm font-medium text-[#f1f5f9] mb-4">Generate New Report</h2>
            <ReportConfigForm onGenerate={handleGenerate} />
          </div>
        </div>
      </div>
    </div>
  );
}