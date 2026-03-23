import { SensorTable } from "@/components/dashboard/SensorTable";
import { mockSensors } from "@/lib/mockData";

export default function EdgePage() {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-[#f1f5f9] mb-1">Edge Status</h1>
        <p className="text-sm text-[#94a3b8]">
          Monitor sensor connectivity and heartbeat status
        </p>
      </div>

      <SensorTable sensors={mockSensors} />
    </div>
  );
}