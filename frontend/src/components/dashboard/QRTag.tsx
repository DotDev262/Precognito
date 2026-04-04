"use client";

import { QRCodeSVG } from "qrcode.react";

interface QRTagProps {
  assetId: string;
  assetName: string;
}

/**
 * @fileoverview Printable QR Tag component for physical asset identification.
 * @param {QRTagProps} props Component props.
 * @returns {JSX.Element} The rendered QR tag.
 */
export function QRTag({ assetId, assetName }: QRTagProps) {
  const printTag = () => {
    window.print();
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 inline-flex flex-col items-center gap-4">
      <div className="text-center">
        <h3 className="text-gray-900 font-bold text-lg uppercase tracking-tight">PRECOGNITO</h3>
        <p className="text-gray-500 text-[10px] font-medium leading-none">ASSET IDENTIFICATION TAG</p>
      </div>
      
      <div className="p-2 bg-white border-4 border-gray-900 rounded-sm">
        <QRCodeSVG 
          value={assetId} 
          size={160}
          level="H"
          includeMargin={false}
        />
      </div>

      <div className="text-center">
        <p className="text-gray-900 font-mono font-bold text-sm">{assetId}</p>
        <p className="text-gray-600 text-xs mt-1">{assetName}</p>
      </div>

      <div className="w-full pt-4 border-t border-gray-100 flex justify-center no-print">
        <button
          onClick={printTag}
          className="flex items-center gap-2 px-4 py-2 bg-[#0f172a] text-white text-xs font-bold rounded hover:bg-black transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
          </svg>
          PRINT PHYSICAL TAG
        </button>
      </div>

      <style jsx global>{`
        @media print {
          body * {
            visibility: hidden;
          }
          .bg-white, .bg-white * {
            visibility: visible;
          }
          .bg-white {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            box-shadow: none !important;
            border: 1px solid #eee !important;
          }
          .no-print {
            display: none !important;
          }
        }
      `}</style>
    </div>
  );
}
