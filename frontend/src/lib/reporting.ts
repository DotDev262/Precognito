import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

/**
 * Download data as CSV
 */
export function downloadCSV(data: any[], fileName: string) {
  if (data.length === 0) return;

  const headers = Object.keys(data[0]).join(",");
  const rows = data.map((obj) =>
    Object.values(obj)
      .map((val) => `"${val}"`)
      .join(",")
  );
  
  const csvContent = [headers, ...rows].join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", `${fileName}.csv`);
  link.style.visibility = "hidden";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/**
 * Download data as PDF table
 */
export function downloadPDF(data: any[], title: string, fileName: string) {
  if (data.length === 0) return;

  const doc = new jsPDF();
  doc.setFontSize(18);
  doc.text(title, 14, 22);
  doc.setFontSize(11);
  doc.setTextColor(100);
  doc.text(`Generated on ${new Date().toLocaleString()}`, 14, 30);

  const headers = Object.keys(data[0]);
  const body = data.map(obj => Object.values(obj));

  autoTable(doc, {
    startY: 35,
    head: [headers],
    body: body,
    theme: 'striped',
    headStyles: { fillColor: [15, 23, 42] },
  });

  doc.save(`${fileName}.pdf`);
}
