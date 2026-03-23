import { notFound } from "next/navigation";
import { getAssetById, getFFTData, getRULTrend, getFaultPrediction } from "@/lib/mockData";
import { AssetDetailHeader } from "@/components/dashboard/AssetDetailHeader";
import { FFTChart } from "@/components/dashboard/FFTChart";
import { RULTrendChart } from "@/components/dashboard/RULTrendChart";
import { FaultBadge } from "@/components/dashboard/FaultBadge";

interface AssetDetailPageProps {
  params: Promise<{ id: string }>;
}

export default async function AssetDetailPage({ params }: AssetDetailPageProps) {
  const { id } = await params;
  const asset = getAssetById(id);

  if (!asset) {
    notFound();
  }

  const fftData = getFFTData(id);
  const rulTrend = getRULTrend(id);
  const faultPrediction = getFaultPrediction(id);

  return (
    <div className="p-6 space-y-6">
      <AssetDetailHeader asset={asset} />

      {faultPrediction && (
        <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
          <h2 className="text-sm font-medium text-[#f1f5f9] mb-3">Fault Prediction</h2>
          <FaultBadge prediction={faultPrediction} />
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
          <h2 className="text-sm font-medium text-[#f1f5f9] mb-4">FFT Spectrum</h2>
          <FFTChart data={fftData} />
        </div>

        <div className="bg-[#1e293b] border border-[#334155] rounded-lg p-6">
          <h2 className="text-sm font-medium text-[#f1f5f9] mb-4">RUL Trend (7 Days)</h2>
          <RULTrendChart data={rulTrend} />
        </div>
      </div>
    </div>
  );
}