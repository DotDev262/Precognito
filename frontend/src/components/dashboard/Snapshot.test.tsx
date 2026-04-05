import { describe, it, expect, vi, beforeAll, afterAll } from "vitest";
import { render } from "@testing-library/react";
import { AssetCard } from "./AssetCard";
import { Asset } from "@/lib/types";

describe("Visual Snapshots", () => {
  const originalToLocaleString = Date.prototype.toLocaleString;

  beforeAll(() => {
    // Mock toLocaleString to always return a fixed format regardless of locale/timezone
    Date.prototype.toLocaleString = vi.fn().mockImplementation(function() {
      // @ts-ignore
      const d = new Date(this.getTime());
      return `${d.getUTCMonth() + 1}/${d.getUTCDate()}/${d.getUTCFullYear()}, ${d.getUTCHours() % 12 || 12}:00:00 PM`;
    });
  });

  afterAll(() => {
    Date.prototype.toLocaleString = originalToLocaleString;
  });

  it("AssetCard should match snapshot", () => {
    const mockAsset: Asset = {
      id: "motor_1",
      name: "Motor 1",
      status: "GREEN",
      lastUpdated: "2026-04-04T12:00:00Z",
      type: "motor",
      location: "Factory Floor A",
      rms: 0.05,
      rul: 150
    };
    
    const { asFragment } = render(<AssetCard asset={mockAsset} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
