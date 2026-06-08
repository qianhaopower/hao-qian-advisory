import html2canvas from "html2canvas";

export async function downloadElementAsImage(
  elementId: string,
  fileName: string
): Promise<boolean> {
  const element = document.getElementById(elementId);
  if (!element) return false;

  const canvas = await html2canvas(element, {
    backgroundColor: "#0b1020",
    scale: 2,
    useCORS: true,
    logging: false,
  });

  const link = document.createElement("a");
  link.download = fileName;
  link.href = canvas.toDataURL("image/png");
  link.click();
  return true;
}
