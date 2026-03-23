import { AlertList } from "@/components/dashboard/AlertList";
import { mockAlerts } from "@/lib/mockData";

export default function AlertsPage() {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-[#f1f5f9] mb-1">Alerts</h1>
        <p className="text-sm text-[#94a3b8]">
          Real-time alerts from asset monitoring
        </p>
      </div>

      <AlertList alerts={mockAlerts} />
    </div>
  );
}